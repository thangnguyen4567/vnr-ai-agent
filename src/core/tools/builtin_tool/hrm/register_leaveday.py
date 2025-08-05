from langchain_core.tools import tool
import json
from src.core.tools.builtin_tool.http_request_runner import do_authenticated_http_request
from src.config import settings
from datetime import datetime

@tool("register_leaveday",return_direct=False)
async def register_leaveday(start_date: str, end_date: str, reason: str) -> str:
    """Đăng ký nghỉ phép của nhân viên"""
    start = datetime.strptime(start_date, "%Y/%m/%d")
    end = datetime.strptime(end_date, "%Y/%m/%d")
    data = {
        "ProfileIDs": "54c12a16-a53e-4246-8c7b-7b409c8b2c35",
        "UserSubmit": "1bd02879-f5d7-4860-8021-41e5f5081114",
        "UserApproveID": "ed0049e3-74d8-48d4-a466-8e43808a0c28",
        "UserApproveID4": "08c2cf82-c4bb-4084-903a-589da93510be",
        "ListLeaveDayItem": [
            {
                "ID": "3ff1d163-9638-4059-8b26-e0e14fc22357",
                "ListProfileID": [
                    "54c12a16-a53e-4246-8c7b-7b409c8b2c35"
                ],
                "DateStart": start.strftime("%Y/%m/%d"),
                "DateEnd": end.strftime("%Y/%m/%d"),
                "LeaveDayTypeID": "6a1c865a-5b1f-42bb-96a4-4b3a1645bfb5",
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
        result = await do_authenticated_http_request(
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