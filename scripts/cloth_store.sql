-- ============================================================
-- Commercial Cloth Store - MySQL Database Schema + Sample Data
-- Run: mysql -u root -p < scripts/cloth_store.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS cloth_store
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE cloth_store;

-- ------------------------------------------------------------
-- Drop tables (reverse dependency order) — safe for re-run
-- ------------------------------------------------------------
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS categories;
SET FOREIGN_KEY_CHECKS = 1;

-- ------------------------------------------------------------
-- categories
-- ------------------------------------------------------------
CREATE TABLE categories (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    slug        VARCHAR(120)  NOT NULL,
    description TEXT          NULL,
    is_active   TINYINT(1)    NOT NULL DEFAULT 1,
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_categories_name (name),
    UNIQUE KEY uq_categories_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- products
-- ------------------------------------------------------------
CREATE TABLE products (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    category_id     INT            NOT NULL,
    name            VARCHAR(200)   NOT NULL,
    slug            VARCHAR(220)   NOT NULL,
    description     TEXT           NULL,
    sku             VARCHAR(50)    NOT NULL,
    price           DECIMAL(10, 2) NOT NULL,
    discount_price  DECIMAL(10, 2) NULL,
    stock_quantity  INT            NOT NULL DEFAULT 0,
    size            VARCHAR(20)    NULL,
    color           VARCHAR(50)    NULL,
    brand           VARCHAR(100)   NULL,
    image_url       VARCHAR(500)   NULL,
    is_featured     TINYINT(1)     NOT NULL DEFAULT 0,
    is_active       TINYINT(1)     NOT NULL DEFAULT 1,
    created_at      DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_products_slug (slug),
    UNIQUE KEY uq_products_sku (sku),
    KEY idx_products_category_id (category_id),
    KEY idx_products_is_featured (is_featured),
    KEY idx_products_is_active (is_active),
    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id) REFERENCES categories (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- customers
-- ------------------------------------------------------------
CREATE TABLE customers (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    full_name  VARCHAR(150) NOT NULL,
    email      VARCHAR(150) NOT NULL,
    phone      VARCHAR(20)  NULL,
    address    VARCHAR(500) NULL,
    city       VARCHAR(100) NULL,
    country    VARCHAR(100) NULL,
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_customers_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- orders
-- ------------------------------------------------------------
CREATE TABLE orders (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    customer_id      INT            NOT NULL,
    order_number     VARCHAR(30)    NOT NULL,
    status           VARCHAR(30)    NOT NULL DEFAULT 'pending',
    total_amount     DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    shipping_address VARCHAR(500)   NULL,
    notes            VARCHAR(500)   NULL,
    created_at       DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_orders_order_number (order_number),
    KEY idx_orders_customer_id (customer_id),
    KEY idx_orders_status (status),
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ------------------------------------------------------------
-- order_items
-- ------------------------------------------------------------
CREATE TABLE order_items (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    order_id   INT            NOT NULL,
    product_id INT            NOT NULL,
    quantity   INT            NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal   DECIMAL(12, 2) NOT NULL,
    KEY idx_order_items_order_id (order_id),
    KEY idx_order_items_product_id (product_id),
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders (id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id) REFERENCES products (id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Sample data (optional — comment out if not needed)
-- ============================================================

INSERT INTO categories (name, slug, description, is_active) VALUES
('Men',   'men',   'Men''s clothing',       1),
('Women', 'women', 'Women''s clothing',     1),
('Kids',  'kids',  'Children''s clothing',  1);

INSERT INTO products (
    category_id, name, slug, sku, price, discount_price,
    stock_quantity, size, color, brand, is_featured, is_active
) VALUES
(1, 'Classic Cotton T-Shirt', 'men-cotton-tshirt', 'MEN-TS-001',
 29.99, 24.99, 100, 'L',  'Navy',  'UrbanWear',   1, 1),
(1, 'Slim Fit Denim Jeans',   'men-slim-jeans',    'MEN-JN-002',
 59.99, NULL,  50,  '32', 'Blue',  'DenimCo',     0, 1),
(2, 'Floral Summer Dress',    'women-floral-dress','WOM-DR-001',
 79.99, 64.99, 40,  'M',  'Floral','BloomStyle',  1, 1),
(3, 'Kids Hoodie',            'kids-hoodie',       'KID-HD-001',
 34.99, NULL,  60,  'S',  'Red',   'LittleStars', 0, 1);

INSERT INTO customers (full_name, email, phone, address, city, country) VALUES
('Jane Doe',   'jane@example.com',  '+1-555-0101', '123 Main St',   'New York',    'USA'),
('John Smith', 'john@example.com',  '+1-555-0102', '456 Oak Ave',   'Los Angeles', 'USA');

INSERT INTO orders (customer_id, order_number, status, total_amount, shipping_address) VALUES
(1, 'ORD-SAMPLE000001', 'confirmed', 49.98, '123 Main St, New York, USA');

INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES
(1, 1, 2, 24.99, 49.98);

-- ============================================================
-- Optional: create dedicated app user (uncomment and edit)
-- ============================================================
-- CREATE USER IF NOT EXISTS 'cloth_user'@'localhost' IDENTIFIED BY 'your_secure_password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON cloth_store.* TO 'cloth_user'@'localhost';
-- FLUSH PRIVILEGES;
