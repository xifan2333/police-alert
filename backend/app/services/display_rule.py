"""显示规则服务"""
from sqlalchemy.orm import Session
from app.models.display_rule import DisplayRule
import json
from typing import List, Dict, Any, Optional


def get_rules_by_page(db: Session, page_code: str, table_code: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    获取指定页面的显示规则

    Args:
        db: 数据库会话
        page_code: 页面编码
        table_code: 表格编码（可选），用于区分同一页面内的多个表格

    Returns:
        规则列表
    """
    query = db.query(DisplayRule).filter(
        DisplayRule.page_code == page_code,
        DisplayRule.is_enabled == 1
    )

    # 如果指定了 table_code，则过滤
    if table_code is not None:
        query = query.filter(DisplayRule.table_code == table_code)

    rules = query.order_by(DisplayRule.priority).all()

    result = []
    for rule in rules:
        result.append({
            "table_code": rule.table_code,
            "rule_type": rule.rule_type,
            "rule_name": rule.rule_name,
            "rule_config": json.loads(rule.rule_config),
            "priority": rule.priority,
            "description": rule.description
        })

    return result


def apply_color_rules(item_data: Dict[str, Any], rules: List[Dict[str, Any]]) -> Dict[str, Optional[str]]:
    """
    应用颜色规则

    Args:
        item_data: 数据项
        rules: 规则列表

    Returns:
        样式信息 {font_color, style_token}
    """
    style = {
        "font_color": None,
        "style_token": None
    }

    # 按优先级遍历规则
    for rule in rules:
        if rule["rule_type"] != "color":
            continue

        rule_config = rule["rule_config"]
        field = rule_config.get("field")
        conditions = rule_config.get("conditions", [])

        # 获取字段值
        field_value = item_data.get(field)
        if field_value is None:
            continue

        # 检查条件
        for condition in conditions:
            operator = condition.get("operator")
            value = condition.get("value")

            matched = False
            if operator == "<=":
                matched = field_value <= value
            elif operator == ">=":
                matched = field_value >= value
            elif operator == "==":
                matched = field_value == value
            elif operator == "eq":
                matched = field_value == value
            elif operator == "in":
                values = condition.get("values", [])
                matched = field_value in values

            if matched:
                style["font_color"] = condition.get("font_color")
                style["style_token"] = condition.get("style_token")
                return style  # 命中第一个规则后返回

    return style
