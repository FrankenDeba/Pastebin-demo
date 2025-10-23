from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Pastes(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    paste: str = Field(index=True)
    url: str = Field(index=True)

# Code above omitted 👆

sqlite_file_name = "pastes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Code below omitted 👇

# Code above omitted 👆

from sqlmodel import SQLModel
print("keys:::all", SQLModel.metadata.tables.keys())


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Code below omitted 👇

# Code above omitted 👆

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# Code below omitted 👇
# Code above omitted 👆

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Code below omitted 👇

__all__ = ["get_session", "Pastes"]
