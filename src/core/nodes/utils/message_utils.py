from typing import List
from langchain_core.messages import (
    AIMessage,
    ToolMessage,
    BaseMessage,
    trim_messages,
)

def organize_messages(
    messages: List[BaseMessage], 
    max_token: int = 15 
) -> List[BaseMessage]:
    """
    Sắp xếp các tin nhắn thành một danh sách, tối ưu hóa cho việc sử dụng token

    Args:
        messages: Danh sách các tin nhắn cần sắp xếp
        max_token: Số lượng token tối đa được sử dụng

    Returns:
        Danh sách các tin nhắn đã được sắp xếp để tối ưu việc sử dụng token
    """
    trimmed_messages = trim_messages(
        messages, 
        max_tokens=max_token,
        strategy="last",
        token_counter=len,
        include_system=False,
        allow_partial=True,
        start_on="human"
    )

    return repair_messages(trimmed_messages)

def repair_messages(messages: List[BaseMessage]) -> List[BaseMessage]:
    """
    Sửa lỗi trong danh sách tin nhắn khi có AIMessage với tool_calls nhưng không có ToolMessage tương ứng

    Args:
        messages: Danh sách tin nhắn cần sửa chữa

    Returns:
        Danh sách tin nhắn đã được sửa chữa
    """

    repaired_messages = []

    # Lưu trữ các tool_call_id và tool_message_id
    tool_call_ids = set()
    tool_message_ids = set()

    # Tìm tất cả các tool_call_id và tool_message_id
    for message in messages:
        if isinstance(message, AIMessage) and hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                if 'id' in tool_call:
                    tool_call_ids.add(tool_call['id'])
                    
        elif isinstance(message, ToolMessage) and hasattr(message, "tool_call_id"):
            tool_message_ids.add(message.tool_call_id)

    # Tìm các tool_call_id bị thiếu
    missing_tool_call_ids = tool_call_ids - tool_message_ids

    # Duyệt qua từng tin nhắn
    i = 0

    while i < len(messages):
        message = messages[i]
        # Kiểm tra xem tin nhắn có phải là AIMessage và có tool_calls không
        if isinstance(message, AIMessage) and hasattr(message, "tool_calls") and message.tool_calls:
            # Kiểm tra xem có tool_call_id nào bị thiếu không
            has_missing_tool_call = any(
                tool_call.get("id") in missing_tool_call_ids
                for tool_call in message.tool_calls
            )
            # Nếu có tool_call_id bị thiếu
            if has_missing_tool_call:
                # Kiểm tra xem tin nhắn tiếp theo có phải là ToolMessage không
                if i == len(messages) - 1 or not isinstance(messages[i + 1], ToolMessage):
                    # Bỏ qua tin nhắn này 
                    i += 1
                    continue

        # Thêm tin nhắn đã sửa vào danh sách tin nhắn đã sửa
        repaired_messages.append(message)
        i += 1

    return repaired_messages
 
def extract_text_content(content: any) -> str:
    """
    Trích xuất nội dung văn bản từ content của tin nhắn

    Args:
        content: Nội dung của tin nhắn ( có thể là str hoặc dict)

    Returns:
        Chuối nội dung văn bản
    """
    if isinstance(content, str):
        return content
    
    if isinstance(content, dict):
        content = [content]

    if not isinstance(content, list):
        return str(content)
    
    texts = []
    for item in content:
        if (
            isinstance(item, dict) and
            item.get("type") == "text" and
            item.get("text")
        ):
            texts.append(item.get("text"))
        elif isinstance(item, str):
            texts.append(item)

    return "\n".join(texts).strip()