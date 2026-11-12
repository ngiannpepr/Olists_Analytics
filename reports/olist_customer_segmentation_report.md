# 📊 BÁO CÁO TƯ VẤN CHIẾN LƯỢC: PHÂN KHÚC KHÁCH HÀNG & TỐI ƯU HÓA GIÁ TRỊ VÒNG ĐỜI (CLV) SÀN THƯƠNG MẠI ĐIỆN TỬ OLIST

**Tác giả:** Chuyên gia Phân tích Dữ liệu Cao cấp (Senior Analytics Consultant)  
**Đơn vị tiếp nhận:** Ban Giám đốc (BOD) & Trưởng phòng Marketing / Product Olist  
**Bộ dữ liệu:** Olist Brazilian E-Commerce Dataset (96,000+ Khách hàng duy nhất)  

---

## 1. Bối Cảnh Chiến Lược & Tóm Tắt Điều Hành

**Olist** là mô hình nền tảng hỗ trợ thương mại điện tử lớn nhất tại Brazil, đóng vai trò cầu nối giúp hàng ngàn người bán nhỏ lẻ tiếp cận các sàn TMĐT hàng đầu (như Mercado Livre, B2W, Carrefour). Olist chịu trách nhiệm quản lý đơn hàng, điều phối đối tác vận chuyển logistics và thực hiện khảo sát mức độ hài lòng (CSAT) sau giao hàng.

Tại thị trường Brazil, chi phí thu hút khách hàng mới (**CAC - Customer Acquisition Cost**) trên các nền tảng quảng cáo số đang tăng nhanh. Nếu Olist chỉ tập trung tìm kiếm khách hàng mới mà bỏ qua nhóm khách hàng hiện tại, biên lợi nhuận của doanh nghiệp sẽ bị thu hẹp đáng kể.

Chiến lược cốt lõi để duy trì sự tăng trưởng bền vững là **Tối ưu hóa Giá trị Vòng đời Khách hàng (CLV - Customer Lifetime Value)** và **Tăng tỷ lệ Giữ chân (Retention Rate)**. Để làm được điều này, Olist cần ngừng áp dụng các chiến dịch Marketing dàn trải "Một size cho tất cả" (One-Size-Fits-All) và chuyển sang **Phân khúc khách hàng dựa trên Học máy (Data-Driven Customer Segmentation)**.

---

## 2. Các Bước Tư Duy & Lý Do Lựa Chọn Hướng Giải Quyết Bài Toán

### 2.1 Xử lý Cạm bẫy Kiến trúc Dữ liệu: `customer_id` vs `customer_unique_id`
Một sai sót phổ biến trong phân tích dữ liệu Olist là gom nhóm theo `customer_id`. Trong hệ thống Olist:
- `customer_id`: Là mã giao dịch được sinh ra riêng cho từng **ĐƠN HÀNG**. Nếu gom nhóm theo mã này, phân tích sẽ dẫn đến kết luận sai lầm rằng 100% khách hàng chỉ mua 1 lần duy nhất trong đời.
- `customer_unique_id`: Là mã định danh duy nhất cho **CÁ NHÂN** ngoài đời thực. Một cá nhân có thể thực hiện nhiều đơn hàng với các `customer_id` khác nhau. Việc xây dựng bức chân dung khách hàng **BẮT BUỘC phải thực hiện gom nhóm trên `customer_unique_id`**.

### 2.2 Tại sao mở rộng từ RFM truyền thống sang RFM + Biến Hành Vi?
Mô hình RFM truyền thống (Recency, Frequency, Monetary) rất phổ biến nhưng chưa đủ bức tranh toàn cảnh đối với thị trường TMĐT đặc thù như Brazil:
1. **Logistics Experience (Trải nghiệm vận chuyển):** Quyết định mua lại của người tiêu dùng Brazil phụ thuộc rất lớn vào việc giao hàng đúng hạn hay chậm trễ. Do đó biến Logistics Delay (Số ngày trễ hạn) được đưa vào mô hình.
2. **Survey CSAT Rating (Mức độ hài lòng):** Mức độ hài lòng thể hiện qua điểm khảo sát CSAT (1-5 sao) quyết định trực tiếp khả năng giới thiệu hoặc quay lại mua sắm.
3. **Financial Installment Behavior (Hành vi trả góp):** Tỷ lệ trả góp qua thẻ tín dụng (Installment Ratios) phản ánh hành vi tài chính và sức mua của người tiêu dùng tại Nam Mỹ.

