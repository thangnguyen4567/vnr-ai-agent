import json
from typing import Optional, Dict, Any
from src.core.tools.builtin_tool.base_response import APIResponse
import httpx
import base64
import time
import jwt
import requests
import logging
from src.config import settings

# Cấu hình logger
logger = logging.getLogger(__name__)

async def do_async_http_request(
    url: str,
    method: str = 'GET',
    auth_method: Optional[str] = 'bearer',
    auth_params: Optional[Dict[str, Any]] = {},
    headers: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None,
) -> APIResponse:
    """
    Thực hiện HTTP request
    """
    headers = headers or {}

    if auth_method:
        headers = await apply_authentication(headers, auth_method, auth_params)

    method = method.upper()
    headers['Content-Type'] = 'application/json'

    request_kwargs = {
        "url": url,
        "method": method,
        "headers": headers,
        "params": query_params,
        "timeout": timeout,
    }
    
    content_type = headers.get("Content-Type", "").lower()
    if 'application/x-www-form-urlencoded' in content_type:
        request_kwargs["data"] = query_params
        logger.info(f"Request data: {json.dumps(query_params)}")
    else:
        request_kwargs["json"] = query_params
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
            except ValueError:
                response_data = None
                logger.info(f"Response không phải JSON format - Content: {response.content[:1000]}")

            return APIResponse(
                success=True,
                message="Request successful",
                data=response_data,
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

async def do_async_http_request_basic(
    url: str,
    method: str = 'GET',
    auth_method: Optional[str] = 'bearer',
    auth_params: Optional[Dict[str, Any]] = {},
    headers: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None,
) -> APIResponse:
    """
    Thực hiện HTTP request
    """

    method = method.upper()
    headers = headers or {}

    if auth_method:
        headers = await apply_authentication(headers, auth_method, auth_params)

    headers['Content-Type'] = 'application/json'

    request_kwargs = {
        "url": url,
        "method": method,
        "headers": headers,
        "params": query_params,
        "timeout": timeout,
    }
    
    content_type = headers.get("Content-Type", "").lower()
    if 'application/x-www-form-urlencoded' in content_type:
        request_kwargs["data"] = query_params
        logger.info(f"Request data: {json.dumps(query_params)}")
    else:
        request_kwargs["json"] = query_params
        logger.info(f"Request body: {json.dumps(query_params)}")

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
        except ValueError:
            response_data = None
            logger.info(f"Response không phải JSON format - Content: {response.content[:1000]}")

        return response_data


async def apply_authentication(
    headers: Dict[str, Any],
    auth_method: str = 'bearer',
    auth_params: Dict[str, Any] = {}
) -> Dict[str, Any]:
    """
    Áp dụng phương thức xác thực cho HTTP request.
    
    Các phương thức xác thực hỗ trợ:
    - basic: Xác thực Basic (username/password)
    - bearer: Xác thực Bearer token
    - api_key: Xác thực bằng API key
    - oauth2: Xác thực OAuth 2.0
    - custom: Xác thực tùy chỉnh theo header
    
    Args:
        headers: Headers hiện tại của request
        auth_method: Phương thức xác thực (basic, bearer, api_key, oauth2, digest, custom)
        auth_params: Thông số xác thực tương ứng với từng phương thức
        
    Returns:
        Dict[str, Any]: Headers đã được cập nhật với thông tin xác thực
    """
    auth_method = settings.MULTI_AGENT_CONFIG['auth']['method']
    auth_params = {
        "token": settings.MULTI_AGENT_CONFIG['auth']['token'] if auth_method == "bearer" else settings.API_TOKEN
    }   

    headers = headers or {}
    
    if auth_method == "basic":
        if "username" in auth_params and "password" in auth_params:
            auth_str = f"{auth_params['username']}:{auth_params['password']}"
            encoded = base64.b64encode(auth_str.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
    
    elif auth_method == "bearer":
        if "token" in auth_params:
            headers["Authorization"] = f"Bearer {auth_params['token']}"
    
    elif auth_method == "api_key":
        if "key" in auth_params and "name" in auth_params:
            # API key có thể được đặt trong header hoặc query params
            placement = auth_params.get("placement", "header")
            if placement == "header":
                headers[auth_params["name"]] = auth_params["key"]
                
    elif auth_method == "oauth2":
        if is_token_valid(auth_params['token']):
            headers["Authorization"] = f"Bearer {auth_params['token']}"
        else:
            auth_params['token'] = await get_new_token()
            settings.update_api_token(auth_params['token'])
            headers["Authorization"] = f"Bearer {auth_params['token']}"
   
            
    elif auth_method == "custom":
        # Cho phép thêm header tùy chỉnh
        if "headers" in auth_params and isinstance(auth_params["headers"], dict):
            headers.update(auth_params["headers"])
    
    return headers


def is_token_valid(token: str) -> bool:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp_timestamp = payload.get("exp")
        if not exp_timestamp:
            return False
        return time.time() < exp_timestamp
    except Exception as e:
        print(e)
        return False

async def get_new_token() -> str:
    auth_header = requests.auth._basic_auth_str(settings.AUTH_CONFIG['client_id'], settings.AUTH_CONFIG['client_secret'])
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": auth_header
    }
    data = {
        "grant_type": "password",
        "username": settings.AUTH_CONFIG['username'],
        "password": settings.AUTH_CONFIG['password']
    }
    try:
        response = requests.post(settings.AUTH_CONFIG['token_url'], headers=headers, data=data, verify=False)
        response.raise_for_status()
        logger.info(f"Lấy token mới thành công")
        return response.json()['access_token']
    except Exception as e: 
        logger.error(f"Lỗi khi lấy token mới: {e}")
        return None