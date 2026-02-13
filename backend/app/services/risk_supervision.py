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
    problem_type: Optional[str] = None,
    officer_name: Optional[str] = None,
    sort_field: str = "days_remaining",
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
        problem_type: 问题类型筛选
        officer_name: 责任民警筛选
        sort_field: 排序字段
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
    if problem_type:
        query = query.filter(RiskSupervision.problem_type == problem_type)
    if officer_name:
        query = query.filter(RiskSupervision.officer_name == officer_name)

    # 查询总数
    total = query.count()

    # 排序
    sort_map = {
        'case_number': RiskSupervision.case_number,
        'case_time': RiskSupervision.case_time,
        'deadline': RiskSupervision.deadline,
        'days_remaining': RiskSupervision.deadline
    }

    sort_column = sort_map.get(sort_field, RiskSupervision.deadline)

    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

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
            specific_content = json.loads(item.risk_issues)
        except:
            specific_content = [item.risk_issues]

        # 计算剩余天数
        days_remaining = calc_days_remaining(item.deadline)

        # 构建数据项（纯数据，无样式）
        item_data = {
            "id": item.id,
            "case_number": item.case_number,
            "case_name": item.case_name,
            "case_time": item.case_time,
            "case_type": item.case_type,
            "problem_type": item.problem_type,
            "specific_content": specific_content,
            "deadline": item.deadline,
            "officer_name": item.officer_name,
            "days_remaining": days_remaining
        }

        items.append(item_data)

    return items, total, rules


def get_officer_options(db: Session) -> List[str]:
    """获取去重的警员列表"""
    officers = (
        db.query(RiskSupervision.officer_name)
        .distinct()
        .order_by(RiskSupervision.officer_name.asc())
        .all()
    )
    return [o[0] for o in officers]


def get_case_type_options(db: Session) -> List[str]:
    """获取去重的案件类型列表"""
    case_types = (
        db.query(RiskSupervision.case_type)
        .distinct()
        .order_by(RiskSupervision.case_type.asc())
        .all()
    )
    return [c[0] for c in case_types]
