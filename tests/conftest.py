from typing import Generator

import pytest
from sqlalchemy import Engine, Insert, create_engine, insert
from sqlalchemy.schema import Column, MetaData, Table
from sqlalchemy.types import Integer, String

from sql_test_demo.config import read_config


def create_env_engine() -> Engine:
    """
    Read config.yaml and create an engine.
    """
    pg_secrets = read_config().postgresql
    return create_engine(
        f"postgresql+psycopg2://{pg_secrets.user}:{pg_secrets.password}@{pg_secrets.host}:{pg_secrets.port}/{pg_secrets.database}"
    )


def create_address_table(metadata_obj: MetaData) -> Table:
    """Create a Table object with he given columns."""
    address = Table(
        "address",  # table name
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("postcode", String(7), nullable=True),
        Column("woonplaats", String(60), nullable=True),
        schema="public",
    )
    return address


def insert_address_data(address: Table) -> Insert:
    """
    Create an Insert object with the given values for the address table.
    """
    return insert(address).values(
        [
            {"postcode": "7334 DP", "woonplaats": "Apeldoorn"},
            {"postcode": "7334DP", "woonplaats": None},
            {"postcode": "7334", "woonplaats": "Apeldoorn"},
            {"postcode": None, "woonplaats": "Apeldoorn"},
        ]
    )


@pytest.fixture
def db() -> Generator[Engine, None, None]:
    """
    Provision the test database and yield a connection for the duration of the tests.
    """
    # Create database engine and objects
    engine = create_env_engine()
    metadata_obj = MetaData()
    address = create_address_table(metadata_obj)
    metadata_obj.create_all(bind=engine, tables=[address])

    # Insert test data
    with engine.connect() as conn:
        for statement in [insert_address_data(address=address)]:
            conn.execute(statement=statement)
            conn.commit()
    # yield engine, run tests
    print("Yield engine for usage in tests.")
    yield engine

    # Delete table after tests
    print("Dropping tables")
    metadata_obj.drop_all(engine)


if __name__ == "__main__":
    create_env_engine()
