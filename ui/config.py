import streamlit as st
import uuid
import json
import yaml
import os

def config():
    st.set_page_config(layout="wide")
    st.title("🧱 Multi-Agent AI Configuration")
    st.session_state.agent_config = None

    # Tạo CSS tùy chỉnh
    st.markdown("""
    <style>
        .tool-container {
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 5px;
        }
        .params-container {
            border-left: 3px solid #4285f4;
            padding: 5px;
            margin: 5px 0;
            border-radius: 5px;
        }
        .param-item {
            padding: 8px;
            margin-bottom: 8px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        h6 {
            padding:0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Function to load configuration from YAML file
    def load_yaml_config(file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        return None

    # Function to save configuration to YAML file
    def save_yaml_config(config, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True

    # Path to the YAML config file
    # yaml_config_path = "settings/multi_agent.yaml"
    yaml_config_path = "settings/custom_multi_agent.yaml"

    # Luôn load cấu hình từ YAML khi khởi động
    if st.session_state.agent_config is None:
        yaml_config = load_yaml_config(yaml_config_path)
        if yaml_config:
            st.session_state.agent_config = yaml_config
    else:
        # Khởi tạo config mặc định nếu không load được
        st.session_state.agent_config = {
            "agent_id": str(uuid.uuid4()),
            "name": "Multi Agent",
            "type": "multi",
            "agents": [],
            "sub_agents": []
        }

    config = st.session_state.agent_config

    # Main config
    config["name"] = "Multi Agent"
    config["agent_id"] = str(uuid.uuid4())

    # Đảm bảo agents array tồn tại nhưng không hiển thị
    if 'agents' not in config:
        config['agents'] = []

    # Add Sub-agent
    if st.button("➕ Thêm Sub-agent"):
        # Tạo agent chính mới nếu cần
        new_id = str(uuid.uuid4())
        config["agents"].append({
            "id": new_id,
            "name": "New Agent",
            "description": ""
        })
        
        # Tạo sub-agent liên kết với agent chính
        config["sub_agents"].append({
            "agent_id": new_id,
            "name": "New Agent",
            "type": "fc",
            "nodes": {
                "llm": {
                    "provider": "openai",
                    "agent_prompt": ""
                },
                "tools": []
            }
        })

    # Tạo map agent_id -> description để tìm kiếm nhanh
    agent_descriptions = {agent["id"]: agent["description"] for agent in config.get("agents", [])}
    agent_names = {agent["id"]: agent["name"] for agent in config.get("agents", [])}

    # Hiển thị danh sách sub-agent
    for idx, agent in enumerate(config.get("sub_agents", [])):
        with st.expander(f"🚀 {agent['name']} ({agent['agent_id']})", expanded=True):
            col1, col2 = st.columns([2, 10])
            
            # Tìm agent chính tương ứng với sub-agent
            agent_main_id = agent["agent_id"]
            agent_name = agent_names.get(agent_main_id, agent["name"])
            
            # Cập nhật tên cho cả agent chính và sub-agent
            new_name = col1.text_input("Tên agent", value=agent_name, key=f"name_{idx}")
            agent["name"] = new_name
            
            # Cập nhật tên của agent chính tương ứng
            for main_agent in config.get("agents", []):
                if main_agent["id"] == agent_main_id:
                    main_agent["name"] = new_name
                    break
            
            agent["type"] = 'fc'
            
            # Thêm agent_id từ danh sách agents chính nếu có
            agent_options = [a["id"] for a in config.get("agents", [])]
            
            if agent_options and agent_main_id not in agent_options:
                # Nếu agent_id hiện tại không còn trong danh sách, thêm vào
                config["agents"].append({
                    "id": agent_main_id,
                    "name": agent["name"],
                    "description": ""
                })
                agent_options.append(agent_main_id)
            
            # Ensure nodes structure exists
            if "nodes" not in agent:
                agent["nodes"] = {"llm": {"provider": "openai", "agent_prompt": ""}, "tools": []}
            elif "llm" not in agent["nodes"]:
                agent["nodes"]["llm"] = {"provider": "openai", "agent_prompt": ""}
            
            agent["nodes"]["llm"]["provider"] = 'openai'
            
            # Lấy mô tả từ agent chính
            current_description = ""
            for main_agent in config["agents"]:
                if main_agent["id"] == agent_main_id:
                    current_description = main_agent["description"]
                    break
            
            # Cập nhật mô tả cho agent chính
            new_description = col2.text_input("Mô tả agent", value=current_description, key=f"desc_{idx}")
            for main_agent in config["agents"]:
                if main_agent["id"] == agent_main_id:
                    main_agent["description"] = new_description
                    break
            
            st.markdown("### Tools")
            # Ensure tools array exists
            if "tools" not in agent["nodes"]:
                agent["nodes"]["tools"] = []
                
            for tool_idx, tool in enumerate(agent["nodes"]["tools"]):
                # Sử dụng HTML container để tạo khung cho tool
                st.markdown(f"""
                <div class="tool-container">
                    <h5>Tool #{tool_idx + 1}</h5>
                </div>
                """, unsafe_allow_html=True)
                
                with st.container():
                    cols = st.columns([2, 2, 4, 2, 1, 1])
                    
                    # Xác định loại tool
                    tool_types = ["http", "built_in"]
                    type_index = tool_types.index(tool.get("type", "http")) if tool.get("type") in tool_types else 0
                    tool["type"] = cols[0].selectbox("Loại tool", options=tool_types, index=type_index, key=f"tool_type_{idx}_{tool_idx}")
                    
                    tool["name"] = cols[1].text_input("Tên tool", value=tool.get("name", ""), key=f"tool_name_{idx}_{tool_idx}")
                    tool["description"] = cols[2].text_input("Mô tả tool", value=tool.get("description", ""), key=f"tool_desc_{idx}_{tool_idx}")
                    
                    if tool["type"] == "http":
                        tool["tool_path"] = cols[3].text_input("URL API", value=tool.get("tool_path", ""), key=f"tool_url_{idx}_{tool_idx}")
                        method_options = ["GET", "POST", "PUT", "DELETE"]
                        default_method = tool.get("method", "GET")
                        method_index = method_options.index(default_method) if default_method in method_options else 0
                        tool["method"] = cols[4].selectbox("Method", options=method_options, index=method_index, key=f"tool_method_{idx}_{tool_idx}")
                    else:
                        # Nếu là built_in tool, không cần hiển thị tool_path và method
                        cols[3].text_input("URL API", value="", disabled=True, key=f"tool_url_disabled_{idx}_{tool_idx}")
                        cols[4].selectbox("Method", options=[""], disabled=True, key=f"tool_method_disabled_{idx}_{tool_idx}")
                        if "tool_path" in tool:
                            tool.pop("tool_path")
                        if "method" in tool:
                            tool.pop("method")

                    with cols[5]:
                        st.markdown("<div style='margin-top: 25px'></div>", unsafe_allow_html=True)
                        if st.button("❌ Xóa", key=f"del_tool_{idx}_{tool_idx}"):
                            agent["nodes"]["tools"].pop(tool_idx)
                            st.rerun()

                    # Khởi tạo input_params nếu chưa có và nếu là http tool
                    if tool["type"] == "http":
                        if "input_params" not in tool:
                            tool["input_params"] = []

                        # Hiển thị input parameters
                        with st.expander(f"⚙️ Input Parameters của Tool: {tool['name']}", expanded=False):
                            for param_idx, param in enumerate(tool.get("input_params", [])):
                                # Sử dụng HTML để tạo khung cho mỗi parameter
                                st.markdown(f"""
                                <div class="param-item">
                                    <h6>Parameter #{param_idx + 1}</h6>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                with st.container():
                                    param_cols = st.columns([2, 4, 2, 2, 1, 1])
                                    param["name"] = param_cols[0].text_input("Tên tham số", value=param.get("name", ""), key=f"param_name_{idx}_{tool_idx}_{param_idx}")
                                    param["description"] = param_cols[1].text_input("Mô tả", value=param.get("description", ""), key=f"param_desc_{idx}_{tool_idx}_{param_idx}")
                                    
                                    input_methods = ["query", "header", "path", "body"]
                                    method_index = input_methods.index(param.get("input_method", "query")) if param.get("input_method") in input_methods else 0
                                    param["input_method"] = param_cols[2].selectbox("Phương thức", options=input_methods, index=method_index, key=f"param_method_{idx}_{tool_idx}_{param_idx}")
                                    
                                    param["default"] = param_cols[3].text_input("Giá trị mặc định", value=param.get("default", ""), key=f"param_default_{idx}_{tool_idx}_{param_idx}")

                                    param_types = ["string", "number", "boolean", "array", "date"]
                                    type_index = param_types.index(param.get("type", "string")) if param.get("type") in param_types else 0
                                    param["type"] = param_cols[4].selectbox("Kiểu", options=param_types, index=type_index, key=f"param_type_{idx}_{tool_idx}_{param_idx}")

                                    with param_cols[5]:
                                        st.markdown("<div style='margin-top: 25px'></div>", unsafe_allow_html=True)
                                        if st.button("❌ Xóa",key=f"del_param_{idx}_{tool_idx}_{param_idx}"):
                                            tool["input_params"].pop(param_idx)
                                            st.rerun()
                                    
                                    # Hiển thị required nếu cần
                                    param["required"] = st.checkbox("Bắt buộc", value=param.get("required", False), key=f"param_required_{idx}_{tool_idx}_{param_idx}")
                                    
                                    st.markdown("---")

                            if st.button("➕ Thêm Parameter", key=f"add_param_{idx}_{tool_idx}"):
                                tool["input_params"].append({
                                    "name": "",
                                    "description": "",
                                    "input_method": "query",
                                    "type": "string"
                                })
                                st.rerun()
                    else:
                        # Nếu là built_in tool, loại bỏ input_params nếu có
                        if "input_params" in tool:
                            tool.pop("input_params")

            if st.button("➕ Thêm Tool", key=f"add_tool_{idx}"):
                agent["nodes"]["tools"].append({
                    "type": "http",
                    "name": "new_tool",
                    "description": "",
                    "tool_path": "",
                    "input_params": []
                })
                st.rerun()

            if st.button("❌ Xóa Sub-agent", key=f"del_agent_{idx}"):
                config["sub_agents"].pop(idx)
                st.rerun()

    st.markdown("---")

    # Save config
    col1, col2 = st.columns(2)

    # Lưu file YAML
    if col1.button("💾 Lưu vào YAML", help=f"Lưu cấu hình vào file {yaml_config_path}"):
        save_success = save_yaml_config(config, yaml_config_path)
        if save_success:
            st.success(f"Đã lưu cấu hình vào file {yaml_config_path}")
        else:
            st.error(f"Không thể lưu vào file {yaml_config_path}")

    # Lưu file JSON
    json_data = json.dumps(config, indent=2, ensure_ascii=False)
    col2.download_button(
        label="📥 Tải file JSON",
        data=json_data,
        file_name="multi_agent_config.json",
        mime="application/json"
    )

    # Xem toàn bộ cấu hình
    with st.expander("📄 Xem JSON cấu hình", expanded=False):
        st.json(config)

    with st.expander("📄 Xem YAML cấu hình", expanded=False):
        yaml_string = yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False)
        st.code(yaml_string, language="yaml")