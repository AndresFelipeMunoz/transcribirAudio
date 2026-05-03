from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))