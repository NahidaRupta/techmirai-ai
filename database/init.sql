-- TechMirai AI Database Setup Script
-- PostgreSQL Database

-- Create database
CREATE DATABASE techmirai_db;

-- Connect to the database
\c techmirai_db;

-- Create user (if not exists)
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'techmirai') THEN
      CREATE USER techmirai WITH PASSWORD 'techmirai123';
   END IF;
END
$do$;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE techmirai_db TO techmirai;

-- Create contact_submissions table
CREATE TABLE IF NOT EXISTS contact_submissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    timestamp TIMESTAMP,
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_email ON contact_submissions(email);
CREATE INDEX idx_status ON contact_submissions(status);
CREATE INDEX idx_created_at ON contact_submissions(created_at DESC);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_contact_submissions_updated_at BEFORE UPDATE
    ON contact_submissions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant table privileges
GRANT ALL PRIVILEGES ON TABLE contact_submissions TO techmirai;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO techmirai;

-- Insert sample data for testing (optional)
INSERT INTO contact_submissions (name, company, email, message, language, status)
VALUES 
    ('Test User', 'Test Company', 'test@example.com', 'This is a test message', 'en', 'new'),
    ('テストユーザー', 'テスト会社', 'test-ja@example.com', 'これはテストメッセージです', 'ja', 'new');

-- Verify installation
SELECT 'Database setup complete!' as status;
SELECT COUNT(*) as sample_records FROM contact_submissions;