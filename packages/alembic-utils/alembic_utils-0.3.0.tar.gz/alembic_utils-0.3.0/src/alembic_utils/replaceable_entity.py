# pylint: disable=unused-argument,invalid-name,line-too-long
import logging
from contextlib import contextmanager
from itertools import zip_longest
from pathlib import Path
from typing import List, Optional, Type, TypeVar

from alembic.autogenerate import comparators, renderers
from alembic.operations import Operations
from flupy import flu
from sqlalchemy.orm import Session

from alembic_utils.dependencies import defer_dependent
from alembic_utils.exceptions import (
    DuplicateRegistration,
    FailedToGenerateComparable,
    UnreachableException,
)
from alembic_utils.reversible_op import ReversibleOp
from alembic_utils.statement import escape_colon, normalize_whitespace, strip_terminating_semicolon

log = logging.getLogger(__name__)

T = TypeVar("T", bound="ReplaceableEntity")


@contextmanager
def simulate_entity(sess: Session, entity):
    """Creates *entities* in a transaction so postgres rendered definition
    can be retrieved
    """
    try:
        sess.begin_nested()
        with defer_dependent(sess, entity):
            sess.execute(entity.to_sql_statement_create_or_replace())
            yield sess
    finally:
        sess.rollback()


class ReplaceableEntity:
    """A SQL Entity that can be replaced"""

    _CACHE = {}

    def __init__(self, schema: str, signature: str, definition: str):
        self.schema: str = normalize_whitespace(schema)
        self.signature: str = normalize_whitespace(signature)
        self.definition: str = escape_colon(strip_terminating_semicolon(definition))

    @classmethod
    def from_sql(cls: Type[T], sql: str) -> T:
        """Create an instance from a SQL string"""
        raise NotImplementedError()

    @property
    def literal_schema(self) -> str:
        """Wrap a schema name in literal quotes
        Useful for emitting SQL statements
        """
        return f'"{self.schema}"'

    @classmethod
    def from_path(cls: Type[T], path: Path) -> T:
        """Create an instance instance from a SQL file path"""
        with path.open() as sql_file:
            sql = sql_file.read()
        return cls.from_sql(sql)

    @classmethod
    def from_database(cls, sess: Session, schema="%") -> List[T]:
        """Collect existing entities from the database for given schema"""
        raise NotImplementedError()

    def to_sql_statement_create(self) -> str:
        """ Generates a SQL "create function" statement for PGFunction """
        raise NotImplementedError()

    def to_sql_statement_drop(self, cascade=False) -> str:
        """ Generates a SQL "drop function" statement for PGFunction """
        raise NotImplementedError()

    def to_sql_statement_create_or_replace(self) -> str:
        """ Generates a SQL "create or replace function" statement for PGFunction """
        raise NotImplementedError()

    def get_database_definition(self: T, sess: Session) -> T:  # $Optional[T]:
        """ Looks up self and return the copy existing in the database (maybe)the"""
        with simulate_entity(sess, self) as sess:
            # Drop self
            sess.execute(self.to_sql_statement_drop())

            # collect all remaining entities
            db_entities = self.from_database(sess, schema=self.schema)
            db_entities = sorted(db_entities, key=lambda x: x.identity)

        with simulate_entity(sess, self) as sess:
            # collect all remaining entities
            all_w_self = self.from_database(sess, schema=self.schema)
            all_w_self = sorted(all_w_self, key=lambda x: x.identity)

        # Find "self" by diffing the before and after
        for without_self, with_self in zip_longest(db_entities, all_w_self):
            if without_self is None or without_self.identity != with_self.identity:
                return with_self

        raise UnreachableException()

    def render_self_for_migration(self, omit_definition=False) -> str:
        """Render a string that is valid python code to reconstruct self in a migration"""
        var_name = self.to_variable_name()
        class_name = self.__class__.__name__
        escaped_definition = self.definition if not omit_definition else "# not required for op"

        return f"""{var_name} = {class_name}(
            schema="{self.schema}",
            signature="{self.signature}",
            definition={repr(escaped_definition)}
        )\n\n"""

    @classmethod
    def render_import_statement(cls) -> str:
        """Render a string that is valid python code to import current class"""
        module_path = cls.__module__
        class_name = cls.__name__
        return f"from {module_path} import {class_name}\nfrom sqlalchemy import text as sql_text"

    @property
    def identity(self) -> str:
        """A string that consistently and globally identifies a function"""
        return f"{self.schema}.{self.signature}"

    def to_variable_name(self) -> str:
        """A deterministic variable name based on PGFunction's contents """
        schema_name = self.schema.lower()
        object_name = self.signature.split("(")[0].strip().lower()
        return f"{schema_name}_{object_name}"

    def get_required_migration_op(self, sess: Session) -> Optional[ReversibleOp]:
        """Get the migration operation required for autogenerate"""
        # All entities in the database for self's schema
        entities_in_database = self.from_database(sess, schema=self.schema)

        with simulate_entity(sess, self) as sess:
            db_def = self.get_database_definition(sess)

        for x in entities_in_database:

            if (db_def.identity, normalize_whitespace(db_def.definition)) == (
                x.identity,
                normalize_whitespace(x.definition),
            ):
                return None

            if db_def.identity == x.identity:
                return ReplaceOp(self)

        return CreateOp(self)


##############
# Operations #
##############


@Operations.register_operation("create_entity", "invoke_for_target")
class CreateOp(ReversibleOp):
    def reverse(self):
        return DropOp(self.target)


@Operations.register_operation("drop_entity", "invoke_for_target")
class DropOp(ReversibleOp):
    def reverse(self):
        return CreateOp(self.target)


