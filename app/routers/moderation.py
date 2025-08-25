from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas import ModerateTextRequest, ModerateImageRequest, ModerationResponse
from app.database import get_db
from app.services import hash_content, moderate_text as service_moderate_text, moderate_image as service_moderate_image, send_notification
from app.crud import create_request, create_result, create_notification_log, get_analytics

router = APIRouter(prefix="/api/v1/moderate", tags=["moderation"])

@router.post("/text")
def moderate_text_endpoint(req: ModerateTextRequest, db: Session = Depends(get_db)):
    try:
        content_hash = hash_content(req.text)
        request = create_request(db, "text", content_hash, "processed", req.email)
        result = service_moderate_text(req.text)
        create_result(db, request.id, result)
        if result["classification"] != "safe":
            send_notification("slack", f"Inappropriate content detected: {result['classification']} (Text: {req.text})")
            create_notification_log(db, request.id, "slack", "sent")
        return ModerationResponse(**result)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="This content has already been submitted for moderation.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/image")
def moderate_image_endpoint(req: ModerateImageRequest, db: Session = Depends(get_db)):
    try:
        content_hash = hash_content(req.image_url)
        request = create_request(db, "image", content_hash, "processed", req.email)
        result = service_moderate_image(req.image_url)
        create_result(db, request.id, result)
        if result["classification"] != "safe":
            send_notification("slack", f"Inappropriate image detected: {result['classification']} (URL: {req.image_url})")
            create_notification_log(db, request.id, "slack", "sent")
        return ModerationResponse(**result)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="This image has already been submitted for moderation.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/summary")
def get_summary(user: str, db: Session = Depends(get_db)):
    return get_analytics(db, user)