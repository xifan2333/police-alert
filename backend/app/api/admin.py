"""管理后台 API"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import risk_supervision, dispute_management, display_rule
from app.models import RiskSupervision, DisputeManagement, DisplayRule, PoliceAlert, CallRecord
import pandas as pd
import json
from datetime import datetime
from typing import Optional
import os

router = APIRouter(prefix="/admin", tags=["管理后台"])


@router.get("/template/{data_type}")
async def download_template(data_type: str):
    """
    下载 Excel 模板

    Args:
        data_type: 数据类型 (risk_supervision | dispute_management | police_alert | call_record)
    """
    templates = {
        "risk_supervision": {
            "filename": "执法问题风险盯办_模板.xlsx",
            "columns": [
                "案件编号", "案件名称", "案发时间", "案件类型",
                "风险问题", "整改期限", "责任民警"
            ]
        },
        "dispute_management": {
            "filename": "矛盾纠纷闭环管理_模板.xlsx",
            "columns": [
                "事件名称", "事件类型", "事件内容", "事发时间",
                "风险等级", "责任民警", "处置进度"
            ]
        },
        "police_alert": {
            "filename": "警情记录_模板.xlsx",
            "columns": [
                "警情编号", "警情类型", "警情名称", "警情时间",
                "地点地址", "所属社区", "报警人姓名", "责任民警"
            ]
        },
        "call_record": {
            "filename": "报警记录_模板.xlsx",
            "columns": [
                "报警编号", "报��人姓名", "报警人电话", "报警时间",
                "报警地点", "是否有效"
            ]
        }
    }

    if data_type not in templates:
        raise HTTPException(status_code=400, detail="无效的数据类型")

    template_info = templates[data_type]

    # 创建示例数据
    df = pd.DataFrame(columns=template_info["columns"])

    # 添加示例行
    if data_type == "risk_supervision":
        df.loc[0] = [
            "330903202401010001",
            "示例案件",
            "2026-01-20 10:00",
            "刑事",
            "案件笔录未关联,执法音视频未上传",
            "2026-01-30 18:00",
            "张三"
        ]
    elif data_type == "dispute_management":
        df.loc[0] = [
            "东港社区邻里纠纷",
            "邻里纠纷",
            "居民张某与李某因楼上漏水问题产生纠纷",
            "2026-01-20 10:00",
            "高",
            "赵六",
            "未调解"
        ]
    elif data_type == "police_alert":
        df.loc[0] = [
            "JQ202401230001",
            "偷盗/传统盗财",
            "东港小区电动车被盗案",
            "2026-01-20 08:30",
            "浙江省舟山市普陀区东港街道东港小区3号楼",
            "东港社区",
            "张三",
            "陈警官"
        ]
    elif data_type == "call_record":
        df.loc[0] = [
            "BJ202401230001",
            "张三",
            "13800138000",
            "2026-01-20 08:30",
            "东港小区3号楼",
            "是"
        ]

    # 保存到临时文件
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file = os.path.join(temp_dir, template_info["filename"])

    df.to_excel(temp_file, index=False, engine='openpyxl')

    return FileResponse(
        temp_file,
        filename=template_info["filename"],
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@router.post("/import")
async def import_data(
    file: UploadFile = File(...),
    data_type: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    导入 Excel 数据

    Args:
        file: Excel 文件
        data_type: 数据类型 (risk_supervision | dispute_management | police_alert | call_record)
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="只支持 Excel 文件")

    try:
        # 读取 Excel
        df = pd.read_excel(file.file, engine='openpyxl')

        imported_count = 0

        if data_type == "risk_supervision":
            # 清空现有数据
            db.query(RiskSupervision).delete()

            # 导入新数据
            for _, row in df.iterrows():
                # 解析风险问题
                risk_issues = row['风险问题'].split(',') if pd.notna(row['风险问题']) else []

                # 解析日期
                case_time = pd.to_datetime(row['案发时间']) if pd.notna(row['案发时间']) else datetime.now()
                deadline = pd.to_datetime(row['整改期限']) if pd.notna(row['整改期限']) else datetime.now()

                item = RiskSupervision(
                    case_number=str(row['案件编号']),
                    case_name=str(row['案件名称']),
                    case_time=case_time,
                    case_type=str(row['案件类型']),
                    risk_issues=json.dumps(risk_issues, ensure_ascii=False),
                    deadline=deadline,
                    officer_name=str(row['责任民警']),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.add(item)
                imported_count += 1

        elif data_type == "dispute_management":
            # 清空现有数据
            db.query(DisputeManagement).delete()

            # 导入新数据
            for _, row in df.iterrows():
                # 解析日期
                event_time = pd.to_datetime(row['事发时间']) if pd.notna(row['事发时间']) else datetime.now()

                item = DisputeManagement(
                    event_name=str(row['事件名称']),
                    event_type=str(row['事件类型']),
                    content=str(row['事件内容']),
                    event_time=event_time,
                    risk_level=str(row['风险等级']),
                    officer_name=str(row['责任民警']),
                    status=str(row['处置进度']),
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.add(item)
                imported_count += 1

        elif data_type == "police_alert":
            # 清空现有数据
            db.query(PoliceAlert).delete()

            # 导入新数据
            for _, row in df.iterrows():
                # 解析日期
                alert_time = pd.to_datetime(row['警情时间']) if pd.notna(row['警情时间']) else datetime.now()

                item = PoliceAlert(
                    alert_number=str(row['警情编号']),
                    alert_type=str(row['警情类型']),
                    alert_name=str(row['警情名称']),
                    alert_time=alert_time,
                    location_address=str(row['地点地址']) if pd.notna(row['地点地址']) else None,
                    location_community=str(row['所属社区']) if pd.notna(row['所属社区']) else None,
                    reporter_name=str(row['报警人姓名']) if pd.notna(row['报警人姓名']) else None,
                    officer_name=str(row['责任民警']) if pd.notna(row['责任民警']) else None,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.add(item)
                imported_count += 1

        elif data_type == "call_record":
            # 清空现有数据
            db.query(CallRecord).delete()

            # 导入新数据
            for _, row in df.iterrows():
                # 解析日期
                call_time = pd.to_datetime(row['报警时间']) if pd.notna(row['报警时间']) else datetime.now()

                # 解析是否有效
                is_valid = 1 if str(row['是否有效']) == '是' else 0

                item = CallRecord(
                    call_number=str(row['报警编号']),
                    reporter_name=str(row['报警人姓名']),
                    reporter_phone=str(row['报警人电话']) if pd.notna(row['报警人电话']) else None,
                    call_time=call_time,
                    call_address=str(row['报警地点']) if pd.notna(row['报警地点']) else None,
                    is_valid=is_valid,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.add(item)
                imported_count += 1

        else:
            raise HTTPException(status_code=400, detail="无效的数据类型")

        db.commit()

        return {
            "code": 200,
            "message": "导入成功",
            "data": {
                "imported_count": imported_count
            }
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")


@router.get("/rules")
async def get_rules(db: Session = Depends(get_db)):
    """获取所有规则"""
    rules = db.query(DisplayRule).order_by(DisplayRule.page_code, DisplayRule.priority).all()

    result = []
    for rule in rules:
        result.append({
            "id": rule.id,
            "page_code": rule.page_code,
            "rule_type": rule.rule_type,
            "rule_name": rule.rule_name,
            "rule_config": json.loads(rule.rule_config),
            "priority": rule.priority,
            "is_enabled": rule.is_enabled,
            "description": rule.description
        })

    return {
        "code": 200,
        "data": result
    }


@router.post("/rules")
async def create_rule(rule_data: dict, db: Session = Depends(get_db)):
    """创建新规则"""
    try:
        rule = DisplayRule(
            page_code=rule_data["page_code"],
            rule_type=rule_data.get("rule_type", "color"),
            rule_name=rule_data["rule_name"],
            rule_config=json.dumps(rule_data["rule_config"], ensure_ascii=False),
            priority=rule_data.get("priority", 1),
            is_enabled=rule_data.get("is_enabled", 1),
            description=rule_data.get("description", "")
        )
        db.add(rule)
        db.commit()
        db.refresh(rule)

        return {
            "code": 200,
            "message": "创建成功",
            "data": {"id": rule.id}
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")


@router.put("/rules/{rule_id}")
async def update_rule(
    rule_id: int,
    rule_data: dict,
    db: Session = Depends(get_db)
):
    """更新规则"""
    rule = db.query(DisplayRule).filter(DisplayRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")

    # 更新字段
    if "page_code" in rule_data:
        rule.page_code = rule_data["page_code"]
    if "rule_type" in rule_data:
        rule.rule_type = rule_data["rule_type"]
    if "rule_name" in rule_data:
        rule.rule_name = rule_data["rule_name"]
    if "description" in rule_data:
        rule.description = rule_data["description"]
    if "is_enabled" in rule_data:
        rule.is_enabled = rule_data["is_enabled"]
    if "priority" in rule_data:
        rule.priority = rule_data["priority"]
    if "rule_config" in rule_data:
        rule.rule_config = json.dumps(rule_data["rule_config"], ensure_ascii=False)

    db.commit()

    return {
        "code": 200,
        "message": "更新成功"
    }


@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    """删除规则"""
    rule = db.query(DisplayRule).filter(DisplayRule.id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")

    db.delete(rule)
    db.commit()

    return {
        "code": 200,
        "message": "删除成功"
    }
