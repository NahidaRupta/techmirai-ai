from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uvicorn
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from email.mime.text import MIMEText    
from email.mime.multipart import MIMEMultipart
import smtplib

# Database setup
uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# Fallback to your local ThinkPad database if no environment variable is found
SQLALCHEMY_DATABASE_URL = uri or "postgresql://techmirai:techmirai123@localhost/techmirai_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class ContactSubmission(Base):
    __tablename__ = "contact_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    message = Column(Text, nullable=False)
    language = Column(String(10), default='en')
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='new')  # new, contacted, closed
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class ContactRequest(BaseModel):
    name: str
    company: Optional[str] = None
    email: EmailStr
    message: str
    language: str = 'en'
    timestamp: Optional[str] = None

class ContactResponse(BaseModel):
    success: bool
    message: str
    submission_id: Optional[int] = None

# FastAPI app
app = FastAPI(title="TechMirai AI API", version="1.0.0")

# CORS middleware
origins = [
    "https://techmirai-ai.com",
    "https://www.techmirai-ai.com",
    "https://nahidarupta.github.io",
    "http://localhost:4200", # Keeps your local ThinkPad testing working
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "info@techmirai-ai.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # Set this in environment
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "info@techmirai-ai.com")

def send_email_notification(contact: ContactRequest, submission_id: int):
    """Send email notification to admin"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"New Contact Form Submission #{submission_id}"
        msg['From'] = SMTP_USER
        msg['To'] = ADMIN_EMAIL
        
        # Create email body
        text = f"""
New Contact Form Submission

Name: {contact.name}
Company: {contact.company or 'N/A'}
Email: {contact.email}
Language: {contact.language}
Timestamp: {contact.timestamp or datetime.utcnow().isoformat()}

Message:
{contact.message}

---
TechMirai AI Contact System
        """
        
        html = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2 style="color: #0052FF;">New Contact Form Submission #{submission_id}</h2>
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <td style="padding: 10px; background: #f8f9fc; font-weight: bold;">Name:</td>
            <td style="padding: 10px;">{contact.name}</td>
        </tr>
        <tr>
            <td style="padding: 10px; background: #f8f9fc; font-weight: bold;">Company:</td>
            <td style="padding: 10px;">{contact.company or 'N/A'}</td>
        </tr>
        <tr>
            <td style="padding: 10px; background: #f8f9fc; font-weight: bold;">Email:</td>
            <td style="padding: 10px;"><a href="mailto:{contact.email}">{contact.email}</a></td>
        </tr>
        <tr>
            <td style="padding: 10px; background: #f8f9fc; font-weight: bold;">Language:</td>
            <td style="padding: 10px;">{contact.language.upper()}</td>
        </tr>
        <tr>
            <td style="padding: 10px; background: #f8f9fc; font-weight: bold;">Timestamp:</td>
            <td style="padding: 10px;">{contact.timestamp or datetime.utcnow().isoformat()}</td>
        </tr>
    </table>
    <h3 style="color: #050A1F; margin-top: 20px;">Message:</h3>
    <div style="background: #f8f9fc; padding: 15px; border-left: 3px solid #0052FF; margin-top: 10px;">
        {contact.message}
    </div>
    <hr style="margin-top: 30px; border: none; border-top: 1px solid #e2e8f0;">
    <p style="color: #64748B; font-size: 12px;">TechMirai AI Contact System</p>
</body>
</html>
        """
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        if SMTP_PASSWORD:  # Only send if SMTP is configured
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)
        else:
            print(f"Email notification would be sent for submission #{submission_id}")
            
    except Exception as e:
        print(f"Error sending email: {e}")

# API Routes
@app.get("/")
async def read_root():
    return {
        "status": "TechMirai AI API is Online",
        "docs": "/docs",
        "message": "Welcome to the backend"
    }

@app.post("/api/contact", response_model=ContactResponse)
async def submit_contact(
    contact: ContactRequest,
    db: Session = Depends(get_db)
):
    """Handle contact form submissions"""
    try:
        db_submission = ContactSubmission(
            name=contact.name,
            company=contact.company,
            email=contact.email,
            message=contact.message,
            language=contact.language,
            status='new'
        )
        
        db.add(db_submission)
        db.commit()
        db.refresh(db_submission)
        
        send_email_notification(contact, db_submission.id)
        
        return ContactResponse(
            success=True,
            message="Contact form submitted successfully",
            submission_id=db_submission.id
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/submissions")
async def get_submissions(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all contact submissions (admin endpoint)"""
    query = db.query(ContactSubmission)
    
    if status:
        query = query.filter(ContactSubmission.status == status)
    
    submissions = query.order_by(ContactSubmission.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": query.count(),
        "submissions": [
            {
                "id": s.id,
                "name": s.name,
                "company": s.company,
                "email": s.email,
                "message": s.message,
                "language": s.language,
                "status": s.status,
                "created_at": s.created_at.isoformat()
            }
            for s in submissions
        ]
    }

@app.put("/api/submissions/{submission_id}/status")
async def update_submission_status(
    submission_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update submission status (admin endpoint)"""
    submission = db.query(ContactSubmission).filter(ContactSubmission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    submission.status = status
    db.commit()
    
    return {"success": True, "message": f"Status updated to {status}"}


# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# === Keep this at the VERY BOTTOM if you have it ===
# @app.get("/{full_path:path}")
# ...

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)