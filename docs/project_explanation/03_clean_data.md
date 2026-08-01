# 03. Giải Thích Chi Tiết Quá Trình Làm Sạch Dữ Liệu (Data Cleaning)

Quá trình Data Cleaning được thực hiện cực kỳ nghiêm ngặt nhằm đảm bảo tính toàn vẹn dữ liệu (Data Integrity). Dưới đây là bảng tổng hợp đầy đủ từng bước:

| Bước Cleaning | Thực Hiện? | File Thực Hiện | Trước Khi Clean | Sau Khi Clean | Lý Do Kỹ Thuật / Business Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Lọc Đơn hàng (Order Status Filtering)** | **CÓ** | `src/data_merger.py`<br>`src/feature_engineering.py` | 99,441 đơn (bao gồm cả đơn bị hủy `canceled`, thiếu hàng `unavailable`). | Giữ lại 96,478 đơn hàng có `order_status == 'delivered'`. | Đơn bị hủy không phát sinh doanh thu thực tế và không phản ánh đúng hành vi tiêu dùng. |
| **2. Ép kiểu Datetime (Datatype Conversion)** | **CÓ** | `src/data_merger.py` | các cột `order_purchase_timestamp`, `order_delivered_customer_date` ở dạng chuỗi (String/Object). | Chuyển thành kiểu `datetime64[ns]` chuẩn Pandas. | Cho phép trừ ngày tháng để tính chỉ số Recency và Số ngày trễ đơn. |
| **3. Xử lý Trùng lặp (Duplicates Removal)** | **CÓ** | `src/data_merger.py` | Nhiều bản ghi trùng lặp khi merge bảng Payments hoặc Reviews. | Gom nhóm (`groupby('order_id')`) bằng hàm `sum()`, `mean()`, `mode()`. | Đảm bảo mỗi `order_id` chỉ xuất hiện đúng 1 dòng trong bảng Master. |
| **4. Xử lý Missing Value: Review Score** | **CÓ** | `src/feature_engineering.py` | Khách hàng không điền bài khảo sát đánh giá bị `NaN`. | Điền giá trị trung vị tổng thể `5.0` sao (`fillna(median)`). | Giữ nguyên dữ liệu khách hàng mà không làm méo lệch phân bố điểm trung bình. |
| **5. Xử lý Missing Value: Tên Danh mục** | **CÓ** | `src/data_merger.py` | Sản phẩm chưa có bản dịch tiếng Anh bị `NaN`. | Điền bằng tên gốc tiếng Bồ Đào Nha hoặc `'unknown'`. | Không làm mất thông tin danh mục sản phẩm khi phân tích thói quen mua sắm. |
| **6. Xử lý Missing Value: Thời gian giao hàng** | **CÓ** | `src/feature_engineering.py` | Một số đơn thiếu ngày giao thực tế bị `NaN`. | Điền giá trị 0.0 cho độ trễ và điền Median cho số ngày giao. | Đảm bảo các chỉ số số học không bị lỗi tính toán khi chạy Machine Learning. |
| **7. Định dạng & Chuẩn hóa (Formatting & Standardization)** | **CÓ** | `src/data_merger.py` | Cột tên danh mục bị gạch dưới `product_category_name_english`. | Chuyển về tên tiếng Anh chuẩn. | Giúp biểu đồ EDA hiển thị tên danh mục dễ đọc. |
| **8. Phát hiện & Xử lý Outlier (Outlier Treatment)** | **CÓ** | `src/clustering_engine.py` | Các cột Tiền (`monetary`), Tần suất (`frequency`) có một số giá trị cực cao làm méo phân bố. | Áp dụng biến đổi Log `np.log1p()` + `RobustScaler()`. | Giúp thuật toán K-Means không bị kéo lệch bởi các điểm dữ liệu dị biệt (Outliers). |
| **9. Quy tắc Business (Business Rules Verification)** | **CÓ** | `src/data_merger.py` | Cột `payment_value` ở một số đơn lẻ bị khuyết thiếu. | Tự động tính lại bằng `total_price + freight_value`. | Đảm bảo tổng tiền thanh toán luôn chính xác với tiền hàng thực tế. |
