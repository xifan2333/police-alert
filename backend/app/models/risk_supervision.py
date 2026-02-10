"""执法问题风险盯办数据模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base
from datetime import datetime


class RiskSupervision(Base):
    """执法问题风险盯办表"""
    __tablename__ = "t_risk_supervision"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_number = Column(String(50), unique=True, nullable=False, index=True)
    case_name = Column(String(200), nullable=False)
    case_time = Column(DateTime, nullable=False)
    case_type = Column(String(10), nullable=False)
    risk_issues = Column(Text, nullable=False)  # JSON 数组字符串
    deadline = Column(DateTime, nullable=False, index=True)
    officer_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


    def __repr__(self):
        return f"<RiskSupervision(case_number={self.case_number}, case_name={self.case_name})>"