@Operations.register_operation("replace_entity", "invoke_for_target")
class ReplaceOp(ReversibleOp):
    def reverse(self):
        return RevertOp(self.target)


class RevertOp(ReversibleOp):
    # Revert is never in an upgrade, so no need to implement reverse
    pass


###################
# Implementations #
###################


@Operations.implementation_for(CreateOp)
def create_entity(operations, operation):
    target: ReplaceableEntity = operation.target
    operations.execute(target.to_sql_statement_create())


@Operations.implementation_for(DropOp)
def drop_entity(operations, operation):
    target: ReplaceableEntity = operation.target
    operations.execute(target.to_sql_statement_drop())


@Operations.implementation_for(ReplaceOp)
@Operations.implementation_for(RevertOp)
def replace_or_revert_entity(operations, operation):
    target: ReplaceableEntity = operation.target
    operations.execute(target.to_sql_statement_create_or_replace())


##########
# Render #
##########


@renderers.dispatch_for(CreateOp)
def render_create_entity(autogen_context, op):
    target = op.target
    autogen_context.imports.add(target.render_import_statement())
    variable_name = target.to_variable_name()
    return target.render_self_for_migration() + f"op.create_entity({variable_name})"


@renderers.dispatch_for(DropOp)
def render_drop_entity(autogen_context, op):
    target = op.target
    autogen_context.imports.add(target.render_import_statement())
    variable_name = target.to_variable_name()
    return (
        target.render_self_for_migration(omit_definition=False) + f"op.drop_entity({variable_name})"
    )


@renderers.dispatch_for(ReplaceOp)
def render_replace_entity(autogen_context, op):
    target = op.target
    autogen_context.imports.add(target.render_import_statement())
    variable_name = target.to_variable_name()
    return target.render_self_for_migration() + f"op.replace_entity({variable_name})"


@renderers.dispatch_for(RevertOp)
def render_revert_entity(autogen_context, op):
    """Collect the entity definition currently live in the database and use its definition
    as the downgrade revert target"""
    target = op.target
    autogen_context.imports.add(target.render_import_statement())

    context = autogen_context
    engine = context.connection.engine

    with engine.connect() as connection:
        sess = Session(bind=connection)
        db_target = op.target.get_database_definition(sess)

    variable_name = db_target.to_variable_name()
    return db_target.render_self_for_migration() + f"op.replace_entity({variable_name})"


##################
# Event Listener #
##################


def register_entities(
    entities: List[T],
    schemas: Optional[List[str]] = None,
    exclude_schemas: Optional[List[str]] = None,
) -> None:
    """Create an event listener to watch for changes in registered entities when migrations are created using
    `alembic revision --autogenerate`

    **Parameters:**

    * **entities** - *List[ReplaceableEntity]*: A list of entities (PGFunction, PGView, etc) to monitor for revisions
    * **schemas** - *Optional[List[str]]*: A list of SQL schema names to monitor. Note, schemas referenced in registered entities are automatically monitored.
    * **exclude_schemas** - *Optional[List[str]]*: A list of SQL schemas to ignore. Note, explicitly registered entities will still be monitored.
    """

    @comparators.dispatch_for("schema")
    def compare_registered_entities(
        autogen_context, upgrade_ops, sqla_schemas: List[Optional[str]]
    ):
        engine = autogen_context.connection.engine

        # Ensure pg_functions have unique identities (not registered twice)
        for ident, function_group in flu(entities).group_by(key=lambda x: x.identity):
            if len(function_group.collect()) > 1:
                raise DuplicateRegistration(
                    f"PGFunction with identity {ident} was registered multiple times"
                )

        # User registered schemas + automatically registered schemas (from SQLA Metadata)
        observed_schemas: List[str] = []
        if schemas is not None:
            for schema in schemas:
                observed_schemas.append(schema)

        sqla_schemas = [schema for schema in sqla_schemas or [] if schema is not None]
        observed_schemas.extend(sqla_schemas)

        for entity in entities:
            observed_schemas.append(entity.schema)

        # Remove excluded schemas
        observed_schemas = [x for x in set(observed_schemas) if x not in (exclude_schemas or [])]

        with engine.connect() as connection:

            for entity in entities:
                print(f"Processing {entity.__class__.__name__} {entity.identity}")

                try:
                    # Start a parent transaction
                    # Bind the session within the parent transaction
                    transaction = connection.begin()
                    sess = Session(bind=connection)
                    maybe_op = entity.get_required_migration_op(sess)
                    if maybe_op:
                        upgrade_ops.ops.append(maybe_op)

                        print(
                            f"Detected {maybe_op.__class__.__name__} for {entity.__class__.__name__} {entity.identity}"
                        )

                finally:
                    transaction.rollback()

            try:
                # Start a parent transaction
                # Bind the session within the parent transaction
                transaction = connection.begin()
                sess = Session(bind=connection)

                # Convert the user defined definitions to the database rendered definitions
                local_entities = []
                for ent in entities:
                    with simulate_entity(sess, ent) as sess:
                        local_entity = ent.get_database_definition(sess)
                        local_entities.append(local_entity)

                # All database entities currently live
                # Check if anything needs to drop
                for entity_class in ReplaceableEntity.__subclasses__():

                    # Entities within the schemas that are live
                    for schema in observed_schemas:

                        db_entities = entity_class.from_database(sess, schema=schema)

                        # Check for functions that were deleted locally
                        for db_entity in db_entities:
                            for local_entity in local_entities:
                                if db_entity.identity == local_entity.identity:
                                    break
                            else:
                                # No match was found locally
                                upgrade_ops.ops.append(DropOp(db_entity))
                                print(
                                    f"Detected DropOp drop {db_entity.__class__.__name__} {db_entity.identity}"
                                )

            finally:
                transaction.rollback()
