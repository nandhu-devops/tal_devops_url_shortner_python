# URL Shortener Service

A modern URL shortening service built with Python FastAPI backend and simple HTML/JavaScript frontend. This application demonstrates modern web development practices and serves as a platform for DevOps implementation exercises.

## Application Components

### Backend (FastAPI)
- RESTful API for URL shortening
- PostgreSQL database integration
- Rate limiting
- URL validation
- Analytics tracking

### Frontend
- Simple and responsive design
- URL submission form
- QR code generation for shortened URLs
- Basic analytics display

### Features
- URL shortening with custom alias support
- QR code generation
- Click tracking and analytics
- Rate limiting
- API documentation (Swagger/OpenAPI)

## Technical Stack
- Backend: Python FastAPI
- Database: PostgreSQL
- Frontend: HTML, JavaScript, Bootstrap
- API Documentation: OpenAPI/Swagger
- Container: Docker
- Orchestration: Kubernetes
- Database Migration: Alembic

## Local Development Setup
1. Backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. Frontend:
   ```bash
   cd frontend
   python -m http.server 8080
   ```

## API Endpoints
- POST /api/shorten - Create short URL
- GET /{short_id} - Redirect to original URL
- GET /api/stats/{short_id} - Get URL statistics
- GET /api/health - Health check endpoint

## Database Schema
```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_id VARCHAR(10) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    custom_alias VARCHAR(50) UNIQUE
);

CREATE TABLE clicks (
    id SERIAL PRIMARY KEY,
    url_id INTEGER REFERENCES urls(id),
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    referrer TEXT,
    user_agent TEXT
);
```


### Minimum Tasks (Infra Creation)
- Provision infrastructure either on self managed K8s / EKS using terraform 
- Set up a simple GitHub Actions or Jenkins pipeline to run Terraform commands (terraform fmt, validate, and plan).
- Automate Terraform execution with a pipeline trigger on push to a specific branch.
- Create Dockerfiles 
- Set up multi-stage builds
- Configure environment variables
- Set up health check endpoints
- Configure basic logging

### Target Tasks (Deployment)
- Refactor the Terraform code to use modules for reusability.
- Store Terraform state in an S3 bucket with DynamoDB for state locking.
- Write Deployment.yaml and service.yaml files for deployment on k8s.
- Use helm for deplyment using gitops
- Handle environment variables using k8s secrets

### Stretch 
- Setup Argo CD for automatic deplyoment 
- Setup Promethues and grafana 
- setup basic alerts