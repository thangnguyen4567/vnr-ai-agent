from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from enum import Enum

router = APIRouter(prefix="/recruitment", tags=["recruitment"])

# --- Mock Data ---

# Recruitment stages
class RecruitmentStage(str, Enum):
    APPLICATION = "application_received"
    RESUME_SCREENING = "resume_screening"
    PHONE_INTERVIEW = "phone_interview"
    TECHNICAL_ASSESSMENT = "technical_assessment"
    ONSITE_INTERVIEW = "onsite_interview"
    REFERENCE_CHECK = "reference_check"
    OFFER = "offer"
    ONBOARDING = "onboarding"
    REJECTED = "rejected"

# Candidates data
candidates = {
    "CAN001": {
        "id": "CAN001",
        "full_name": "Nguyễn Văn A",
        "email": "nguyenvana@email.com",
        "phone": "0901234567",
        "position_applied": "Software Engineer",
        "department": "Technical",
        "application_date": date(2023, 7, 10),
        "current_stage": RecruitmentStage.TECHNICAL_ASSESSMENT,
        "progress": [
            {
                "stage": RecruitmentStage.APPLICATION,
                "date": date(2023, 7, 10),
                "notes": "Application received via company website"
            },
            {
                "stage": RecruitmentStage.RESUME_SCREENING,
                "date": date(2023, 7, 12),
                "notes": "Resume looks good, strong technical background"
            },
            {
                "stage": RecruitmentStage.PHONE_INTERVIEW,
                "date": date(2023, 7, 15),
                "notes": "Good communication skills, aligned with company culture"
            },
            {
                "stage": RecruitmentStage.TECHNICAL_ASSESSMENT,
                "date": date(2023, 7, 20),
                "notes": "Technical test sent, waiting for submission"
            }
        ]
    },
    "CAN002": {
        "id": "CAN002",
        "full_name": "Trần Thị B",
        "email": "tranthib@email.com",
        "phone": "0912345678",
        "position_applied": "HR Specialist",
        "department": "Human Resources",
        "application_date": date(2023, 6, 25),
        "current_stage": RecruitmentStage.ONSITE_INTERVIEW,
        "progress": [
            {
                "stage": RecruitmentStage.APPLICATION,
                "date": date(2023, 6, 25),
                "notes": "Application received via LinkedIn"
            },
            {
                "stage": RecruitmentStage.RESUME_SCREENING,
                "date": date(2023, 6, 28),
                "notes": "Good experience in HR field"
            },
            {
                "stage": RecruitmentStage.PHONE_INTERVIEW,
                "date": date(2023, 7, 5),
                "notes": "Professional attitude, good communication skills"
            },
            {
                "stage": RecruitmentStage.ONSITE_INTERVIEW,
                "date": date(2023, 7, 15),
                "notes": "Scheduled for onsite interview"
            }
        ]
    },
    "CAN003": {
        "id": "CAN003",
        "full_name": "Lê Văn C",
        "email": "levanc@email.com",
        "phone": "0923456789",
        "position_applied": "Sales Manager",
        "department": "Sales",
        "application_date": date(2023, 7, 5),
        "current_stage": RecruitmentStage.OFFER,
        "progress": [
            {
                "stage": RecruitmentStage.APPLICATION,
                "date": date(2023, 7, 5),
                "notes": "Application received via referral"
            },
            {
                "stage": RecruitmentStage.RESUME_SCREENING,
                "date": date(2023, 7, 7),
                "notes": "Excellent sales background and experience"
            },
            {
                "stage": RecruitmentStage.PHONE_INTERVIEW,
                "date": date(2023, 7, 12),
                "notes": "Strong communication and leadership skills"
            },
            {
                "stage": RecruitmentStage.TECHNICAL_ASSESSMENT,
                "date": date(2023, 7, 18),
                "notes": "Case study completed with excellent results"
            },
            {
                "stage": RecruitmentStage.ONSITE_INTERVIEW,
                "date": date(2023, 7, 25),
                "notes": "Great performance in interview, team recommends offer"
            },
            {
                "stage": RecruitmentStage.OFFER,
                "date": date(2023, 8, 1),
                "notes": "Offer prepared and waiting for approval"
            }
        ]
    }
}

# Interview schedule
interview_schedule = [
    {
        "id": "INT001",
        "candidate_id": "CAN001",
        "candidate_name": "Nguyễn Văn A",
        "position": "Software Engineer",
        "interview_type": "Technical Interview",
        "date": date.today() + timedelta(days=1),
        "time": "10:00",
        "duration": 60,  # minutes
        "location": "Meeting Room A",
        "interviewer": "Trần Văn D (Technical Lead)",
        "notes": "Focus on backend development skills and system design"
    },
    {
        "id": "INT002",
        "candidate_id": "CAN002",
        "candidate_name": "Trần Thị B",
        "position": "HR Specialist",
        "interview_type": "Final Interview",
        "date": date.today() + timedelta(days=3),
        "time": "14:00",
        "duration": 90,  # minutes
        "location": "Meeting Room C",
        "interviewer": "Nguyễn Thị E (HR Director)",
        "notes": "Discuss previous experience and situational scenarios"
    },
    {
        "id": "INT003",
        "candidate_id": "CAN003",
        "candidate_name": "Lê Văn C",
        "position": "Sales Manager",
        "interview_type": "Offer Discussion",
        "date": date.today() + timedelta(days=2),
        "time": "15:30",
        "duration": 45,  # minutes
        "location": "Director's Office",
        "interviewer": "Phạm Văn F (Sales Director)",
        "notes": "Discuss offer details and start date"
    }
]

# --- Model Definitions ---

class CandidateProgress(BaseModel):
    stage: RecruitmentStage
    date: date
    notes: Optional[str] = None

class CandidateStatus(BaseModel):
    id: str
    full_name: str
    position_applied: str
    department: str
    application_date: date
    current_stage: RecruitmentStage
    progress: List[CandidateProgress]

# --- Route Handlers ---

@router.get("/candidate-status", response_model=CandidateStatus)
async def get_candidate_status(candidate_name: str = Query(..., description="Full name of the candidate")):
    """
    Tra cứu trạng thái ứng viên
    Example: "Ứng viên Nguyễn Văn A đang ở bước nào?"
    """
    # Search for candidate by name (case-insensitive)
    candidate_name_lower = candidate_name.lower()
    found_candidate = None
    
    for candidate in candidates.values():
        if candidate_name_lower in candidate["full_name"].lower():
            found_candidate = candidate
            break
    
    if not found_candidate:
        raise HTTPException(status_code=404, detail=f"No candidate found with name: {candidate_name}")
    
    return found_candidate

@router.get("/interview-reminders")
async def get_interview_reminders(days_ahead: int = Query(1, description="Number of days ahead to check for interviews")):
    """
    Nhắc lịch phỏng vấn
    Example: "Bạn có lịch phỏng vấn ứng viên Nguyễn lúc 10h sáng mai"
    """
    today = date.today()
    target_date = today + timedelta(days=days_ahead)
    
    # Find interviews scheduled for the target date
    upcoming_interviews = [
        interview for interview in interview_schedule 
        if interview["date"] == target_date
    ]
    
    if not upcoming_interviews:
        if days_ahead == 1:
            return "No interviews scheduled for tomorrow."
        else:
            return f"No interviews scheduled for the next {days_ahead} days."
    
    return upcoming_interviews