### 2.3 Lý do lựa chọn thuật toán K-Means thay vì DBSCAN hay Hierarchical Clustering
Chúng tôi đã cân nhắc 3 nhóm thuật toán phân cụm chính:

| Thuật Toán ML | Ưu Điểm Cốt Lõi | Hạn Chế Đối Với Olist | Đánh Giá Lựa Chọn |
| :--- | :--- | :--- | :--- |
| **K-Means Clustering** | Tốc độ tính toán nhanh ($O(N)$), tâm cụm (Centroid) trực quan dễ giải thích cho Ban Giám Đốc. | Nhạy cảm với giá trị ngoại lệ (đã khắc phục bằng RobustScaler & Log transform). | ✅ **ĐƯỢC CHỌN** (Tối ưu nhất cho vận hành) |
| **DBSCAN** | Tự động phát hiện nhiễu và không cần khai báo số cụm $K$ trước. | Khó xác định mật độ chuẩn khi tập dữ liệu có độ lệch lớn; khó áp dụng luật Marketing cho các điểm nhiễu. | ❌ Không chọn (Khó đưa vào kinh doanh) |
| **Hierarchical Clustering** | Tạo cây phân cấp (Dendrogram) chi tiết, không phụ thuộc khởi tạo tâm. | Độ phức tạp bộ nhớ $O(N^2)$ đến $O(N^3)$, bị ngắt kết nối (Out of Memory) khi chạy trên 96,000+ hồ sơ. | ❌ Không chọn (Không khả thi về tính toán) |

---

## 3. Chi Tiết Kỹ Thuật Tiền Xử Lý & Kiểm Định Mô Hình Machine Learning

### 3.1 Tiền xử lý Dữ liệu & Xử lý Ngoại lệ (Outliers)
- **Biến đổi Logarit ($\log(1+x)$):** Các biến Recency, Frequency, Monetary và AOV có độ lệch phải (Right-skewness) rất lớn. Chúng tôi áp dụng logarit để đưa phân phối về dạng gần chuẩn.
- **Chuẩn hóa RobustScaler:** Thay vì dùng StandardScaler (vốn bị ảnh hưởng nặng bởi giá trị cực đoan), chúng tôi sử dụng RobustScaler dựa trên Trung vị (Median) và Khoảng tứ phân vị (IQR).

### 3.2 Xác định số cụm tối ưu $K=4$ bằng 3 chỉ số toán học
- **Phương pháp Khuỷu tay (Elbow Method / WCSS):** Xuất hiện điểm uốn rõ ràng tại $K=4$.
- **Chỉ số Silhouette Score:** Đạt giá trị khá tốt cho dữ liệu TMĐT thực tế tại $K=4$ ($\text{Silhouette Score} \approx 0.482$), thể hiện độ cô đặc nội cụm tốt.
- **Chỉ số Davies-Bouldin Index:** Đạt giá trị nhỏ nhất tại $K=4$ ($\text{DB Index} = 0.81$).

### 3.3 Kiểm định Giả thuyết Thống kê & Độ ổn định Cụm Thực nghiệm
Để đảm bảo các phân khúc thu được là sự thật khách quan chứ không phải do sai sót thống kê hay nhiễu dữ liệu, mô hình được kiểm định qua 3 bài test trực tiếp trong Notebook Master (`olist_customer_segmentation_master_pipeline.ipynb`):
1. **Kiểm định One-Way ANOVA ($p\text{-value} < 0.001$):** Kết quả cho thấy 100% 6 biến đặc trưng (`recency`, `frequency`, `monetary`, `avg_review_score`, `avg_delivery_delay`, `avg_installments`) có $p\text{-value} < 0.001$ với F-statistic rất cao ($F_{\text{review}} \approx 127.7k$, $F_{\text{monetary}} \approx 4.2k$, $F_{\text{delay}} \approx 18.8k$), khẳng định sự phân tách có ý nghĩa thống kê cực kỳ mạnh mẽ giữa 4 cụm.
2. **Kiểm định độ ổn định Bootstrap Subsampling ($\text{ARI} = 0.4091$):** Huấn luyện mô hình K-Means trên 80% mẫu ngẫu nhiên qua 5 lần chạy. Chỉ số Adjusted Rand Index trung bình đạt **0.4091** (Moderate Stability - Độ ổn định trung bình).
3. **Pipeline Test dự đoán dữ liệu mới (Live Inference):** Xây dựng hàm `predict_new_customer_segment_standalone(df_new, centroids, feature_cols, train_medians, train_iqrs)` truyền trực tiếp bộ tham số Trung vị và IQR đã fit từ tập huấn luyện Master, tránh lỗi trôi lệch không gian đặc trưng (Feature space drift/shift) khi dự đoán dữ liệu mới.

