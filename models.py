from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from config import settings

DATABASE_URL = settings.database_url

# Asyncpg requires the correct dialect 'postgresql+asyncpg'
engine = create_engine(DATABASE_URL, future=True, echo=True)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, index=True),
    Column("email", String, index=True),
)
