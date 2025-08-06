import streamlit as st
import uuid
import yaml
import os
from typing import Dict, Any
from src.core.tools.builtin_tool import built_in_tools_name

class ConfigManager:
    """Lớp quản lý cấu hình"""
    
    def __init__(self, config_path: str):
        """Khởi tạo ConfigManager với đường dẫn file cấu hình"""
        self.config_path = config_path

        if "agent_config" not in st.session_state:
            st.session_state.agent_config = self.load_config()
            
    def load_config(self) -> Dict[str, Any]:
        """Load cấu hình từ file YAML"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as file:
                    config = yaml.safe_load(file)
                    if config:
                        return config
        except Exception as e:
            st.error(f"Lỗi khi đọc file cấu hình: {str(e)}")
        
        # Cấu hình mặc định nếu không load được
        return {
            "agent_id": str(uuid.uuid4()),
            "name": "Multi Agent",
            "type": "multi",
            "sub_agents": [],
            "auth": {
                "method": "",
                "token": "",
                "url_endpoint": "http://localhost:8000/"
            }
        }
    
    def save_config(self) -> bool:
        """Lưu cấu hình vào file YAML"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(st.session_state.agent_config, file, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False)
            return True
        except Exception as e:
            st.error(f"Lỗi khi lưu cấu hình: {str(e)}")
            return False
    
    def create_sub_agent(self):
        """Tạo một sub-agent mới"""
        new_id = str(uuid.uuid4())
        st.session_state.agent_config["sub_agents"].append({
            "agent_id": new_id,
            "name": "New Agent",
            "description": "",
            "type": "fc",
            "nodes": {
                "llm": {
                    "provider": "openai",
                    "agent_prompt": ""
                },
                "tools": []
            }
        })
        self.save_config()
    
    def delete_sub_agent(self, idx: int):
        """Xóa một sub-agent theo index"""
        if 0 <= idx < len(st.session_state.agent_config.get("sub_agents", [])):
            st.session_state.agent_config["sub_agents"].pop(idx)
            self.save_config()
    
    def create_tool(self, agent_idx: int):
        """Thêm một tool mới cho agent"""
        if 0 <= agent_idx < len(st.session_state.agent_config.get("sub_agents", [])):
            agent = st.session_state.agent_config["sub_agents"][agent_idx]
            if "nodes" not in agent:
                agent["nodes"] = {"llm": {"provider": "openai", "agent_prompt": ""}, "tools": []}
            elif "tools" not in agent["nodes"]:
                agent["nodes"]["tools"] = []
                
            agent["nodes"]["tools"].append({
                "type": "http",
                "name": "new_tool",
                "description": "",
                "tool_path": "",
                "input_params": []
            })
            self.save_config()
    
    def delete_tool(self, agent_idx: int, tool_idx: int):
        """Xóa một tool khỏi agent"""
        if 0 <= agent_idx < len(st.session_state.agent_config.get("sub_agents", [])):
            agent = st.session_state.agent_config["sub_agents"][agent_idx]
            if ("nodes" in agent and "tools" in agent["nodes"] and 
                0 <= tool_idx < len(agent["nodes"]["tools"])):
                agent["nodes"]["tools"].pop(tool_idx)
                self.save_config()
    
    def create_param(self, agent_idx: int, tool_idx: int):
        """Thêm một parameter mới cho tool"""
        if 0 <= agent_idx < len(st.session_state.agent_config.get("sub_agents", [])):
            agent = st.session_state.agent_config["sub_agents"][agent_idx]
            if ("nodes" in agent and "tools" in agent["nodes"] and 
                0 <= tool_idx < len(agent["nodes"]["tools"])):
                tool = agent["nodes"]["tools"][tool_idx]
                if "input_params" not in tool:
                    tool["input_params"] = []
                    
                tool["input_params"].append({
                    "name": "",
                    "description": "",
                    "input_method": "query",
                    "type": "string",
                    "default": "",
                    "required": False
                })
                self.save_config()
    
    def delete_param(self, agent_idx: int, tool_idx: int, param_idx: int):
        """Xóa một parameter khỏi tool"""
        if 0 <= agent_idx < len(st.session_state.agent_config.get("sub_agents", [])):
            agent = st.session_state.agent_config["sub_agents"][agent_idx]
            if ("nodes" in agent and "tools" in agent["nodes"] and 
                0 <= tool_idx < len(agent["nodes"]["tools"])):
                tool = agent["nodes"]["tools"][tool_idx]
                if "input_params" in tool and 0 <= param_idx < len(tool["input_params"]):
                    tool["input_params"].pop(param_idx)
                    self.save_config()
                    
    def get_config(self) -> Dict[str, Any]:
        """Lấy cấu hình hiện tại"""
        return st.session_state.agent_config
    
    def get_yaml_string(self) -> str:
        """Chuyển đổi cấu hình hiện tại thành chuỗi YAML"""
        return yaml.dump(st.session_state.agent_config, default_flow_style=False, 
                       allow_unicode=True, sort_keys=False)

