import pytest
from fastapi.testclient import TestClient
from src.api.app import app


@pytest.fixture(scope="module")
def client():
    """
    Tạo một TestClient để thực hiện các request test đến ứng dụng FastAPI.
    
    Returns:
        TestClient: Client để test API
    """
    with TestClient(app) as test_client:
        yield test_client 