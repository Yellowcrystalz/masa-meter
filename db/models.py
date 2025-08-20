from sqlalchemy import Column, DateTime, Integer, ForeignKey, Sequence, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base, engine


class Speaker(Base):
    __tablename__ = "speakers"
    username = Column(String(50), primary_key=True)

    mentions = relationship("MasaMention", back_populates="speaker")


class MasaMention(Base):
    __tablename__ = "masa_mentions"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    speaker_username = Column(String(50), ForeignKey("speakers.username"))

    speaker = relationship("Speaker", back_populates="mentions")


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
