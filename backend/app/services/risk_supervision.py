"""执法问题风险盯办服务"""
from sqlalchemy.orm import Session
from app.models.risk_supervision import RiskSupervision
from app.services.display_rule import get_rules_by_page, apply_color_rules
from app.utils.timezone import calc_days_remaining
import json
from typing import List, Dict, Any, Tuple, Optional


def list_risk_supervision(
    db: Session,
    page: int = 1,
    page_size: int = 50,
    case_type: Optional[str] = None,
    risk_type: Optional[str] = None,
    officer_name: Optional[str] = None,
    sort_order: str = "asc",
    include_rules: bool = True
) -> Tuple[List[Dict[str, Any]], int, List[Dict[str, Any]]]:
    """
    获取执法问题风险盯办列表

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页数量
        case_type: 案件类型筛选
        risk_type: 风险类型筛选
        officer_name: 责任民警筛选
        sort_order: 排序方向 (asc/desc)
        include_rules: 是否包含规则

    Returns:
        (items, total, rules)
    """
    # 构建查询
    query = db.query(RiskSupervision)

    # 筛选条件
    if case_type:
        query = query.filter(RiskSupervision.case_type == case_type)
    if risk_type:
        query = query.filter(RiskSupervision.risk_type == risk_type)
    if officer_name:
        query = query.filter(RiskSupervision.officer_name == officer_name)

    # 查询总数
    total = query.count()

    # 排序（deadline 等价于 days_remaining）
    if sort_order == "desc":
        query = query.order_by(
            RiskSupervision.deadline.desc(),
            RiskSupervision.case_time.desc()
        )
    else:
        query = query.order_by(
            RiskSupervision.deadline.asc(),
            RiskSupervision.case_time.desc()
        )

    # 分页
    offset = (page - 1) * page_size
    items_db = query.offset(offset).limit(page_size).all()

    # 获取规则（不再在后端应用，由前端统一处理）
    rules = []
    if include_rules:
        rules = get_rules_by_page(db, "risk_supervision")

    # 转换数据（返回纯数据，不应用样式）
    items = []
    for item in items_db:
        # 解析 risk_issues JSON
        try:
            risk_issues = json.loads(item.risk_issues)
        except:
            risk_issues = [item.risk_issues]

        # 计算剩余天数
        days_remaining = calc_days_remaining(item.deadline)

        # 构建数据项（纯数据，无样式）
        item_data = {
            "id": item.id,
            "case_number": item.case_number,
            "case_name": item.case_name,
            "case_time": item.case_time,
            "case_type": item.case_type,
            "risk_type": item.risk_type,
            "risk_issues": risk_issues,
            "deadline": item.deadline,
            "officer_name": item.officer_name,
            "days_remaining": days_remaining
        }

        items.append(item_data)

    return items, total, rules
