from fastapi import APIRouter, Query
from typing import Optional, List

router = APIRouter(prefix="/goals", tags=["Goals"])

employee_assigned_goals = [
    {
        "employee_id": "EMP001",
        "employee_name": "Nguyễn Văn A",
        "department": "Kinh doanh",
        "goal_name": "Doanh số quý 3",
        "target_value": "500 triệu",
        "status": "approved"
    },
    {
        "employee_id": "EMP002",
        "employee_name": "Trần Thị B",
        "department": "Kinh doanh",
        "goal_name": "Số lượng khách hàng mới",    
        "target_value": "30 khách hàng",
        "status": "pending"
    },
    {
        "employee_id": "EMP003",
        "employee_name": "Trần Văn Dũng",
        "department": "Kinh doanh", 
        "goal_name": "Tỷ lệ chuyển đổi",
        "target_value": "25%",
        "status": "rejected"
    },
    {
        "employee_id": "EMP004",
        "employee_name": "Lê Thị Mai",
        "department": "CSKH",
        "goal_name": "Đánh giá hài lòng khách hàng",
        "target_value": "4.5/5 sao",
        "status": "pending"
    },
    {
        "employee_id": "EMP005",
        "employee_name": "Nguyễn Thị C",
        "department": "CSKH",
        "goal_name": "Giải quyết khiếu nại",
        "target_value": "90% trong 24h",
        "status": "approved"
    },
    {
        "employee_id": "EMP006",
        "employee_name": "Phạm Minh Tuấn",
        "department": "IT",
        "goal_name": "Hoàn thành dự án CRM",
        "target_value": "Trước 30/9",
        "status": "approved"
    },
    {
        "employee_id": "EMP007",
        "employee_name": "Hoàng Thị Lan",
        "department": "IT",
        "goal_name": "Giảm thời gian phản hồi hệ thống",
        "target_value": "Dưới 200ms",
        "status": "pending"
    },
    {
        "employee_id": "EMP008",
        "employee_name": "Vũ Đức Thắng",
        "department": "IT",
        "goal_name": "Tỷ lệ uptime hệ thống",
        "target_value": "99.9%",
        "status": "approved"
    }
]

department_goals = [
    {
        "department": "Kinh doanh",
        "goal_name": "Doanh số quý 3",
        "target_value": "500 triệu",
    },
    {
        "department": "Kinh doanh",
        "goal_name": "Số lượng khách hàng mới",
        "target_value": "30 khách hàng",
    },
    {
        "department": "Kinh doanh",
        "goal_name": "Tỷ lệ chuyển đổi",
        "target_value": "25%",
    },
    {
        "department": "CSKH",
        "goal_name": "Đánh giá hài lòng khách hàng",
        "target_value": "4.5/5 sao",
    },
    {
        "department": "CSKH",
        "goal_name": "Giải quyết khiếu nại",
        "target_value": "90% trong 24h",
    },
    {
        "department": "IT",
        "goal_name": "Hoàn thành dự án CRM",
        "target_value": "Trước 30/9",
    },
    {
        "department": "IT",
        "goal_name": "Giảm thời gian phản hồi hệ thống",
        "target_value": "Dưới 200ms",
    },
    {
        "department": "IT",
        "goal_name": "Tỷ lệ uptime hệ thống",
        "target_value": "99.9%",
    }
]
# 2. Hỏi mục tiêu của bộ phận/nhân viên
@router.get("/view")
def view_goal(department: Optional[str] = None, employee_name: Optional[str] = None, employee_id: Optional[str] = None):

    if department:
        return {
            "data": [goal for goal in department_goals if department.lower() in goal["department"].lower()]
        }
    elif employee_name:
        return {
            "data": [goal for goal in employee_assigned_goals if employee_name.lower() in goal["employee_name"].lower()]
        }
    elif employee_id:
        return {
            "data": [goal for goal in employee_assigned_goals if employee_id.lower() in goal["employee_id"].lower()]
        }
    else:
        return {
            "data": employee_assigned_goals
        }

# 3. Nhân viên chưa có mục tiêu
@router.get("/unassigned")
def get_employees_without_goals():
    return {
        "data": [
            {"employee_id": "EMP003", "name": "Trần Văn Dũng", "department": "Kinh doanh"},
            {"employee_id": "EMP004", "name": "Lê Thị Mai", "department": "CSKH"},
            {"employee_id": "EMP005", "name": "Nguyễn Thị C", "department": "CSKH"},
            {"employee_id": "EMP006", "name": "Phạm Minh Tuấn", "department": "IT"},
            {"employee_id": "EMP007", "name": "Hoàng Thị Lan", "department": "IT"},
            {"employee_id": "EMP008", "name": "Vũ Đức Thắng", "department": "IT"}
        ]
    }

# 9. Lấy danh sách kho mục tiêu (dùng để gợi ý)
@router.get("/presets")
def get_preset_goals(department: Optional[str] = None):
    all_goals = [
        {"id": "g001", "goal_name": "Doanh số tháng", "description": "Đạt doanh số tối thiểu theo tháng",  "department": "Kinh doanh"},
        {"id": "g003", "goal_name": "Chăm sóc khách hàng", "description": "Gọi điện chăm sóc 50 KH/tháng", "department": "CSKH"},
        {"id": "g002", "goal_name": "Tăng lượt truy cập website", "description": "Tăng 20% traffic website", "department": "IT"},
        {"id": "g004", "goal_name": "Tổ chức hội thảo", "description": "Tổ chức ít nhất 1 sự kiện trong tháng", "department": "Marketing"}
    ]

    if department:
        return {
            "data": [goal for goal in all_goals if department.lower() in goal["department"].lower()]
        }
    else:
        return {
            "data": all_goals
        }

# 5. Nhắc nhở nhân viên chưa có mục tiêu
@router.get("/remind")
def remind_employees(employee_ids: List[str] = Query(...)):
    return {"message": f"Đã gửi nhắc nhở tới {len(employee_ids)} nhân viên."}

# 6. Mục tiêu cần phê duyệt
@router.get("/pending-approvals")
def get_pending_approvals():
    return {
        "data": [
            {"goal_id": "g001", "employee_name": "Nguyễn Văn A", "goal_name": "Ký 5 hợp đồng", "department": "Kinh doanh"},
            {"goal_id": "g002", "employee_name": "Trần Thị Ngọc", "goal_name": "Tổ chức hội thảo", "department": "Marketing"},
            {"goal_id": "g003", "employee_name": "Lê Thị Mai", "goal_name": "Gọi điện chăm sóc 50 KH/tháng", "department": "CSKH"},
            {"goal_id": "g004", "employee_name": "Phạm Minh Tuấn", "goal_name": "Hoàn thành dự án CRM", "department": "IT"},
            {"goal_id": "g005", "employee_name": "Hoàng Thị Lan", "goal_name": "Giảm thời gian phản hồi hệ thống", "department": "IT"},
            {"goal_id": "g006", "employee_name": "Vũ Đức Thắng", "goal_name": "Tỷ lệ uptime hệ thống", "department": "IT"}
        ]
    }

# 7. Giao mục tiêu
@router.get("/assign")
def assign_goal(employee_id: str, goal_id: str):
    return {"message": f"Đã giao mục tiêu cho nhân viên {employee_id} với mục tiêu {goal_id}"}

# 8. Phê duyệt mục tiêu
@router.get("/approve")
def approve_goal(goal_id: str):
    return {"message": f"Mục tiêu {goal_id} đã được phê duyệt"}
