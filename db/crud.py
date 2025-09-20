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

"""Provide database operations for the Masa Meter application.

Define functions to manage Speakers and MasaMention entries in the database.
This includes creating, deleting, and querying speakers, incrementing the
Masa meter, retrieving meter counts, fetching history, and generating a
leaderboard.
"""

from datetime import datetime, timedelta, timezone
from typing import Tuple

from sqlalchemy import Select, Subquery, Result, func, select
from sqlalchemy.orm import Session

from db.models import Speaker, MasaMention


def check_speaker(session: Session, username: str) -> Speaker | None:
    """Check if speaker's usesrname exists in the database.

    Args:
        session: A SQLAlchemy session with the database.
        username: The username to be query.

    Returns:
        The Speaker object if it exits; otherwise returns None.
    """

    return session.get(Speaker, username)


def create_speaker(session: Session, username: str) -> Speaker:
    """ Create a new entry Speaker entry in the database.

    Args:
        session: A SQLAlchemy session with the database.
        username: The username of the new Speaker entry.

    Returns:
        The newly created Speaker object or an existing Speaker object if the
        username already exits.
    """

    speaker: Speaker = check_speaker(session, username)

    if speaker:
        return speaker

    speaker = Speaker(username=username)

    session.add(speaker)
    session.commit()
    session.refresh(speaker)

    return speaker


def delete_speaker(session: Session, username: str) -> Speaker | None:
    """Delete Speaker from the database.

    Args:
        session: A SQLAlchemy session with the database.
        username: The username of the Speaker to be deleted.

    Returns:
        The Speaker object that was deleted if it exits; otherwise None
    """

    speaker: Speaker = check_speaker(session, username)

    if speaker:
        session.delete(speaker)
        session.commit()

    return speaker


def create_mention(session: Session, username: str) -> MasaMention:
    """Create a MasaMention entry in the database.

    Creates a Speaker object/entry if the username was not in the database.

    Args:
        session: A SQLAlchemy session with the database.
        username: The username of the Speaker attached to the mention.

    Returns:
        The newly created MasaMention object.
    """

    speaker: Speaker = check_speaker(session, username)

    if speaker is None:
        speaker = create_speaker(session, username)

    mention: MasaMention = MasaMention(speaker=speaker)

    session.add(mention)
    session.commit()
    session.refresh(mention)

    return mention


def delete_mention(session: Session, mention_id: str) -> MasaMention | None:
    """Delete MasaMention from the database.

    Args:
        session: A SQLAlchemy session with the database.
        mention_id: The id of the MasaMention to be deleted.

    Returns:
        The MasaMention object that was deleted if it exits; otherwise None
    """

    mention: MasaMention = session.get(MasaMention, mention_id)

    if mention:
        session.delete(mention)
        session.commit()

    return mention


def get_meter(session: Session) -> int:
    """Fetch the number of MasaMention entries in the database.

    Args:
        session: A SQLAlchemy session with the database.

    Returns:
        The int count of the Masa meter.
    """

    stmt: Select = select(func.count(MasaMention.id))

    result: int = session.scalar(stmt)
    return result


def get_history(session: Session) -> Result:
    """Retrieve all records in the MasaMention table.

    Args:
        session: A SQLAlchemy session with the database.

    Returns:
        The SQL Alchemy result object containing every MasaMention entry.
        Each entry is organized as a tuple in the form:
            (id, date, speaker_username)
    """

    stmt: Select = (
        select(MasaMention.date, MasaMention.speaker_username)
    )

    results: Result = session.execute(stmt)

    return results


def get_leaderboard(session: Session) -> Result:
    """Retrieve the Speaker's with the most entries in the MasaMention table.


    Args:
        session: A SQLAlchemy session with the database.

    Returns:
        The SQL Alchemy result object containing speakers ordered from most to
        fewest MasaMention entries. Each row is a tuple:
            (speaker_username, count)
    """

    stmt: Select = (
        select(MasaMention.speaker_username, func.count(MasaMention.id))
        .group_by(MasaMention.speaker_username)
        .order_by(func.count(MasaMention.id).desc())
    )

    results: Result = session.execute(stmt)

    return results


def _get_birthday() -> Tuple[datetime, datetime]:
    """
    """
    
    birthday_str: str = "-09-14T05:00:00+00:00"
    current_date: datetime = datetime.now(timezone.utc)
    current_year: int = current_date.year
    birthday_str = str(current_year) + birthday_str
    birthday_date: datetime = datetime.fromisoformat(birthday_str)

    if current_date > birthday_date:
        birthday_date = str(current_year - 1) + birthday_str

    end_date = str(current_year + 1) + birthday_str

    return birthday_date, end_date


def get_achievements(session: Session) -> list[str]:
    """
    """

    achievements_list: list[str] = []

    # Masa Master: Who said it the most

    stmt: Select = (
        select(MasaMention.speaker_username)
        .group_by(MasaMention.speaker_username)
        .order_by(func.count(MasaMention.id).desc())
        .limit(1)
    )
    achievements_list.append(session.scalar(stmt))

    # Silent Sashimi: Who said it the least

    stmt = (
        select(MasaMention.speaker_username)
        .group_by(MasaMention.speaker_username)
        .order_by(func.count(MasaMention.id).asc())
        .limit(1)
    )
    achievements_list.append(session.scalar(stmt))

    # Tempura Titan: Who said it the most in one day

    subq: Subquery = (
        select(
            MasaMention.speaker_username,
            MasaMention.date, func.count(MasaMention.date).label("masa_count")
        )
        .group_by(MasaMention.speaker_username, func.date(MasaMention.date))
        .subquery()
    )

    stmt = (
        select(subq.c.speaker_username)
        .group_by(subq.c.speaker_username)
        .order_by(func.max(subq.c.masa_count).desc())
        .limit(1)
    )

    achievements_list.append(session.scalar(stmt))

    # Nigiri Ninja: Who is the only one to say it on a day

    stmt = (
        select(MasaMention.speaker_username)
        .group_by(func.date(MasaMention.date))
        .having(1 == func.count(MasaMention.date))
        .order_by(func.count(MasaMention.date).desc())
        .limit(1)
    )
    achievements_list.append(session.scalar(stmt))

    # Special Sushi: Who said it on my birthday

    birthday_dates: Tuple[datetime, datetime] = _get_birthday()

    stmt = (
        select(MasaMention.speaker_username)
        .where(
            (MasaMention.date >= birthday_dates[0]) &
            (MasaMention.date < birthday_dates[1])
        )
        .limit(1)
    )
    achievements_list.append(session.scalar(stmt))

    return achievements_list