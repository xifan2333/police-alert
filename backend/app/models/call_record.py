"""报警记录数据模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from app.core.database import Base
from datetime import datetime


class CallRecord(Base):
    """报警记录表"""
    __tablename__ = "t_call_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    call_number = Column(String(50), unique=True, nullable=False, index=True)
    reporter_name = Column(String(100), nullable=False, index=True)
    reporter_phone = Column(String(20))
    call_time = Column(DateTime, nullable=False, index=True)
    call_address = Column(Text)
    is_valid = Column(Integer, nullable=False, default=1)  # 是否有效（0否/1是）
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        Index('idx_call_reporter', 'reporter_name'),
        Index('idx_call_time', 'call_time'),
    )

    def __repr__(self):
        return f"<CallRecord(call_number={self.call_number}, reporter_name={self.reporter_name})>"
