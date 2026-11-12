# 08. Giải Thích Các Biểu Đồ (Dashboard & Chart Explanation)

Dự án xuất ra 2 biểu đồ trực quan hóa cốt lõi lưu tại `reports/figures/`:

## 1. Biểu đồ 1: K-Means Evaluation Metrics (`kmeans_evaluation_metrics.png`)
- **Loại biểu đồ:** Dual-Axis Line Chart (Biểu đồ đường 2 trục tung).
- **Mục đích Business:** Xác định số lượng cụm khách hàng tối ưu nhất ($K$) để chia.
- **Giải thích:**
  - *Trục trái (Đường xanh - Inertia/WCSS):* Thể hiện tổng bình phương khoảng cách trong cụm. Số cụm càng tăng thì Inertia càng giảm. Tại $K=4$, đường cong bắt đầu đi ngang (Điểm gấp khúc Elbow).
  - *Trục phải (Đường đỏ - Silhouette Score):* Thể hiện độ phân tách giữa các cụm. Đạt đỉnh cao tại $K=4$ ($	ext{Silhouette Score} pprox 0.48$), chứng tỏ 4 cụm là cấu trúc phân tách rõ ràng nhất.

---

## 2. Biểu đồ 2: Cluster PCA 2D Scatter Plot (`cluster_pca_scatter.png`)
- **Loại biểu đồ:** 2D Scatter Plot với phân ma trận PCA (Principal Component Analysis).
- **Mục đích Business:** Trực quan hóa vị trí của 93,358 khách hàng trên mặt phẳng 2D xem các cụm có bị đè lên nhau không.
- **Insight:** 
  - 4 màu sắc phân tách thành 4 vùng không gian rõ rệt.
  - Cụm `Cluster_0` (`Core Budget Shoppers`) chiếm tỷ trọng lớn (~44%) ở mức chi tiêu phổ thông.
  - Cụm `Cluster_1` (`Dissatisfied`) & Cụm `Cluster_3` (`Severe Delay & At-Risk`) phân tách rõ nét do điểm CSAT thấp và số ngày trễ đơn cao.
  - Cụm `Cluster_2` (`High-Value Installment Spenders`) nằm tách biệt ở phân vùng giá trị đơn hàng cao và kỳ trả góp lớn.
