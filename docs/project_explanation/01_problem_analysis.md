# 01. Phân Tích Bài Toán Doanh Nghiệp & Mục Tiêu Dự Án (Problem Statement & Business Objectives)

## 1. Bối Cảnh Nghiên Cứu & Bài Toán Doanh Nghiệp (Problem Statement)
> **Bối cảnh:**
> Bộ dữ liệu được cung cấp bởi Olist, một tập đoàn thương mại điện tử lớn nhất ở Brazil. Olist kết nối các doanh nghiệp vừa và nhỏ từ khắp Brazil với các kênh bán hàng thông qua một hợp đồng duy nhất. Những người bán hàng này có thể bán sản phẩm của mình thông qua cửa hàng của Olist và vận chuyển trực tiếp đến khách hàng bằng cách sử dụng các đối tác hậu cần của Olist.
> Sau khi khách hàng mua sản phẩm từ Olist Store, người bán sẽ nhận được thông báo thực hiện đơn hàng đó. Sau khi khách hàng nhận được sản phẩm hoặc đến hạn giao hàng dự kiến, khách hàng sẽ nhận được một bản khảo sát về mức độ hài lòng qua email, nơi họ có thể đưa ra ghi chú về trải nghiệm mua hàng và viết nhận xét đánh giá.
>
> **Mục tiêu Doanh nghiệp (Business Goal):**
> Nghiên cứu và xây dựng hệ thống phân khúc khách hàng đa chiều cho Olist, đề xuất danh mục sản phẩm và chiến lược tiếp cận phù hợp cho từng cụm khách hàng. Kết quả phân tích cung cấp cho Growth Marketing Team để tối ưu hóa chiến dịch quảng cáo nhắm mục tiêu (Targeted Ads) và Product/Engineering Team để phát triển hệ thống gợi ý sản phẩm cá nhân hóa (Recommendation Systems).

---

## 2. Phân Tích Chi Tiết Bài Toán Kinh Doanh

### Bối cảnh bài toán:
Olist là một sàn thương mại điện tử kết nối người bán nhỏ lẻ (Sellers) và người mua (Customers). Do quy mô lớn (hàng trăm nghìn khách hàng), Olist gặp vấn đề **không thể tiếp thị đại trà** (không thể gửi cùng 1 tin nhắn quảng cáo hay áp dụng cùng 1 chính sách cho tất cả mọi người).

### Mục tiêu Kinh doanh (Business Goals):
1. **Marketing Team:** Cần chia khách hàng thành các nhóm (segments) có chung hành vi để chạy quảng cáo nhắm mục tiêu (Ads Targeting), giảm chi phí quảng cáo và tăng tỷ lệ mua lại (Retention Rate).
2. **Product / Dev Team:** Cần hiểu nhu cầu mua sắm và thói quen thanh toán của từng nhóm để thiết kế hệ thống gợi ý sản phẩm (Recommendation System) hiển thị trên App/Web.

### Các câu hỏi Business cần trả lời:
- Olist hiện có bao nhiêu nhóm khách hàng cốt lõi?
- Đặc điểm của từng nhóm là gì (Mua bao nhiêu tiền? Mua bao nhiêu lần? Có hài lòng không? Giao hàng có trễ không?)?
- Làm sao để nhận diện được nhóm khách hàng mang lại nhiều lợi nhuận nhất (VIP) và nhóm khách hàng có nguy cơ rời bỏ (At-Risk)?
- Chiến lược tiếp thị (Ads) và gợi ý sản phẩm cho từng nhóm nên thực hiện như thế nào?

---

## 3. Phân Loại Đầu Ra Nghiên Cứu (Project Deliverables)

### 🎯 Mục Tiêu Cốt Lõi (Core Deliverables):
1. **Khám phá và Làm sạch Dữ liệu (EDA & Data Cleaning):** Xử lý null, trùng lặp, ép kiểu ngày tháng, lọc đơn hàng hợp lệ.
2. **Phân khúc Khách hàng bằng ML (K-Means Clustering):**
   - Xây dựng chỉ số RFM (Recency, Frequency, Monetary).
   - Chọn số cụm $K$ tối ưu (dùng Elbow Method / Silhouette Score).
   - Phân cụm và trực quan hóa kết quả.
3. **Phân tích Chân dung Cụm (Cluster Profiling):** Mô tả đặc điểm trung bình của từng nhóm khách hàng.
4. **Đề xuất Chiến lược (Business Recommendations):** Khuyến nghị cụ thể cho team Marketing và team Dev.
5. **Đóng gói sản phẩm:** Hệ thống Notebooks phân tích, Báo cáo chuyên sâu (.pdf/.md) và Pipeline mô-đun hóa tái sử dụng.

### 🚀 Tính Năng Mở Rộng & Chuyên Sâu (Advanced Implementation):
- **RFM Mở rộng (Extended Features):** Không chỉ tính RFM mà tính thêm điểm đánh giá trung bình (`review_score`), độ trễ giao hàng (`delivery_delay`), đợt trả góp (`installments`), độ đa dạng danh mục (`category_diversity`).
- **Data Pipeline Modular (`src/`):** Viết code dạng module hóa Python chuyên nghiệp để tái sử dụng thay vì chỉ viết code phẳng trong notebook.
- **Trực quan hóa nâng cao:** Vẽ đồ thị PCA 2D/3D phân tách các cụm.
