from typing import Optional, Dict, Any
from src.core.tools.builtin_tool.base_response import APIResponse
import httpx

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
            request_kwargs["data"] = body
        else:
            request_kwargs["json"] = body

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