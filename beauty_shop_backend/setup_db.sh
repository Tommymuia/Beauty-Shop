#!/bin/bash

echo "Setting up PostgreSQL database..."

# Switch to postgres user and create database and user
sudo -u postgres psql << EOF
-- Drop existing database and user if they exist
DROP DATABASE IF EXISTS beauty_shop_db;
DROP USER IF EXISTS beauty_admin;

-- Create user
CREATE USER beauty_admin WITH PASSWORD 'Group8';

-- Create database
CREATE DATABASE beauty_shop_db OWNER beauty_admin;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE beauty_shop_db TO beauty_admin;

\c beauty_shop_db

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO beauty_admin;

\q
EOF

echo "✅ Database setup complete!"
echo "Database: beauty_shop_db"
echo "User: beauty_admin"
echo "Password: Group8"
