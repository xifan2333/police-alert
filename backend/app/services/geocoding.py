"""地理编码服务"""
from sqlalchemy.orm import Session
from app.models.geocoding_cache import GeocodingCache
from typing import Optional, Tuple
from decimal import Decimal


def get_coordinates(
    db: Session,
    address: str
) -> Optional[Tuple[Decimal, Decimal]]:
    """
    获取地址的经纬度（先查缓存，没有则返回None）

    Args:
        db: 数据库会话
        address: 地址

    Returns:
        (longitude, latitude) 或 None
    """
    # 查询缓存
    cache = db.query(GeocodingCache).filter(
        GeocodingCache.address == address
    ).first()

    if cache:
        return (cache.longitude, cache.latitude)

    return None


def save_coordinates(
    db: Session,
    address: str,
    longitude: Decimal,
    latitude: Decimal
) -> GeocodingCache:
    """
    保存地址的经纬度到缓存

    Args:
        db: 数据库会话
        address: 地址
        longitude: 经度
        latitude: 纬度

    Returns:
        缓存记录
    """
    # 检查是否已存在
    cache = db.query(GeocodingCache).filter(
        GeocodingCache.address == address
    ).first()

    if cache:
        # 更新
        cache.longitude = longitude
        cache.latitude = latitude
    else:
        # 创建新记录
        cache = GeocodingCache(
            address=address,
            longitude=longitude,
            latitude=latitude
        )
        db.add(cache)

    db.commit()
    db.refresh(cache)

    return cache


def batch_get_coordinates(
    db: Session,
    addresses: list
) -> dict:
    """
    批量获取地址的经纬度

    Args:
        db: 数据库会话
        addresses: 地址列表

    Returns:
        {address: (longitude, latitude)}
    """
    result = {}

    for address in addresses:
        coords = get_coordinates(db, address)
        if coords:
            result[address] = coords

    return result
