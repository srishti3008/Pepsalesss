import uuid, datetime as dt, enum
from sqlalchemy import Column, String, Enum, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field

from .database import Base


class Channel(str, enum.Enum):
    email = "email"
    sms = "sms"
    in_app = "in_app"


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    channel = Column(Enum(Channel), nullable=False)
    subject = Column(String(255))
    message = Column(Text, nullable=False)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    sent_at = Column(DateTime)


class NotificationIn(BaseModel):
    user_id: uuid.UUID
    channel: Channel
    subject: str | None = None
    message: str = Field(..., max_length=4000)


class NotificationOut(NotificationIn):
    id: uuid.UUID
    sent: bool
    created_at: dt.datetime
    sent_at: dt.datetime | None

    class Config:
        orm_mode = True