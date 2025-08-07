from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
import json

@tool("get_policy",return_direct=True)
def get_policy(config: RunnableConfig = None) -> str:
    """Tra chính sách của công ty , hỗ trợ tra cứu, giải đáp thắc mắc, hướng dẫn sử dụng hệ thống"""

    data = [
        {
            "context": "Công ty đang áp dụng chính sách phúc lợi dành cho các trường hợp hiếu hỉ của nhân viên bao gồm: kết hôn, sinh con, và có tang sự trong gia đình như cha/mẹ ruột, vợ/chồng hoặc con qua đời. Mức hỗ trợ sẽ khác nhau tuỳ từng trường hợp và được cập nhật theo từng năm. Chính sách này nhằm hỗ trợ tinh thần và tài chính cho nhân viên trong những sự kiện quan trọng của cuộc sống. Để biết chính xác mức hỗ trợ, quy trình nhận trợ cấp, nhân viên có thể tra cứu văn bản 'Chính sách phúc lợi nội bộ' hoặc liên hệ phòng Nhân sự."
        },
        {
            "context": "Khi đăng nhập vào hệ thống HRM và gặp thông báo 'Tài khoản chưa được kích hoạt', có thể do một trong các nguyên nhân sau: (1) Nhân viên mới chưa được HR tạo và cấp quyền truy cập. (2) Hợp đồng lao động chưa có hiệu lực hoặc chưa hoàn tất thủ tục onboard. (3) Nhân viên đang trong giai đoạn nghỉ việc, nghỉ thai sản, hoặc tạm hoãn hợp đồng. (4) Tài khoản đã bị vô hiệu hóa do nghỉ việc hoặc lý do quản trị hệ thống. Để xử lý, nhân viên nên liên hệ trực tiếp bộ phận Nhân sự để được kiểm tra trạng thái tài khoản và hướng dẫn kích hoạt nếu cần."
        },
        {
            "context": "Thông tin trong hợp đồng lao động (bao gồm lương, chức danh, thời hạn hợp đồng, hoặc địa điểm làm việc) không thể được thay đổi trực tiếp bởi nhân viên. Nếu có nhu cầu điều chỉnh, nhân viên cần gửi đề xuất đến quản lý trực tiếp hoặc phòng Nhân sự. Sau khi được xét duyệt, HR sẽ thực hiện quy trình điều chỉnh, có thể bao gồm việc lập phụ lục hợp đồng hoặc tạo hợp đồng mới. Tất cả các thay đổi sẽ được lưu trữ và cập nhật trên hệ thống HRM sau khi hoàn tất. Quy trình này đảm bảo tính pháp lý và minh bạch cho cả người lao động và công ty."
        },
        {
            "context": "Việc kết xuất hợp đồng lao động của nhân viên có thể được thực hiện thông qua hệ thống HRM bởi những người dùng có quyền thích hợp (thường là HR hoặc quản lý). Người dùng cần truy cập vào mục 'Hợp đồng lao động', chọn tên nhân viên cần thao tác, sau đó sử dụng các chức năng như 'Xem hợp đồng', 'Tải hợp đồng' hoặc 'In hợp đồng'. File hợp đồng có thể ở định dạng PDF và đã bao gồm đầy đủ thông tin pháp lý. Trong trường hợp người dùng không có quyền truy cập chức năng này, cần liên hệ phòng Nhân sự hoặc quản trị hệ thống để được hỗ trợ cấp quyền hoặc thực hiện thay."
        },
        {
            "context": "Chính sách nghỉ phép của công ty được quy định cụ thể như sau: (1) Mỗi nhân viên được cấp 12 ngày nghỉ phép có lương mỗi năm. (2) Nhân viên cần đăng ký nghỉ phép trước ít nhất 3 ngày làm việc thông qua hệ thống HRM. (3) Yêu cầu nghỉ phép phải được quản lý trực tiếp phê duyệt. (4) Trong trường hợp khẩn cấp, nhân viên cần thông báo cho quản lý càng sớm càng tốt và hoàn thành thủ tục đăng ký nghỉ phép ngay khi có thể. (5) Số ngày nghỉ phép chưa sử dụng có thể được chuyển sang năm sau nhưng không quá 5 ngày. Để đăng ký nghỉ phép, nhân viên truy cập vào mục 'Đăng ký nghỉ phép' trên hệ thống, chọn ngày bắt đầu, ngày kết thúc và điền lý do nghỉ."
        },
        {
            "context": "Chính sách ngày phép năm của công ty hiện tại: (1) Nhân viên làm việc đủ 12 tháng được hưởng 12 ngày phép năm có lương. (2) Nhân viên mới làm việc chưa đủ 12 tháng được tính phép theo tỷ lệ 1 ngày/tháng. (3) Ngày phép được cập nhật vào đầu mỗi năm dương lịch. (4) Trường hợp nghỉ phép nhiều ngày liên tục (từ 5 ngày trở lên) cần đăng ký trước ít nhất 2 tuần. (5) Nhân viên có thể kiểm tra số ngày phép còn lại trong năm thông qua mục 'Thông tin nghỉ phép' trên hệ thống HRM. (6) Ngày phép được sử dụng linh hoạt theo nhu cầu cá nhân và phù hợp với kế hoạch công việc của phòng ban. (7) Ngày phép không sử dụng hết trong năm hiện tại sẽ được thanh toán theo quy định của công ty hoặc chuyển tối đa 5 ngày sang năm sau, tùy theo chính sách từng thời điểm."
        },
        {
            "context": "Quy trình đăng ký tăng ca trên hệ thống HRM như sau: (1) Nhân viên cần truy cập vào mục 'Đăng ký tăng ca' trên hệ thống HRM. (2) Điền đầy đủ thông tin bao gồm ngày làm việc, giờ bắt đầu, giờ kết thúc và lý do tăng ca. (3) Chọn hình thức thanh toán tăng ca (tiền mặt hoặc nghỉ bù). (4) Gửi yêu cầu để quản lý trực tiếp phê duyệt. (5) Theo dõi trạng thái phê duyệt trên hệ thống. Lưu ý: Việc đăng ký tăng ca cần được thực hiện và phê duyệt trước khi thực hiện tăng ca, trừ trường hợp khẩn cấp cần được giải trình cụ thể. Thời gian tăng ca được tính theo quy định của Bộ luật Lao động với các mức phụ cấp khác nhau tùy thuộc vào thời điểm tăng ca (ngày thường, cuối tuần, ngày lễ)."
        },
        {
            "context": "Hướng dẫn sử dụng hệ thống HRM: (1) Đăng nhập: Truy cập vào trang web của hệ thống HRM bằng tên đăng nhập và mật khẩu được cung cấp. (2) Trang chủ: Hiển thị thông tin tổng quan về dữ liệu cá nhân, thông báo mới và các chức năng chính. (3) Menu chính: Bao gồm các mục Thông tin cá nhân, Chấm công, Đăng ký nghỉ phép, Đăng ký tăng ca, Lương & Phúc lợi, và Báo cáo. (4) Thông tin cá nhân: Xem và cập nhật thông tin cá nhân như số điện thoại, địa chỉ, người liên hệ khẩn cấp. (5) Chấm công: Xem lịch sử chấm công, báo cáo điểm danh và yêu cầu điều chỉnh (nếu có sai sót). (6) Đăng ký nghỉ phép/tăng ca: Tạo yêu cầu mới, kiểm tra số ngày phép còn lại, theo dõi trạng thái yêu cầu. (7) Lương & Phúc lợi: Xem thông tin lương, phiếu lương và các phúc lợi hiện tại. (8) Báo cáo: Truy cập các báo cáo liên quan đến thông tin cá nhân. (9) Trợ giúp: Liên hệ với bộ phận IT hoặc HR nếu gặp vấn đề kỹ thuật hoặc có thắc mắc."
        }
    ]

    return json.dumps(data)