from re import S
from langchain_core.tools import tool
import json
from src.core.tools.builtin_tool.http_request_runner import do_async_http_request, do_async_http_request_basic, is_token_valid, get_new_token
from src.config import settings
from datetime import datetime
from typing import Literal
import uuid
import logging
import requests

logger = logging.getLogger(__name__)
@tool("register_goal",return_direct=False)
async def register_goal(
    type: Literal['KPI', 'OKR', 'SMART'] = 'KPI',
    goal_name: str = None,
    target: int = None,
    weight: int = 100,
    start_date: str = None,
    end_date: str = None,
    department_name: str = None,
    employee_name: str = None,
    scope: Literal['Organization', 'Individual'] = 'Organization',
    measurement_unit: Literal['Ngày', 'Giờ', 'VNĐ', 'Phần trăm'] = 'VNĐ',
) -> str:
    """
        Đăng ký giao mục tiêu cho bộ phận loại mục tiêu mặc định là 'KPI', phạm vi mặc định là 'Organization', Thời gian mục tiêu theo quý hoặc năm
        Nếu phạm vi là 'Organization' thì cần truyền vào tên phòng ban
        Nếu phạm vi là 'Individual' thì cần truyền vào tên nhân viên
        Bạn cần xác nhận thông tin và các tham số truyền vào với người dùng trước khi thực hiện
    """
    url = settings.DIFY_WORKFLOW_CONFIG['url']

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + settings.DIFY_WORKFLOW_CONFIG['token']
    }
    # Kiểm tra token hợp lệ
    if not is_token_valid(settings.API_TOKEN):
        settings.API_TOKEN = await get_new_token()
        settings.update_api_token(settings.API_TOKEN)

    payload = {
        "inputs": {
            "scope": scope,
            "goal_name": goal_name,
            "start_date": start_date,
            "end_date": end_date,
            "weight": weight,
            "department_name": department_name,
            "employee_name": employee_name,
            "measurement_unit": measurement_unit,
            "target": target,
            "type": type,
            "token": settings.API_TOKEN
        },
        "query": "no query",
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "nouser",
        "files": []
    }
    try:
        response = requests.post(verify=False, url=url, headers=headers, json=payload)
        if response.status_code == 400:
            return 'Thực hiện giao mục tiêu thất bại: ' + response.json()['message']
    except Exception as e:
        return 'Thực hiện giao mục tiêu thất bại: ' + str(e)

    return response.json()['answer']

# @tool("register_goal",return_direct=False)
# async def register_goal(
#     type: Literal['KPI', 'OKR', 'SMART'] = 'KPI',
#     goal_name: str = None,
#     target: int = None,
#     weight: int = None,
#     start_date: str = None,
#     end_date: str = None,
#     department_name: str = None,
#     employee_name: str = None,
#     scope: Literal['Organization', 'Individual'] = 'Organization',
#     measurement_unit: Literal['Ngày', 'Giờ', 'VNĐ', 'Phần trăm'] = 'VNĐ',
# ) -> str:
    """
        Đăng ký giao mục tiêu cho bộ phận loại mục tiêu mặc định là 'KPI', phạm vi mặc định là 'Organization', Thời gian mục tiêu theo quý hoặc năm
        Nếu phạm vi là 'Organization' thì cần truyền vào tên phòng ban
        Nếu phạm vi là 'Individual' thì cần truyền vào tên nhân viên
        Bạn cần xác nhận thông tin và các tham số truyền vào với người dùng trước khi thực hiện
    """
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")
    org_structure_id = None
    employee_profile_id = None
    measurement_unit_id = None
    #Lấy ID đơn vị đo lường
    try:
        measurement_units = await do_async_http_request_basic(
            url=settings.MULTI_AGENT_CONFIG['auth']['url_endpoint'] + "proxy/shared/api/v1/Dynamic/GetDataSourceComboboxEntity",
            query_params={
                "EntityName": "Cat_MeasurementUnit",
                "TextField": "Name",
                "ValueField": "Id"
            }
        )
        measurement_unit_id = next((unit['Value'] for unit in measurement_units['Data'] if unit['Text'].lower() == measurement_unit.lower()), None)
    except Exception as e:
        return 'Không tìm thấy dữ liệu đơn vị đo lường trong hệ thống'

    # Nếu phạm vi là Organization thì lấy org_structure_id từ department_name
    if scope == 'Organization':
        org_structures = await do_async_http_request_basic(
            url=settings.MULTI_AGENT_CONFIG['auth']['url_endpoint'] + "proxy/eva/api/v1/Eva_Goal/GetOrgTreeView",
        )
        try:
            org_structure_id = next((org_structure['Id'] for org_structure in org_structures['Data'] if department_name.lower() in org_structure['Name'].lower()), None)
            if not org_structure_id:
                return 'Không tìm thấy phòng ban trong hệ thống'
            else:
                employee_profile = await do_async_http_request_basic(
                    url=settings.MULTI_AGENT_CONFIG['auth']['url_endpoint'] + "proxy/eva/api/v1/Eva_Goal/GetMangerOrgstructureById/" + org_structure_id
                )
                employee_profile_id = employee_profile['Data']['ManagerProfileId']
        except Exception as e:
            return 'Không tìm thấy dữ liệu phòng ban trong hệ thống'

    # Nếu phạm vi là Individual thì lấy employee_profile_id từ employee_name
    elif scope == 'Individual':
        try:
            employee_profiles = await do_async_http_request_basic(
                url=settings.MULTI_AGENT_CONFIG['auth']['url_endpoint'] + "proxy/eva/api/v1/Eva_Goal/GetListEmployee",
            )
            employee_profile_id = next((employee_profile['Id'] for employee_profile in employee_profiles['Data'] if employee_name.lower() in employee_profile['Name'].lower()), None)
        except Exception as e:
            return 'Không tìm thấy dữ liệu nhân viên trong hệ thống'
        
    data = {
        "Type": type,
        # "GoalTemplateId": "ae290f52-8e4b-498a-ab18-4a6ef59c25cc",
        "Code": str(uuid.uuid4()),
        "Name": goal_name,
        # "GroupId": "054e1cfc-9615-4d2c-9ad3-7ac48abfc28d",
        "MeasurementScaleId": "550e8400-e29b-41d4-a716-446655440002",
        "Target": target,
        "MeasurementUnitId": measurement_unit_id,
        "Weight": weight,
        "PeriodId": "10ccde32-a23f-4697-b627-77d5fef75d37",
        "PeriodTime": [
            start_date.strftime("%Y/%m/%d %H:%M:%S"),
            end_date.strftime("%Y/%m/%d %H:%M:%S")
        ],
        "AssignmentScope": scope,
        "AssignedToOrgStructureId": org_structure_id,
        "AssignedToProfileId": employee_profile_id,
        "StartDate": start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "EndDate": end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "Status": "E_WAITING_CONFIRM"
    }
    try:
        result = await do_async_http_request(
            url=settings.MULTI_AGENT_CONFIG['auth']['url_endpoint'] + "proxy/eva/api/v1/Eva_Goal",
            method="POST",
            query_params=data,
        )
    except Exception as e:
        logger.error(f"Thực hiện giao mục tiêu thất bại: {str(e)}")
        return 'Thực hiện giao mục tiêu thất bại'
    return json.dumps(result.data)