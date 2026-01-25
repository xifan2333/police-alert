"""报警记录数据模型 - 按日期统计"""
from sqlalchemy import Column, Integer, String, Date, Index, UniqueConstraint
from app.core.database import Base
from datetime import date


class CallRecord(Base):
    """报警记录表 - 按日期统计重复报警次数"""
    __tablename__ = "t_call_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    call_date = Column(Date, nullable=False, index=True, comment="报警日期")
    call_address = Column(String(200), nullable=False, index=True, comment="报警地点")
    count = Column(Integer, nullable=False, default=1, comment="当日该地点报警次数")

    __table_args__ = (
        UniqueConstraint("call_date", "call_address", name="uq_call_record_date_address"),
        Index('idx_date_address', 'call_date', 'call_address'),
    )

    def __repr__(self):
        return f"<CallRecord(date={self.call_date}, address={self.call_address}, count={self.count})>"
