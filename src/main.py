import uvicorn


def main():
    """Hàm chính để khởi động API"""
    print("Đang khởi động AI API...")
    uvicorn.run(
        "src.api.app:app", host="localhost", port=8000, reload=True, log_level="info"
    )


if __name__ == "__main__":
    main()
