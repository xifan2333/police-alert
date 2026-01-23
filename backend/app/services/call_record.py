"""报警记录服务"""
from sqlalchemy.orm import Session
from app.models.call_record import CallRecord
from typing import List, Dict, Any, Tuple, Optional


def list_call_records(
    db: Session,
    page: int = 1,
    page_size: int = 50,
    is_valid: Optional[int] = None
) -> Tuple[List[Dict[str, Any]], int]:
    """
    获取报警记录列表

    Args:
        db: 数据库会话
        page: 页码
        page_size: 每页数量
        is_valid: 是否有效筛选

    Returns:
        (items, total)
    """
    # 构建查询
    query = db.query(CallRecord)

    # 筛选条件
    if is_valid is not None:
        query = query.filter(CallRecord.is_valid == is_valid)

    # 查询总数
    total = query.count()

    # 排序：按报警时间降序
    query = query.order_by(CallRecord.call_time.desc())

    # 分页
    offset = (page - 1) * page_size
    items_db = query.offset(offset).limit(page_size).all()

    # 转换数据
    items = []
    for item in items_db:
        items.append({
            "id": item.id,
            "call_number": item.call_number,
            "reporter_name": item.reporter_name,
            "reporter_phone": item.reporter_phone,
            "call_time": item.call_time,
            "call_address": item.call_address,
            "is_valid": item.is_valid
        })

    return items, total


def get_repeat_reporters(
    db: Session,
    min_count: int = 2
) -> List[Dict[str, Any]]:
    """
    获取重复报警人统计

    Args:
        db: 数据库会话
        min_count: 最小报警次数

    Returns:
        重复报警人列表
    """
    from sqlalchemy import func

    # 按报警人分组统计
    results = db.query(
        CallRecord.reporter_name,
        func.count(CallRecord.id).label('count'),
        func.max(CallRecord.call_time).label('last_call_time')
    ).group_by(
        CallRecord.reporter_name
    ).having(
        func.count(CallRecord.id) >= min_count
    ).order_by(
        func.count(CallRecord.id).desc()
    ).all()

    # 转换为列表
    reporters = []
    for reporter_name, count, last_call_time in results:
        reporters.append({
            "reporter_name": reporter_name,
            "count": count,
            "last_call_time": last_call_time
        })

    return reporters
