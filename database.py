from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time
from dotenv import load_dotenv
import os

# Load variables from .env file
if not os.getenv("IN_DOCKER"):
    load_dotenv(override=True)
print("RAW USE_DOCKER ENV =", os.getenv("USE_DOCKER"))
DEBUG = os.getenv("DEBUG", "False") == "True"

# Switch between local and docker
USE_DOCKER = os.getenv("USE_DOCKER", "False") == "True"


DATABASE_URL = os.getenv("DATABASE_URL_DOCKER") if USE_DOCKER else os.getenv("DATABASE_URL_LOCAL")


print("use_docker = ", USE_DOCKER)
print("DATABASE_URL= ", DATABASE_URL)
def get_engine_with_retry(url, retries=10, delay=2):
    for i in range(retries):
        try:
            engine = create_engine(url)
            # test connection
            conn = engine.connect()
            conn.close()
            print("Database is ready!")
            return engine
        except OperationalError:
            print(f"Postgres not ready, retry {i+1}/{retries}. Waiting {delay}s...")
            time.sleep(delay)
    raise RuntimeError("Could not connect to the database after several retries")

# Create engine only after DB is ready
engine = get_engine_with_retry(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String, nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)
