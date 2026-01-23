"""地理编码缓存数据模型"""
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from app.core.database import Base
from datetime import datetime


class GeocodingCache(Base):
    """地理编码缓存表 - 用于快速本地查询经纬度"""
    __tablename__ = "t_geocoding_cache"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(500), unique=True, nullable=False, index=True)
    longitude = Column(DECIMAL(10, 7), nullable=False)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<GeocodingCache(address={self.address}, lng={self.longitude}, lat={self.latitude})>"
