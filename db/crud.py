from sqlalchemy import DateTime
from sqlalchemy.orm import Session

from db.models import User, Report


def get_user(session: Session, username: str) -> User:
    return session.query(User).filter(User.username == username).first()


def create_user(session: Session, username: str) -> User:
    user = get_user(session, username)

    if user:
        return user

    user = User(username=username)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def delete_user(session: Session, username: str) -> User:
    user = get_user(session, username)

    if user:
        session.delete(user)
        session.commit()

    return user


def increment_meter(session: Session, date: DateTime, reporter_username: str, offender_username: str) -> Report:
    reporter = get_user(session, reporter_username)
    offender = get_user(session, offender_username)

    if reporter is None:
        reporter = create_user(session, reporter_username)

    if offender is None:
        offender = create_user(session, offender_username)

    report = Report(date=date, reporter=reporter, offender=offender)

    session.add(report)
    session.commit()
    session.refresh(report)

    return report
