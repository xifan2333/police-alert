"""执法问题风险盯办 Schema"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class StyleInfo(BaseModel):
    """样式信息"""
    font_color: Optional[str] = None
    background_color: Optional[str] = None
    style_token: Optional[str] = None


class RiskSupervisionItem(BaseModel):
    """执法问题风险盯办项"""
    id: int
    case_number: str = Field(..., min_length=18, max_length=18)
    case_name: str
    case_time: datetime
    case_type: str
    risk_type: str
    risk_issues: List[str]
    deadline: datetime
    officer_name: str
    days_remaining: int
    style: StyleInfo

    class Config:
        from_attributes = True


class RiskSupervisionListResponse(BaseModel):
    """执法问题风险盯办列表响应"""
    code: int = 200
    data: dict  # {total: int, items: List[RiskSupervisionItem], rules: List[dict]}
