"""生成测试数据的临时脚本"""
import pandas as pd
from datetime import datetime, timedelta
import random

# 创建执法问题风险盯办测试数据
def create_risk_supervision_data():
    """创建执法问题风险盯办测试数据"""
    now = datetime.now()

    case_types = ["刑事", "行政", "治安"]
    risk_issues_list = [
        "案件笔录未关联,执法音视频未上传",
        "调解协议书未上传",
        "强制措施超期提醒",
        "案件材料不完整",
        "执法程序不规范"
    ]
    officers = ["张三", "李四", "王五", "赵六", "孙七", "周八"]

    data = []
    for i in range(20):
        case_number = f"330903202401{str(i+1).zfill(6)}"
        case_name = f"案件{i+1}"
        case_time = now - timedelta(days=random.randint(1, 30))
        case_type = random.choice(case_types)
        risk_issues = random.choice(risk_issues_list)
        deadline = now + timedelta(days=random.randint(-5, 15))
        officer_name = random.choice(officers)

        data.append([
            case_number,
            case_name,
            case_time.strftime("%Y-%m-%d %H:%M"),
            case_type,
            risk_issues,
            deadline.strftime("%Y-%m-%d %H:%M"),
            officer_name
        ])

    df = pd.DataFrame(data, columns=[
        "案件编号", "案件名称", "案发时间", "案件类型",
        "风险问题", "整改期限", "责任民警"
    ])

    filename = "执法问题风险盯办_测试数据.xlsx"
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"✅ 已生成: {filename}")
    return filename


# 创建矛盾纠纷闭环管理测试数据
def create_dispute_management_data():
    """创建矛盾纠纷闭环管理测试数据"""
    now = datetime.now()

    event_types = ["邻里纠纷", "物业纠纷", "合同纠纷", "家庭纠纷", "劳资纠纷"]
    risk_levels = ["高", "中", "低"]
    statuses = ["未调解", "待盯办", "调解中", "已调解"]
    officers = ["张三", "李四", "王五", "赵六", "孙七", "周八"]

    contents = [
        "居民张某与李某因楼上漏水问题产生纠纷，双方情绪激动，需要及时调解处理。",
        "业主王某长期占用公共停车位，引发其他业主不满，物业协调未果。",
        "商铺租户与房东因租金上涨问题产生分歧，双方协商未果，需要调解介入。",
        "邻居因装修噪音问题产生矛盾，多次沟通无果，需要第三方调解。",
        "小区业主因宠物饲养问题产生纠纷，影响邻里关系。"
    ]

    data = []
    for i in range(20):
        event_name = f"事件{i+1}"
        event_type = random.choice(event_types)
        content = random.choice(contents)
        event_time = now - timedelta(days=random.randint(1, 30))
        risk_level = random.choice(risk_levels)
        officer_name = random.choice(officers)
        status = random.choice(statuses)

        data.append([
            event_name,
            event_type,
            content,
            event_time.strftime("%Y-%m-%d %H:%M"),
            risk_level,
            officer_name,
            status
        ])

    df = pd.DataFrame(data, columns=[
        "事件名称", "事件类型", "事件内容", "事发时间",
        "风险等级", "责任民警", "处置进度"
    ])

    filename = "矛盾纠纷闭环管理_测试数据.xlsx"
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"✅ 已生成: {filename}")
    return filename


if __name__ == "__main__":
    print("🚀 开始生成测试数据...")
    print()

    # 生成两种类型的测试数据
    risk_file = create_risk_supervision_data()
    dispute_file = create_dispute_management_data()

    print()
    print("=" * 50)
    print("✨ 测试数据生成完成！")
    print()
    print("📁 生成的文件：")
    print(f"  1. {risk_file}")
    print(f"  2. {dispute_file}")
    print()
    print("📝 使用方法：")
    print("  1. 访问管理页面: http://localhost:3000/admin")
    print("  2. 选择对应的数据类型")
    print("  3. 上传生成的 Excel 文件")
    print("=" * 50)
