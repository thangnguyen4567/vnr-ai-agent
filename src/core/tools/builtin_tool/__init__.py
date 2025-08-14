from src.core.tools.builtin_tool.lms import lms_tools
from src.core.tools.builtin_tool.hrm import hrm_tools

built_in_tools = lms_tools + hrm_tools


built_in_tools_name = {
    tool.name: tool
    for tool in hrm_tools + lms_tools
}