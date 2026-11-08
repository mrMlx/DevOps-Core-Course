from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import platform
import socket
import os
from datetime import datetime, timezone
import logging


SERVICE_NAME = "my-devops-service"
SERVICE_VERSION = "1.0.0"
START_TIME = datetime.now(timezone.utc)


host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "5000"))
debug = os.getenv("DEBUG", "False").lower()
debug = (debug == "true")
app = FastAPI()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.architecture(),
        "cpu_count": os.cpu_count(),
        "python_version": platform.python_version()
    }

def get_uptime():
    return datetime.now(timezone.utc) - START_TIME

def get_runtime():
    uptime = get_uptime()
    return {
        "uptime_seconds": int(uptime.total_seconds()),
        "uptime_human": f"{int(uptime.total_seconds()) // 3600} hour, {int(uptime.total_seconds()) % 3600 // 60} minutes",
        "current_time": datetime.now(timezone.utc).isoformat(),
        "timezone": "UTC"
    }

def get_endpoints():
    return [
            {
                "path": "/",
                "method": "GET",
                "description": "Returns full service and system info"
            },
            {
                "path": "/health",
                "method": "GET",
                "description": "Health check endpoint"
            }   
            
        ]

# Error 404
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=404, 
        content={"error": exc.detail, "status": "error", "path": request.url.path}
        )

# Error 500
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logging.error(f"Internal  error: {exc}")
    return JSONResponse(
        status_code=500, 
        content={"error": "Internal Server Error", "status": "error"}
        )

# Check heath
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": int(get_uptime().total_seconds())
        }

# Get info about service
@app.get("/")
def get_root(request: Request):
    data = {
        "service" : {
            "name": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "description": "FastAPI application for DevOps lab",
            "framework": "FastAPI"
        }, 
        "system": get_system_info(),
        "runtime": get_runtime(),
        "request": {
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "method": request.method,
            "path": request.url.path
        },
        "endpoints": get_endpoints()
    }
    return data


if __name__ == "__main__":
    import uvicorn
    logging.info("Application started")
    uvicorn.run(app, host=host, port=port, reload=debug)