from pydantic import BaseModel, EmailStr
from typing import Optional

class ModerateTextRequest(BaseModel):
    email: EmailStr  # Geçerli e-posta
    text: str  # Moderasyon için metin

class ModerateImageRequest(BaseModel):
    email: EmailStr
    image_url: str  # Resim URL'si

class ModerationResponse(BaseModel):
    classification: str  # 'toxic', 'spam', 'harassment', 'safe'
    confidence: float  # 0.0-1.0
    reasoning: str  # Gerekçe

class AnalyticsSummary(BaseModel):
    total_requests: int  # Toplam istek
    toxic_count: int  # Toksik içerik sayısı