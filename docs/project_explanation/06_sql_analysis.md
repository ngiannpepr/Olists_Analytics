# 06. Phân Tích Bằng SQL / Pandas Query (Data Analytics)

Mặc dù dự án chạy trên Python Pandas, các thao tác truy vấn được thiết kế tương đương với các câu lệnh **SQL Analytics** phức tạp:

## 1. Truy vấn Gom nhóm Đơn hàng theo Khách hàng (Equivalent to SQL GROUP BY)
```sql
-- SQL Equivalent: Tổng hợp hành vi mua sắm của từng khách hàng duy nhất
SELECT 
    c.customer_unique_id,
    DATEDIFF('2018-08-30', MAX(o.order_purchase_timestamp)) AS recency,
    COUNT(DISTINCT o.order_id) AS frequency,
    SUM(p.payment_value) AS monetary,
    AVG(r.review_score) AS avg_review_score,
    AVG(DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date)) AS avg_delivery_delay
FROM olist_orders o
JOIN olist_customers c ON o.customer_id = c.customer_id
LEFT JOIN olist_order_payments p ON o.order_id = p.order_id
LEFT JOIN olist_order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_unique_id;
```

---

## 2. Truy vấn Phân tích Cụm Khách hàng (Equivalent to SQL Cluster Aggregation)
```sql
-- SQL Equivalent: Thống kê chỉ số trung bình của 4 cụm khách hàng sau khi phân cụm
SELECT 
    cluster_name,
    COUNT(customer_unique_id) AS total_customers,
    ROUND(AVG(recency), 1) AS avg_recency_days,
    ROUND(AVG(frequency), 2) AS avg_orders,
    ROUND(AVG(monetary), 2) AS avg_lifetime_value,
    ROUND(AVG(avg_review_score), 2) AS avg_csat_score
FROM customer_clusters
GROUP BY cluster_name
ORDER BY avg_lifetime_value DESC;
```
