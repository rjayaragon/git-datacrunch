CREATE TABLE dim_customers
(
customer_id SERIAL PRIMARY KEY,
name TEXT,
email TEXT,
location TEXT,
signup_date DATE
);

CREATE TABLE dim_products
(
product_id SERIAL PRIMARY KEY,
product_name TEXT,
category TEXT,
product_price NUMERIC(10,2)
);

CREATE TABLE fact_sales
(
order_id SERIAL PRIMARY KEY,
customer_id INT REFERENCES dim_customers(customer_id),
product_id INT REFERENCES dim_products(product_id),
order_date DATE,
quantity_sold INT,
revenue NUMERIC(10,2)
);


