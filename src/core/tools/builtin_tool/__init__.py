from src.core.tools.builtin_tool.get_goal import get_goal
from src.core.tools.builtin_tool.empty_tool import empty_tool
from src.core.tools.builtin_tool.lms import lms_tools

built_in_tools = [get_goal, empty_tool] + lms_tools