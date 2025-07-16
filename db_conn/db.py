import pathlib
from dotenv import find_dotenv, dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

file_path = pathlib.Path().cwd()
static_dir = str(pathlib.Path(pathlib.Path().cwd(), "static"))
config = dotenv_values(find_dotenv(f"{file_path}/.env"))

# Database setup
SQLALCHEMY_DATABASE_URL = config.get("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