class AgentUI:
    """Lớp xử lý giao diện người dùng cho agent"""

    def __init__(self, config_manager: ConfigManager):
        """Khởi tạo AgentUI với ConfigManager"""
        self.config_manager = config_manager
    
    def render_main_interface(self):
        """Hiển thị giao diện chính"""
        st.set_page_config(layout="wide")
        st.title("🧱 Multi-Agent AI Configuration")
        
        # Thêm agent mới
        if st.button("➕ Thêm Sub-agent"):
            self.config_manager.create_sub_agent()
            st.rerun()

        # Nhập url endpoint
        with st.expander(f"🔑 Xác thực", expanded=False):
            self.url_endpoint = st.text_input("URL Endpoint", value=self.config_manager.get_config()["auth"]["url_endpoint"])
            auth_method = self.config_manager.get_config()["auth"]["method"]
            auth_method_options = ["bearer", "basic", "api_key", "oauth2"]
            default_index = auth_method_options.index(auth_method) if auth_method in auth_method_options else 0
            self.authentication_method = st.selectbox("Phương thức xác thực", options=auth_method_options, index=default_index)
            self.token = st.text_input("Token", value=self.config_manager.get_config()["auth"]["token"])
        
        # Hiển thị danh sách agents
        self._render_agent_list()
        
        st.markdown("---")
        
        # Nút lưu cấu hình
        col1, col2 = st.columns(2)
        if col1.button("💾 Lưu vào YAML", help=f"Lưu cấu hình vào file {self.config_manager.config_path}"):
            st.session_state.agent_config["auth"]["token"] = self.token
            st.session_state.agent_config["auth"]["url_endpoint"] = self.url_endpoint
            st.session_state.agent_config["auth"]["method"] = self.authentication_method
            save_success = self.config_manager.save_config()
            if save_success:
                st.success(f"Đã lưu cấu hình vào file {self.config_manager.config_path}")
            else:
                st.error(f"Không thể lưu vào file {self.config_manager.config_path}")
        
        # Hiển thị YAML
        with st.expander("📄 Xem YAML cấu hình", expanded=False):
            yaml_string = self.config_manager.get_yaml_string()
            st.code(yaml_string, language="yaml")
    
    def _render_agent_list(self):
        """Hiển thị danh sách sub-agents"""
        for idx, agent in enumerate(self.config_manager.get_config().get("sub_agents", [])):
            with st.expander(f"🚀 {agent['name']} ({agent['agent_id']})", expanded=False):
                with st.container():
                    col1, col2 = st.columns([2, 10])
                    
                    # Cập nhật tên và mô tả
                    new_name = col1.text_input("Tên agent", value=agent.get("name", ""), key=f"name_{idx}")
                    agent["name"] = new_name
                    
                    agent["type"] = 'fc'
                    
                    # Đảm bảo cấu trúc nodes
                    self._ensure_agent_structure(agent)
                    
                    # Cập nhật mô tả
                    new_description = col2.text_input("Mô tả agent", value=agent.get("description", ""), key=f"desc_{idx}")
                    agent["description"] = new_description
                    
                    # Hiển thị tools
                    st.markdown("### Tools")
                    self._render_tools(agent, idx)
                    
                    # Nút thêm tool
                    if st.button("➕ Thêm Tool", key=f"add_tool_{idx}"):
                        self.config_manager.create_tool(idx)
                        st.rerun()
                    
                    # Nút xóa agent
                    if st.button("❌ Xóa Sub-agent", key=f"del_agent_{idx}"):
                        self.config_manager.delete_sub_agent(idx)
                        st.rerun()
        
    def _ensure_agent_structure(self, agent: Dict[str, Any]):
        """Đảm bảo agent có cấu trúc dữ liệu đúng"""
        if "nodes" not in agent:
            agent["nodes"] = {"llm": {"provider": "openai", "agent_prompt": ""}, "tools": []}
        elif "llm" not in agent["nodes"]:
            agent["nodes"]["llm"] = {"provider": "openai", "agent_prompt": ""}
        
        agent["nodes"]["llm"]["provider"] = 'openai'
        
        if "tools" not in agent["nodes"]:
            agent["nodes"]["tools"] = []
    
    def _render_tools(self, agent: Dict[str, Any], agent_idx: int):
        """Hiển thị danh sách tools của agent"""
        for tool_idx, tool in enumerate(agent["nodes"].get("tools", [])):
            # Header cho tool
            st.markdown(f"""
            <div class="tool-container">
                <h5>Tool #{tool_idx + 1}</h5>
            </div>
            """, unsafe_allow_html=True)
            
            with st.container():
                # Layout cho tool
                cols = st.columns([2, 2, 4, 2, 1, 1])
                
                # Loại tool
                tool_types = ["http", "built_in", "store"]
                type_index = tool_types.index(tool.get("type", "http")) if tool.get("type") in tool_types else 0
                new_type = cols[0].selectbox("Loại tool", options=tool_types, index=type_index, key=f"tool_type_{agent_idx}_{tool_idx}")
                
                # Nếu loại tool thay đổi, cập nhật cấu trúc
                if tool.get("type") != new_type:
                    tool["type"] = new_type
                    if new_type == "built_in":
                        if "tool_path" in tool:
                            tool.pop("tool_path")
                        if "method" in tool:
                            tool.pop("method")
                        if "input_params" in tool:
                            tool.pop("input_params")
                    else:  # http
                        if "input_params" not in tool:
                            tool["input_params"] = []
                else:
                    tool["type"] = new_type
                
                # Các thuộc tính khác của tool
                if tool["type"] == "built_in":
                    tool["name"] = cols[1].selectbox("Method", options=list(built_in_tools_name.keys()), key=f"tool_method_{agent_idx}_{tool_idx}")

                else:   
                    tool["name"] = cols[1].text_input("Tên tool", value=tool.get("name", ""), key=f"tool_name_{agent_idx}_{tool_idx}")
                
                tool["description"] = cols[2].text_input("Mô tả tool", value=tool.get("description", ""), key=f"tool_desc_{agent_idx}_{tool_idx}")
                
                # Các thuộc tính dựa vào loại tool
                if tool["type"] == "http":
                    tool["tool_path"] = cols[3].text_input("URL API", value=tool.get("tool_path", ""), key=f"tool_url_{agent_idx}_{tool_idx}")
                    method_options = ["GET", "POST", "PUT", "DELETE"]
                    default_method = tool.get("method", "GET")
                    method_index = method_options.index(default_method) if default_method in method_options else 0
                    tool["method"] = cols[4].selectbox("Method", options=method_options, index=method_index, key=f"tool_method_{agent_idx}_{tool_idx}")
                elif tool["type"] == "store":
                    tool["store_name"] = cols[3].text_input("Tên store", value=tool.get("store_name", ""), key=f"tool_store_name_{agent_idx}_{tool_idx}")
                    tool["rec_take"] = cols[4].text_input("Số lượng lấy", value=tool.get("rec_take", "5"), key=f"tool_rec_take_{agent_idx}_{tool_idx}")
                else:
                    # Nếu là built_in tool, không cần hiển thị tool_path và method
                    cols[3].text_input("URL API", value="", disabled=True, key=f"tool_url_disabled_{agent_idx}_{tool_idx}")
                    cols[4].selectbox("Method", options=[""], disabled=True, key=f"tool_method_disabled_{agent_idx}_{tool_idx}")
                
                # Nút xóa tool
                with cols[5]:
                    st.markdown("<div style='margin-top: 25px'></div>", unsafe_allow_html=True)
                    if st.button("❌ Xóa", key=f"del_tool_{agent_idx}_{tool_idx}"):
                        self.config_manager.delete_tool(agent_idx, tool_idx)
                        st.rerun()
                
                # Hiển thị parameters nếu là http tool
                if tool["type"] == "http" or tool["type"] == "store":
                    self._render_tool_parameters(tool, agent_idx, tool_idx)
    
    def _render_tool_parameters(self, tool: Dict[str, Any], agent_idx: int, tool_idx: int):
        """Hiển thị parameters của tool"""
        if "input_params" not in tool:
            tool["input_params"] = []
        
        # Expander cho parameters
        with st.expander(f"⚙️ Input Parameters của Tool: {tool['name']}", expanded=False):
            # Hiển thị từng parameter
            for param_idx, param in enumerate(tool.get("input_params", [])):
                self._render_parameter(param, agent_idx, tool_idx, param_idx)
            
            # Nút thêm parameter
            if st.button("➕ Thêm Parameter", key=f"add_param_{agent_idx}_{tool_idx}"):
                self.config_manager.create_param(agent_idx, tool_idx)
                st.rerun()
    
    def _render_parameter(self, param: Dict[str, Any], agent_idx: int, tool_idx: int, param_idx: int):
        """Hiển thị một parameter cụ thể"""
        # Header cho parameter
        st.markdown(f"""
        <div class="param-item">
            <h6>Parameter #{param_idx + 1}</h6>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            param_cols = st.columns([2, 4, 2, 2, 1, 1])
            
            # Các thuộc tính của parameter
            param["name"] = param_cols[0].text_input("Tên tham số", value=param.get("name", ""), key=f"param_name_{agent_idx}_{tool_idx}_{param_idx}")
            param["description"] = param_cols[1].text_input("Mô tả", value=param.get("description", ""), key=f"param_desc_{agent_idx}_{tool_idx}_{param_idx}")
            
            # Phương thức input
            input_methods = ["query", "header", "path", "body"]
            method_index = input_methods.index(param.get("input_method", "query")) if param.get("input_method") in input_methods else 0
            param["input_method"] = param_cols[2].selectbox("Phương thức", options=input_methods, index=method_index, key=f"param_method_{agent_idx}_{tool_idx}_{param_idx}")
            
            # Giá trị mặc định
            param["default"] = param_cols[3].text_input("Giá trị mặc định", value=param.get("default", ""), key=f"param_default_{agent_idx}_{tool_idx}_{param_idx}")
            
            # Kiểu dữ liệu
            param_types = ["string", "number", "boolean", "array", "date"]
            type_index = param_types.index(param.get("type", "string")) if param.get("type") in param_types else 0
            param["type"] = param_cols[4].selectbox("Kiểu", options=param_types, index=type_index, key=f"param_type_{agent_idx}_{tool_idx}_{param_idx}")
            
            # Nút xóa parameter
            with param_cols[5]:
                st.markdown("<div style='margin-top: 25px'></div>", unsafe_allow_html=True)
                if st.button("❌ Xóa", key=f"del_param_{agent_idx}_{tool_idx}_{param_idx}"):
                    self.config_manager.delete_param(agent_idx, tool_idx, param_idx)
                    st.rerun()
            
            # Checkbox bắt buộc
            param["required"] = st.checkbox("Bắt buộc", value=param.get("required", False), key=f"param_required_{agent_idx}_{tool_idx}_{param_idx}")
            
            st.markdown("---")

def config():
    """Hàm chính để khởi tạo ứng dụng config"""
    # Đường dẫn đến file cấu hình
    yaml_config_path = "settings/custom_multi_agent.yaml"
    
    # Khởi tạo ConfigManager
    config_manager = ConfigManager(yaml_config_path)
    
    # Khởi tạo và render UI
    agent_ui = AgentUI(config_manager)
    agent_ui.render_main_interface()