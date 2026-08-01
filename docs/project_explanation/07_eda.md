# 07. Phân Tích Khám Phá Dữ Liệu (Exploratory Data Analysis - EDA)

## Các Phát Hiện EDA Quan Trọng:

### 1. Phân bố Trạng thái Đơn hàng (Order Status)
- Hơn **97% đơn hàng** ở trạng thái `delivered` (Giao hàng thành công).
- Tỷ lệ đơn hủy (`canceled`) chiếm chưa tới 0.6%, chủ yếu do hết hàng hoặc người bán không xác nhận.

### 2. Phân bố Phương thức Thanh toán (Payment Types)
- **Thẻ tín dụng (Credit Card):** Chiếm ưu thế tuyệt đối (**73.9%** tổng giao dịch).
- **Boleto (Hóa đơn ngân hàng Brazil):** Chiếm **19.0%** (Dành cho khách không dùng thẻ).
- **Voucher & Debit Card:** Chiếm phần nhỏ còn lại (~7.1%).

### 3. Hành vi Trả góp (Installments)
- Hơn **52% khách hàng thanh toán bằng thẻ tín dụng chọn trả góp** (từ 2 đến 10 đợt).
- Các đơn hàng giá trị cao (trên 300 BRL) có tỷ lệ chọn trả góp 6-10 tháng lên tới **80%**.

### 4. Mức Độ Hài Lòng (Review Score)
- Điểm đánh giá trung bình toàn sàn là **4.08 / 5.0**.
- **77% đơn hàng** nhận được đánh giá 4 hoặc 5 sao.
- Khoảng **14% đơn hàng** nhận đánh giá 1 sao. **Nguyên nhân cốt lõi dẫn đến 1 sao là do Đơn hàng giao chậm quá ngày hẹn (Delivery Delay)** chứ không phải do chất lượng sản phẩm.
