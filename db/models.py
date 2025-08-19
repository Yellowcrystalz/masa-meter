from sqlalchemy import Column, DateTime, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship

from db.database import Base, engine


class User(Base):
    __tablename__ = "users"
    username = Column(String(50), primary_key=True)

    reports_made = relationship("Report", back_populates="reporter", foreign_keys="Report.reporter_username")
    reports_received = relationship("Report", back_populates="offender", foreign_keys="Report.offender_username")


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    date = Column(DateTime(timezone=False))
    reporter_username = Column(String(50), ForeignKey("users.username"))
    offender_username = Column(String(50), ForeignKey("users.username"))

    reporter = relationship("User", back_populates="reports_made", foreign_keys=[reporter_username])
    offender = relationship("User", back_populates="reports_received", foreign_keys=[offender_username])


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
