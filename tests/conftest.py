from typing import Generator

import pytest
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from gima_common.configuration.settings import read_settings
from sqlalchemy import Engine, Insert, create_engine, insert
from sqlalchemy.schema import Column, MetaData, Table
from sqlalchemy.types import Integer, String


def get_password():
    # Get database password from Azure Key Vault
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url="https://kv-pls-gima-test-rsc.vault.azure.net", credential=credential
    )
    secret = client.get_secret("pg-gima-test")
    return secret.value


def create_env_engine() -> Engine:
    try:
        # Lees lokale config.yaml, of gemounte secrets
        local_secrets = read_settings()["secrets"]["postgres"]
        return create_engine(
            f'postgresql+psycopg2://{local_secrets["user"]}:{local_secrets["password"]}@{local_secrets["host"]}:{local_secrets["port"]}/{local_secrets["database"]}'
        )
    except KeyError:
        # Haal database uit KeyVault (alleen benaderbaar vanuit MAP test v-net)
        # TODO: switch tussen test en prod
        return create_engine(
            f"postgresql+psycopg2://dbadmin:{get_password()}@pg-gima-test.postgres.database.azure.com:5432/test"
        )


def create_address_table(metadata_obj: MetaData) -> Table:
    """Create a Table object with he given columns."""
    address = Table(
        "address",  # table name
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("postcode", String(7), nullable=True),
        Column("woonplaats", String(60), nullable=True),
        schema="zwemmb1", # TODO: switch schema afhankelijk van omgeving
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
    yield engine

    # Delete table after tests
    metadata_obj.drop_all(engine)


if __name__ == "__main__":
    create_env_engine()
