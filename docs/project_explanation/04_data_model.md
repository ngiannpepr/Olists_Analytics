# 04. Mô Hình Dữ Liệu (Data Modeling)

## 1. Mô Hình Dữ Liệu Hiện Tại Là Gì?

Dự án áp dụng kết hợp mô hình **Star Schema (Mô hình Ngôi sao)** ở mức lưu trữ cơ sở dữ liệu quan hệ và biến đổi thành **Flat Consolidated Table (Bảng phẳng tổng hợp)** ở mức phân tích Machine Learning.

- **Star Schema gốc:**
  - **Bảng Fact Trung Tâm:** `olist_orders_dataset` liên kết với các bảng Fact phụ (`order_items`, `order_payments`, `order_reviews`).
  - **Các Bảng Dimension Xung Quanh:** `olist_customers`, `olist_products`, `product_category_name_translation`, `sellers`.

---

## 2. Khóa Chính (Primary Key) & Khóa Ngoại (Foreign Key)

```text
[olist_customers]
  - customer_id (PK)
  - customer_unique_id (Business PK)
       │
       │ (1:N) via customer_id
       ▼
[olist_orders]
  - order_id (PK)
  - customer_id (FK)
       │
       ├────── (1:N) via order_id ────► [olist_order_items] (order_id FK, product_id FK)
       ├────── (1:N) via order_id ────► [olist_order_payments] (order_id FK)
       └────── (1:N) via order_id ────► [olist_order_reviews] (order_id FK)
```

- **`customer_id` (Order-level Key):** Mã nhận diện cho từng đơn hàng (mỗi lần mua hàng tạo ra 1 `customer_id` mới).
- **`customer_unique_id` (Customer-level Key):** Mã định danh duy nhất của 1 con người thực tế.
- **`order_id`:** Mã đơn hàng duy nhất.
- **`product_id`:** Mã sản phẩm duy nhất.

---

## 3. Mối Quan Hệ Giữa Các Bảng (Relationships)

1. `olist_customers` ── (1 : N) ──► `olist_orders`: 1 Khách hàng thực tế (`customer_unique_id`) có thể đặt nhiều Đơn hàng (`customer_id`).
2. `olist_orders` ── (1 : N) ──► `olist_order_items`: 1 Đơn hàng có thể chứa nhiều Sản phẩm.
3. `olist_orders` ── (1 : N) ──► `olist_order_payments`: 1 Đơn hàng có thể thanh toán bằng nhiều đợt/phương thức.
4. `olist_orders` ── (1 : 1/N) ──► `olist_order_reviews`: 1 Đơn hàng có thể có 1 hoặc nhiều bài đánh giá khảo sát.
5. `olist_products` ── (N : 1) ──► `product_category_name_translation`: Nhiều sản phẩm thuộc 1 danh mục.
