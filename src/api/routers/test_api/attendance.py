from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from enum import Enum

router = APIRouter(prefix="/attendance", tags=["attendance"])

# --- Mock Data ---

# Employee IDs matching those in human-resources.py
employees = ["EMP001", "EMP002", "EMP003"]

# Leave types
class LeaveType(str, Enum):
    ANNUAL = "annual"
    SICK = "sick"
    PERSONAL = "personal"
    UNPAID = "unpaid"
    OTHER = "other"

# Leave request status
class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

# Leave balance by employee
leave_balance = {
    "EMP001": {
        "annual": 12,
        "sick": 30,
        "personal": 3,
    },
    "EMP002": {
        "annual": 14,
        "sick": 30,
        "personal": 3,
    },
    "EMP003": {
        "annual": 18,
        "sick": 30,
        "personal": 3,
    }
}

# Leave requests
leave_requests = [
    {
        "id": "LEA001",
        "employee_id": "EMP001",
        "leave_type": LeaveType.ANNUAL,
        "start_date": date(2023, 7, 15),
        "end_date": date(2023, 7, 16),
        "status": LeaveStatus.APPROVED,
        "reason": "Family vacation",
        "created_at": datetime(2023, 7, 10)
    },
    {
        "id": "LEA002",
        "employee_id": "EMP002",
        "leave_type": LeaveType.SICK,
        "start_date": date(2023, 8, 3),
        "end_date": date(2023, 8, 3),
        "status": LeaveStatus.APPROVED,
        "reason": "Doctor appointment",
        "created_at": datetime(2023, 8, 1)
    }
]

# Attendance records by employee and month
attendance_records = {
    "1": {  # Tháng 1
        "working_days": 22,
        "present_days": 21,
        "leave_days": 1,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-01-01", "check_in": "08:15", "check_out": "17:30", "status": "present"},
            {"date": "2023-01-02", "check_in": "08:30", "check_out": "17:45", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "2": {  # Tháng 2
        "working_days": 20,
        "present_days": 19,
        "leave_days": 1,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-02-01", "check_in": "08:20", "check_out": "17:40", "status": "present"},
            {"date": "2023-02-02", "check_in": "08:15", "check_out": "17:30", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "3": {  # Tháng 3
        "working_days": 23,
        "present_days": 22,
        "leave_days": 0,
        "absent_days": 1,
        "daily_records": [
            {"date": "2023-03-01", "check_in": "08:10", "check_out": "17:35", "status": "present"},
            {"date": "2023-03-02", "check_in": "08:25", "check_out": "17:40", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "4": {  # Tháng 4
        "working_days": 20,
        "present_days": 20,
        "leave_days": 0,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-04-03", "check_in": "08:05", "check_out": "17:30", "status": "present"},
            {"date": "2023-04-04", "check_in": "08:15", "check_out": "17:45", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "5": {  # Tháng 5
        "working_days": 21,
        "present_days": 19,
        "leave_days": 2,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-05-02", "check_in": "08:10", "check_out": "17:30", "status": "present"},
            {"date": "2023-05-03", "check_in": "08:20", "check_out": "17:40", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "6": {  # Tháng 6
        "working_days": 22,
        "present_days": 21,
        "leave_days": 1,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-06-01", "check_in": "08:15", "check_out": "17:35", "status": "present"},
            {"date": "2023-06-02", "check_in": "08:25", "check_out": "17:45", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "7": {  # Tháng 7
        "working_days": 21,
        "present_days": 20,
        "leave_days": 1,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-07-03", "check_in": "08:10", "check_out": "17:35", "status": "present"},
            {"date": "2023-07-04", "check_in": "08:20", "check_out": "17:40", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "8": {  # Tháng 8
        "working_days": 23,
        "present_days": 22,
        "leave_days": 0,
        "absent_days": 1,
        "daily_records": [
            {"date": "2023-08-01", "check_in": "08:15", "check_out": "17:30", "status": "present"},
            {"date": "2023-08-02", "check_in": "08:25", "check_out": "17:45", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "9": {  # Tháng 9
        "working_days": 21,
        "present_days": 21,
        "leave_days": 0,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-09-01", "check_in": "08:05", "check_out": "17:30", "status": "present"},
            {"date": "2023-09-04", "check_in": "08:15", "check_out": "17:35", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "10": {  # Tháng 10
        "working_days": 22,
        "present_days": 20,
        "leave_days": 2,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-10-02", "check_in": "08:10", "check_out": "17:30", "status": "present"},
            {"date": "2023-10-03", "check_in": "08:20", "check_out": "17:40", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "11": {  # Tháng 11
        "working_days": 22,
        "present_days": 21,
        "leave_days": 1,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-11-01", "check_in": "08:15", "check_out": "17:35", "status": "present"},
            {"date": "2023-11-02", "check_in": "08:25", "check_out": "17:45", "status": "present"},
            # More days would be here in a real system
        ]
    },
    "12": {  # Tháng 12
        "working_days": 21,
        "present_days": 19,
        "leave_days": 2,
        "absent_days": 0,
        "daily_records": [
            {"date": "2023-12-01", "check_in": "08:10", "check_out": "17:30", "status": "present"},
            {"date": "2023-12-04", "check_in": "08:20", "check_out": "17:40", "status": "present"},
            # More days would be here in a real system
        ]
    }
}

# --- Route Handlers ---
@router.post("/leave-request")
async def create_leave_request(employee_id: str, leave_type: LeaveType, start_date: str, end_date: str, reason: str):
    """
    Request leave/time off
    Example: "Tôi muốn xin nghỉ phép 2 ngày bắt đầu từ thứ 6 tuần này"
    """
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Validate dates
    if datetime.strptime(end_date, "%d/%m/%Y") < datetime.strptime(start_date, "%d/%m/%Y"):
        raise HTTPException(status_code=400, detail="End date cannot be before start date")
    
    # Check leave balance
    employee_balance = leave_balance.get(employee_id, {})
    leave_days = (datetime.strptime(end_date, "%d/%m/%Y") - datetime.strptime(start_date, "%d/%m/%Y")).days + 1
    
    leave_type_balance = employee_balance.get(leave_type, 0)
    if leave_type != LeaveType.UNPAID and leave_days > leave_type_balance:
        raise HTTPException(status_code=400, detail=f"Insufficient leave balance. You have {leave_type_balance} days remaining.")
    
    # Create new request
    new_request = {
        "id": f"LEA{len(leave_requests) + 1:03d}",
        "employee_id": employee_id,
        "leave_type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": LeaveStatus.PENDING,
        "reason": reason,
        "created_at": datetime.now()
    }
    
    leave_requests.append(new_request)
    
    return new_request

@router.get("/attendance-record")
async def get_attendance_record(month: int = Query(None, description="Month to query (1-12)")):
    """
    Query attendance records
    Example: "Tháng 6 tôi có bao nhiêu ngày công chuẩn?"
    """
    employee_records = attendance_records.get(str(month), {})
    if not employee_records:
        raise HTTPException(status_code=404, detail="No attendance records for this month")
    return employee_records