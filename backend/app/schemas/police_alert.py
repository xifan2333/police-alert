"""警情记录 Pydantic 模式"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PoliceAlertBase(BaseModel):
    alert_number: str
    alert_type: str
    alert_name: str
    alert_time: datetime
    location_address: Optional[str] = None
    location_community: Optional[str] = None
    reporter_name: Optional[str] = None
    officer_name: Optional[str] = None


class PoliceAlertCreate(PoliceAlertBase):
    pass


class PoliceAlertUpdate(BaseModel):
    alert_type: Optional[str] = None
    alert_name: Optional[str] = None
    alert_time: Optional[datetime] = None
    location_address: Optional[str] = None
    location_community: Optional[str] = None
    reporter_name: Optional[str] = None
    officer_name: Optional[str] = None


class PoliceAlertResponse(PoliceAlertBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
