from typing import Optional, Dict, Any
from src.core.tools.builtin_tool.base_response import APIResponse
import httpx
import base64

async def do_async_http_request(
    url: str,
    method: str,
    path_params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
    query_params: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None,
) -> APIResponse:
    """
    Thực hiện HTTP request
    """

    method = method.upper()
    headers = headers or {}
    headers['Content-Type'] = 'application/json'

    request_kwargs = {
        "url": url,
        "method": method,
        "headers": headers,
        "params": query_params,
        "timeout": timeout,
    }
    if body is not None:
        content_type = headers.get("Content-Type", "").lower()
        if 'application/x-www-form-urlencoded' in content_type:
            request_kwargs["data"] = query_params
        else:
            request_kwargs["json"] = query_params

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(**request_kwargs)
            try:
                response_data = response.json() if response.content and response.headers.get("Content-Type", "").startswith("application/json") else None
            except ValueError:
                response_data = None

            return APIResponse(
                success=True,
                message="Request successful",
                data=response_data,
            )

    except httpx.TimeoutException as e:
        return APIResponse(
            success=False,
            message=f"Request timed out after {timeout} seconds",
        )

    except httpx.ConnectError as e:
        return APIResponse(
            success=False,
            message=f"Connection error: {str(e)}",
        )
    
    except httpx.RequestError as e:
        return APIResponse(
            success=False,
            message=f"Request error: {str(e)}",
        )


def apply_authentication(
    headers: Dict[str, Any],
    auth_method: str,
    auth_params: Dict[str, Any]
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
        if "access_token" in auth_params:
            headers["Authorization"] = f"Bearer {auth_params['access_token']}"
            
    elif auth_method == "custom":
        # Cho phép thêm header tùy chỉnh
        if "headers" in auth_params and isinstance(auth_params["headers"], dict):
            headers.update(auth_params["headers"])
    
    return headers


async def do_authenticated_http_request(
    url: str,
    method: str,
    path_params: Optional[Dict[str, Any]] = None,
    auth_method: Optional[str] = 'bearer',
    auth_params: Optional[Dict[str, Any]] = {},
    headers: Optional[Dict[str, Any]] = {},
    query_params: Optional[Dict[str, Any]] = None,
    body: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None,
) -> APIResponse:
    """
    Thực hiện HTTP request với xác thực
    """
    headers = headers or {}
    
    if auth_method:
        headers = apply_authentication(headers, auth_method, auth_params)
        
    return await do_async_http_request(
        url=url,
        method=method,
        path_params=path_params,
        headers=headers,
        query_params=query_params,
        body=body,
        timeout=timeout
    )