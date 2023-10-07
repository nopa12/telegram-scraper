import uuid
import enum
from datetime import datetime

from sqlalchemy import Float, UnicodeText, Uuid, DateTime, Column, Integer, String, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TgMsgsRaw(Base):
    __tablename__ = 'tg_msgs_raw'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tg_id = Column(Integer, index=True, nullable=False)
    tg_date = Column(DateTime, nullable=False)
    tg_chat = Column(String, nullable=False)
    tg_chat_id = Column(Integer, index=True, nullable=False)
    tg_msg = Column(UnicodeText)
    
class TgMedia(Base):
    __tablename__ = 'tg_images'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tg_msg_id = Column(Uuid(as_uuid=True), nullable=False, index=True)
    
    tg_file_path = Column(UnicodeText)