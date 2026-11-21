from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from backend.rag.upload import router as document_upload_router
from backend.rag.chat import router as chat_router

# Initialize SENTINELAI application
app = FastAPI(
    title="SENTINELAI",
    description="AI-Powered Real-Time Edge Surveillance and Safety Monitoring System",
    version="1.0.0"
)


# Register RAG APIs

app.include_router(document_upload_router)
app.include_router(chat_router)

# React frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------
# HOME ROUTE
# -----------------------------------------

@app.get("/")
async def home():
    return {
        "application": "SENTINELAI",
        "message": "Intelligent Surveillance Backend is Running!",
        "status": "ACTIVE",
        "version": "1.0.0"
    }


# -----------------------------------------
# SYSTEM HEALTH
# -----------------------------------------

@app.get("/api/system-health")
async def system_health():

    return {
        "frontend": "Online",
        "backend": "Online",
        "ai_engine": "Pending",
        "camera_service": "Pending",
        "database": "Ready",
        "gpu": "CPU Mode",
        "timestamp": datetime.now().isoformat()
    }


# -----------------------------------------
# INCIDENT MANAGEMENT
# -----------------------------------------

@app.get("/api/incidents")
async def get_incidents():

    return {
        "total": 0,
        "incidents": [],
        "message": "No incidents recorded yet."
    }


# -----------------------------------------
# CAMERA STATUS
# -----------------------------------------

@app.get("/api/cameras")
async def get_cameras():

    return {
        "total_cameras": 0,
        "active_cameras": 0,
        "cameras": [],
        "status": "Waiting for camera connection"
    }


# -----------------------------------------
# AI ENGINE STATUS
# -----------------------------------------

@app.get("/api/ai-status")
async def ai_status():

    return {
        "model": "YOLO11n",
        "inference_device": "CPU",
        "status": "NOT_INITIALIZED",
        "tracking": "NOT_INITIALIZED",
        "message": "AI detection engine will be initialized in the next development phase."
    }


# -----------------------------------------
# SERVER TIME
# -----------------------------------------

@app.get("/api/server-time")
async def server_time():

    return {
        "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Running"
    }


# -----------------------------------------
# APPLICATION STATUS
# -----------------------------------------

@app.get("/api/status")
async def application_status():

    return {
        "application": "SENTINELAI",
        "status": "Operational",
        "services": {
            "api": "Online",
            "frontend": "Online",
            "ai_engine": "Pending",
            "video_processing": "Pending",
            "incident_management": "Ready"
        }
    }