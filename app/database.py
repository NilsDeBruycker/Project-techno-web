from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker

engine = create_engine(
"sqlite:///data/db.sqlite"
, # Path to the database file
echo=True, # Show generated SQL code in the terminal
)
