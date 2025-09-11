from langchain_core.tools import tool
from typing import Literal

@tool("ui_action",return_direct=False)
async def ui_action(
        action: Literal['navigate', 'fill_form', 'click_button', 'search:toolbar'], 
        value_search: str = '',
        key_button: str = '',
        pageId: str = '',
        form_values: dict = {},
        form_key: str = ''

    ) -> str:
    """
    Chỉ thực hiện khi đã có danh sách các screen được tìm kiếm từ tool search_screen_schema
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
            return 'Chuyển màn hình thành công'
        else:
            return 'Không tìm thấy màn hình'
    elif action == 'fill_form':
        if form_values and form_key:
            return 'Điền thông tin vào form thành công'
        else:
            return 'Không tìm thấy form'
    elif action == 'click_button':
        if key_button:
            return 'Click button thành công'
        else:
            return 'Không tìm thấy button'
    elif action == 'search:toolbar':
        if value_search:
            return 'Tìm kiếm thành công'
        else:
            return 'Không tìm thấy giá trị tìm kiếm'