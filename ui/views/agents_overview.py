import os
import yaml
import streamlit as st

from ui.config_manager import ConfigManager


def _list_multi_agent_files():
    configs_dir = "settings/multi_agents"
    try:
        files = [f for f in os.listdir(configs_dir) if f.endswith("_multi_agent.yaml")]
        files.sort()
        return configs_dir, files
    except Exception:
        return configs_dir, []


def render_agents_overview():
    """Màn hình danh sách các multi-agent dưới dạng thẻ với menu bánh răng."""
    st.title("🧱 Multi-Agent - Danh sách cấu hình")

    # Dialog xác nhận xóa
    @st.dialog("Xác nhận xóa")
    def _show_delete_confirm_dialog():
        target = st.session_state.get("confirm_delete_target")
        if not target:
            st.write("Không có mục để xóa.")
            return
        st.warning(
            f"Bạn có chắc chắn muốn xóa cấu hình '{target['file_name']}'?",
            icon="⚠️",
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Hủy", key=f"cancel_delete_{target['key']}"):
                st.session_state.pop("confirm_delete_target", None)
                st.rerun()
        with col2:
            if st.button("OK, xóa", key=f"confirm_delete_{target['key']}"):
                try:
                    os.remove(target["yaml_path"])
                    if st.session_state.get("selected_multi_agent_file") == target["file_name"]:
                        st.session_state.selected_multi_agent_file = ""
                    st.success("Đã xóa cấu hình")
                except Exception as e:
                    st.error(f"Không thể xóa: {str(e)}")
                finally:
                    st.session_state.pop("confirm_delete_target", None)
                    st.rerun()

    # Nếu có mục đang chờ xác nhận xóa thì mở dialog
    if st.session_state.get("confirm_delete_target"):
        _show_delete_confirm_dialog()

    configs_dir, config_files = _list_multi_agent_files()

    # Form tạo mới cấu hình
    with st.expander("➕ Tạo mới cấu hình", expanded=False):
        new_display_name = st.text_input("Tên hiển thị", value="", key="overview_new_name")
        new_prefix = st.text_input("Mã dự án", value="", key="overview_new_prefix")
        public_key = st.text_input("Langfuse public key", value="", key="overview_new_public_key")
        secret_key = st.text_input("Langfuse secret key", value="", key="overview_new_secret_key")
        if st.button("Tạo", key="overview_create_new"):
            new_filename = f"{new_prefix}_multi_agent.yaml"
            new_path = f"{configs_dir}/{new_filename}"
            if os.path.exists(new_path):
                st.error("File đã tồn tại")
            else:
                ok = ConfigManager.create_new_config(new_path, new_display_name, public_key, secret_key)
                if ok:
                    st.session_state.selected_multi_agent_file = new_filename
                    st.success("Đã tạo cấu hình mới")
                    st.rerun()

    st.markdown("---")

    if not config_files:
        st.info("Chưa có cấu hình nào. Hãy tạo mới ở trên.")
        return

    # Hiển thị dạng lưới thẻ
    num_cols = 3
    rows = [config_files[i:i + num_cols] for i in range(0, len(config_files), num_cols)]
    for row_idx, row_files in enumerate(rows):
        cols = st.columns(num_cols)
        for col_idx, file_name in enumerate(row_files):
            with cols[col_idx]:
                card_key = f"card_{row_idx}_{col_idx}_{file_name}"
                with st.container(border=True):
                    prefix_name = file_name.rsplit("_multi_agent.yaml", 1)[0]
                    yaml_path = f"{configs_dir}/{file_name}"

                    display_name = None
                    try:
                        with open(yaml_path, 'r', encoding='utf-8') as f:
                            cfg = yaml.safe_load(f) or {}
                            display_name = cfg.get("name")
                    except Exception:
                        display_name = None

                    header_cols = st.columns([8, 1])
                    project_cols = st.columns([1, 1])
                    with project_cols[0]:
                        st.text(f"Mã dự án: {prefix_name}")
                    # Tiêu đề card: hiển thị theo tên (fallback tiền tố) kèm icon 🤖
                    title_text = f"🤖 {display_name or prefix_name}"
                    if header_cols[0].button(title_text, key=f"open_{card_key}"):
                        st.session_state.selected_multi_agent_file = file_name
                        st.session_state.agent_config_view = "detail"
                        st.rerun()

                    # Menu bánh răng
                    with header_cols[1]:
                        menu = st.popover("⚙️", use_container_width=True)
                        with menu:
                            if st.button("✏️ Chỉnh sửa", key=f"edit_{card_key}"):
                                st.session_state.selected_multi_agent_file = file_name
                                st.session_state.agent_config_view = "detail"
                                st.rerun()
                            if st.button("🗑️ Xóa", key=f"delete_{card_key}"):
                                st.session_state.confirm_delete_target = {
                                    "file_name": file_name,
                                    "yaml_path": yaml_path,
                                    "key": card_key,
                                }
                                _show_delete_confirm_dialog()

                    # Bỏ caption để tránh lặp lại tên


