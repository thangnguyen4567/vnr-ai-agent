from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
import json
from typing import Optional

@tool("get_goal",return_direct=False)
def get_goal(department: Optional[str] = None, config: RunnableConfig = None) -> str:
    """Lấy mục tiêu KPI của tất cả các phòng ban hoặc lấy theo bộ phận"""
    data = [
    {
        "GoalName": "Tổng doanh thu toàn tập đoàn năm 2025",
        "Type": "Tài chính",
        "Department": "Ban điều hành",
        "Representative": "Hoàng Vũ Anh Quân",
        "JobTitle": "Tổng giám đốc",
        "Process": 40,
        "TotalTarget": 120000000000000,
        "DoneTarget": 12000000000000,
        "Allocated": "60%",
        "Weight": "40%"
    },
    {
        "GoalName": "Doanh thu ô tô sản xuất & phân phối",
        "Type": "Tài chính",
        "Department": "CLD AUTO",
        "Representative": "Lê Hồng Hải",
        "JobTitle": "GĐ CLD AUTO",
        "Process": 60,
        "TotalTarget": 60000000000000,
        "DoneTarget": 6000000000000,
        "Allocated": "15%",
        "Weight": "40%"
    },
    {
        "GoalName": "Doanh thu trồng trọt & chế biến",
        "Type": "Tài chính",
        "Department": "CLD AGRICO",
        "Representative": "Nguyễn Xuân Hoài",
        "JobTitle": "GĐ CLD AGRICO",
        "Process": 65,
        "TotalTarget": 20000000000000,
        "DoneTarget": 2000000000000,
        "Allocated": "40%",
        "Weight": "40%"
    },
    {
        "GoalName": "Doanh thu logistics & vận tải",
        "Type": "Tài chính",
        "Department": "CLD LOGI",
        "Representative": "Vũ Văn Thái",
        "JobTitle": "GĐ CLD LOGI",
        "TotalTarget": 15000000000000,
        "DoneTarget": 1500000000000,
        "Allocated": "20%",
        "Weight": "40%"
    },
    {
        "GoalName": "Doanh thu tổng thầu và đầu tư xây dựng",
        "Type": "Tài chính",
        "Department": "CLD DICO",
        "Representative": "Đoàn Trung Hiếu",
        "JobTitle": "GĐ CLD DICO",
        "Process": 50,
        "ParentID": "1",
        "TotalTarget": 15000000000000,
        "DoneTarget": 1500000000000,
        "Allocated": "10%",
        "Weight": "40%"
    },
    {
        "GoalName": "Doanh thu phân phối, bán lẻ & dịch vụ",
        "Type": "Tài chính",
        "Department": "CLD INDUSTRIES",
        "Representative": "Nguyễn Thái Hòa",
        "JobTitle": "GĐ CLD IND",
        "Process": 45,
        "ParentID": "1",
        "TotalTarget": 10000000000000,
        "DoneTarget": 1000000000000,
        "Allocated": "10%",
        "Weight": "40%"
    }
    ]
    if department:
        data = [item for item in data if department.lower() in item["Department"].lower()]

    return json.dumps(data)