from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter(prefix="/salary", tags=["salary"])

salary_records = {
    "1": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 8,
            "rate": 150000,
            "amount": 1200000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 0
        },
        "working_days": {
            "standard": 22,
            "actual": 22
        },
        "net_salary": 16475000,
        "payment_status": "paid",
        "payment_date": "2023-02-10"
    },
    "2": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 10,
            "rate": 150000,
            "amount": 1500000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 0
        },
        "working_days": {
            "standard": 20,
            "actual": 20
        },
        "net_salary": 16775000,
        "payment_status": "paid",
        "payment_date": "2023-03-10"
    },
    "3": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 5,
            "rate": 150000,
            "amount": 750000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 500000
        },
        "working_days": {
            "standard": 23,
            "actual": 22
        },
        "net_salary": 15525000,
        "payment_status": "paid",
        "payment_date": "2023-04-10"
    },
    "4": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 7,
            "rate": 150000,
            "amount": 1050000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 0
        },
        "working_days": {
            "standard": 20,
            "actual": 20
        },
        "net_salary": 16325000,
        "payment_status": "paid",
        "payment_date": "2023-05-10"
    },
    "5": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 9,
            "rate": 150000,
            "amount": 1350000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 0
        },
        "working_days": {
            "standard": 21,
            "actual": 21
        },
        "net_salary": 16625000,
        "payment_status": "paid",
        "payment_date": "2023-06-10"
    },
    "6": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 12,
            "rate": 150000,
            "amount": 1800000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 500000
        },
        "working_days": {
            "standard": 22,
            "actual": 21
        },
        "net_salary": 16575000,
        "payment_status": "paid",
        "payment_date": "2023-07-10"
    },
    "7": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 6,
            "rate": 150000,
            "amount": 900000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 0
        },
        "working_days": {
            "standard": 21,
            "actual": 21
        },
        "net_salary": 16175000,
        "payment_status": "paid",
        "payment_date": "2023-08-10"
    },
    "8": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 8,
            "rate": 150000,
            "amount": 1200000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 250000
        },
        "working_days": {
            "standard": 23,
            "actual": 22.5
        },
        "net_salary": 16225000,
        "payment_status": "paid",
        "payment_date": "2023-09-10"
    },
    "9": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 10,
            "rate": 150000,
            "amount": 1500000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 0
        },
        "working_days": {
            "standard": 21,
            "actual": 21
        },
        "net_salary": 16775000,
        "payment_status": "paid",
        "payment_date": "2023-10-10"
    },
    "10": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 7,
            "rate": 150000,
            "amount": 1050000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 0
        },
        "working_days": {
            "standard": 22,
            "actual": 22
        },
        "net_salary": 16325000,
        "payment_status": "paid",
        "payment_date": "2023-11-10"
    },
    "11": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 9,
            "rate": 150000,
            "amount": 1350000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 250000
        },
        "working_days": {
            "standard": 22,
            "actual": 21.5
        },
        "net_salary": 16375000,
        "payment_status": "paid",
        "payment_date": "2023-12-10"
    },
    "12": {
        "base_salary": 15000000,
        "allowances": {
            "meal": 1000000,
            "transport": 500000,
            "position": 2000000
        },
        "overtime": {
            "hours": 15,
            "rate": 150000,
            "amount": 2250000
        },
        "deductions": {
            "tax": 1500000,
            "social_insurance": 1350000,
            "health_insurance": 225000,
            "unemployment_insurance": 150000,
            "absence": 0
        },
        "working_days": {
            "standard": 21,
            "actual": 21
        },
        "net_salary": 17525000,
        "payment_status": "paid",
        "payment_date": "2024-01-10"
    }
}

# --- Model Definition ---

class SalaryDetail(BaseModel):
    employee_id: str
    year_month: str
    base_salary: int
    allowances: Dict[str, int]
    overtime: Dict[str, Any]
    deductions: Dict[str, int]
    working_days: Dict[str, int]
    net_salary: int
    payment_status: str
    payment_date: Optional[str] = None

# --- Route Handler ---

@router.get("/salary-details")
async def get_salary_details(month: int = Query(None, description="Month to query (1-12)")):
    """
    View personal salary details
    Example: "Cho tôi xem chi tiết lương tháng 6"
    """
    
    employee_salaries = salary_records.get(str(month), {})
    
    return employee_salaries
