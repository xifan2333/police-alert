"""警情记录数据模型 - 按日期统计"""
from sqlalchemy import Column, Integer, String, Date, CheckConstraint, Index, UniqueConstraint
from app.core.database import Base
from datetime import date


class PoliceAlert(Base):
    """警情记录表 - 按日期统计次数"""
    __tablename__ = "t_police_alert"

    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_date = Column(Date, nullable=False, index=True, comment="警情日期")
    alert_type = Column(String(50), nullable=False, index=True, comment="警情类型")
    location = Column(String(100), nullable=False, index=True, comment="地点")
    count = Column(Integer, nullable=False, default=1, comment="当日该类型该地点警情次数")

    __table_args__ = (
        CheckConstraint(
            "alert_type IN ('偷盗', '诈骗', '涉黄', '涉赌', '纠纷', '人身伤害')",
            name="check_alert_type"
        ),
        UniqueConstraint("alert_date", "alert_type", "location", name="uq_police_alert_date_type_location"),
        Index('idx_date_type_location', 'alert_date', 'alert_type', 'location'),
    )

    def __repr__(self):
        return f"<PoliceAlert(date={self.alert_date}, type={self.alert_type}, location={self.location}, count={self.count})>"
