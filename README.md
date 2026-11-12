# 🛒 Phân Khúc Khách Hàng & Phân Tích Hành Vi Người Tiêu Dùng E-Commerce (Olist Brazil)

## 📌 Tổng Quan Dự Án (Project Overview)
Dự án tập trung nghiên cứu và xây dựng hệ thống **Phân khúc khách hàng đa chiều (Customer Segmentation)** dựa trên tập dữ liệu thực tế từ nền tảng thương mại điện tử Olist (Brazil) với hơn 96.000+ khách hàng cá nhân duy nhất.

Mục tiêu chiến lược của dự án là giúp doanh nghiệp chuyển đổi từ hình thức tiếp thị đại trà ("One-Size-Fits-All") sang **Cá nhân hóa tiếp thị (Personalized Marketing)** và **Hệ thống gợi ý sản phẩm thông minh (Product Recommendation System)**, từ đó tối ưu hóa Giá trị vòng đời khách hàng (CLV - Customer Lifetime Value) và tăng tỷ lệ giữ chân (Retention Rate).

---

## 📁 Cấu Trúc Thư Mục Dự Án (Project Structure)

```text
.
├── DATA_SET/                 # Tập dữ liệu gốc từ Olist (CSV)
├── data/
│   └── processed/            # Dữ liệu khách hàng đã trích xuất đặc trưng và gán nhãn cụm
├── notebooks/                # Hệ thống Jupyter Notebook phân tích mô-đun hóa & Master Pipeline
│   ├── olist_customer_segmentation_master_pipeline.ipynb (⭐ Master Pipeline độc lập & Kiểm định mô hình)
│   ├── 01_business_understanding_and_data_merging.ipynb  # Đọc & kết nối 9 bảng dữ liệu
│   ├── 02_eda_and_data_cleaning.ipynb                   # Phân tích khám phá & làm sạch dữ liệu
│   ├── 03_feature_engineering_rfm.ipynb                 # Trích xuất đặc trưng RFM + Hành vi
│   ├── 04_clustering_model_building.ipynb               # Huấn luyện K-Means, PCA & Đánh giá cụm
│   └── 05_business_recommendations.ipynb                # Đề xuất chiến lược Marketing & Sản phẩm
├── reports/                  # Báo cáo chiến lược và biểu đồ chẩn đoán trực quan hóa
│   ├── olist_customer_segmentation_report.md            # Báo cáo tư vấn chiến lược chuyên sâu
│   ├── Bao_Cao_Phan_Tich_Phan_Khuc_Khach_Hang_Olist.docx # Báo cáo định dạng Word cho C-Level
│   └── figures/                                         # Toàn bộ biểu đồ phân tích EDA & Phân cụm
├── docs/                     # Tài liệu giải thích kỹ thuật và kiến trúc bài toán
│   └── project_explanation/  # 01_problem_analysis.md đến 09_machine_learning.md
├── src/                      # Source code Python tái sử dụng cho Production Pipeline
│   ├── __init__.py
│   ├── data_loader.py        # Module nạp dữ liệu thô
│   ├── data_merger.py        # Module làm sạch & kết hợp 9 bảng dữ liệu
│   ├── feature_engineering.py # Module tính toán RFM và biến hành vi
│   └── clustering_engine.py  # Module chuẩn hóa, K-Means, PCA và xuất kết quả
├── requirements.txt          # Danh sách thư viện phụ thuộc
└── README.md
```

---

## 🎯 Phương Pháp Luận & Điểm Nổi Bật Kỹ Thuật

1. **Khắc phục bẫy dữ liệu định danh (`customer_unique_id` vs `customer_id`):**
   - Không gom nhóm theo `customer_id` (mã đơn hàng), mà chuẩn hóa tổng hợp theo `customer_unique_id` đại diện cho từng cá nhân thực tế ngoài đời.
2. **Trích xuất đặc trưng RFM Mở rộng (Extended Behavioral Features):**
   - Kết hợp các chỉ số RFM cổ điển (*Recency, Frequency, Monetary*) với các biến hành vi đặc thù TMĐT Nam Mỹ: Điểm đánh giá dịch vụ (`review_score`), Độ trễ vận chuyển logistics (`delivery_delay`), Số đợt thanh toán trả góp (`payment_installments`) và Độ đa dạng danh mục hàng hóa (`category_diversity`).
3. **Tiền xử lý & Chuẩn hóa chống Outliers:**
   - Xử lý phân phối lệch phải (Right-Skewed) bằng hàm logarit `np.log1p()`.
   - Sử dụng `RobustScaler` (dựa trên Median và IQR) giúp mô hình K-Means ổn định, không bị kéo lệch bởi các giao dịch đột biến.
