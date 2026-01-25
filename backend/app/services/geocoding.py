"""地理编码服务"""
from sqlalchemy.orm import Session
from app.models.geocoding_cache import GeocodingCache
from typing import Optional, Tuple
from decimal import Decimal
import httpx
import json
import logging

logger = logging.getLogger(__name__)


async def get_coordinates_with_api(
    db: Session,
    address: str,
    tianditu_key: str
) -> Optional[Tuple[Decimal, Decimal]]:
    """
    获取地址的经纬度（先查缓存，没有则调用天地图API）

    Args:
        db: 数据库会话
        address: 地址
        tianditu_key: 天地图API密钥

    Returns:
        (longitude, latitude) 或 None
    """
    # 1. 先查缓存
    cache = db.query(GeocodingCache).filter(
        GeocodingCache.address == address
    ).first()

    if cache:
        logger.info(f"从缓存获取坐标: {address}")
        return (cache.longitude, cache.latitude)

    # 2. 缓存中没有，调用天地图API
    if not tianditu_key:
        logger.warning("天地图API Key未配置")
        return None

    try:
        coords = await fetch_from_tianditu(address, tianditu_key)
        if coords:
            # 3. 存入缓存
            save_coordinates(db, address, coords[0], coords[1])
            logger.info(f"从天地图获取并缓存坐标: {address}")
            return coords
    except Exception as e:
        logger.error(f"获取坐标失败: {address}, 错误: {e}")

    return None


async def fetch_from_tianditu(address: str, api_key: str) -> Optional[Tuple[Decimal, Decimal]]:
    """
    从天地图API获取坐标

    Args:
        address: 地址
        api_key: API密钥

    Returns:
        (longitude, latitude) 或 None
    """
    url = "http://api.tianditu.gov.cn/geocoder"
    params = {
        "ds": json.dumps({"keyWord": address}),
        "tk": api_key
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "0" and data.get("location"):
                location = data["location"]
                lon = Decimal(str(location["lon"]))
                lat = Decimal(str(location["lat"]))
                return (lon, lat)
            else:
                logger.warning(f"天地图API返回错误: {data}")
                return None
    except Exception as e:
        logger.error(f"调用天地图API失败: {e}")
        return None


def get_coordinates(
    db: Session,
    address: str
) -> Optional[Tuple[Decimal, Decimal]]:
    """
    获取地址的经纬度（仅查缓存）

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
