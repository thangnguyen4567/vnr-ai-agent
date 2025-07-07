def test_create_goal(client):
    """
    Test endpoint generate/goal xử lý request và trả về kết quả đúng
    """

    # Gọi API
    response = client.post("/generate/goal")
    
    # Kiểm tra kết quả
    assert response.status_code == 200


def test_create_formula(client):
    """
    Test endpoint generate/formula xử lý request và trả về kết quả đúng
    """
    # Gọi API
    response = client.post("/generate/formula")
    
    # Kiểm tra kết quả
    assert response.status_code == 200