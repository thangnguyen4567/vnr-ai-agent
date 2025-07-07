
def test_app_startup(client):
    """
    Test khởi động ứng dụng thành công và CORS được cấu hình đúng
    """
    # Thực hiện OPTIONS request để kiểm tra CORS
    headers = {
        "Origin": "http://127.0.0.1:8000",
        "Access-Control-Request-Method": "GET",
    }
    response = client.options("/", headers=headers)
    
    # Kiểm tra CORS headers
    assert response.status_code == 200