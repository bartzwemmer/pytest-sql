from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Postgresql:
    """
    PostgreSQL database configuration.
    """
    host: str
    port: int
    database: str
    user: str
    password: str
    schema: str


@dataclass(frozen=True)
class Config:
    """
    Application configuration.
    """
    postgresql: Postgresql
