from langchain_core.tools import tool
import json
from src.core.tools.builtin_tool.http_request_runner import do_async_http_request
from src.config import settings
from datetime import datetime

@tool("register_overtime",return_direct=False)
async def register_overtime(
    WorkDate: str,
    WorkDateTo: str,
    TimeFrom: str,
    TimeTo: str,
    reason: str,
    ProfileID: str = '54c12a16-a53e-4246-8c7b-7b409c8b2c35',
) -> str:
    """Đăng ký tăng ca của nhân viên"""
    work_date = datetime.strptime(WorkDate, "%Y/%m/%d").strftime("%Y/%m/%d")
    work_date_to = datetime.strptime(WorkDateTo, "%Y/%m/%d").strftime("%Y/%m/%d")
    time_from = datetime.strptime(TimeFrom, "%H:%M").strftime("%H:%M")
    time_to = datetime.strptime(TimeTo, "%H:%M").strftime("%H:%M")
    data = {
        "ObjectRegister": "E_Emp",
        "UserApproveID": "a20128a7-cd70-4fc3-9050-56d4befff410",
        "UserApproveID2": "a20128a7-cd70-4fc3-9050-56d4befff410",
        "UserApproveID4": "a20128a7-cd70-4fc3-9050-56d4befff410",
        "IsAddNewAndSendMail": True,
        "ProfileIds": ProfileID,
        "ListOvertimeItem": [
            {
                "MethodPayment": "E_CASHOUT",
                "WorkDate": work_date + " 00:00",
                "TimeFrom": work_date + " " + time_from,
                "ProfileIds": [
                    ProfileID
                ],
                "TimeTo": work_date + " " + time_to,
                "RegisterHours": 1,
                "OvertimeReasonID": "2da1de16-97c7-42af-9f92-e48193c59e30",
                "DurationType": "E_OT_LATE",
                "ReasonOT": reason,
                "WorkDateTo": work_date_to + " 00:00",
                "ShiftID": "ba3e1c66-8869-4ff7-9ba0-cce86328cbb1",
                "ListProfileID": [
                    ProfileID
                ],
                "ListWorkDateRepeat": [
                    work_date
                ],
                "LevelApproved": 2
            }
        ],
    }
    try:
        result = await do_async_http_request(
            url=settings.MULTI_AGENT_CONFIG['auth']['url_endpoint'] + "api/Att_OvertimePlan/CreateOrUpdateOvertimePlanNew",
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