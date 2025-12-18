from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import items

app = FastAPI(
    title="Learn English API",
    description="Backend API for Learn English from Zero for Vietnamese",
    version="1.0.0"
)

# --- CORS Configuration ---
origins = [
    "https://learnenglishzero.io.vn",      # Production frontend
    "https://www.learnenglishzero.io.vn",  # WWW subdomain
    "http://localhost:3000",               # Local frontend dev
    "http://127.0.0.1:3000",               # Local frontend dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- End CORS Configuration ---

app.include_router(items.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Learn English API", "status": "ok"}


@app.get("/hello")
def hello():
    """Test endpoint for frontend connection"""
    return {"message": "Hello from learnenglishzero API!", "status": "ok"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "learn-english-api"}
