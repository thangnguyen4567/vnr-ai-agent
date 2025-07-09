def test_create_goal(client):
    """
    Test endpoint generate/goal xử lý request và trả về kết quả đúng
    """
    # Mock data input
    input_data = {
        "question": "Tạo 1 mục tiêu cho phòng kinh doanh"
    }
    
    # Gọi API
    response = client.post("/generate/goal", json=input_data)
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    assert response.json()

def test_create_formula(client):
    """
    Test endpoint generate/formula xử lý request và trả về kết quả đúng
    """
    # Mock data input
    input_data = {
        "question": "Tạo công thức tính doanh số",
        "enum": "Tổng doanh số, Mục tiêu công ty, Số khách hàng mới",
        "prompt": "Công thức tính doanh số dựa trên tỉ lệ hoàn thành",
        "chat_history": [
            {"human": "Công thức phải dùng phép chia?", "bot": "Vâng, tôi sẽ đưa vào phép chia"}
        ]
    }
    
    # Gọi API
    response = client.post("/generate/formula", json=input_data)
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    assert response.json()
