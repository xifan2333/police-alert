"""矛盾纠纷闭环管理 Schema"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class StyleInfo(BaseModel):
    """样式信息"""
    font_color: Optional[str] = None
    background_color: Optional[str] = None
    style_token: Optional[str] = None


class DisputeManagementItem(BaseModel):
    """矛盾纠纷闭环管理项"""
    id: int
    event_name: str
    event_type: str
    content: str = Field(..., max_length=150)
    event_time: datetime
    risk_level: str
    officer_name: str
    status: str
    style: StyleInfo

    class Config:
        from_attributes = True


class DisputeManagementListResponse(BaseModel):
    """矛盾纠纷闭环管理列表响应"""
    code: int = 200
    data: dict  # {total: int, items: List[DisputeManagementItem], rules: List[dict]}
