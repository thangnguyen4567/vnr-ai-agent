from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter(prefix="/hr", tags=["human-resources"])

# --- Mock Data ---

# Employee information
mock_employees = {
    "EMP001": {
        "id": "EMP001",
        "full_name": "Nguyễn Văn A",
        "birth_date": date(1990, 5, 15),
        "address": "123 Đường Lê Lợi, Quận 1, TP.HCM",
        "email": "nguyenvana@company.com",
        "phone": "0901234567",
        "department": "Technical",
        "position": "Software Engineer",
        "hire_date": date(2018, 3, 10)
    },
    "EMP002": {
        "id": "EMP002",
        "full_name": "Trần Thị B",
        "birth_date": date(1992, 8, 22),
        "address": "456 Đường Nguyễn Huệ, Quận 3, TP.HCM",
        "email": "tranthib@company.com",
        "phone": "0912345678",
        "department": "Human Resources",
        "position": "HR Specialist",
        "hire_date": date(2019, 7, 5)
    },
    "EMP003": {
        "id": "EMP003",
        "full_name": "Lê Văn C",
        "birth_date": date(1985, 3, 30),
        "address": "789 Đường Cách Mạng Tháng 8, Quận 10, TP.HCM",
        "email": "levanc@company.com",
        "phone": "0923456789",
        "department": "Sales",
        "position": "Sales Manager",
        "hire_date": date(2015, 1, 20)
    }
}

# Work history
mock_work_history = {
    "EMP001": [
        {"date": date(2018, 3, 10), "event": "Joined company", "position": "Intern"},
        {"date": date(2018, 9, 1), "event": "Position change", "position": "Staff"},
        {"date": date(2020, 4, 15), "event": "Promotion", "position": "Software Engineer"}
    ],
    "EMP002": [
        {"date": date(2019, 7, 5), "event": "Joined company", "position": "HR Staff"},
        {"date": date(2021, 7, 10), "event": "Promotion", "position": "HR Specialist"}
    ],
    "EMP003": [
        {"date": date(2015, 1, 20), "event": "Joined company", "position": "Sales Staff"},
        {"date": date(2017, 3, 1), "event": "Promotion", "position": "Deputy Sales Manager"},
        {"date": date(2019, 12, 1), "event": "Promotion", "position": "Sales Manager"}
    ]
}

# --- Model Definitions ---

class WorkHistoryItem(BaseModel):
    date: date
    event: str
    position: str

class WorkHistoryResponse(BaseModel):
    full_name: str
    history: List[WorkHistoryItem]

# --- Route Handlers ---

@router.get("/employee-profile")
async def get_employee_profile(employee_name: str):
    """
    Tra cứu hồ sơ cá nhân
    Example: "Cho tôi xem hồ sơ nhân sự của Nguyễn Văn A"
    """
    for employee in mock_employees.values():
        if employee["full_name"].lower() == employee_name.lower():
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")

@router.get("/work-history")
async def get_work_history(employee_name: str):
    """
    Xem lịch sử công tác
    Example: "Lịch sử thăng chức của tôi ra sao?"
    """
    for employee in mock_employees.values():
        if employee["full_name"].lower() == employee_name.lower():
            return {
                "full_name": employee["full_name"],
                "history": mock_work_history[employee["id"]]
            }
    raise HTTPException(status_code=404, detail="Employee not found")