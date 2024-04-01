# Constants
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.models.db.mg import Base


@pytest.fixture(autouse=True, scope="function")
def test_session(db):
    # Base.metadata.create_all(engine) # create all tables

    session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db,
        expire_on_commit=False,
    )()

    yield session_local  # every test will get a new db session

    session_local.rollback()  # rollback the transactions

    for table in reversed(Base.metadata.sorted_tables):
        session_local.execute(text(f"DELETE FROM {table.name};"))
        session_local.commit()

    session_local.close()
