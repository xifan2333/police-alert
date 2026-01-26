"""警情态势服务 - 简化版"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.police_alert import PoliceAlert
from app.models.call_record import CallRecord
from app.models.geocoding_cache import GeocodingCache
from app.services import geocoding
from app.services.display_rule import get_rules_by_page, apply_color_rules
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple


def get_time_range(time_period: str = "month") -> Tuple[datetime, datetime, datetime, datetime]:
    """
    计算时间范围

    Args:
        time_period: 时间维度 (week/month/year)

    Returns:
        (当前开始时间, 当前结束时间, 上期开始时间, 去年同期开始时间)
    """
    now = datetime.now()

    if time_period == "week":
        # 当前周：最近7天
        current_start = now - timedelta(days=7)
        current_end = now
        # 上周：前7-14天
        prev_start = now - timedelta(days=14)
        prev_end = now - timedelta(days=7)
        # 去年同周
        yoy_start = now - timedelta(days=365)
        yoy_end = now - timedelta(days=358)
    elif time_period == "month":
        # 当前月：最近30天
        current_start = now - timedelta(days=30)
        current_end = now
        # 上月：前30-60天
        prev_start = now - timedelta(days=60)
        prev_end = now - timedelta(days=30)
        # 去年同月
        yoy_start = now - timedelta(days=365)
        yoy_end = now - timedelta(days=335)
    elif time_period == "year":
        # 当前年：最近365天
        current_start = now - timedelta(days=365)
        current_end = now
        # 上年：前365-730天
        prev_start = now - timedelta(days=730)
        prev_end = now - timedelta(days=365)
        # 前年同期
        yoy_start = now - timedelta(days=730)
        yoy_end = now - timedelta(days=365)
    else:
        # 默认月
        current_start = now - timedelta(days=30)
        current_end = now
        prev_start = now - timedelta(days=60)
        prev_end = now - timedelta(days=30)
        yoy_start = now - timedelta(days=365)
        yoy_end = now - timedelta(days=335)

    return current_start, current_end, prev_start, yoy_start


def calculate_ratio(current: int, previous: int) -> str:
    """
    计算同比/环比

    Args:
        current: 当前数量
        previous: 对比数量

    Returns:
        百分比字符串，如 "+10%" 或 "-5%" 或 "N/A"
    """
    if previous == 0:
        return "N/A"

    ratio = ((current - previous) / previous) * 100
    if ratio > 0:
        return f"+{ratio:.1f}%"
    else:
        return f"{ratio:.1f}%"


def get_police_classification(db: Session, time_period: str = "month", apply_rules: bool = True) -> Tuple[List[List], List[Dict]]:
    """
    获取警情分类同环比分析

    Args:
        db: 数据库会话
        time_period: 时间维度
        apply_rules: 是否应用显示规则

    Returns:
        (数据列表, 规则应用结果)
        数据列表: [['名称', 数量, '同比', '环比'], ...]
        规则应用结果: [{'row_index': 0, 'font_color': '#ff0000', 'style_token': 'danger'}, ...]
    """
    current_start, current_end, prev_start, yoy_start = get_time_range(time_period)

    # 6种警情类型（移除"有效警情"，它是统计概念）
    alert_types = [
        '偷盗',
        '诈骗',
        '涉黄',
        '涉赌',
        '纠纷',
        '人身伤害'
    ]

    result = []

    for alert_type in alert_types:
        # 当前周期数量 - 使用 sum(count) 而不是 count(id)
        current_count = db.query(func.sum(PoliceAlert.count)).filter(
            PoliceAlert.alert_type == alert_type,
            PoliceAlert.alert_date >= current_start.date(),
            PoliceAlert.alert_date <= current_end.date()
        ).scalar() or 0

        # 上期数量（环比）
        prev_count = db.query(func.sum(PoliceAlert.count)).filter(
            PoliceAlert.alert_type == alert_type,
            PoliceAlert.alert_date >= prev_start.date(),
            PoliceAlert.alert_date < current_start.date()
        ).scalar() or 0

        # 去年同期数量（同比）
        yoy_count = db.query(func.sum(PoliceAlert.count)).filter(
            PoliceAlert.alert_type == alert_type,
            PoliceAlert.alert_date >= yoy_start.date(),
            PoliceAlert.alert_date < (yoy_start + (current_end - current_start)).date()
        ).scalar() or 0

        # 计算同比和环比
        yoy_ratio = calculate_ratio(current_count, yoy_count)
        mom_ratio = calculate_ratio(current_count, prev_count)

        result.append([alert_type, current_count, yoy_ratio, mom_ratio])

    # 添加"有效警情"作为总计
    total_count = sum(row[1] for row in result)
    total_yoy = db.query(func.sum(PoliceAlert.count)).filter(
        PoliceAlert.alert_date >= yoy_start.date(),
        PoliceAlert.alert_date < (yoy_start + (current_end - current_start)).date()
    ).scalar() or 0
    total_prev = db.query(func.sum(PoliceAlert.count)).filter(
        PoliceAlert.alert_date >= prev_start.date(),
        PoliceAlert.alert_date < current_start.date()
    ).scalar() or 0

    result.append(['有效警情', total_count, calculate_ratio(total_count, total_yoy), calculate_ratio(total_count, total_prev)])

    # 应用显示规则
    row_styles = []
    if apply_rules:
        rules = get_rules_by_page(db, "situation")
        for row_index, row in enumerate(result):
            item_data = {
                "name": row[0],
                "count": row[1],
                "yoy": row[2],
                "mom": row[3]
            }
            style = apply_color_rules(item_data, rules)
            if style.get("font_color") or style.get("style_token"):
                row_styles.append({
                    "row_index": row_index,
                    "font_color": style.get("font_color"),
                    "style_token": style.get("style_token")
                })

    return result, row_styles


def get_location_distribution(
    db: Session,
    alert_type: str,
    time_period: str = "month",
    limit: int = 5
) -> List[List]:
    """
    获取指定警情类型的地点分布 Top N

    Args:
        db: 数据库会话
        alert_type: 警情类型
        time_period: 时间维度
        limit: 返回数量

    Returns:
        [['地点', 数量], ...]
    """
    current_start, current_end, _, _ = get_time_range(time_period)

    # 按地点统计 - 使用 sum(count)
    results = db.query(
        PoliceAlert.location,
        func.sum(PoliceAlert.count).label('count')
    ).filter(
        PoliceAlert.alert_type == alert_type,
        PoliceAlert.alert_date >= current_start.date(),
        PoliceAlert.alert_date <= current_end.date()
    ).group_by(
        PoliceAlert.location
    ).order_by(
        func.sum(PoliceAlert.count).desc()
    ).limit(limit).all()

    return [[location, int(count)] for location, count in results]


def get_repeat_alarms(db: Session, limit: int = 5) -> List[List]:
    """
    获取重复报警统计（按地点统计）

    Returns:
        [['地点', 次数, '最近报警日期'], ...]
    """
    # 按地点分组统计 - 使用 sum(count)
    results = db.query(
        CallRecord.call_address,
        func.sum(CallRecord.count).label('total_count'),
        func.max(CallRecord.call_date).label('last_date')
    ).group_by(
        CallRecord.call_address
    ).having(
        func.sum(CallRecord.count) >= 2  # 至少2次才算重复
    ).order_by(
        func.sum(CallRecord.count).desc()
    ).limit(limit).all()

    # 格式化日期
    result = []
    for address, count, last_date in results:
        last_date_str = last_date.strftime('%Y-%m-%d') if last_date else 'N/A'
        result.append([address, int(count), last_date_str])

    return result


def get_communities_with_stats(db: Session) -> List[Dict]:
    """
    获取社区坐标及统计数据（使用 GeocodingCache）

    Returns:
        [{'name': '社区名', 'lng': 经度, 'lat': 纬度, 'caseCount': 案件数, 'disputeCount': 纠纷数}, ...]
    """
    # 获取所有不重复的地点
    locations = db.query(PoliceAlert.location).distinct().all()
    locations = [loc[0] for loc in locations]

    result = []
    for location in locations:
        # 从缓存中查找经纬度
        cache = db.query(GeocodingCache).filter(
            GeocodingCache.address == location
        ).first()

        if not cache:
            # TODO: 如果缓存中没有，调用天地图API获取
            # 暂时跳过没有缓存的地点
            continue

        # 统计该地点的案件数 - 使用 sum(count)
        case_count = db.query(func.sum(PoliceAlert.count)).filter(
            PoliceAlert.location == location
        ).scalar() or 0

        # 统计该地点的纠纷数 - 使用 sum(count)
        dispute_count = db.query(func.sum(PoliceAlert.count)).filter(
            PoliceAlert.location == location,
            PoliceAlert.alert_type == '纠纷'
        ).scalar() or 0

        result.append({
            'name': location,
            'lng': float(cache.longitude),
            'lat': float(cache.latitude),
            'caseCount': int(case_count),
            'disputeCount': int(dispute_count)
        })

    return result


async def get_situation_data(
    db: Session,
    time_period: str = "month",
    alert_types: List[str] = None
) -> Dict[str, Any]:
    """
    获取警情态势页面所有数据

    Args:
        db: 数据库会话
        time_period: 时间维度 (week/month/year)
        alert_types: 地图显示的警情类型列表，默认为 ['偷盗', '诈骗']

    Returns:
        完整的态势数据（包含地图数据和每个表格的显示规则）
    """
    # 警情分类总览（纯数据，不应用规则）
    police_classification, _ = get_police_classification(db, time_period, apply_rules=False)

    # 各类警情地点分布
    theft_traditional = get_location_distribution(db, '偷盗', time_period)
    telecom_fraud = get_location_distribution(db, '诈骗', time_period)
    vice_cases = get_location_distribution(db, '涉黄', time_period)
    dispute_cases = get_location_distribution(db, '纠纷', time_period)
    fight_cases = get_location_distribution(db, '人身伤害', time_period)
    gambling_cases = get_location_distribution(db, '涉赌', time_period)

    # 重复报警
    repeat_alarms = get_repeat_alarms(db)

    # 地图数据（带经纬度）
    if alert_types is None:
        alert_types = ['偷盗', '诈骗']
    map_data = await get_map_data(db, alert_types, time_period)

    # 为每个表格获取独立的显示规则
    display_rules = {
        "policeClassification": get_rules_by_page(db, "situation", "policeClassification"),
        "theftTraditional": get_rules_by_page(db, "situation", "theftTraditional"),
        "telecomFraud": get_rules_by_page(db, "situation", "telecomFraud"),
        "viceCases": get_rules_by_page(db, "situation", "viceCases"),
        "disputeCases": get_rules_by_page(db, "situation", "disputeCases"),
        "fightCases": get_rules_by_page(db, "situation", "fightCases"),
        "gamblingCases": get_rules_by_page(db, "situation", "gamblingCases"),
        "repeatAlarms": get_rules_by_page(db, "situation", "repeatAlarms")
    }

    return {
        'policeClassification': police_classification,
        'theftTraditional': theft_traditional,
        'telecomFraud': telecom_fraud,
        'viceCases': vice_cases,
        'disputeCases': dispute_cases,
        'fightCases': fight_cases,
        'gamblingCases': gambling_cases,
        'repeatAlarms': repeat_alarms,
        'mapData': map_data,
        'displayRules': display_rules
    }


async def get_map_data(
    db: Session,
    alert_types: List[str],
    time_period: str = "month"
) -> List[Dict[str, Any]]:
    """
    获取地图标记数据（带经纬度和缓存逻辑）

    Args:
        db: 数据库会话
        alert_types: 警情类型列表，如 ['偷盗', '诈骗']
        time_period: 时间维度

    Returns:
        [
            {
                'location': '地点名称',
                'alertType': '警情类型',
                'count': 数量,
                'lng': 经度,
                'lat': 纬度
            },
            ...
        ]
    """
    current_start, current_end, _, _ = get_time_range(time_period)

    # 天地图 API Key（写死 - 服务器端）
    tianditu_key = "6244a8e0c7b2d0632b98bf5a2e4571c6"

    # 查询指定类型的警情数据
    results = db.query(
        PoliceAlert.location,
        PoliceAlert.alert_type,
        func.sum(PoliceAlert.count).label('count')
    ).filter(
        PoliceAlert.alert_type.in_(alert_types),
        PoliceAlert.alert_date >= current_start.date(),
        PoliceAlert.alert_date <= current_end.date()
    ).group_by(
        PoliceAlert.location,
        PoliceAlert.alert_type
    ).all()

    # 处理每个地点，获取经纬度
    map_data = []
    for location, alert_type, count in results:
        # 先从缓存查询
        coords = geocoding.get_coordinates(db, location)

        # 如果缓存中没有，调用天地图 API
        if not coords and tianditu_key:
            coords = await geocoding.get_coordinates_with_api(db, location, tianditu_key)

        # 如果有坐标，添加到结果中
        if coords:
            map_data.append({
                'location': location,
                'alertType': alert_type,
                'count': int(count),
                'lng': float(coords[0]),
                'lat': float(coords[1])
            })

    return map_data
