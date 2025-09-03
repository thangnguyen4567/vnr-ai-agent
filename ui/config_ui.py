import streamlit as st

from typing import Dict, Any

from src.core.tools.builtin_tool import built_in_tools_name
from src.utils.save_schema import save_schema

from ui.config_manager import ConfigManager


def _ensure_agent_structure(agent: Dict[str, Any]):
    """Đảm bảo agent có cấu trúc dữ liệu đúng"""
    if "nodes" not in agent:
        agent["nodes"] = {"llm": {"provider": "openai", "agent_prompt": ""}, "tools": []}
    elif "llm" not in agent["nodes"]:
        agent["nodes"]["llm"] = {"provider": "openai", "agent_prompt": ""}

    agent["nodes"]["llm"]["provider"] = 'openai'

    if "tools" not in agent["nodes"]:
        agent["nodes"]["tools"] = []


def _render_parameter(config_manager: ConfigManager, param: Dict[str, Any], agent_idx: int, tool_idx: int, param_idx: int):
    """Hiển thị một parameter cụ thể"""
    st.markdown(
        f"""
        <div class="param-item">
            <h6>Parameter #{param_idx + 1}</h6>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        param_cols = st.columns([2, 4, 2, 2, 1, 1])

        param["name"] = param_cols[0].text_input(
            "Tên tham số", value=param.get("name", ""), key=f"param_name_{agent_idx}_{tool_idx}_{param_idx}"
        )
        param["description"] = param_cols[1].text_input(
            "Mô tả", value=param.get("description", ""), key=f"param_desc_{agent_idx}_{tool_idx}_{param_idx}"
        )

        input_methods = ["query", "header", "path", "body"]
        method_index = input_methods.index(param.get("input_method", "query")) if param.get("input_method") in input_methods else 0
        param["input_method"] = param_cols[2].selectbox(
            "Phương thức", options=input_methods, index=method_index, key=f"param_method_{agent_idx}_{tool_idx}_{param_idx}"
        )

        param["default"] = param_cols[3].text_input(
            "Giá trị mặc định", value=param.get("default", ""), key=f"param_default_{agent_idx}_{tool_idx}_{param_idx}"
        )

        param_types = ["string", "number", "boolean", "array", "date"]
        type_index = param_types.index(param.get("type", "string")) if param.get("type") in param_types else 0
        param["type"] = param_cols[4].selectbox(
            "Kiểu", options=param_types, index=type_index, key=f"param_type_{agent_idx}_{tool_idx}_{param_idx}"
        )

        with param_cols[5]:
            st.markdown("<div style='margin-top: 25px'></div>", unsafe_allow_html=True)
            if st.button("❌ Xóa", key=f"del_param_{agent_idx}_{tool_idx}_{param_idx}"):
                config_manager.delete_param(agent_idx, tool_idx, param_idx)
                st.rerun()

        param["required"] = st.checkbox(
            "Bắt buộc", value=param.get("required", False), key=f"param_required_{agent_idx}_{tool_idx}_{param_idx}"
        )

        st.markdown("---")


def _render_tool_parameters(config_manager: ConfigManager, tool: Dict[str, Any], agent_idx: int, tool_idx: int):
    """Hiển thị parameters của tool"""
    if "input_params" not in tool:
        tool["input_params"] = []

    with st.expander(f"⚙️ Input Parameters của Tool: {tool['name']}", expanded=False):
        for param_idx, param in enumerate(tool.get("input_params", [])):
            _render_parameter(config_manager, param, agent_idx, tool_idx, param_idx)

        if st.button("➕ Thêm Parameter", key=f"add_param_{agent_idx}_{tool_idx}"):
            config_manager.create_param(agent_idx, tool_idx)
            st.rerun()


def _render_tools(config_manager: ConfigManager, agent: Dict[str, Any], agent_idx: int):
    """Hiển thị danh sách tools của agent"""
    nodes = agent.get("nodes") or {}
    tools = nodes.get("tools") or []

    for tool_idx, tool in enumerate(tools):
        st.markdown(
            f"""
            <div class="tool-container">
                <h5>Tool #{tool_idx + 1}</h5>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container():
            cols = st.columns([2, 2, 4, 2, 1.5, 0.5])

            tool_types = ["http", "built_in", "store", "workflow"]
            type_index = tool_types.index(tool.get("type", "http")) if tool.get("type") in tool_types else 0
            new_type = cols[0].selectbox(
                "Loại tool", options=tool_types, index=type_index, key=f"tool_type_{agent_idx}_{tool_idx}"
            )

            if tool.get("type") != new_type:
                tool["type"] = new_type
                if new_type == "built_in":
                    if "tool_path" in tool:
                        tool.pop("tool_path")
                    if "method" in tool:
                        tool.pop("method")
                    if "input_params" in tool:
                        tool.pop("input_params")
                elif new_type == "http":
                    if "input_params" not in tool:
                        tool["input_params"] = []
                    if "store_name" in tool:
                        tool.pop("store_name")
                    if "tool_type" in tool:
                        tool.pop("tool_type")
                    if "token_workflow" in tool:
                        tool.pop("token_workflow")
                elif new_type == "workflow":
                    if "input_params" not in tool:
                        tool["input_params"] = []
                    if "store_name" in tool:
                        tool.pop("store_name")
                    if "tool_type" in tool:
                        tool.pop("tool_type")
            else:
                tool["type"] = new_type

            if tool["type"] == "built_in":
                default_name = tool.get("name", "")
                name_index = list(built_in_tools_name.keys()).index(default_name) if default_name in list(built_in_tools_name.keys()) else 0
                tool["name"] = cols[1].selectbox(
                    "Tên tool", options=list(built_in_tools_name.keys()), index=name_index, key=f"tool_name_{agent_idx}_{tool_idx}"
                )
            else:
                tool["name"] = cols[1].text_input(
                    "Tên tool", value=tool.get("name", ""), key=f"tool_name_{agent_idx}_{tool_idx}"
                )

            tool["description"] = cols[2].text_input(
                "Mô tả tool", value=tool.get("description", ""), key=f"tool_desc_{agent_idx}_{tool_idx}"
            )

            if tool["type"] == "http":
                tool["tool_path"] = cols[3].text_input(
                    "URL API", value=tool.get("tool_path", ""), key=f"tool_url_{agent_idx}_{tool_idx}"
                )
                method_options = ["GET", "POST", "PUT", "DELETE"]
                default_method = tool.get("method", "GET")
                method_index = method_options.index(default_method) if default_method in method_options else 0
                tool["method"] = cols[4].selectbox(
                    "Method", options=method_options, index=method_index, key=f"tool_method_{agent_idx}_{tool_idx}"
                )
            elif tool["type"] == "store":
                tool["store_name"] = cols[3].text_input(
                    "Tên store", value=tool.get("store_name", ""), key=f"tool_store_name_{agent_idx}_{tool_idx}"
                )
                tool["tool_type"] = cols[4].selectbox(
                    "Loại store", options=["dynamic", "standard"], index=0, key=f"tool_store_type_{agent_idx}_{tool_idx}"
                )
            elif tool["type"] == "workflow":
                tool["token_workflow"] = cols[3].text_input(
                    "Token Workflow", value=tool.get("token_workflow", ""), key=f"tool_token_workflow_{agent_idx}_{tool_idx}"
                )
            else:
                cols[3].text_input("URL API", value="", disabled=True, key=f"tool_url_disabled_{agent_idx}_{tool_idx}")
                cols[4].selectbox("Method", options=[""], disabled=True, key=f"tool_method_disabled_{agent_idx}_{tool_idx}")

            with cols[5]:
                st.markdown("<div style='margin-top: 25px'></div>", unsafe_allow_html=True)
                if st.button("❌", key=f"del_tool_{agent_idx}_{tool_idx}"):
                    config_manager.delete_tool(agent_idx, tool_idx)
                    st.rerun()

            if tool["type"] in ("http", "store", "workflow"):
                _render_tool_parameters(config_manager, tool, agent_idx, tool_idx)


def agent_config():
    """Trang cấu hình Agent (UI danh sách sub-agents và tools)"""
    st.title("🧱 Multi-Agent Configuration")

    yaml_config_path = "settings/prod_multi_agent.yaml"
    config_manager = ConfigManager(yaml_config_path)

    if st.button("➕ Thêm Sub-agent"):
        config_manager.create_sub_agent()
        st.rerun()

    for idx, agent in enumerate(config_manager.get_config().get("sub_agents", [])):
        with st.expander(f"🚀 {agent['name']} ({agent['agent_id']})", expanded=False):
            with st.container():
                col1, col2 = st.columns([2, 10])

                new_name = col1.text_input("Tên agent", value=agent.get("name", ""), key=f"name_{idx}")
                agent["name"] = new_name

                _ensure_agent_structure(agent)

                new_description = col2.text_input(
                    "Mô tả agent", value=agent.get("description", ""), key=f"desc_{idx}"
                )
                agent["description"] = new_description

                if agent['type'] == 'ui':
                    try:
                        with open('settings/ui_schema.json', 'r') as file:
                            lines = file.readlines()
                            logs = ''.join(lines) if lines else ""
                    except Exception as e:
                        logs = f"Lỗi khi đọc file schema: {str(e)}"
                    schema_text = st.text_area('Schema', logs, height=700)
                    if st.button("Lưu Schema", key=f"save_schema_{idx}"):
                        with open('settings/ui_schema.json', 'w') as file:
                            file.write(schema_text)
                        save_schema()
                        st.success("Đã lưu schema")
                else:
                    st.markdown("### Tools")
                    _render_tools(config_manager, agent, idx)

                    if st.button("➕ Thêm Tool", key=f"add_tool_{idx}"):
                        config_manager.create_tool(idx)
                        st.rerun()

                if st.button("❌ Xóa Sub-agent", key=f"del_agent_{idx}"):
                    config_manager.delete_sub_agent(idx)
                    st.rerun()

    st.markdown("---")

    with st.expander("📄 Xem YAML cấu hình", expanded=False):
        yaml_string = config_manager.get_yaml_string()
        st.code(yaml_string, language="yaml")

    if st.button("💾 Lưu vào YAML", help=f"Lưu cấu hình vào file {yaml_config_path}"):
        save_success = config_manager.save_config()
        if save_success:
            st.success(f"Đã lưu cấu hình vào file {yaml_config_path}")
        else:
            st.error(f"Không thể lưu vào file {yaml_config_path}")


def execution_config():
    """Trang cấu hình thực thi (endpoint, auth, workflow)"""
    st.title("🔧 Execution Configuration")

    yaml_config_path = "settings/prod_multi_agent.yaml"
    config_manager = ConfigManager(yaml_config_path)

    settings_dict = config_manager.get_config().get("settings", {})

    st.markdown("#### Cấu hình kết nối")
    url_endpoint = st.text_input("URL Endpoint", value=settings_dict.get("url_endpoint", ""))
    workflow_url = st.text_input("Workflow URL", value=settings_dict.get("workflow_url", ""))

    st.markdown("#### Xác thực")
    auth_method = settings_dict.get("auth_method", "oauth2")
    auth_method_options = ["bearer", "basic", "oauth2"]
    default_index = auth_method_options.index(auth_method) if auth_method in auth_method_options else 0
    authentication_method = st.selectbox("Phương thức xác thực", options=auth_method_options, index=default_index)
    
    

    token_url = client_id = client_secret = username = password = token = ""
    if authentication_method == "oauth2":
        token_url = st.text_input("Token URL", value=settings_dict.get("token_url", ""))
        client_id = st.text_input("Client ID", value=settings_dict.get("client_id", ""))
        client_secret = st.text_input("Client Secret", value=settings_dict.get("client_secret", ""))
        username = st.text_input("Username", value=settings_dict.get("username", ""))
        password = st.text_input("Password", value=settings_dict.get("password", ""))
    elif authentication_method == "bearer":
        token = st.text_input("Token", value=settings_dict.get("token", ""))
    elif authentication_method == "basic":
        username = st.text_input("Username", value=settings_dict.get("username", ""))
        password = st.text_input("Password", value=settings_dict.get("password", ""))

    col1, col2 = st.columns(2)
    if col1.button("💾 Lưu cấu hình thực thi"):
        st.session_state.agent_config.get("settings", {})["url_endpoint"] = url_endpoint
        st.session_state.agent_config.get("settings", {})["auth_method"] = authentication_method
        st.session_state.agent_config.get("settings", {})["workflow_url"] = workflow_url
        if authentication_method == "oauth2":
            st.session_state.agent_config.get("settings", {})["token_url"] = token_url
            st.session_state.agent_config.get("settings", {})["client_id"] = client_id
            st.session_state.agent_config.get("settings", {})["client_secret"] = client_secret
            st.session_state.agent_config.get("settings", {})["username"] = username
            st.session_state.agent_config.get("settings", {})["password"] = password
        if authentication_method == "bearer":
            st.session_state.agent_config.get("settings", {})["token"] = token
        if authentication_method == "basic":
            st.session_state.agent_config.get("settings", {})["username"] = username
            st.session_state.agent_config.get("settings", {})["password"] = password

        save_success = config_manager.save_config()
        if save_success:
            st.success(f"Đã lưu cấu hình vào file {yaml_config_path}")
        else:
            st.error(f"Không thể lưu vào file {yaml_config_path}")