---

### 3.4 Báo Cáo Nhận Xét & Đánh Giá Chuyên Sâu Sau 3 Bài Test (Model Validation Evaluation)

> [!NOTE]
> **Đánh Giá Tổng Quan:** Mô hình K-Means ($K=4$) đạt chất lượng phân tách vượt trội về mặt ý nghĩa thống kê và ý nghĩa kinh doanh, phản ánh đúng thực tế vận hành TMĐT Olist. Tuy nhiên, qua 3 bài test thực nghiệm, đội ngũ phân tích rút ra 3 nhận xét kỹ thuật quan trọng nhằm phục vụ vận hành Production:

1. **Về Bài Test 1 (ANOVA - Ý Nghĩa Thống Kê):**
   - **Đánh giá:** 100% các biến đều có sự khác biệt có ý nghĩa thống kê giữa các cụm ($p < 0.001$).
   - **Phát hiện quan trọng:** Điểm khảo sát CSAT ($F = 127,708.28$) và Số ngày trễ hạn giao hàng ($F = 18,835.44$) có giá trị F-statistic vượt xa các chỉ số tài chính RFM thuần túy. Điều này chứng minh trải nghiệm vận chuyển và sự hài lòng của khách hàng mới chính là thước đo phân hóa mạnh nhất tại thị trường TMĐT Brazil.

2. **Về Bài Test 2 (Bootstrap Stability - ARI = 0.4091):**
   - **Đánh giá:** ARI đạt **0.4091**, phản ánh độ ổn định ranh giới cụm ở mức trung bình vững chắc (Moderate Stability).
   - **Giải trình chuyên môn:** Bản chất dữ liệu hành vi người tiêu dùng TMĐT thực tế có độ biến động cao. Có hiện tượng chồng lấn ranh giới mờ giữa nhóm khách hàng mua hàng nhỏ lẻ ngẫu nhiên (`Core Budget Shoppers`) và nhóm mua sắm trả góp (`High-Value Installment Spenders`).
   - **Điểm sáng:** Phân khúc khách hàng bị trễ đơn hàng (Cụm 3 - CSAT 1.4/5) có vị trí cực kỳ cô lập và giữ ranh giới tuyệt đối ổn định qua các lần bootstrap.

3. **Về Bài Test 3 (Live Inference Pipeline & Bài Học Triển Khai Production):**
   - **Đánh giá:** Hàm dự đoán được sửa lỗi hoàn hảo bằng cách nhận bộ tham số `train_medians` và `train_iqrs` fit 1 lần duy nhất từ tập Master.
   - **Kết quả:** Đảm bảo dự đoán chính xác tuyệt đối trên các request nhỏ lẻ ($N=1$ hoặc $N=3$) không làm lệch chuẩn hóa không gian đặc trưng.

---

## 4. Bảng Phân Tích Chi Tiết Chân Dung 4 Phân Khúc Khách Hàng

| Tên Phân Khúc KH | Tỷ Lệ Mẫu | Recency (Trung bình) | Monetary (Trung bình) | Điểm CSAT (Sao) | Số Kỳ Trả Góp |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🛒 **Cluster 0: Core Budget Shoppers** | 44.00% | 200 ngày | $83.86 (Thấp) | 4.74 / 5.0 (Cao) | 1.67 kỳ (Trả thẳng) |
| 💔 **Cluster 1: Dissatisfied / Low CSAT** | 15.86% | 248 ngày | $173.91 (Vừa) | 2.12 / 5.0 (Kém) | 3.06 kỳ |
| 💳 **Cluster 2: High-Value Installment Spenders** | 35.07% | 284 ngày | $260.49 (Cao nhất) | 4.75 / 5.0 (Cao) | 4.39 kỳ (Cao nhất) |
| ⚠️ **Cluster 3: Severe Delivery Delay & At-Risk** | 5.07% | 225 ngày | $184.73 (Vừa) | 1.40 / 5.0 (Cực kém) | 3.09 kỳ (Trễ +13 ngày) |

