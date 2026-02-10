"""数据库初始化脚本"""
from app.core.database import engine, Base, SessionLocal
from app.models import DisplayRule
import json


def init_database():
    """初始化数据库"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")

    # 初始化显示规则
    db = SessionLocal()
    try:
        # 检查是否已有规则
        existing_rules = db.query(DisplayRule).count()
        if existing_rules == 0:
            init_display_rules(db)
            db.commit()
            print("显示规则初始化完成")
        else:
            print("显示规则已存在，跳过初始化")
    except Exception as e:
        print(f"初始化显示规则失败: {e}")
        db.rollback()
    finally:
        db.close()

    print("数据库初始化完成！")


def init_display_rules(db):
    """初始化显示规则"""
    rules = [
        # 执法问题盯办 - 整改期限颜色规则
        DisplayRule(
            page_code="risk_supervision",
            table_code=None,  # 页面级规则
            rule_type="color",
            rule_name="整改期限颜色规则",
            rule_config=json.dumps({
                "field": "days_remaining",
                "conditions": [
                    {
                        "operator": "<=",
                        "value": 3,
                        "font_color": "#f5222d"
                    },
                    {
                        "operator": "<=",
                        "value": 7,
                        "font_color": "#faad14"
                    }
                ]
            }, ensure_ascii=False),
            priority=1,
            is_enabled=1,
            description='剩余天数：≤3天<span style="color:#f5222d">红色</span>，≤7天<span style="color:#faad14">黄色</span>'
        ),
        # 矛盾纠纷管理 - 风险等级颜色规则
        DisplayRule(
            page_code="dispute_management",
            table_code=None,  # 页面级规则
            rule_type="color",
            rule_name="风险等级颜色规则",
            rule_config=json.dumps({
                "field": "risk_level",
                "conditions": [
                    {
                        "operator": "eq",
                        "value": "高",
                        "font_color": "#f5222d"
                    },
                    {
                        "operator": "eq",
                        "value": "中",
                        "font_color": "#faad14"
                    },
                    {
                        "operator": "eq",
                        "value": "低",
                        "font_color": "#52c41a"
                    }
                ]
            }, ensure_ascii=False),
            priority=1,
            is_enabled=1,
            description='风险等级：高-<span style="color:#f5222d">红色</span>，中-<span style="color:#faad14">黄色</span>，低-<span style="color:#52c41a">绿色</span>'
        ),
        # 警情态势 - 警情分类总览 - 数量高亮
        DisplayRule(
            page_code="situation",
            table_code="policeClassification",
            rule_type="color",
            rule_name="警情数量高亮",
            rule_config=json.dumps({
                "field": "数量",
                "conditions": [
                    {
                        "operator": ">=",
                        "value": 50,
                        "font_color": "#f5222d"
                    },
                    {
                        "operator": ">=",
                        "value": 30,
                        "font_color": "#faad14"
                    }
                ]
            }, ensure_ascii=False),
            priority=1,
            is_enabled=1,
            description='警情数量：≥50<span style="color:#f5222d">红色</span>，≥30<span style="color:#faad14">黄色</span>'
        ),
        # 警情态势 - 偷盗地点 - 数量高亮
        DisplayRule(
            page_code="situation",
            table_code="theftTraditional",
            rule_type="color",
            rule_name="偷盗数量高亮",
            rule_config=json.dumps({
                "field": "数量",
                "conditions": [
                    {
                        "operator": ">=",
                        "value": 10,
                        "font_color": "#f5222d"
                    },
                    {
                        "operator": ">=",
                        "value": 5,
                        "font_color": "#faad14"
                    }
                ]
            }, ensure_ascii=False),
            priority=1,
            is_enabled=1,
            description='偷盗数量：≥10<span style="color:#f5222d">红色</span>，≥5<span style="color:#faad14">黄色</span>'
        ),
        # 警情态势 - 诈骗小区 - 数量高亮
        DisplayRule(
            page_code="situation",
            table_code="telecomFraud",
            rule_type="color",
            rule_name="诈骗数量高亮",
            rule_config=json.dumps({
                "field": "数量",
                "conditions": [
                    {
                        "operator": ">=",
                        "value": 8,
                        "font_color": "#f5222d"
                    },
                    {
                        "operator": ">=",
                        "value": 4,
                        "font_color": "#faad14"
                    }
                ]
            }, ensure_ascii=False),
            priority=1,
            is_enabled=1,
            description='诈骗数量：≥8<span style="color:#f5222d">红色</span>，≥4<span style="color:#faad14">黄色</span>'
        ),
        # 警情态势 - 重复报警 - 次数高亮
        DisplayRule(
            page_code="situation",
            table_code="repeatAlarms",
            rule_type="color",
            rule_name="重复报警次数高亮",
            rule_config=json.dumps({
                "field": "报警次数",
                "conditions": [
                    {
                        "operator": ">=",
                        "value": 5,
                        "font_color": "#f5222d"
                    },
                    {
                        "operator": ">=",
                        "value": 3,
                        "font_color": "#faad14"
                    }
                ]
            }, ensure_ascii=False),
            priority=1,
            is_enabled=1,
            description='报警次数：≥5<span style="color:#f5222d">红色</span>，≥3<span style="color:#faad14">黄色</span>'
        )
    ]

    for rule in rules:
        db.add(rule)


if __name__ == "__main__":
    init_database()
