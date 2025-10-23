# models/crud.py
from typing import Annotated
from fastapi import Query, HTTPException
from sqlmodel import Session, select
from .main import get_session, Pastes, engine, create_db_and_tables
import uuid

from data_models import PasteText


def read_pastes(
    url: str | None = None,
    session: Session | None = None,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Pastes]:
    """Return a list of Paste rows.

    If `session` is not provided (e.g. when called outside of a FastAPI request
    context), a local Session is created using the module `engine`.
    """
    statement = select(Pastes).offset(offset).limit(limit)
    # If no session provided, ensure tables exist and create a session for this call
    if session is None:
        # create tables if they don't exist yet (helps when calling outside FastAPI startup)
        create_db_and_tables()
        with Session(engine) as local_session:
            if url:
                print("read_pastes url:", url, type(url))
                stmt = select(Pastes).where(Pastes.url == url)
                paste = local_session.exec(stmt).first()
                if not paste:
                    raise HTTPException(status_code=404, detail="Paste not found")
                return paste
            result = local_session.exec(statement)
            return result.all()

    # Otherwise use the provided session (injected by FastAPI)
    if url:
        stmt = select(Pastes).where(Pastes.url == url)
        paste = session.exec(stmt).first()
        if not paste:
            raise HTTPException(status_code=404, detail="Paste not found")
        return paste

    result = session.exec(statement)
    return result.all() or ""

def create_paste(paste: str, url: str, session: Session | None = None,) -> PasteText:
    """Create a new Paste row in the database."""
    # Generate a UUID (e.g., a random UUID version 4)
    my_uuid = uuid.uuid4()

    # Get the integer representation of the UUID
    uuid_as_int = my_uuid.int

    id = int(str(uuid_as_int)[:6])

   

    if session is None:
        # create tables if they don't exist yet (helps when calling outside FastAPI startup)
        create_db_and_tables()
        with Session(engine) as local_session:
            new_paste = Pastes(paste=paste, url=url, id=id)
            local_session.add(new_paste)
            local_session.commit()
            local_session.refresh(new_paste)
            return PasteText(paste=new_paste.paste, url=new_paste.url)

    # Otherwise use the provided session (injected by FastAPI)
    new_paste = Pastes(paste=paste, url=url, id=id)
    session.add(new_paste)
    session.commit()
    session.refresh(new_paste)
    return PasteText(paste=new_paste.paste, url=new_paste.url)