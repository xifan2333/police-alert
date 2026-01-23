"""地理编码缓存 Pydantic 模式"""
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class GeocodingCacheBase(BaseModel):
    address: str
    longitude: Decimal
    latitude: Decimal


class GeocodingCacheCreate(GeocodingCacheBase):
    pass


class GeocodingCacheResponse(GeocodingCacheBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
