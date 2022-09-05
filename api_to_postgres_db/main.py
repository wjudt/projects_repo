from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
import sqlalchemy

engine = sqlalchemy.create_engine('postgresql+psycopg2://postgres:postgres@localhost/postgres')
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)






connection = engine.connect()
metadata = sqlalchemy.MetaData()
area1 = sqlalchemy.Table('area1_flat', metadata, autoload=True, autoload_with=engine)

# print(area1.columns.keys()) #show column names
# print(repr(metadata.tables['area1_flat'])) #show metadata

query = sqlalchemy.select([area1])
cursor = connection.execute(query)
result = cursor.fetchall()
print(result[:3])



app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello World"}


@app.get("/{name}")
async def say_hello(name: int):
    return {"message": f"Hello {name}"}