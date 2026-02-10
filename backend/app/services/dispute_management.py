"""矛盾纠纷闭环管理服务"""
from sqlalchemy.orm import Session
from app.models.dispute_management import DisputeManagement
from app.services.display_rule import get_rules_by_page, apply_color_rules
from typing import List, Dict, Any, Tuple, Optional


def list_dispute_management(
    db: Session,
    page: int = 1,
    page_size: int = 50,
    status: Optional[str] = None,
    risk_level: Optional[str] = None,
    officer_name: Optional[str] = None,
    include_rules: bool = True
) -> Tuple[List[Dict[str, Any]], int, List[Dict[str, Any]]]:
    """
    获取矛盾纠纷闭环管理列表

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页数量
        status: 处置进度筛选
        risk_level: 风险等级筛选
        officer_name: 责任民警筛选
        include_rules: 是否包含规则

    Returns:
        (items, total, rules)
    """
    # 构建查询
    query = db.query(DisputeManagement)

    # 默认筛选：待化解、待关注
    if status is None:
        query = query.filter(DisputeManagement.status.in_(["待化解", "待关注"]))
    else:
        query = query.filter(DisputeManagement.status == status)

    # 风险等级筛选
    if risk_level:
        query = query.filter(DisputeManagement.risk_level == risk_level)

    # 警员筛选
    if officer_name:
        query = query.filter(DisputeManagement.officer_name == officer_name)

    # 查询总数
    total = query.count()

    # 排序：风险等级高优先，事发时间降序
    risk_level_order = {
        "高": 1,
        "中": 2,
        "低": 3
    }

    # 分页
    offset = (page - 1) * page_size
    items_db = query.offset(offset).limit(page_size).all()

    # 手动排序（SQLite 不支持 CASE WHEN）
    items_db = sorted(items_db, key=lambda x: (
        risk_level_order.get(x.risk_level, 99),
        -x.event_time.timestamp()
    ))

    # 获取规则
    rules = []
    if include_rules:
        rules = get_rules_by_page(db, "dispute_management")

    # 转换数据
    items = []
    for item in items_db:
        # 构建数据项
        item_data = {
            "id": item.id,
            "event_name": item.event_name,
            "event_type": item.event_type,
            "content": item.content,
            "event_time": item.event_time,
            "risk_level": item.risk_level,
            "officer_name": item.officer_name,
            "status": item.status
        }

        # 应用样式规则
        style = apply_color_rules({"risk_level": item.risk_level}, rules)
        item_data["style"] = style

        items.append(item_data)

    return items, total, rules


def get_officer_options(db: Session) -> List[str]:
    """获取去重的警员列表"""
    officers = (
        db.query(DisputeManagement.officer_name)
        .distinct()
        .order_by(DisputeManagement.officer_name.asc())
        .all()
    )
    return [o[0] for o in officers]
