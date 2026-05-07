# TechMirai AI - Full Stack Application

Complete full-stack website for TechMirai AI with backend API, database, and responsive frontend.

## 📁 Project Structure

```
techmirai-fullstack/
├── frontend/           # Frontend HTML, CSS, JavaScript
│   ├── index.html     # Main website (Arial font, mobile-optimized)
│   └── app.js         # JavaScript for forms, language switching
├── backend/           # FastAPI backend
│   ├── main.py        # FastAPI application
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── database/          # Database setup
│   └── init.sql       # PostgreSQL initialization script
├── nginx/             # Nginx configuration
│   └── nginx.conf
└── docker-compose.yml # Docker deployment configuration
```

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Domain name pointed to your server (optional, for production)

### Step 1: Clone/Download Files
```bash
cd techmirai-fullstack
```

### Step 2: Configure Environment
```bash
cd backend
cp .env.example .env
# Edit .env with your actual email credentials
nano .env
```

### Step 3: Start Everything
```bash
cd ..
docker-compose up -d
```

### Step 4: Access the Website
- Website: http://localhost
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔧 Manual Setup (Without Docker)

### Step 1: Setup Database

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql -f database/init.sql
```

### Step 2: Setup Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env

# Run the server
python main.py
```

Backend will run on: http://localhost:8000

### Step 3: Setup Frontend

For development, you can use Python's built-in server:

```bash
cd frontend
python3 -m http.server 3000
```

Frontend will run on: http://localhost:3000

## 📧 Email Configuration

To enable email notifications for contact form submissions:

1. Get an App Password from Gmail:
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Generate App Password

2. Update `.env` file:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
ADMIN_EMAIL=info@techmirai-ai.com
```

## 🗄️ Database Schema

### contact_submissions table
```sql
- id: Serial (Primary Key)
- name: VARCHAR(255)
- company: VARCHAR(255)
- email: VARCHAR(255)
- message: TEXT
- language: VARCHAR(10)
- status: VARCHAR(50) - 'new', 'contacted', 'closed'
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

## 📡 API Endpoints

### Public Endpoints
- `POST /api/contact` - Submit contact form
- `GET /health` - Health check

### Admin Endpoints
- `GET /api/submissions` - Get all submissions
  - Query params: `skip`, `limit`, `status`
- `PUT /api/submissions/{id}/status` - Update submission status

### Example API Call
```javascript
fetch('/api/contact', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        name: 'John Doe',
        company: 'ABC Corp',
        email: 'john@example.com',
        message: 'Interested in AI solutions',
        language: 'en'
    })
})
```

## 🌐 Production Deployment

### Option 1: Docker Deployment

1. **Setup Domain**
```bash
# Point your domain (techmirai-ai.com) to server IP
```

2. **Configure SSL (Let's Encrypt)**
```bash
# Install certbot
sudo apt-get install certbot

# Get SSL certificate
sudo certbot certonly --standalone -d techmirai-ai.com -d www.techmirai-ai.com

# Copy certificates to nginx/ssl/
sudo cp /etc/letsencrypt/live/techmirai-ai.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/techmirai-ai.com/privkey.pem nginx/ssl/key.pem
```

3. **Update docker-compose.yml**
```yaml
# Uncomment nginx service ports
ports:
  - "80:80"
  - "443:443"
```

4. **Deploy**
```bash
docker-compose up -d
```

### Option 2: Manual Deployment

1. **Setup Nginx**
```bash
sudo apt-get install nginx
sudo cp nginx/nginx.conf /etc/nginx/sites-available/techmirai
sudo ln -s /etc/nginx/sites-available/techmirai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

2. **Setup Systemd Service**
```bash
# Create service file
sudo nano /etc/systemd/system/techmirai-backend.service
```

```ini
[Unit]
Description=TechMirai Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/techmirai/backend
Environment="PATH=/var/www/techmirai/backend/venv/bin"
ExecStart=/var/www/techmirai/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable techmirai-backend
sudo systemctl start techmirai-backend
```

## 🔒 Security Checklist

- [ ] Change database password in production
- [ ] Set strong SECRET_KEY in .env
- [ ] Configure CORS for specific domains only
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set up firewall (ufw/iptables)
- [ ] Regular database backups
- [ ] Keep dependencies updated
- [ ] Add rate limiting to API endpoints
- [ ] Enable CSRF protection for forms

## 📊 Monitoring

### Check Backend Status
```bash
# Docker
docker logs techmirai_backend

# Manual
tail -f /var/log/techmirai/backend.log
```

### Check Database
```bash
# Docker
docker exec -it techmirai_db psql -U techmirai -d techmirai_db

# Manual
sudo -u postgres psql techmirai_db
```

### View Submissions
```sql
SELECT * FROM contact_submissions ORDER BY created_at DESC LIMIT 10;
```

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check connection string in .env
DATABASE_URL=postgresql://user:password@localhost/database
```

### Email Not Sending
```bash
# Verify SMTP settings in .env
# Check app password is correct
# Test with: python -m smtplib
```

### CORS Errors
```python
# In backend/main.py, update CORS settings:
allow_origins=["https://techmirai-ai.com"]
```

## 📱 Mobile Optimization

The frontend is fully responsive with:
- Mobile-first design with Arial font
- Hamburger menu for mobile
- Touch-friendly buttons (44px minimum)
- Optimized for phones (320px+) and tablets
- Fast loading with minimal CSS/JS

## 🔄 Updates & Maintenance

### Update Backend
```bash
cd backend
pip install -r requirements.txt --upgrade
sudo systemctl restart techmirai-backend
```

### Database Migrations
```bash
# Backup first
pg_dump techmirai_db > backup.sql

# Run migrations
psql techmirai_db < migration.sql
```

### Update Frontend
Simply replace files in `frontend/` directory and restart nginx.

## 📝 License

Copyright © 2026 TechMirai AI. All rights reserved.

## 🤝 Support

For technical support:
- Email: info@techmirai-ai.com
- Location: Wako-shi, Saitama, Japan

---

**Built with:**
- Frontend: HTML5, CSS3 (Arial font), Vanilla JavaScript
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Deployment: Docker, Nginx
- Email: SMTP (Gmail compatible)
