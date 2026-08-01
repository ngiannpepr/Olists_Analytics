# 09. Chi Tiết Mô Hình Machine Learning (Machine Learning Engine)

## 1. Khai Báo Bài Toán Machine Learning
- **Loại bài toán:** Unsupervised Learning (Học không giám sát) -> **Clustering (Phân cụm)**.
- **Thuật toán:** **K-Means Clustering**.
- **Mục tiêu:** Tự động phát hiện các nhóm khách hàng ẩn trong dữ liệu mà không cần nhãn gán trước.

---

## 2. Đầu Vào & Đầu Ra (Input & Output)

- **Input (Tập đặc trưng Features):**
  1. `recency`: Số ngày từ lần mua cuối.
  2. `frequency`: Số đơn hàng đã đặt.
  3. `monetary`: Tổng số tiền đã chi tiêu.
  4. `avg_review_score`: Điểm đánh giá trung bình.
  5. `avg_delivery_delay`: Mức độ trễ đơn trung bình.
  6. `avg_installments`: Số đợt trả góp trung bình.
- **Output:** Nhãn phân cụm (`Cluster_0`, `Cluster_1`, `Cluster_2`, `Cluster_3`).

---

## 3. Các Bước Tiền Xử Lý Dữ Liệu Cho ML (ML Preprocessing)

1. **Biến đổi Log Transformation (`np.log1p`):** Do các cột $R, F, M$ bị lệch phải nặng (Right-skewed), áp dụng Log giúp đưa dữ liệu về dạng Phân bố chuẩn (Gaussian-like).
2. **Chuẩn hóa Scaler (`RobustScaler`):** Đưa tất cả các cột về cùng quy mô bằng vị trí Trung vị (Median) và Khoảng tứ phân vị (IQR), giúp thuật toán K-Means không bị ảnh hưởng bởi điểm dữ liệu cực trị.

---

## 4. Kết Quả Mô Hình & Đánh Giá Metrics
- **Số cụm tối ưu ($K$):** $K = 4$.
- **Silhouette Score:** `0.482` (Đạt mức khá tốt cho dữ liệu E-commerce thực tế, các cụm tách biệt rõ ràng).
- **Inertia (WCSS):** Giảm mạnh từ K=2 xuống K=4 và đi ngang sau K=4.
