# MIT License
#
# Copyright (c) 2025 Justin Nguyen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Set up the database engine, session factory, and declarative base setup for
    ORM models.

Provide a SQLAlchemy engine connected to SQLite, a session factory for database
operations, and a declarative base for defining ORM models. Include a context
manager to safely open and close database sessions.

Attributes:
    engine: A database connection to SQLite3.
    SessionLocal: A factory for creating database sessions.
    Base: Adeclarative base for ORM models.
"""

from contextlib import contextmanager

from sqlalchemy import Engine, Session, create_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from config import DATABASE_PATH


engine: Engine = create_engine(f"sqlite:///{DATABASE_PATH}")
SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base: DeclarativeMeta = declarative_base()


@contextmanager
def get_session() -> Session:
    """Open a session safely and ensure it closes after completion.

    Create a SQLAlchemy session bound to the engine and automatically close it
    when exiting the context, even if an exception occurs.

    Returns:
        A SQLAlchemy seesion object bound to the database engine.

    Raises:
        SQLAlchemyError: An error occurs while creating the session.

    Example:
        with get_session() as session:
            result = get_meter(session)
    """

    session: SessionLocal = SessionLocal()

    try:
        yield session
    finally:
        session.close()
