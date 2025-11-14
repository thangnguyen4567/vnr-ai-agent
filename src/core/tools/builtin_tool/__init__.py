from src.core.tools.builtin_tool.lms import lms_tools
from src.core.tools.builtin_tool.ui_action import ui_action_tools
from src.core.tools.builtin_tool.succession import succession_tools

built_in_tools = lms_tools + ui_action_tools + succession_tools

built_in_tools_name = {
    tool.name: tool
    for tool in lms_tools
    + succession_tools
}