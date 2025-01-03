"""Define useful functions to interact with the database
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


"""engine = create_engine("sqlite:///leadme.db", echo=True)
session = scoped_session(sessionmaker(
                            autocommit=False,
                            autoflush=False,
                            bind=engine
                        ))"""

"""def init_db():
    initialize the database by mapping the defined models with database
    tables
    from . import models
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def shutdown_session(exception=None):
    session.remove()"""
