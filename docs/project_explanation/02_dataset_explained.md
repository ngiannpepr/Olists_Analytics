# 02. Giải Thích Chi Tiết Bộ Dữ Liệu (Dataset Explained)

## 1. Tổng Quan 9 Bảng Dữ Liệu Gốc (Raw Tables)

Bộ dữ liệu Olist gồm 9 bảng CSV liên kết với nhau theo mô hình Cơ sở dữ liệu quan hệ (Relational Schema):

| Tên Bảng | Loại Bảng | Số Dòng Gốc | Nội Dung Dữ Liệu | Vai Trò Trong Dự Án |
| :--- | :--- | :--- | :--- | :--- |
| `olist_customers_dataset.csv` | **Dimension** | 99,441 | Thông tin địa lý của người mua (`customer_id`, `customer_unique_id`, city, state, zip) | Chứa **`customer_unique_id`** (ID thực của con người) - Khóa cốt lõi để gom nhóm phân cụm. |
| `olist_orders_dataset.csv` | **Fact** | 99,441 | Thông tin đơn hàng (`order_id`, `customer_id`, `order_status`, mốc thời gian mua/giao hàng) | Bảng trung tâm liên kết đơn hàng với mốc thời gian. |
| `olist_order_items_dataset.csv` | **Fact Detail** | 112,650 | Chi tiết từng món hàng trong đơn (`order_id`, `product_id`, `seller_id`, `price`, `freight_value`) | Cung cấp tiền hàng, cước ship, số lượng sản phẩm. |
| `olist_order_payments_dataset.csv` | **Fact Detail** | 103,886 | Thông tin thanh toán (`order_id`, `payment_type`, `payment_installments`, `payment_value`) | Cung cấp tổng tiền thanh toán thực tế và số đợt trả góp. |
| `olist_order_reviews_dataset.csv` | **Fact Detail** | 99,224 | Khảo sát đánh giá khách hàng (`order_id`, `review_score`, `review_comment`) | Cung cấp độ hài lòng của khách hàng (1-5 sao). |
| `olist_products_dataset.csv` | **Dimension** | 32,951 | Thông tin sản phẩm (`product_id`, `product_category_name`, kích thước, trọng lượng) | Cung cấp danh mục sản phẩm. |
| `olist_sellers_dataset.csv` | **Dimension** | 3,095 | Thông tin người bán (`seller_id`, city, state) | Thông tin đối tác bán hàng. |
| `product_category_name_translation.csv` | **Dimension** | 71 | Bảng tra cứu dịch tên danh mục từ tiếng Bồ Đào Nha sang tiếng Anh | Giúp chuẩn hóa tên danh mục sản phẩm dễ đọc. |
| `olist_geolocation_dataset.csv` | **Dimension** | 1,000,163 | Tọa độ địa lý (Lat, Lng) theo mã bưu chính (zip_code_prefix) | Dùng cho phân tích bản đồ địa lý (không dùng trực tiếp cho clustering). |

---

## 2. Phân Biệt Khái Niệm: Fact vs Dimension

- **Bảng Fact (Bảng Sự kiện/Giao dịch):** Chứa các dữ liệu phát sinh theo thời gian, có thể đo lường bằng con số (VD: Tiền hàng, phí ship, ngày giờ mua, điểm đánh giá). 
  - *Trong dự án:* `orders`, `order_items`, `order_payments`, `order_reviews`.
- **Bảng Dimension (Bảng Chiều/Thực thể):** Chứa các thông tin mô tả đối tượng (VD: Tên khách hàng, Tên sản phẩm, Tên thành phố, Danh mục).
  - *Trong dự án:* `customers`, `products`, `sellers`, `category_translation`, `geolocation`.

---

## 3. Quá Trình Biến Đổi: Tại Sao Từ 9 Bảng Gom Lại Còn 3 Bảng Processed?

### Sơ đồ chuyển đổi dữ liệu (Data Transformation Diagram):

```text
[RAW TABLES (9 Bảng)]
├── olist_orders_dataset
├── olist_order_items_dataset
├── olist_order_payments_dataset
├── olist_order_reviews_dataset
├── olist_products_dataset
├── product_category_name_translation
├── olist_customers_dataset
├── olist_sellers_dataset (Ít ảnh hưởng phân cụm khách -> Loại bỏ khỏi master)
└── olist_geolocation_dataset (Chủ yếu tọa độ bản đồ -> Loại bỏ khỏi master)
          │
          │ (1. Aggregate items, payments, reviews lên Cấp Order_ID)
          │ (2. Merge với Customers theo Customer_ID)
          ▼
[PROCESSED TABLE 1: master_orders.csv] ──► 99,441 dòng x 24 cột (Cấp Đơn hàng)
          │
          │ (3. GroupBy theo customer_unique_id để tính chỉ số RFM + Behavioral)
          ▼
[PROCESSED TABLE 2: customer_features.csv] ──► 93,358 dòng x 13 cột (Cấp Khách hàng)
          │
          │ (4. Chạy K-Means ML Clustering)
          ▼
[PROCESSED TABLE 3: customer_clusters.csv] ──► 93,358 dòng x 17 cột (Đã gán nhãn Cluster)
```

### Lý giải chi tiết từng bảng gốc:
- **Giữ nguyên & Merge:** `orders`, `order_items`, `order_payments`, `order_reviews`, `products`, `category_translation`, `customers`.
- **Không đưa vào Master Pipeline (`sellers`, `geolocation`):**
  - `sellers`: Bài toán là Phân cụm **Khách hàng** (Customer Segmentation), không phải phân cụm Người bán (Seller). Việc đưa thông tin người bán vào chỉ làm nhiễu dữ liệu.
  - `geolocation`: Chứa hơn 1 triệu dòng tọa độ kinh độ/vĩ độ trùng lặp. Thông tin địa lý cấp bang/thành phố đã có sẵn trong bảng `customers`. Loại bỏ bảng này giúp tiết kiệm bộ nhớ và tăng tốc độ xử lý mà **không làm mất bất kỳ thông tin quan trọng nào của khách hàng**.
