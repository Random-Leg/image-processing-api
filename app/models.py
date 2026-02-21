from sqlalchemy import Column, String, Integer, Text
from .database import Base

class ImageRecord(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True, index=True)
    original_name = Column(String)
    status = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    format = Column(String)
    size_bytes = Column(Integer)
    processed_at = Column(String)
    error = Column(Text, nullable=True)