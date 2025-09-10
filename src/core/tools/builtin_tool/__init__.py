from src.core.tools.builtin_tool.lms import lms_tools
from src.core.tools.builtin_tool.hrm import hrm_tools
from src.core.tools.builtin_tool.ui_action import ui_action_tools

built_in_tools = lms_tools + hrm_tools + ui_action_tools

built_in_tools_name = {
    tool.name: tool
    for tool in hrm_tools + lms_tools
}