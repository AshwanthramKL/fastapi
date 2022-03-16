from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:Martialeagle1$@localhost:5432/fastapi_test' 

engine = create_engine(SQLALCHEMY_DATABASE_URL) # Responsible for establishing a connection

TestingSessionLocal = sessionmaker(autocommit= False, autoflush= False, bind = engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # run our code before we run our testClient
    def override_get_db():#going to create a session for our database everytime its called

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
    # run our code after our test finishes

