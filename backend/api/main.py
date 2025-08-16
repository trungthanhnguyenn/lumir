from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.module.router.get_numerology_infor import router as numerology_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Lumir AI Numerology API",
    description="API tính toán thần số học dựa trên tên và ngày sinh",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Lỗi server nội bộ",
            "error": str(exc) if app.debug else "Internal server error"
        }
    )

# Include routers
app.include_router(numerology_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Lumir AI Numerology API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/numerology/health"
    }

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "lumir-ai-numerology"}