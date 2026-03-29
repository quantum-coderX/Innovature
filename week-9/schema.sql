-- Week 9 E-commerce Backend Schema (PostgreSQL)

-- Drop tables if they exist (for development/testing)
DROP TABLE IF EXISTS cart_item CASCADE;
DROP TABLE IF EXISTS cart CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;

-- Category table
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- User table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) DEFAULT '',
    role INTEGER NOT NULL DEFAULT 2,
    phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (role IN (1, 2))
);

-- Product table
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    sku VARCHAR(100) UNIQUE,
    seller_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES category(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (stock >= 0)
);

-- Cart table
CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (status IN ('open', 'checkout', 'completed', 'abandoned'))
);

-- CartItem table
CREATE TABLE cart_item (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES cart(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES product(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (quantity > 0)
);

-- Create indexes for better query performance
CREATE INDEX idx_product_name ON product(name);
CREATE INDEX idx_product_price ON product(price);
CREATE INDEX idx_product_category ON product(category_id);
CREATE INDEX idx_product_sku ON product(sku);
CREATE INDEX idx_product_seller ON product(seller_id);
CREATE INDEX idx_user_email ON "user"(email);
CREATE INDEX idx_cart_user ON cart(user_id);
CREATE INDEX idx_cart_status ON cart(status);
CREATE INDEX idx_cart_item_cart ON cart_item(cart_id);
CREATE INDEX idx_cart_item_product ON cart_item(product_id);

-- Sample data
INSERT INTO category (name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Clothing', 'Apparel and fashion items'),
('Books', 'Physical and digital books'),
('Home & Garden', 'Home improvement and garden items'),
('Sports', 'Sports equipment and outdoor gear');

INSERT INTO "user" (name, email, role, phone, address, is_active) VALUES
('Sam Seller', 'seller1@example.com', 1, '555-0101', '12 Market St', true),
('Nina Seller', 'seller2@example.com', 1, '555-0102', '44 Commerce Ave', true),
('Ben Buyer', 'buyer1@example.com', 2, '555-0201', '123 Main St', true),
('Lia Buyer', 'buyer2@example.com', 2, '555-0202', '456 Oak Ave', true);

INSERT INTO product (name, description, price, stock, sku, seller_id, category_id) VALUES
('Laptop', 'High-performance laptop with 16GB RAM', 999.99, 50, 'LAPTOP-001', 1, 1),
('Smartphone', '5G smartphone with 128GB storage', 599.99, 150, 'PHONE-001', 1, 1),
('Headphones', 'Noise-cancelling wireless headphones', 199.99, 200, 'HEAD-001', 1, 1),
('T-Shirt', 'Cotton t-shirt in various colors', 29.99, 500, 'TSHIRT-001', 2, 2),
('Jeans', 'Durable denim jeans', 79.99, 300, 'JEANS-001', 2, 2),
('Python Book', 'Complete guide to Python programming', 49.99, 100, 'BOOK-001', 2, 3),
('Garden Tools Set', 'Set of 5 garden tools', 89.99, 75, 'GARDEN-001', 2, 4),
('Running Shoes', 'Professional running shoes', 119.99, 200, 'SHOES-001', 2, 5),
('Yoga Mat', 'Non-slip yoga exercise mat', 39.99, 150, 'YOGA-001', 2, 5),
('Coffee Maker', 'Programmable coffee maker', 149.99, 120, 'COFFEE-001', 1, 4);
