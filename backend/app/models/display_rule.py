"""显示规则配置数据模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from app.core.database import Base
from datetime import datetime


class DisplayRule(Base):
    """显示规则配置表"""
    __tablename__ = "t_display_rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    page_code = Column(String(50), nullable=False)
    rule_type = Column(String(50), nullable=False)
    rule_name = Column(String(100), nullable=False)
    rule_config = Column(Text, nullable=False)  # JSON 字符串
    priority = Column(Integer, nullable=False, default=0)
    is_enabled = Column(Integer, nullable=False, default=1)
    description = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        Index('idx_display_rule_page_code', 'page_code'),
        Index('idx_display_rule_rule_type', 'rule_type'),
        Index('idx_display_rule_priority', 'priority'),
    )

    def __repr__(self):
        return f"<DisplayRule(page_code={self.page_code}, rule_name={self.rule_name})>"
