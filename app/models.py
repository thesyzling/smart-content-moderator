from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base

class ModerationRequest(Base):
    __tablename__ = "moderation_requests"
    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String, index=True)  # 'text' veya 'image'
    content_hash = Column(String, unique=True)
    status = Column(String)  # 'pending', 'processed'
    email = Column(String)  # Kullanıcı e-postası
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModerationResult(Base):
    __tablename__ = "moderation_results"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("moderation_requests.id"))
    classification = Column(String)  # 'toxic', 'spam', 'harassment', 'safe'
    confidence = Column(Float)
    reasoning = Column(String)
    llm_response = Column(String)

class NotificationLog(Base):
    __tablename__ = "notification_logs"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("moderation_requests.id"))
    channel = Column(String)  # 'slack' veya 'email'
    status = Column(String)  # 'sent', 'failed'
    sent_at = Column(DateTime(timezone=True), server_default=func.now())