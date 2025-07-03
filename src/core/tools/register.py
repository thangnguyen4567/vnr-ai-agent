from langchain_core.tools import BaseTool
from src.core.tools.builtin_tool import built_in_tools

PARAM_TYPE = {
    "string": "string",
    "number": "number",
    "boolean": "boolean",
    "array": "array",
    "object": "object"
}

class ToolInitializer:
    def __init__(self):
        self.built_in_tools_name = [tool.name for tool in built_in_tools]

    def _resolve_schema_references(self,schema_obj, full_schema):
        """
        Đệ quy giải quyết các tham chiếu trong schema

        Args:
            schema_obj: Schema object cần giải quyết
            full_schema: Schema toàn bộ để tìm các tham chiếu

        Returns:
            Resolved schema object
        """
        if isinstance(schema_obj, dict):
            # Xử lý trường hợp có $ref
            if '$ref' in schema_obj:
                ref_path = schema_obj['$ref']

                # Xử lý tham chiếu đến $defs
                if ref_path.startswith('#/$defs/'):
                    ref_name = ref_path.split('/')[-1]
                    if '$defs' in full_schema and ref_name in full_schema['$defs']:
                        # Lấy schema từ $defs và giải quyết tham chiếu
                        resolved_schema = self._resolve_schema_references(
                            full_schema['$defs'][ref_name].copy(), 
                            full_schema
                        )
                        # Giữ nguyên các thuộc tính khác trong schema gốc
                        for key, value in schema_obj.items():
                            if key != '$ref':
                                resolved_schema[key] = value

                        return resolved_schema
                    
                # Nếu không phải là tham chiếu đến $defs, giữ nguyên schema
                return schema_obj
            
            # Đệ quy giải quyết các thuộc tính dict hoặc list
            resolved_obj = {}
            for key, value in schema_obj.items():
                resolved_obj[key] = self._resolve_schema_references(value, full_schema)
            return resolved_obj
        
        # Xử lý trường hợp là list
        elif isinstance(schema_obj, list):
            return [self._resolve_schema_references(item, full_schema) for item in schema_obj]
        
        # Trường hợp còn lại, giữ nguyên schema
        else:
            return schema_obj

    def convert_to_schema(self,tools: list[BaseTool],llm_provider: str):
        """ Convert tool to schema format base on model provider"""
        schemas = []
        for tool in tools:
            orginal_schema = tool.args_schema.model_json_schema()

            resolved_schema = self._resolve_schema_references(orginal_schema, orginal_schema)

            schema = {
                "name": tool.name,
                "description": tool.description,
                "parameters": resolved_schema
            }

            if llm_provider == "google":
                schema["parameters"].pop("title", None)
                for k, v in schema["parameters"]["properties"].items():
                    if "anyOf" in v:
                        v.update(v["anyOf"][0])
                        v.pop("anyOf", None)
                    v.pop("title", None)
                    v.pop("default", None)

            schema["parameters"]["properties"].pop("state", None)
            if "required" in schema["parameters"]:
                schema["parameters"]["required"] = [
                    key for key in schema["parameters"]["required"] if key != "state"
                ]
            if llm_provider == "google":
                schemas.append(schema)
            else:
                tool_schema = {
                    "type": "function",
                    "function": schema
                }
                schemas.append(tool_schema)

        return schemas

    def convert_http_tool_to_schema(self,tool: dict,llm_provider: str):
        """Convert tools to schema format base on model provider"""
        properties = {}
        required = []

        for param in tool["input_params"]:
            if param.get("enabled", True):
                param_name = param.get("name")
                param_type = PARAM_TYPE.get(param.get("type"), "string")

                param_schema = {
                    "type": param_type,
                    "description": param.get("description", "")
                }

                if param_type == "array":
                    param_schema["items"] = {
                        "type": "number" if param.get("items_type") == "number" else "string"
                    }

                if "default" in param:
                    param_schema["default"] = param.get("default")

                properties[param_name] = param_schema

                if param.get("required", False) and "default" not in param:
                    required.append(param_name)

        parameters = {
            "type": "object",
            "properties": properties,
        }

        if required:
            parameters["required"] = required

        schema = {
            "name": tool["name"],
            "description": tool.get("description", ""),
            "parameters": parameters
        }

        if llm_provider == "google":
            for k, v in parameters["parameters"]["properties"].items():
                if "anyOf" in v:
                    v.update(v["anyOf"][0])
                    v.pop("anyOf", None)
                if "title" in v:
                    v.pop("title", None)
                if "default" in v:
                    v.pop("default", None)
            return schema
        else:
            return {
                "type": "function",
                "function": schema
            }

    def initialize_tools(self,agent_config: dict):
        """ Initialize tools for agent based on agent config """
        tools = []
        raw_tools = agent_config.get("nodes", {}).get("tools", [])

        llm_provider = agent_config["nodes"]["llm"]["provider"]
        http_tool_registry = {}

        for tool in raw_tools:
            if tool["type"] == "built_in" and tool["name"] in self.built_in_tools_name:
                built_in_tool = next((t for t in built_in_tools if t.name == tool["name"]), None)
                if built_in_tool:
                    tools.extend(self.convert_to_schema([built_in_tool],llm_provider))
            elif tool["type"] == "http":
                tool_schema = self.convert_http_tool_to_schema(tool,llm_provider)
                tools.append(tool_schema)
                http_tool_registry[tool["name"]] = {
                    "url": tool["tool_path"],
                    "method": tool.get("method", "GET"),
                    "provider": tool.get("provider"),
                    "input_params": tool["input_params"],
                    "output_params": tool["output_params"]
                }
            else:
                raise ValueError(f"Tool type {tool['type']} is not supported")

        return tools,http_tool_registry
       




