"""时间维度工具函数"""
from datetime import datetime, timedelta
from typing import Tuple


def get_time_range(time_range: str) -> Tuple[datetime, datetime]:
    """
    根据时间维度获取时间范围

    Args:
        time_range: 时间维度（week/month/year）

    Returns:
        (start_time, end_time)
    """
    now = datetime.now()

    if time_range == "week":
        # 本周：从周一开始
        start_time = now - timedelta(days=now.weekday())
        start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now
    elif time_range == "month":
        # 本月：从月初开始
        start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_time = now
    elif time_range == "year":
        # 本年：从年初开始
        start_time = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_time = now
    else:
        # 默认本月
        start_time = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_time = now

    return start_time, end_time


def get_comparison_time_range(time_range: str) -> Tuple[Tuple[datetime, datetime], Tuple[datetime, datetime]]:
    """
    获取同比和环比的时间范围

    Args:
        time_range: 时间维度（week/month/year）

    Returns:
        ((mom_start, mom_end), (yoy_start, yoy_end))
    """
    now = datetime.now()

    if time_range == "week":
        # 环比：上周
        mom_end = now - timedelta(days=now.weekday())
        mom_end = mom_end.replace(hour=23, minute=59, second=59)
        mom_start = mom_end - timedelta(days=6)
        mom_start = mom_start.replace(hour=0, minute=0, second=0)

        # 同比：去年同周
        yoy_end = now - timedelta(days=365)
        yoy_end = yoy_end - timedelta(days=yoy_end.weekday()) + timedelta(days=6)
        yoy_start = yoy_end - timedelta(days=6)
        yoy_start = yoy_start.replace(hour=0, minute=0, second=0)

    elif time_range == "month":
        # 环比：上月
        if now.month == 1:
            mom_start = datetime(now.year - 1, 12, 1)
        else:
            mom_start = datetime(now.year, now.month - 1, 1)

        mom_end = now.replace(day=1, hour=0, minute=0, second=0) - timedelta(seconds=1)

        # 同比：去年同月
        yoy_start = datetime(now.year - 1, now.month, 1)
        if now.month == 12:
            yoy_end = datetime(now.year, 1, 1) - timedelta(seconds=1)
        else:
            yoy_end = datetime(now.year - 1, now.month + 1, 1) - timedelta(seconds=1)

    elif time_range == "year":
        # 环比：去年
        mom_start = datetime(now.year - 1, 1, 1)
        mom_end = datetime(now.year, 1, 1) - timedelta(seconds=1)

        # 同比：前年
        yoy_start = datetime(now.year - 2, 1, 1)
        yoy_end = datetime(now.year - 1, 1, 1) - timedelta(seconds=1)

    else:
        # 默认本月
        if now.month == 1:
            mom_start = datetime(now.year - 1, 12, 1)
        else:
            mom_start = datetime(now.year, now.month - 1, 1)

        mom_end = now.replace(day=1, hour=0, minute=0, second=0) - timedelta(seconds=1)

        yoy_start = datetime(now.year - 1, now.month, 1)
        if now.month == 12:
            yoy_end = datetime(now.year, 1, 1) - timedelta(seconds=1)
        else:
            yoy_end = datetime(now.year - 1, now.month + 1, 1) - timedelta(seconds=1)

    return (mom_start, mom_end), (yoy_start, yoy_end)


def calculate_comparison(current: int, previous: int) -> str:
    """
    计算同比或环比

    Args:
        current: 当前值
        previous: 对比值

    Returns:
        比较结果字符串（如 "+5.2%" 或 "-3.1%"）
    """
    if previous == 0:
        if current == 0:
            return "0%"
        else:
            return "+100%"

    change = ((current - previous) / previous) * 100

    if change > 0:
        return f"+{change:.1f}%"
    elif change < 0:
        return f"{change:.1f}%"
    else:
        return "0%"
