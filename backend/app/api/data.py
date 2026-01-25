"""数据 API 路由"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import risk_supervision, dispute_management, situation
from typing import Optional

router = APIRouter()


@router.get("/risk-supervision", tags=["数据"])
def get_risk_supervision(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    include_rules: bool = Query(True, description="是否包含规则"),
    db: Session = Depends(get_db)
):
    """获取执法问题风险盯办列表"""
    items, total, rules = risk_supervision.list_risk_supervision(
        db, page, page_size, include_rules
    )

    return {
        "code": 200,
        "data": {
            "total": total,
            "items": items,
            "rules": rules if include_rules else []
        }
    }


@router.get("/dispute-management", tags=["数据"])
def get_dispute_management(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="处置进度筛选"),
    risk_level: Optional[str] = Query(None, description="风险等级筛选"),
    include_rules: bool = Query(True, description="是否包含规则"),
    db: Session = Depends(get_db)
):
    """获取矛盾纠纷闭环管理列表"""
    items, total, rules = dispute_management.list_dispute_management(
        db, page, page_size, status, risk_level, include_rules
    )

    return {
        "code": 200,
        "data": {
            "total": total,
            "items": items,
            "rules": rules if include_rules else []
        }
    }


@router.get("/situation", tags=["数据"])
def get_situation_data(
    time_period: str = Query("month", description="时间维度（week/month/year）"),
    db: Session = Depends(get_db)
):
    """获取警情态势页面所需的所有数据（支持时间维度）"""
    data = situation.get_situation_data(db, time_period)

    return {
        "code": 200,
        "data": data
    }
