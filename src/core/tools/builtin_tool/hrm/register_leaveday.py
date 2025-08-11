from langchain_core.tools import tool
import json
from src.core.tools.builtin_tool.http_request_runner import do_async_http_request
from src.config import settings
from datetime import datetime

@tool("register_leaveday",return_direct=False)
async def register_leaveday(start_date: str, end_date: str, reason: str, ProfileID: str) -> str:
    """Đăng ký nghỉ phép của nhân viên"""
    start = datetime.strptime(start_date, "%Y/%m/%d")
    end = datetime.strptime(end_date, "%Y/%m/%d")
    data = {
        "ProfileIDs": ProfileID,
        "UserSubmit": ProfileID,
        "UserApproveID": "a20128a7-cd70-4fc3-9050-56d4befff410",
        "UserApproveID4": "a20128a7-cd70-4fc3-9050-56d4befff410",
        "IsAddNewAndSendMail": True,
        "ListLeaveDayItem": [
            {
                "ID": "3ff1d163-9638-4059-8b26-e0e14fc22357",
                "ListProfileID": [
                    ProfileID
                ],
                "DateStart": start.strftime("%Y/%m/%d"),
                "DateEnd": end.strftime("%Y/%m/%d"),
                "LeaveDayTypeID": "2823f21e-921d-4dd2-83eb-d5e6c04f9ba3",
                "DurationType": "E_FULLSHIFT",
                "ShiftID": "ba3e1c66-8869-4ff7-9ba0-cce86328cbb1",
                "Comment": reason,
                "LeaveDays": 1,
                "LeaveHours": 8,
                "LevelApproved": 2
            }
        ],
        "TotalLeaveDay": 1
    }
    try:
        result = await do_async_http_request(
            url=settings.MULTI_AGENT_CONFIG['auth']['url_endpoint'] + "api/Att_LeaveDay/CreateOrUpdateLeaveday",
            method="POST",
            query_params=data,
            auth_method=settings.MULTI_AGENT_CONFIG['auth']['method'],
            auth_params={
                "token": settings.MULTI_AGENT_CONFIG['auth']['token']
            }
        )
    except Exception as e:
        return 'Đăng ký nghỉ phép thất bại'
    return json.dumps(result.data)