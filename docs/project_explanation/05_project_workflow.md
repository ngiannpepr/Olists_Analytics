# 05. Luồng Công Việc Dự Án (Project Workflow)

Dự án được thực hiện bài bản qua **12 bước tiêu chuẩn** của một dự án Data Science chuyên nghiệp:

```text
1. Nhận dữ liệu (Raw Data Ingestion)
   └─► 2. Khám phá dữ liệu (Initial Data Inspection)
        └─► 3. Data Cleaning (Làm sạch & Lọc đơn hợp lệ)
             └─► 4. Data Modeling & Merging (Hợp nhất 9 bảng)
                  └─► 5. Feature Engineering (Xây dựng RFM + Extended Metrics)
                       └─► 6. SQL / Pandas Analytics (Tổng hợp chỉ số)
                            └─► 7. EDA (Exploratory Data Analysis - Phân tích khám phá)
                                 └─► 8. Visualization (Trực quan hóa đồ thị)
                                      └─► 9. Machine Learning (K-Means Clustering)
                                           └─► 10. Model Evaluation (Elbow & Silhouette)
                                                └─► 11. Customer Profiling & Storytelling
                                                     └─► 12. Strategic Action Plan & Documentation
```

### Chi tiết từng bước:

| STT | Tên Bước | Mục Đích | Đầu Vào | Đầu Ra | File Thực Hiện | Kết Quả Thu Được |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Nhận dữ liệu** | Tải 9 file CSV gốc vào môi trường local | 9 file CSV thô | Dictionary DataFrames | `src/data_loader.py` | Nạp thành công 99k+ đơn hàng vào bộ nhớ |
| 2 | **Khám phá dữ liệu** | Kiểm tra shape, null, kiểu dữ liệu | Raw DataFrames | Bảng thống kê tổng quan | `notebooks/01_...ipynb` | Nắm được cấu trúc bảng và phát hiện cạm bẫy ID |
| 3 | **Data Cleaning** | Lọc đơn giao thành công, xử lý null, ép kiểu ngày | Raw DataFrames | Clean DataFrames | `src/data_merger.py` | 96,478 đơn hàng sạch |
| 4 | **Data Modeling & Merge** | Hợp nhất 9 bảng về bảng Master đơn hàng | Clean DataFrames | `master_orders.csv` | `src/data_merger.py` | File master 99,441 dòng x 24 cột |
| 5 | **Feature Engineering** | Tính chỉ số RFM + Review + Delay + Installments | `master_orders.csv` | `customer_features.csv` | `src/feature_engineering.py` | File 93,358 đặc trưng khách hàng duy nhất |
| 6 | **Pandas Analytics** | Gom nhóm và tính toán các thống kê mô tả | `customer_features.csv` | Bảng chỉ số trung bình | `notebooks/03_...ipynb` | Hiểu phân bố Recency, Frequency, Monetary |
| 7 | **EDA** | Phân tích phân bố doanh thu, phương thức thanh toán | `master_orders.csv` | Biểu đồ phân bố | `notebooks/02_...ipynb` | Nhận diện thói quen trả góp và đánh giá sao |
| 8 | **Visualization** | Vẽ đồ thị trực quan hóa | Matplotlib / Seaborn | File ảnh PNG trong `reports/figures/` | `src/clustering_engine.py` | Đồ thị Elbow curve, PCA 2D Scatter plot |
| 9 | **Machine Learning** | Phân cụm khách hàng bằng K-Means | `customer_features.csv` | Nhãn cụm (`Cluster_0` .. `3`) | `src/clustering_engine.py` | Chia 93,358 khách hàng thành 4 cụm |
| 10 | **Evaluation** | Chọn số cụm $K$ bằng Elbow & Silhouette | Scaled Features Matrix | Chỉ số Inertia & Silhouette | `src/clustering_engine.py` | Điểm Silhouette = 0.482 ở K=4 |
| 11 | **Storytelling** | Xây dựng chân dung 4 nhóm khách hàng | `customer_clusters.csv` | 4 Personas chi tiết | `reports/olist_customer...md` | Nhận diện rõ nhóm VIP, Big Spenders, At-Risk |
| 12 | **Documentation** | Xuất báo cáo tổng hợp và tài liệu hướng dẫn | Kết quả dự án | Thư mục `docs/project_explanation/` | Toàn bộ các file `.md` | Bộ tài liệu bảo vệ dự án hoàn chỉnh |
