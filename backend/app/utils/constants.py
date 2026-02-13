"""共享常量定义"""

# ==================== 执法问题盯办 ====================

# 案件类型
CASE_TYPE_OPTIONS = ["刑事", "行政", "治安"]

# 风险类型
RISK_TYPE_OPTIONS = ["初侦初查问题", "涉案财物问题", "办案期限问题"]

# 风险问题
RISK_ISSUE_OPTIONS = [
    "案件笔录未关联",
    "文书未开具",
    "调解协议书未上传",
    "执法音视频未上传",
    "涉案物品未出入库",
    "未结案卷未归档",
    "治安案件延长审批",
    "强制措施超期提醒"
]

# 问题类型
PROBLEM_TYPE_OPTIONS = [
    "文书开具",
    "笔录上传",
    "办案期限",
    "音视频上传",
    "调查取证",
    "涉案财物",
    "办案程序",
    "其它"
]

PROBLEM_TYPE_DEFAULT = "其它"


# ==================== 矛盾纠纷管理 ====================

# 风险等级
RISK_LEVEL_OPTIONS = ["高", "中", "低"]

# 处置进度
DISPUTE_STATUS_OPTIONS = ["待化解", "待关注", "调解中", "已调解"]


# ==================== 工具函数 ====================

def normalize_problem_type(value) -> tuple[str, bool]:
    """
    标准化问题类型值

    Returns:
        (标准化后的值, 是否使用了默认值)
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        return PROBLEM_TYPE_DEFAULT, True

    normalized = str(value).strip()
    if normalized in PROBLEM_TYPE_OPTIONS:
        return normalized, False

    return PROBLEM_TYPE_DEFAULT, True
