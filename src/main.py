import uvicorn
from src.config import global_config


def print_loaded_config():
    """In ra thông tin cấu hình đã được tải"""
    print("\n=== THÔNG TIN CẤU HÌNH ĐÃ ĐƯỢC TẢI ===")

    # MongoDB config
    print(f"\nMongoDB URI: {global_config.APP_CONFIG.mongodb.uri}")

    # FC Agent config
    if global_config.APP_CONFIG.fc_agent:
        print("\nFC Agent config:")
        print(f"  - Agent ID: {global_config.APP_CONFIG.fc_agent.agent_id}")
        print(f"  - Tên: {global_config.APP_CONFIG.fc_agent.name}")
        print(f"  - Loại: {global_config.APP_CONFIG.fc_agent.type}")
        if global_config.APP_CONFIG.fc_agent.nodes:
            print(f"  - LLM model: {global_config.APP_CONFIG.fc_agent.nodes.llm.model}")
            print(
                f"  - LLM provider: {global_config.APP_CONFIG.fc_agent.nodes.llm.provider}"
            )

    # Multi Agent config
    if global_config.APP_CONFIG.multi_agent:
        print("\nMulti Agent config:")
        print(f"  - Agent ID: {global_config.APP_CONFIG.multi_agent.agent_id}")
        print(f"  - Tên: {global_config.APP_CONFIG.multi_agent.name}")
        print(
            f"  - Số lượng sub-agents: {len(global_config.APP_CONFIG.multi_agent.sub_agents) if global_config.APP_CONFIG.multi_agent.sub_agents else 0}"
        )

    # LLM config
    if global_config.APP_CONFIG.llm:
        print("\nLLM config:")
        print(f"  - Router model: {global_config.APP_CONFIG.llm.router.model}")
        print(f"  - Router provider: {global_config.APP_CONFIG.llm.router.provider}")
        if global_config.APP_CONFIG.llm.openai:
            print(f"  - OpenAI model: {global_config.APP_CONFIG.llm.openai.model}")
        if global_config.APP_CONFIG.llm.gemini:
            print(f"  - Gemini model: {global_config.APP_CONFIG.llm.gemini.model}")


def main():
    """Hàm chính để khởi động API"""
    print("Đang tải cấu hình từ file YAML...")
    print_loaded_config()

    print("\nĐang khởi động AI API...")
    uvicorn.run(
        "src.api.app:app", host="localhost", port=8000, reload=True, log_level="info"
    )


if __name__ == "__main__":
    main()
