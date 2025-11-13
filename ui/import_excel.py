import streamlit as st
import openpyxl
from langchain_core.documents import Document
from src.vectordb.vectordb import VectorDBManager

def import_excel():
    """Màn hình import dữ liệu từ file Excel"""
    st.title("📊 Import dữ liệu từ Excel")

    st.markdown("---")

    # Upload file Excel
    uploaded_file = st.file_uploader(
        "Chọn file Excel để import",
        type=["xlsx", "xls"],
        help="Chỉ chấp nhận file Excel (.xlsx, .xls)"
    )

    if uploaded_file is not None:
        # Hiển thị thông tin file
        st.success(f"Đã chọn file: {uploaded_file.name}")

        # Đọc file Excel
        try:
            # Đọc file Excel bằng openpyxl
            workbook = openpyxl.load_workbook(uploaded_file, data_only=True)

            # Hiển thị các sheet có sẵn
            sheet_names = workbook.sheetnames
            st.subheader("📋 Các sheet trong file")

            selected_sheet = st.selectbox(
                "Chọn sheet để import:",
                sheet_names,
                key="sheet_selector"
            )

            if selected_sheet:
                # Đọc dữ liệu từ sheet được chọn
                worksheet = workbook[selected_sheet]
                data = []

                # Lấy header từ dòng đầu tiên
                headers = []
                for col in range(1, worksheet.max_column + 1):
                    header_value = worksheet.cell(row=1, column=col).value
                    headers.append(header_value if header_value is not None else f"Column_{col}")

                # Đọc dữ liệu từ các dòng còn lại
                for row in range(2, worksheet.max_row + 1):
                    row_data = {}
                    for col_idx, header in enumerate(headers):
                        cell_value = worksheet.cell(row=row, column=col_idx + 1).value
                        row_data[header] = cell_value
                    data.append(row_data)

                # Hiển thị preview dữ liệu
                st.subheader(f"👀 Preview dữ liệu từ sheet: {selected_sheet}")

                # Hiển thị thông tin tổng quan
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Số dòng", len(data))
                with col2:
                    st.metric("Số cột", len(headers))
                with col3:
                    # Đếm số ô có dữ liệu
                    data_count = sum(1 for row in data for value in row.values() if value is not None)
                    st.metric("Số ô có dữ liệu", data_count)

                # Hiển thị preview bảng (giới hạn 10 dòng đầu)
                preview_data = data[:10]
                if preview_data:
                    st.dataframe(preview_data, use_container_width=True)
                else:
                    st.info("Không có dữ liệu trong sheet này.")


                # Nút import dữ liệu
                if st.button("🚀 Import dữ liệu", type="primary", use_container_width=True):
                    # Lưu dữ liệu vào metadata
                    documents = []
                    for row in data:
                        content = row.get("content", "")
                        if 'content' in row:
                            del row['content']
                        doc = Document(page_content=content, metadata=row)
                        documents.append(doc)

                    print(documents)

                    # Tạo index_schema dựa trên các tên cột excel
                    index_schema = []
                    for header in headers:
                        index_schema.append({"name": header, "type": "text"})

                    vector_db = VectorDBManager()
                    vector_db.add_documents(documents, "training_data", index_schema)

                    # Hiển thị kết quả
                    st.success("✅ Đã import thành công!")

        except Exception as e:
            st.error(f"Lỗi khi đọc file Excel: {str(e)}")
            st.info("Vui lòng kiểm tra định dạng file Excel và thử lại.")



if __name__ == "__main__":
    import_excel()
