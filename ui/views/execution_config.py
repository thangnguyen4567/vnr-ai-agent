import streamlit as st
import os

from ui.config_manager import ConfigManager



def execution_config():
    """Trang cấu hình thực thi (endpoint, auth, workflow)"""
    st.title("🔧 Execution Configuration")

    # Chọn file cấu hình trong thư mục settings/multi_agents
    configs_dir = "settings/multi_agents"
    try:
        config_files = [f for f in os.listdir(configs_dir) if f.endswith("_multi_agent.yaml")]
        config_files.sort()
    except Exception:
        config_files = []

    if "selected_multi_agent_file" not in st.session_state:
        st.session_state.selected_multi_agent_file = config_files[0] if config_files else ""

    if config_files:
        prefixes = [f.rsplit("_multi_agent.yaml", 1)[0] for f in config_files]
        prefix_to_file = {p: f for p, f in zip(prefixes, config_files)}

        current_file = st.session_state.selected_multi_agent_file
        current_prefix = (
            current_file.rsplit("_multi_agent.yaml", 1)[0]
            if current_file in config_files
            else prefixes[0]
        )

        selected_prefix = st.selectbox(
            "Chọn dự án",
            options=prefixes,
            index=prefixes.index(current_prefix),
            key="select_project_code_exec",
        )

        target_file = prefix_to_file[selected_prefix]
        if target_file != st.session_state.selected_multi_agent_file:
            st.session_state.selected_multi_agent_file = target_file

        yaml_config_path = f"{configs_dir}/{st.session_state.selected_multi_agent_file}"

    else:
        st.warning("Không tìm thấy file cấu hình trong settings/multi_agents")
        with st.expander("➕ Tạo mới cấu hình", expanded=True):
            new_prefix = st.text_input("Tiền tố file", value="new", key="new_prefix_exec_empty")
            new_display_name = st.text_input("Tên hiển thị", value="New Multi Agent", key="new_name_exec_empty")
            if st.button("Tạo", key="create_new_exec_config_empty"):
                new_filename = f"{new_prefix}_multi_agent.yaml"
                new_path = f"{configs_dir}/{new_filename}"
                if os.path.exists(new_path):
                    st.error("File đã tồn tại")
                else:
                    ok = ConfigManager.create_new_config(new_path, new_display_name)
                    if ok:
                        st.session_state.selected_multi_agent_file = new_filename
                        st.success("Đã tạo cấu hình mới")
                        st.rerun()
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

    st.markdown("#### Cấu hình Langfuse")
    langfuse_public_key = st.text_input("Langfuse Public Key", value=settings_dict.get("langfuse_public_key", ""))
    langfuse_secret_key = st.text_input("Langfuse Secret Key", value=settings_dict.get("langfuse_secret_key", ""))

    col1, col2 = st.columns(2)
    if col1.button("💾 Lưu cấu hình thực thi"):
        st.session_state.agent_config.get("settings", {})["url_endpoint"] = url_endpoint
        st.session_state.agent_config.get("settings", {})["auth_method"] = authentication_method
        st.session_state.agent_config.get("settings", {})["workflow_url"] = workflow_url
        st.session_state.agent_config.get("settings", {})["langfuse_public_key"] = langfuse_public_key
        st.session_state.agent_config.get("settings", {})["langfuse_secret_key"] = langfuse_secret_key
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


