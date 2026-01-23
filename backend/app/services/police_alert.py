"""警情记录服务"""
from sqlalchemy.orm import Session
from app.models.police_alert import PoliceAlert
from typing import List, Dict, Any, Tuple, Optional


def list_police_alerts(
    db: Session,
    page: int = 1,
    page_size: int = 50,
    alert_type: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    community: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], int]:
    """
    获取警情记录列表

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页数量
        alert_type: 警情类型筛选
        start_time: 开始时间
        end_time: 结束时间
        community: 社区筛选

    Returns:
        (items, total)
    """
    # 构建查询
    query = db.query(PoliceAlert)

    # 筛选条件
    if alert_type:
        query = query.filter(PoliceAlert.alert_type == alert_type)
    if start_time:
        query = query.filter(PoliceAlert.alert_time >= start_time)
    if end_time:
        query = query.filter(PoliceAlert.alert_time <= end_time)
    if community:
        query = query.filter(PoliceAlert.location_community == community)

    # 查询总数
    total = query.count()

    # 排序：按警情时间降序
    query = query.order_by(PoliceAlert.alert_time.desc())

    # 分页
    offset = (page - 1) * page_size
    items_db = query.offset(offset).limit(page_size).all()

    # 转换数据
    items = []
    for item in items_db:
        items.append({
            "id": item.id,
            "alert_number": item.alert_number,
            "alert_type": item.alert_type,
            "alert_name": item.alert_name,
            "alert_time": item.alert_time,
            "location_address": item.location_address,
            "location_community": item.location_community,
            "reporter_name": item.reporter_name,
            "officer_name": item.officer_name
        })

    return items, total


def get_alert_statistics(
    db: Session,
    time_range: str = "month"
) -> Dict[str, Any]:
    """
    获取警情类型统计

    Args:
        db: 数据库会话
        time_range: 时间范围（week/month/year）

    Returns:
        统计数据
    """
    from sqlalchemy import func
    from datetime import datetime, timedelta

    # 计算时间范围
    now = datetime.now()
    if time_range == "week":
        start_time = now - timedelta(days=7)
    elif time_range == "month":
        start_time = now - timedelta(days=30)
    elif time_range == "year":
        start_time = now - timedelta(days=365)
    else:
        start_time = now - timedelta(days=30)

    # 按警情类型统计
    results = db.query(
        PoliceAlert.alert_type,
        func.count(PoliceAlert.id).label('count')
    ).filter(
        PoliceAlert.alert_time >= start_time
    ).group_by(
        PoliceAlert.alert_type
    ).all()

    # 转换为字典
    statistics = []
    for alert_type, count in results:
        statistics.append({
            "name": alert_type,
            "count": count
        })

    return {
        "time_range": time_range,
        "start_time": start_time,
        "end_time": now,
        "statistics": statistics
    }


def get_location_distribution(
    db: Session,
    alert_type: str,
    time_range: str = "month"
) -> List[Dict[str, Any]]:
    """
    获取指定警情类型的地点分布

    Args:
        db: 数据库会话
        alert_type: 警情类型
        time_range: 时间范围

    Returns:
        地点分布数据
    """
    from sqlalchemy import func
    from datetime import datetime, timedelta

    # 计算时间范围
    now = datetime.now()
    if time_range == "week":
        start_time = now - timedelta(days=7)
    elif time_range == "month":
        start_time = now - timedelta(days=30)
    elif time_range == "year":
        start_time = now - timedelta(days=365)
    else:
        start_time = now - timedelta(days=30)

    # 按社区统计
    results = db.query(
        PoliceAlert.location_community,
        func.count(PoliceAlert.id).label('count')
    ).filter(
        PoliceAlert.alert_type == alert_type,
        PoliceAlert.alert_time >= start_time,
        PoliceAlert.location_community.isnot(None)
    ).group_by(
        PoliceAlert.location_community
    ).order_by(
        func.count(PoliceAlert.id).desc()
    ).all()

    # 转换为列表
    distribution = []
    for community, count in results:
        distribution.append({
            "location": community,
            "count": count
        })

    return distribution
