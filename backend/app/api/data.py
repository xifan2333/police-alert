"""数据 API 路由"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import risk_supervision, dispute_management, situation
from app.models.display_rule import DisplayRule
from typing import Optional

router = APIRouter()


@router.get("/risk-supervision", tags=["数据"])
def get_risk_supervision(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    case_type: Optional[str] = Query(None, description="案件类型筛选"),
    problem_type: Optional[str] = Query(None, description="问题类型筛选"),
    officer_name: Optional[str] = Query(None, description="责任民警筛选"),
    sort_field: str = Query("days_remaining", description="排序字段"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="排序方向"),
    include_rules: bool = Query(True, description="是否包含规则"),
    db: Session = Depends(get_db)
):
    """获取执法问题风险盯办列表"""
    items, total, rules = risk_supervision.list_risk_supervision(
        db, page, page_size, case_type, problem_type, officer_name, sort_field, sort_order, include_rules
    )

    return {
        "code": 200,
        "data": {
            "total": total,
            "items": items,
            "rules": rules if include_rules else []
        }
    }


@router.get("/risk-supervision/filter-options", tags=["数据"])
def get_risk_supervision_filter_options(db: Session = Depends(get_db)):
    """获取案件筛选选项"""
    officers = risk_supervision.get_officer_options(db)
    case_types = risk_supervision.get_case_type_options(db)
    return {"code": 200, "data": {"officers": officers, "case_types": case_types}}


@router.get("/dispute-management", tags=["数据"])
def get_dispute_management(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="处置进度筛选"),
    risk_level: Optional[str] = Query(None, description="风险等级筛选"),
    officer_name: Optional[str] = Query(None, description="责任民警筛选"),
    sort_field: str = Query("event_time", description="排序字段"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    include_rules: bool = Query(True, description="是否包含规则"),
    db: Session = Depends(get_db)
):
    """获取矛盾纠纷闭环管理列表"""
    items, total, rules = dispute_management.list_dispute_management(
        db, page, page_size, status, risk_level, officer_name, sort_field, sort_order, include_rules
    )

    return {
        "code": 200,
        "data": {
            "total": total,
            "items": items,
            "rules": rules if include_rules else []
        }
    }


@router.get("/dispute-management/filter-options", tags=["数据"])
def get_dispute_management_filter_options(db: Session = Depends(get_db)):
    """获取纠纷筛选选项"""
    officers = dispute_management.get_officer_options(db)
    return {"code": 200, "data": {"officers": officers}}


@router.get("/situation", tags=["数据"])
async def get_situation_data(
    time_period: str = Query("month", description="时间维度（week/month/year）"),
    alert_types: Optional[str] = Query("偷盗,诈骗", description="地图显示的警情类型，逗号分隔"),
    db: Session = Depends(get_db)
):
    """获取警情态势页面所需的所有数据（包含地图数据）"""
    # 解析警情类型
    types_list = [t.strip() for t in alert_types.split(",") if t.strip()]

    # 获取态势数据（包含地图数据）
    data = await situation.get_situation_data(db, time_period, types_list)

    return {
        "code": 200,
        "data": data
    }


@router.get("/display-rules", tags=["数据"])
def get_display_rules(
    page_code: Optional[str] = Query(None, description="页面代码"),
    db: Session = Depends(get_db)
):
    """获取显示规则描述（用于页面底部提示）"""
    # 构建查询
    query = db.query(DisplayRule).filter(DisplayRule.is_enabled == 1)

    # 如果指定了 page_code，只返回该页面的规则
    if page_code:
        query = query.filter(DisplayRule.page_code == page_code)

    rules = query.order_by(DisplayRule.priority.desc()).all()

    # 拼接所有规则描述
    descriptions = [rule.description for rule in rules if rule.description]
    display_text = " | ".join(descriptions) if descriptions else "暂无显示规则"

    return {
        "code": 200,
        "data": {
            "display_rules": display_text
        }
    }
