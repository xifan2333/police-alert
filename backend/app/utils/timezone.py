"""时区工具函数"""
from datetime import datetime, timezone, timedelta
import math


# 中国标准时间 UTC+8
CST = timezone(timedelta(hours=8))


def now_cst() -> datetime:
    """获取当前中国标准时间"""
    return datetime.now(CST)


def calc_days_remaining(deadline: datetime) -> int:
    """
    计算剩余天数

    Args:
        deadline: 截止时间

    Returns:
        剩余天数（向上取整），负数表示已超期
    """
    now = now_cst()

    # 如果 deadline 没有时区信息，假设为 CST
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=CST)

    # 计算时间差（秒）
    delta_seconds = (deadline - now).total_seconds()

    # 转换为天数并向上取整
    days = math.ceil(delta_seconds / 86400)

    return days
