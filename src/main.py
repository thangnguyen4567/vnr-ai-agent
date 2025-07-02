import uvicorn


def main():
    """Hàm chính để khởi động API"""

    print("\nĐang khởi động AI API...")
    uvicorn.run(
        "src.api.app:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )


if __name__ == "__main__":
    main()
