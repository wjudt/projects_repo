from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy

engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:postgres@localhost/postgres')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()