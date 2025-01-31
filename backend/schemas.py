from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class URLBase(BaseModel):
    target_url: str
    custom_alias: Optional[str] = None

class URLResponse(BaseModel):
    target_url: str
    short_id: str
    qr_code: str
    created_at: datetime

class ClickInfo(BaseModel):
    clicked_at: datetime
    referrer: Optional[str]
    user_agent: Optional[str]

class URLStats(BaseModel):
    url: str
    short_id: str
    created_at: datetime
    clicks: int
    recent_clicks: List[ClickInfo]
