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
import os
from dotenv import load_dotenv

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
    "https://NahidaRupta.github.io",
    "http://localhost:3000", # Keeps your local ThinkPad testing working
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

load_dotenv()
## --- Email Configuration ---
# This part stays! It reads the variables you set in Render's "Environment" tab.
# --- Email Configuration ---
# These are global variables. They load once when the app starts.
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "nahida.rahaman37@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "") 
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "nahida.rahaman37@gmail.com")

def send_email_notification(contact: ContactRequest, submission_id: int):
    """Send email notification to admin"""
    
    # 1. Check if we have the password. If not, we can't send.
    if not SMTP_PASSWORD:
        print(f"⚠️ SMTP_PASSWORD not set. Skipping email for submission #{submission_id}")
        return

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🚀 New TechMirai Lead: {contact.name}"
        msg['From'] = SMTP_USER 
        msg['To'] = ADMIN_EMAIL 
        
        # Plain text version
        text = f"New Lead #{submission_id}\nName: {contact.name}\nEmail: {contact.email}\nMessage: {contact.message}"
        
        # Professional HTML version
        html = f"""
        <html>
            <body style="font-family: sans-serif; color: #333;">
                <h2 style="color: #0052FF;">New Contact Form Submission</h2>
                <p><strong>Submission ID:</strong> {submission_id}</p>
                <hr>
                <p><strong>Name:</strong> {contact.name}</p>
                <p><strong>Company:</strong> {contact.company or 'N/A'}</p>
                <p><strong>Email:</strong> {contact.email}</p>
                <p><strong>Message:</strong></p>
                <div style="background: #f4f4f4; padding: 15px; border-radius: 5px;">{contact.message}</div>
            </body>
        </html>
        """
        
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        
        # 2. Connect and Send using the global variables
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"✅ Email notification sent for submission #{submission_id}")
            
    except Exception as e:
        # This will show up in your Render Logs if Google blocks the login
        print(f"❌ SMTP Error: {e}")

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