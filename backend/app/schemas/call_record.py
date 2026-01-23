"""报警记录 Pydantic 模式"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CallRecordBase(BaseModel):
    call_number: str
    reporter_name: str
    reporter_phone: Optional[str] = None
    call_time: datetime
    call_address: Optional[str] = None
    is_valid: int = 1


class CallRecordCreate(CallRecordBase):
    pass


class CallRecordUpdate(BaseModel):
    reporter_name: Optional[str] = None
    reporter_phone: Optional[str] = None
    call_time: Optional[datetime] = None
    call_address: Optional[str] = None
    is_valid: Optional[int] = None


class CallRecordResponse(CallRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
