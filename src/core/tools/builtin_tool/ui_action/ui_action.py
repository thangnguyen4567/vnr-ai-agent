from langchain_core.tools import tool
from typing import Literal

@tool("ui_action",return_direct=False)
async def ui_action(
        action: Literal['navigate', 'fill_form', 'click_button', 'search'], 
        value_search: str = '',
        key_button: str = '',
        pageId: str = '',
        form_values: dict = {},
        form_key: str = ''

    ) -> str:
    """
    Chỉ thực hiện khi đã có danh sách screen_schema
    Thực hiện các hành động trên màn hình dựa vào schema màn hình ( Mở màn hình, điền thông tin vào form, click button, tìm kiếm )
    Args:
        action: Hành động trên màn hình
        key_button: Key của button để click
        pageId: Key của màn hình để chuyển đến
        form_values: Giá trị điền vào các field trong form
        value_search: Giá trị tìm kiếm trên lưới
        form_key: Key của form để điền
    Returns:
        Kết quả thực hiện hành động
    """

    if action == 'navigate':
        if pageId:
            return f"""
                {
                    "type": "navigate", 
                    "pageId": "{pageId}" 
                }
            """
        else:
            return 'Không tìm thấy màn hình'
    elif action == 'fill_form':
        if form_values:
            return f"""
                {
                    "type": "fill_form",
                    "formKey": "{form_key}", 
                    "values": {
                        {form_values}
                    }
                }
            """
        else:
            return 'Không tìm thấy form'
    elif action == 'click_button':
        if key_button:
            return f"""
                {
                    "type": "click_button",
                    "key": "{key_button}"
                }
            """
        else:
            return 'Không tìm thấy button'
    elif action == 'search':
        if value_search:
            return f"""
                {
                    "type": "search",
                    "key": "toolbar:search",
                    "value": "{value_search}"
                }
            """
        else:
            return 'Không tìm thấy giá trị tìm kiếm'        