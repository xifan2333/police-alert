"""显示规则配置 Schema"""
from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class DisplayRuleBase(BaseModel):
    """显示规则基础模型"""
    page_code: str
    table_code: Optional[str] = None
    rule_type: str
    rule_name: str
    rule_config: dict
    priority: int = 0
    is_enabled: int = 1
    description: Optional[str] = None


class DisplayRuleCreate(DisplayRuleBase):
    """创建显示规则"""
    pass


class DisplayRuleResponse(DisplayRuleBase):
    """显示规则响应"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
