from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from enum import Enum

router = APIRouter(prefix="/training", tags=["training"])

# --- Mock Data ---

# Course types
class CourseType(str, Enum):
    SOFT_SKILLS = "soft_skills"
    TECHNICAL = "technical"
    MANAGEMENT = "management"
    COMPLIANCE = "compliance"
    LANGUAGE = "language"
    LEADERSHIP = "leadership"

# Course status
class CourseStatus(str, Enum):
    UPCOMING = "upcoming"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Courses data
courses = [
    {
        "id": "TRN001",
        "name": "Kỹ năng giao tiếp hiệu quả trong công việc",
        "type": CourseType.SOFT_SKILLS,
        "start_date": date.today() + timedelta(days=14),
        "end_date": date.today() + timedelta(days=15),
        "duration_hours": 16,
        "location": "Phòng đào tạo A",
        "max_participants": 20,
        "registered_participants": 12,
        "instructor": "Nguyễn Thị Hương",
        "description": "Học cách giao tiếp hiệu quả trong môi trường chuyên nghiệp, cải thiện kỹ năng thuyết trình và làm chủ nghệ thuật đưa và nhận phản hồi.",
        "target_audience": "Tất cả nhân viên",
        "status": CourseStatus.UPCOMING
    },
    {
        "id": "TRN002",
        "name": "Xây dựng đội nhóm và hợp tác",
        "type": CourseType.SOFT_SKILLS,
        "start_date": date.today() + timedelta(days=21),
        "end_date": date.today() + timedelta(days=21),
        "duration_hours": 8,
        "location": "Hội trường",
        "max_participants": 30,
        "registered_participants": 15,
        "instructor": "Trần Văn Minh",
        "description": "Phát triển kỹ năng làm việc hiệu quả trong nhóm, giải quyết xung đột và tạo môi trường hợp tác.",
        "target_audience": "Trưởng nhóm và thành viên",
        "status": CourseStatus.UPCOMING
    },
    {
        "id": "TRN003",
        "name": "Phát triển JavaScript nâng cao",
        "type": CourseType.TECHNICAL,
        "start_date": date.today() + timedelta(days=7),
        "end_date": date.today() + timedelta(days=9),
        "duration_hours": 24,
        "location": "Phòng thực hành 2",
        "max_participants": 15,
        "registered_participants": 15,
        "instructor": "Lê Thanh Tùng",
        "description": "Đi sâu vào các khái niệm JavaScript nâng cao bao gồm promises, async/await, closures và các framework hiện đại.",
        "target_audience": "Lập trình viên Frontend và Full-stack",
        "status": CourseStatus.UPCOMING
    },
    {
        "id": "TRN004",
        "name": "Kỹ năng lãnh đạo và quản lý cơ bản",
        "type": CourseType.LEADERSHIP,
        "start_date": date.today() + timedelta(days=30),
        "end_date": date.today() + timedelta(days=32),
        "duration_hours": 24,
        "location": "Trung tâm đào tạo quản lý",
        "max_participants": 12,
        "registered_participants": 8,
        "instructor": "Phạm Quang Hùng",
        "description": "Học các kỹ năng lãnh đạo thiết yếu, kỹ thuật quản lý và chiến lược phát triển đội nhóm.",
        "target_audience": "Quản lý và trưởng nhóm",
        "status": CourseStatus.UPCOMING
    },
]

# --- Model Definitions ---

class Course(BaseModel):
    id: str
    name: str
    type: CourseType
    start_date: date
    end_date: date
    duration_hours: int
    location: str
    max_participants: int
    registered_participants: int
    instructor: str
    description: str
    target_audience: str
    status: CourseStatus

# --- Route Handlers ---

@router.get("/courses", response_model=List[Course])
async def search_courses():
    """
    Tra cứu khóa học hiện có
    Example: "Công ty có khoá đào tạo kỹ năng mềm nào sắp tới?"
    """
    
    return courses
