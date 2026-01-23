"""数据 API 路由"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import risk_supervision, dispute_management, police_alert, call_record
from typing import Optional

router = APIRouter()


@router.get("/risk-supervision", tags=["数据"])
def get_risk_supervision(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    include_rules: bool = Query(True, description="是否包含规则"),
    db: Session = Depends(get_db)
):
    """获取执法问题风险盯办列表"""
    items, total, rules = risk_supervision.list_risk_supervision(
        db, page, page_size, include_rules
    )

    return {
        "code": 200,
        "data": {
            "total": total,
            "items": items,
            "rules": rules if include_rules else []
        }
    }


@router.get("/dispute-management", tags=["数据"])
def get_dispute_management(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="处置进度筛选"),
    risk_level: Optional[str] = Query(None, description="风险等级筛选"),
    include_rules: bool = Query(True, description="是否包含规则"),
    db: Session = Depends(get_db)
):
    """获取矛盾纠纷闭环管理列表"""
    items, total, rules = dispute_management.list_dispute_management(
        db, page, page_size, status, risk_level, include_rules
    )

    return {
        "code": 200,
        "data": {
            "total": total,
            "items": items,
            "rules": rules if include_rules else []
        }
    }


@router.get("/police-alerts", tags=["数据"])
def get_police_alerts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    alert_type: Optional[str] = Query(None, description="警情类型筛选"),
    start_time: Optional[str] = Query(None, description="开始时间"),
    end_time: Optional[str] = Query(None, description="结束时间"),
    community: Optional[str] = Query(None, description="社区筛选"),
    db: Session = Depends(get_db)
):
    """获取警情记录列表"""
    items, total = police_alert.list_police_alerts(
        db, page, page_size, alert_type, start_time, end_time, community
    )

    return {
        "code": 200,
        "data": {
            "total": total,
            "items": items
        }
    }


@router.get("/police-alerts/statistics", tags=["数据"])
def get_alert_statistics(
    time_range: str = Query("month", description="时间范围（week/month/year）"),
    db: Session = Depends(get_db)
):
    """获取警情类型统计"""
    statistics = police_alert.get_alert_statistics(db, time_range)

    return {
        "code": 200,
        "data": statistics
    }


@router.get("/police-alerts/location-distribution", tags=["数据"])
def get_location_distribution(
    alert_type: str = Query(..., description="警情类型"),
    time_range: str = Query("month", description="时间范围（week/month/year）"),
    db: Session = Depends(get_db)
):
    """获取指定警情类型的地点分布"""
    distribution = police_alert.get_location_distribution(db, alert_type, time_range)

    return {
        "code": 200,
        "data": distribution
    }


@router.get("/call-records", tags=["数据"])
def get_call_records(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    is_valid: Optional[int] = Query(None, description="是否有效筛选（0否/1是）"),
    db: Session = Depends(get_db)
):
    """获取报警记录列表"""
    items, total = call_record.list_call_records(db, page, page_size, is_valid)

    return {
        "code": 200,
        "data": {
            "total": total,
            "items": items
        }
    }


@router.get("/call-records/repeat-reporters", tags=["数据"])
def get_repeat_reporters(
    min_count: int = Query(2, ge=2, description="最小报警次数"),
    db: Session = Depends(get_db)
):
    """获取重复报警人统计"""
    reporters = call_record.get_repeat_reporters(db, min_count)

    return {
        "code": 200,
        "data": reporters
    }


@router.get("/situation", tags=["数据"])
def get_situation_data():
    """获取警情态势页面所需的所有数据"""
    
    # 警情分类同环比分析
    police_classification = [
        ['偷盗/传统盗财', 10, '10%', '5%'],
        ['通讯网络诈骗/新型盗财', 20, '12%', '8%'],
        ['涉黄', 5, '5%', '2%'],
        ['涉赌', 8, '8%', '3%'],
        ['纠纷', 15, '15%', '10%'],
        ['人身伤害', 12, '10%', '6%'],
        ['有效警情', 70, '10%', '5%']
    ]

    # 偷盗/传统盗财详情
    theft_traditional = [
        ['地点A', 5],
        ['地点B', 4],
        ['地点C', 3],
        ['地点D', 2],
        ['地点E', 1]
    ]

    # 电诈/新型盗财详情
    telecom_fraud = [
        ['小区A', 5],
        ['小区B', 4],
        ['小区C', 3],
        ['小区D', 2],
        ['小区E', 1]
    ]

    # 涉黄案件详情
    vice_cases = [
        ['小区A', 5],
        ['小区B', 4],
        ['小区C', 3],
        ['小区D', 2],
        ['小区E', 1]
    ]

    # 纠纷案件详情
    dispute_cases = [
        ['社区A', 5],
        ['社区B', 4],
        ['社区C', 3],
        ['社区D', 2],
        ['社区E', 1]
    ]

    # 打架斗殴案件详情
    fight_cases = [
        ['区域A', 5],
        ['区域B', 4],
        ['区域C', 3],
        ['区域D', 2],
        ['区域E', 1]
    ]

    # 涉赌案件详情
    gambling_cases = [
        ['地点A', 5],
        ['地点B', 4],
        ['地点C', 3],
        ['地点D', 2],
        ['地点E', 1]
    ]

    # 重复报警案件展示
    repeat_alarms = [
        ['张三', 5, '2023-10-27'],
        ['李四', 4, '2023-10-26'],
        ['王五', 3, '2023-10-25'],
        ['赵六', 2, '2023-10-24'],
        ['钱七', 1, '2023-10-23']
    ]

    # 社区数据
    communities = [
        { "name": "社区A", "lng": 122.3, "lat": 29.95, "caseCount": 10, "disputeCount": 5 },
        { "name": "社区B", "lng": 122.31, "lat": 29.96, "caseCount": 8, "disputeCount": 3 },
        { "name": "社区C", "lng": 122.32, "lat": 29.94, "caseCount": 12, "disputeCount": 7 }
    ]

    return {
        "code": 200,
        "data": {
            "policeClassification": police_classification,
            "theftTraditional": theft_traditional,
            "telecomFraud": telecom_fraud,
            "viceCases": vice_cases,
            "disputeCases": dispute_cases,
            "fightCases": fight_cases,
            "gamblingCases": gambling_cases,
            "repeatAlarms": repeat_alarms,
            "communities": communities
        }
    }
