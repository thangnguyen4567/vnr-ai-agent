import json
from typing import Optional, Dict, Any
from src.core.tools.builtin_tool.base_response import APIResponse
import httpx
import time
import logging
from src.config import settings
from src.core.tools.builtin_tool.http_request_runner import apply_authentication
import copy

# Cấu hình logger
logger = logging.getLogger(__name__)

async def do_async_http_workflow_request(
    url: str,
    query_params: Optional[Dict[str, Any]] = None,
    auth_method: Optional[str] = 'bearer',
    auth_params: Optional[Dict[str, Any]] = {},
    timeout: Optional[int] = None,
    headers: Optional[Dict[str, Any]] = None,
) -> APIResponse:
    """
    Thực hiện HTTP request
    """
    # Kiểm tra token hợp lệ
    safe_headers = copy.deepcopy(headers)
    if auth_method:
        await apply_authentication(safe_headers, auth_method, auth_params)

    query_params["inputs"]["token"] = settings.API_TOKEN

    request_kwargs = {
        "url": url,
        "method": "POST",
        "headers": headers,
        "json": query_params,
        "timeout": timeout,
    }
    
    logger.info(f"Request body: {json.dumps(query_params)}")
    try:
        async with httpx.AsyncClient(verify=False) as client:
            # Bắt đầu thời gian request
            start_time = time.time()
            
            response = await client.request(**request_kwargs)
            
            # Tính thời gian phản hồi
            response_time = time.time() - start_time
            
            # Ghi log response
            logger.info(f"Nhận response từ {url} - Status: {response.status_code} - Thời gian: {response_time:.2f}s")
            
            try:
                response_data = response.json() if response.content and response.headers.get("Content-Type", "").startswith("application/json") else None
                logger.info(f"Response data: {json.dumps(response_data)}")
                # Kiểm tra response status
                if response.status_code != 200:
                    return APIResponse(
                        success=False,
                        message="Failed",
                        data=response_data['message']
                    )
            except ValueError:
                response_data = None

            return APIResponse(
                success=True,
                message="Success",
                data=response_data['answer']
            )

    except httpx.TimeoutException as e:
        error_msg = f"Request timed out after {timeout} seconds"
        logger.error(f"Timeout error khi gọi {url}: {error_msg}")
        return APIResponse(
            success=False,
            message=error_msg,
        )

    except httpx.ConnectError as e:
        error_msg = f"Connection error: {str(e)}"
        logger.error(f"Lỗi kết nối khi gọi {url}: {error_msg}")
        return APIResponse(
            success=False,
            message=error_msg,
        )
    
    except httpx.RequestError as e:
        error_msg = f"Request error: {str(e)}"
        logger.error(f"Lỗi request khi gọi {url}: {error_msg}")
        return APIResponse(
            success=False,
            message=error_msg,
        )
