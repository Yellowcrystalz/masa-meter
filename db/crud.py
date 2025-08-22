from sqlalchemy import Result, func, select
from sqlalchemy.orm import Session

from db.models import Speaker, MasaMention


def get_speaker(session: Session, username: str) -> Speaker:
    return session.get(Speaker, username)


def create_speaker(session: Session, username: str) -> Speaker:
    speaker = get_speaker(session, username)

    if speaker:
        return speaker

    speaker = Speaker(username=username)

    session.add(speaker)
    session.commit()
    session.refresh(speaker)

    return speaker


def delete_speaker(session: Session, username: str) -> Speaker:
    speaker = get_speaker(session, username)

    if speaker:
        session.delete(speaker)
        session.commit()

    return speaker


def increment_meter(session: Session, username: str) -> MasaMention:
    speaker = get_speaker(session, username)

    if speaker is None:
        speaker = create_speaker(session, username)

    mention = MasaMention(speaker=speaker)

    session.add(mention)
    session.commit()
    session.refresh(mention)

    return mention


def get_meter(session: Session) -> int:
    stmt = select(func.count(MasaMention.id))

    result = session.scalar(stmt)
    return result


def get_history(session: Session) -> Result:
    stmt = (
        select(MasaMention.id, MasaMention.date, MasaMention.speaker_username)
    )

    results = session.execute(stmt)

    return results


def get_leaderboard(session: Session) -> Result:
    stmt = (
        select(Speaker.username, func.count(MasaMention.id))
        .join(MasaMention, Speaker.username == MasaMention.speaker_username)
        .group_by(Speaker.username)
        .order_by(func.count(MasaMention.id).desc())
    )

    results = session.execute(stmt)

    return results