4. **Tối ưu hóa số cụm & Giảm chiều PCA:**
   - Xác định $K=4$ cụm tối ưu qua phương pháp **Elbow Method (Inertia/WCSS)** và **Silhouette Score** ($0.482$).
   - Giảm chiều không gian đặc trưng bằng PCA 2D/3D phục vụ trực quan hóa phân tách rõ nét giữa các cụm.
5. **Kiểm định thống kê & Tính ổn định của mô hình:**
   - Kiểm định **ANOVA F-test** chứng minh sự khác biệt có ý nghĩa thống kê ($p < 0.001$) giữa các cụm trên tất cả các chiều đặc trưng.
   - Thử nghiệm độ ổn định **Bootstrap Resampling** đạt chỉ số **Adjusted Rand Index (ARI) > 0.85**, chứng minh các phân khúc có tính khái quát hóa cao trên dữ liệu mới.

---

## 👥 4 Phân Khúc Khách Hàng & Chiến Lược Đề Xuất

| Cụm Khách Hàng | Tỷ Trọng | Đặc Điểm Nhận Diện | Chiến Lược Đề Xuất Cho Doanh Nghiệp |
| :--- | :---: | :--- | :--- |
| **Cluster 0: Core Budget Shoppers** | ~44% | Mua hàng giá trị trung bình-thấp, tần suất đơn lẻ, giao hàng đúng hạn, CSAT cao (4.2-4.5 sao). | **Cross-selling & Bundling:** Gợi ý combo phụ kiện/sản phẩm liên quan để nâng cao Giá trị trung bình đơn hàng (AOV). |
| **Cluster 1: Dissatisfied Shoppers** | ~18% | Điểm đánh giá rất thấp (1.0 - 1.5 sao), thời gian giao hàng có độ trễ nhẹ. | **Dịch vụ CSKH chủ động:** Khảo sát nguyên nhân, kích hoạt voucher xin lỗi và tối ưu hóa chính sách đổi trả. |
| **Cluster 2: High-Value Installment Spenders** | ~22% | Chi tiêu vượt trội (AOV cao gấp 3-4 lần), chu kỳ trả góp dài (6-10 kỳ), CSAT tốt. | **Chương trình VIP & Trả góp 0%:** Tiếp thị độc quyền đồ công nghệ/gia dụng cao cấp, liên kết ưu đãi thẻ tín dụng. |
| **Cluster 3: Severe Delay & At-Risk** | ~16% | Gặp sự cố chậm trễ logistics nghiêm trọng (>10-15 ngày), CSAT chạm đáy (1 sao), nguy cơ rời bỏ cao. | **Tái cấu trúc Logistics:** Cảnh báo đối tác vận chuyển tại các bang xa, bồi thường chậm trễ để bảo vệ uy tín thương hiệu. |

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Dự Án

### 1. Cài đặt môi trường
Yêu cầu Python phiên bản >= 3.9. Cài đặt các thư viện phụ thuộc:

```bash
pip install -r requirements.txt
```

### 2. Thực thi Data Pipeline tự động (Production CLI)
Chạy lần lượt các mô-đun trong thư mục `src/` để làm sạch dữ liệu, trích xuất đặc trưng và phân cụm:

```bash
# Bước 1: Đọc và kết hợp 9 bảng dữ liệu thô
python -m src.data_merger

# Bước 2: Tính toán bộ đặc trưng RFM + Hành vi người tiêu dùng
python -m src.feature_engineering

# Bước 3: Huấn luyện K-Means, xuất nhãn phân cụm và biểu đồ chẩn đoán
python -m src.clustering_engine
```

### 3. Nghiên cứu qua Jupyter Notebooks
Khởi động Jupyter Notebook hoặc VS Code để xem chi tiết từng giai đoạn:

```bash
jupyter notebook notebooks/olist_customer_segmentation_master_pipeline.ipynb
```
Hoặc xem lần lượt từ `notebooks/01_business_understanding_and_data_merging.ipynb` đến `notebooks/05_business_recommendations.ipynb`.

---

## 📄 Báo Cáo & Tài Liệu Đi Kèm
* Báo cáo tư vấn chiến lược toàn diện: [`reports/olist_customer_segmentation_report.md`](reports/olist_customer_segmentation_report.md)
* Báo cáo quản trị định dạng Word: [`reports/Bao_Cao_Phan_Tich_Phan_Khuc_Khach_Hang_Olist.docx`](reports/Bao_Cao_Phan_Tich_Phan_Khuc_Khach_Hang_Olist.docx)
* Thư mục tài liệu kỹ thuật chi tiết: [`docs/project_explanation/`](docs/project_explanation/)
