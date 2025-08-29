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

"""Define ORM models for the Masa Meter database using SQLAlchemy

Provide models to represent speakers and mentions of "Sushi Masa" in the
database.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship

from db.database import Base, engine


class Speaker(Base):
    """Represent a person who has said "Sushi Masa".

    Attributes:
        username: The unique Discord username of the speaker [Primary Key].
        mentions: List of MasaMention objects linked to this speaker.
    """

    __tablename__ = "speakers"
    username = Column(String(50), primary_key=True)

    mentions = relationship("MasaMention", back_populates="speaker")


class MasaMention(Base):
    """Represent an occurence of "Sushi Masa" being spoke by the speaker.

    Attributes:
        id: Primary key for the mention.
        date: ISO-formatted date when the mentioned occured.
        speaker_username:
            Foreign key to the Speaker's username who mentioned "Sushi Masa".
        speaker: The related Speaker object.
    """

    __tablename__ = "masa_mentions"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    date = Column(
        String, default=lambda: datetime.now(timezone.utc).isoformat()
    )
    speaker_username = Column(String(50), ForeignKey("speakers.username"))

    speaker = relationship("Speaker", back_populates="mentions")


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
