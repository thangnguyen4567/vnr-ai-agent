from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from src.config import settings

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
        model=settings.LLM_CONFIG["openai"]["model"],
        api_key=settings.LLM_CONFIG["openai"]["api_key"],
        temperature=settings.LLM_CONFIG["openai"]["temperature"],
        max_tokens=settings.LLM_CONFIG["openai"]["max_tokens"],
        stream_usage=True,
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
        model=settings.LLM_CONFIG["google"]["model"],
        api_key=settings.LLM_CONFIG["google"]["api_key"],
        temperature=settings.LLM_CONFIG["google"]["temperature"],
        max_tokens=settings.LLM_CONFIG["google"]["max_tokens"],
        stream_usage=True,
    )

    return model
