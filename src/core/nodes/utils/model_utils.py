from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
def get_model(**config: Dict[str, Any]):

    provider = config.get("provider", "openai").lower()

    if provider == "openai":
        return _get_openai_model(**config)
    elif provider == "google":
        return _get_google_model(**config)

def _get_openai_model(**config: Dict[str, Any]):
    """
    Lấy model OpenAI

    Args:
        config: Cấu hình model

    Returns:
        Model OpenAI
    """
    model = ChatOpenAI(
        model=config["model"], 
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=config.get("temperature", 0),
        max_tokens=config.get("max_tokens", 1000),
        stream_usage=True
    )

    return model


def _get_google_model(**config: Dict[str, Any]):
    """
    Lấy model Google

    Args:
        config: Cấu hình model

    Returns:
        Model Google
    """
    model = ChatGoogleGenerativeAI(
        model=config["model"], 
        api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=config.get("temperature", 0),
        max_tokens=config.get("max_tokens", 1000),
        stream_usage=True
    )

    return model