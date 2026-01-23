"""数据库初始化脚本"""
from app.core.database import engine, Base, SessionLocal
from app.models import RiskSupervision, DisputeManagement, DisplayRule, PoliceAlert, CallRecord, GeocodingCache
from datetime import datetime, timedelta
import json


def init_database():
    """初始化数据库"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")

    # 初始化示例数据
    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(DisplayRule).count() == 0:
            init_display_rules(db)
            print("显示规则初始化完成")

        if db.query(RiskSupervision).count() == 0:
            init_risk_supervision_data(db)
            print("执法问题示例数据初始化完成")

        if db.query(DisputeManagement).count() == 0:
            init_dispute_management_data(db)
            print("矛盾纠纷示例数据初始化完成")

        if db.query(PoliceAlert).count() == 0:
            init_police_alert_data(db)
            print("警情记录示例数据初始化完成")

        if db.query(CallRecord).count() == 0:
            init_call_record_data(db)
            print("报警记录示例数据初始化完成")

        db.commit()
    except Exception as e:
        print(f"初始化数据时出错: {e}")
        db.rollback()
    finally:
        db.close()

    print("数据库初始化完成！")


def init_display_rules(db):
    """初始化显示规则"""
    rules = [
        # 执法问题风险盯办 - 整改期限颜色规则
        DisplayRule(
            page_code="risk_supervision",
            rule_type="color",
            rule_name="整改期限颜色规则",
            rule_config=json.dumps({
                "field": "days_remaining",
                "conditions": [
                    {
                        "operator": "<=",
                        "value": 3,
                        "font_color": "#f5222d",
                        "background_color": "#fff1f0",
                        "style_token": "deadline_red"
                    },
                    {
                        "operator": "<=",
                        "value": 7,
                        "font_color": "#faad14",
                        "background_color": "#fffbe6",
                        "style_token": "deadline_yellow"
                    }
                ]
            }),
            priority=1,
            is_enabled=1,
            description="根据剩余天数设置颜色：≤3天红色，≤7天黄色"
        ),
        # 矛盾纠纷闭环管理 - 风险等级颜色规则
        DisplayRule(
            page_code="dispute_management",
            rule_type="color",
            rule_name="风险等级颜色规则",
            rule_config=json.dumps({
                "field": "risk_level",
                "conditions": [
                    {
                        "operator": "eq",
                        "value": "高",
                        "font_color": "#f5222d",
                        "background_color": "#fff1f0",
                        "style_token": "risk_high"
                    },
                    {
                        "operator": "eq",
                        "value": "中",
                        "font_color": "#faad14",
                        "background_color": "#fffbe6",
                        "style_token": "risk_mid"
                    },
                    {
                        "operator": "eq",
                        "value": "低",
                        "font_color": "#52c41a",
                        "background_color": "#f6ffed",
                        "style_token": "risk_low"
                    }
                ]
            }),
            priority=1,
            is_enabled=1,
            description="根据风险等级设置颜色：高-红色，中-黄色，低-绿色"
        )
    ]

    for rule in rules:
        db.add(rule)


def init_risk_supervision_data(db):
    """初始化执法问题风险盯办示例数据"""
    now = datetime.now()

    cases = [
        RiskSupervision(
            case_number="330903202401010001",
            case_name="东港路入室盗窃案",
            case_time=now - timedelta(days=5),
            case_type="刑事",
            risk_issues=json.dumps(["案件笔录未关联", "执法音视频未上传"]),
            deadline=now + timedelta(days=2),  # 2天后到期（红色）
            officer_name="张三",
            created_at=now,
            updated_at=now
        ),
        RiskSupervision(
            case_number="330903202401010002",
            case_name="和平小区噪音扰民案",
            case_time=now - timedelta(days=3),
            case_type="行政",
            risk_issues=json.dumps(["调解协议书未上传"]),
            deadline=now + timedelta(days=6),  # 6天后到期（黄色）
            officer_name="李四",
            created_at=now,
            updated_at=now
        ),
        RiskSupervision(
            case_number="330903202401010003",
            case_name="沈家门街道打架斗殴案",
            case_time=now - timedelta(days=7),
            case_type="治安",
            risk_issues=json.dumps(["强制措施超期提醒"]),
            deadline=now + timedelta(days=10),  # 10天后到期（正常）
            officer_name="王五",
            created_at=now,
            updated_at=now
        )
    ]

    for case in cases:
        db.add(case)


def init_dispute_management_data(db):
    """初始化矛盾纠纷闭环管理示例数据"""
    now = datetime.now()

    disputes = [
        DisputeManagement(
            event_name="东港社区邻里纠纷",
            event_type="邻里纠纷",
            content="居民张某与李某因楼上漏水问题产生纠纷，双方情绪激动，需要及时调解处理。",
            event_time=now - timedelta(days=2),
            risk_level="高",
            officer_name="赵六",
            status="未调解",
            created_at=now,
            updated_at=now
        ),
        DisputeManagement(
            event_name="和平小区停车纠纷",
            event_type="物业纠纷",
            content="业主王某长期占用公共停车位，引发其他业主不满，物业协调未果。",
            event_time=now - timedelta(days=1),
            risk_level="中",
            officer_name="孙七",
            status="待盯办",
            created_at=now,
            updated_at=now
        ),
        DisputeManagement(
            event_name="沈家门街道商铺租赁纠纷",
            event_type="合同纠纷",
            content="商铺租户与房东因租金上涨问题产生分歧，双方协商未果，需要调解介入。",
            event_time=now - timedelta(days=3),
            risk_level="低",
            officer_name="周八",
            status="调解中",
            created_at=now,
            updated_at=now
        )
    ]

    for dispute in disputes:
        db.add(dispute)


def init_police_alert_data(db):
    """初始化警情记录示例数据"""
    now = datetime.now()

    alerts = [
        PoliceAlert(
            alert_number="JQ202401230001",
            alert_type="偷盗/传统盗财",
            alert_name="东港小区电动车被盗案",
            alert_time=now - timedelta(days=3),
            location_address="浙江省舟山市普陀区东港街道东港小区3号楼",
            location_community="东港社区",
            reporter_name="张三",
            officer_name="陈警官",
            created_at=now,
            updated_at=now
        ),
        PoliceAlert(
            alert_number="JQ202401230002",
            alert_type="通讯网络诈骗/新型盗财",
            alert_name="网络刷单诈骗案",
            alert_time=now - timedelta(days=2),
            location_address="浙江省舟山市普陀区沈家门街道和平路128号",
            location_community="沈家门社区",
            reporter_name="李四",
            officer_name="林警官",
            created_at=now,
            updated_at=now
        ),
        PoliceAlert(
            alert_number="JQ202401230003",
            alert_type="纠纷",
            alert_name="和平小区邻里纠纷",
            alert_time=now - timedelta(days=1),
            location_address="浙江省舟山市普陀区东港街道和平小区5栋",
            location_community="东港社区",
            reporter_name="王五",
            officer_name="黄警官",
            created_at=now,
            updated_at=now
        )
    ]

    for alert in alerts:
        db.add(alert)


def init_call_record_data(db):
    """初始化报警记录示例数据"""
    now = datetime.now()

    calls = [
        CallRecord(
            call_number="BJ202401230001",
            reporter_name="张三",
            reporter_phone="13800138000",
            call_time=now - timedelta(days=3, hours=2),
            call_address="东港小区3号楼",
            is_valid=1,
            created_at=now,
            updated_at=now
        ),
        CallRecord(
            call_number="BJ202401230002",
            reporter_name="李四",
            reporter_phone="13800138001",
            call_time=now - timedelta(days=2, hours=5),
            call_address="沈家门街道和平路128号",
            is_valid=1,
            created_at=now,
            updated_at=now
        ),
        CallRecord(
            call_number="BJ202401230003",
            reporter_name="张三",
            reporter_phone="13800138000",
            call_time=now - timedelta(days=2, hours=1),
            call_address="东港小区5栋",
            is_valid=1,
            created_at=now,
            updated_at=now
        ),
        CallRecord(
            call_number="BJ202401230004",
            reporter_name="张三",
            reporter_phone="13800138000",
            call_time=now - timedelta(days=1, hours=3),
            call_address="东港小区门口",
            is_valid=0,  # 恶意报警
            created_at=now,
            updated_at=now
        )
    ]

    for call in calls:
        db.add(call)


if __name__ == "__main__":
    init_database()


def init_display_rules(db):
    """初始化显示规则"""
    rules = [
        # 执法问题风险盯办 - 整改期限颜色规则
        DisplayRule(
            page_code="risk_supervision",
            rule_type="color",
            rule_name="整改期限颜色规则",
            rule_config=json.dumps({
                "field": "days_remaining",
                "conditions": [
                    {
                        "operator": "<=",
                        "value": 3,
                        "font_color": "#f5222d",
                        "background_color": "#fff1f0",
                        "style_token": "deadline_red"
                    },
                    {
                        "operator": "<=",
                        "value": 7,
                        "font_color": "#faad14",
                        "background_color": "#fffbe6",
                        "style_token": "deadline_yellow"
                    }
                ]
            }),
            priority=1,
            is_enabled=1,
            description="根据剩余天数设置颜色：≤3天红色，≤7天黄色"
        ),
        # 矛盾纠纷闭环管理 - 风险等级颜色规则
        DisplayRule(
            page_code="dispute_management",
            rule_type="color",
            rule_name="风险等级颜色规则",
            rule_config=json.dumps({
                "field": "risk_level",
                "conditions": [
                    {
                        "operator": "eq",
                        "value": "高",
                        "font_color": "#f5222d",
                        "background_color": "#fff1f0",
                        "style_token": "risk_high"
                    },
                    {
                        "operator": "eq",
                        "value": "中",
                        "font_color": "#faad14",
                        "background_color": "#fffbe6",
                        "style_token": "risk_mid"
                    },
                    {
                        "operator": "eq",
                        "value": "低",
                        "font_color": "#52c41a",
                        "background_color": "#f6ffed",
                        "style_token": "risk_low"
                    }
                ]
            }),
            priority=1,
            is_enabled=1,
            description="根据风险等级设置颜色：高-红色，中-黄色，低-绿色"
        )
    ]

    for rule in rules:
        db.add(rule)


def init_risk_supervision_data(db):
    """初始化执法问题风险盯办示例数据"""
    now = datetime.now()

    cases = [
        RiskSupervision(
            case_number="330903202401010001",
            case_name="东港路入室盗窃案",
            case_time=now - timedelta(days=5),
            case_type="刑事",
            risk_issues=json.dumps(["案件笔录未关联", "执法音视频未上传"]),
            deadline=now + timedelta(days=2),  # 2天后到期（红色）
            officer_name="张三",
            created_at=now,
            updated_at=now
        ),
        RiskSupervision(
            case_number="330903202401010002",
            case_name="和平小区噪音扰民案",
            case_time=now - timedelta(days=3),
            case_type="行政",
            risk_issues=json.dumps(["调解协议书未上传"]),
            deadline=now + timedelta(days=6),  # 6天后到期（黄色）
            officer_name="李四",
            created_at=now,
            updated_at=now
        ),
        RiskSupervision(
            case_number="330903202401010003",
            case_name="沈家门街道打架斗殴案",
            case_time=now - timedelta(days=7),
            case_type="治安",
            risk_issues=json.dumps(["强制措施超期提醒"]),
            deadline=now + timedelta(days=10),  # 10天后到期（正常）
            officer_name="王五",
            created_at=now,
            updated_at=now
        )
    ]

    for case in cases:
        db.add(case)


def init_dispute_management_data(db):
    """初始化矛盾纠纷闭环管理示例数据"""
    now = datetime.now()

    disputes = [
        DisputeManagement(
            event_name="东港社区邻里纠纷",
            event_type="邻里纠纷",
            content="居民张某与李某因楼上漏水问题产生纠纷，双方情绪激动，需要及时调解处理。",
            event_time=now - timedelta(days=2),
            risk_level="高",
            officer_name="赵六",
            status="未调解",
            created_at=now,
            updated_at=now
        ),
        DisputeManagement(
            event_name="和平小区停车纠纷",
            event_type="物业纠纷",
            content="业主王某长期占用公共停车位，引发其他业主不满，物业协调未果。",
            event_time=now - timedelta(days=1),
            risk_level="中",
            officer_name="孙七",
            status="待盯办",
            created_at=now,
            updated_at=now
        ),
        DisputeManagement(
            event_name="沈家门街道商铺租赁纠纷",
            event_type="合同纠纷",
            content="商铺租户与房东因租金上涨问题产生分歧，双方协商未果，需要调解介入。",
            event_time=now - timedelta(days=3),
            risk_level="低",
            officer_name="周八",
            status="调解中",
            created_at=now,
            updated_at=now
        )
    ]

    for dispute in disputes:
        db.add(dispute)


if __name__ == "__main__":
    init_database()
