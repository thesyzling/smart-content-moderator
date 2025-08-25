from sqlalchemy.orm import Session
from .models import ModerationRequest, ModerationResult, NotificationLog
from .schemas import *

def create_request(db: Session, content_type: str, content_hash: str, status: str, email: str):
    req = ModerationRequest(content_type=content_type, content_hash=content_hash, status=status, email=email)
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

def create_result(db: Session, request_id: int, result: dict):
    res = ModerationResult(request_id=request_id, **result)
    db.add(res)
    db.commit()

def create_notification_log(db: Session, request_id: int, channel: str, status: str):
    log = NotificationLog(request_id=request_id, channel=channel, status=status)
    db.add(log)
    db.commit()

def get_analytics(db: Session, email: str):
    total = db.query(ModerationRequest).filter(ModerationRequest.email == email).count()
    toxic = db.query(ModerationResult).join(ModerationRequest).filter(ModerationRequest.email == email, ModerationResult.classification == "toxic").count()
    return {"total_requests": total, "toxic_count": toxic}