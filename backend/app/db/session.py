from sqlmodel import Session, SQLModel, create_engine

import app.core.config as config

engine = create_engine(config.SQLITE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency injection for FastAPI.
    
    return: SQLModel Session
    """
    with Session(engine) as session:
        yield session