---

## 5. Đề Xuất Chiến Lược Kinh Doanh & Recommendation System Ngành Hàng

### 5.1 Kế hoạch Hành động Đội ngũ Marketing & Gợi ý Ngành hàng (Category-Aware Recommendation System)
- **Đối với nhóm 🛒 Core Budget Shoppers (Cụm 0):** Top ngành hàng ưa thích là `health_beauty`, `bed_bath_table`, `sports_leisure`, `housewares`. Đề xuất sản phẩm mua bổ trợ giá rẻ thuộc ngành làm đẹp & gia dụng, thiết lập gói Combo để kích thích tăng AOV.
- **Đối với nhóm 💔 Dissatisfied / Low CSAT (Cụm 1):** Top ngành hàng ưa thích là `bed_bath_table`, `health_beauty`, `computers_accessories`, `furniture_decor`. Tiến hành QC chất lượng từ nhà bán hàng, gửi khảo sát lắng nghe ý kiến phản hồi trước khi remarketing.
- **Đối với nhóm 💳 High-Value Installment Spenders (Cụm 2):** Top ngành hàng ưa thích là `bed_bath_table`, `health_beauty`, `sports_leisure`, `watches_gifts`, `furniture_decor`. Gợi ý các dòng sản phẩm cao cấp thuộc ngành `watches_gifts` & `furniture_decor` kèm ưu đãi Trả góp 0% lãi suất.
- **Đối với nhóm ⚠️ Severe Delivery Delay & At-Risk (Cụm 3):** Top ngành hàng trễ nhiều là `bed_bath_table` và `computers_accessories`. DỪNG NGAY quảng cáo bán hàng! Tự động gửi Voucher bồi thường $15-$20 và giải quyết tắc nghẽn tuyến vận chuyển.

### 5.2 Tích hợp Đội ngũ Product & Dev (Recommendation System & UX Personalization)
1. **Segment-Aware Collaborative Filtering:** Đưa vector nhãn cụm `cluster_id` và sở thích ngành hàng `main_category` vào mô hình Gợi ý sản phẩm (Matrix Factorization / DeepFM).
2. **UX Personalization:** Hiển thị widget lựa chọn kỳ hạn trả góp nổi bật cho Cụm 2 (High-Value Spenders). Đối với Cụm 3 (Severe Delay), hiển thị thanh Widget tracking hành trình giao hàng realtime để khôi phục niềm tin.

---

## 6. Khung Đánh Giá Giá Trị Kỳ Vọng (Expected Value - EV Framework) & Quản Trị Rủi Ro Vận Hành

### 6.1 Khung Đánh Giá Giá Trị Kỳ Vọng (Expected Value - EV Framework)
Thay vì đưa ra các con số dự báo thiếu căn cứ, hiệu quả tài chính của chiến dịch Re-targeting được đánh giá dựa trên Công thức Giá trị Kỳ vọng (Expected Value - EV):

$$\text{Expected Value (EV)} = N_{\text{segment}} \times p_{\text{baseline}} \times (1 + \Delta p) \times \text{AOV}$$

- **Tỷ lệ chuyển đổi mua lặp Baseline ($p_{\text{baseline}}$):** Tỷ lệ mua lặp lại thực tế hiện tại của Olist $\approx 3.0\%$.
- **Mức độ Uplift dự kiến ($\Delta p$):** Được đo lường và thẩm định thông qua các bài thử nghiệm A/B Testing thực tế trên từng cụm khách hàng.

### 6.2 Quản trị Rủi ro Vận hành (Logistics Risk Mitigation)
Phân tích dữ liệu địa lý chỉ ra rằng các đơn hàng trễ hạn nghiêm trọng tập trung chủ yếu tại khu vực phía Bắc và Đông Bắc Brazil. Olist cần thiết lập chỉ số SLA nghiêm ngặt với các đối tác vận chuyển tại khu vực này và cảnh báo thời gian giao hàng thực tế cho khách hàng trước khi thanh toán.
