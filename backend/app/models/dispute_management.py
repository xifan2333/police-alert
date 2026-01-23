"""矛盾纠纷闭环管理数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, Index
from app.core.database import Base
from datetime import datetime


class DisputeManagement(Base):
    """矛盾纠纷闭环管理表"""
    __tablename__ = "t_dispute_management"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String(200), nullable=False)
    event_type = Column(String(100), nullable=False)
    content = Column(String(150), nullable=False)
    event_time = Column(DateTime, nullable=False)
    risk_level = Column(String(10), nullable=False)
    officer_name = Column(String(50), nullable=False)
    status = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint("length(content) <= 150", name="check_content_length"),
        CheckConstraint("risk_level IN ('高', '中', '低')", name="check_risk_level"),
        CheckConstraint("status IN ('未调解', '待盯办', '调解中', '已调解')", name="check_status"),
        Index('idx_dispute_status_risk', 'status', 'risk_level'),
        Index('idx_dispute_event_time', 'event_time'),
        Index('idx_dispute_risk_level', 'risk_level'),
    )

    def __repr__(self):
        return f"<DisputeManagement(event_name={self.event_name}, status={self.status})>"
