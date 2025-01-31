from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import validators
import random
import string
import models
import schemas
from database import SessionLocal, engine
import qrcode
from io import BytesIO
import base64

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

def generate_short_id(length: int = 6):
    """Generate a random short ID"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_qr_code(url: str) -> str:
    """Generate QR code for a URL and return as base64 string"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

@app.post("/api/shorten", response_model=schemas.URLResponse)
def create_short_url(url_request: schemas.URLBase, db: Session = Depends(get_db)):
    """Create a shortened URL"""
    if not validators.url(url_request.target_url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    # Create short URL
    short_id = url_request.custom_alias or generate_short_id()
    
    # Check if custom alias is already taken
    if url_request.custom_alias and db.query(models.URL).filter(models.URL.short_id == short_id).first():
        raise HTTPException(status_code=400, detail="Custom alias already taken")

    db_url = models.URL(
        target_url=url_request.target_url,
        short_id=short_id,
        custom_alias=url_request.custom_alias
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    # Generate QR code
    qr_code = generate_qr_code(f"http://localhost:8000/{short_id}")

    return {
        "target_url": url_request.target_url,
        "short_id": short_id,
        "qr_code": qr_code,
        "created_at": db_url.created_at
    }

@app.get("/{short_id}")
def redirect_to_url(short_id: str, request: Request, db: Session = Depends(get_db)):
    """Redirect to original URL and log the click"""
    # Get URL
    db_url = db.query(models.URL).filter(models.URL.short_id == short_id).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    # Log click
    click = models.Click(
        url_id=db_url.id,
        referrer=request.headers.get("referer"),
        user_agent=request.headers.get("user-agent")
    )
    db.add(click)
    db.commit()

    return {"url": db_url.target_url}

@app.get("/api/stats/{short_id}", response_model=schemas.URLStats)
def get_url_stats(short_id: str, db: Session = Depends(get_db)):
    """Get statistics for a shortened URL"""
    db_url = db.query(models.URL).filter(models.URL.short_id == short_id).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    clicks = db.query(models.Click).filter(models.Click.url_id == db_url.id).all()
    
    return {
        "url": db_url.target_url,
        "short_id": db_url.short_id,
        "created_at": db_url.created_at,
        "clicks": len(clicks),
        "recent_clicks": [
            {
                "clicked_at": click.clicked_at,
                "referrer": click.referrer,
                "user_agent": click.user_agent
            }
            for click in clicks[-5:]  # Last 5 clicks
        ]
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}
