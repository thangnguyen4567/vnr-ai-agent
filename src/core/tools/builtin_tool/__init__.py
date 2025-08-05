from src.core.tools.builtin_tool.empty_tool import empty_tool
from src.core.tools.builtin_tool.lms import lms_tools
from src.core.tools.builtin_tool.hrm import hrm_tools

built_in_tools = [empty_tool] + lms_tools + hrm_tools


built_in_tools_name = {
    tool.name: tool
    for tool in [empty_tool] + hrm_tools
}