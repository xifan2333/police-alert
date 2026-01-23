"""警情记录数据模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint, Index
from app.core.database import Base
from datetime import datetime


class PoliceAlert(Base):
    """警情记录表"""
    __tablename__ = "t_police_alert"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_number = Column(String(50), unique=True, nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)
    alert_name = Column(String(200), nullable=False)
    alert_time = Column(DateTime, nullable=False)
    location_address = Column(Text)  # 地点地址（文本）
    location_community = Column(String(100))
    reporter_name = Column(String(100))
    officer_name = Column(String(50))
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        CheckConstraint(
            "alert_type IN ('偷盗/传统盗财', '通讯网络诈骗/新型盗财', '涉黄', '涉赌', '纠纷', '人身伤害', '打架斗殴', '其他有效警情')",
            name="check_alert_type"
        ),
        Index('idx_alert_type', 'alert_type'),
        Index('idx_alert_time', 'alert_time'),
        Index('idx_alert_community', 'location_community'),
    )

    def __repr__(self):
        return f"<PoliceAlert(alert_number={self.alert_number}, alert_type={self.alert_type})>"
