from fastapi import FastAPI, Request
import platform
import socket
import os
from datetime import datetime, timezone



SERVICE_NAME = "my-devops-service"
SERVICE_VERSION = "1.0.0"
START_TIME = datetime.now(timezone.utc)



app = FastAPI()

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
    uptime = datetime.now(timezone.utc) - START_TIME
    return {
        "uptime_seconds": int((uptime).total_seconds()),
        "uptime_human": f"{int((uptime).total_seconds()) // 3600} hour, {int((uptime).total_seconds()) % 3600 // 60} minutes",
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


@app.get("/health")
def health_check():
    return {"status": "ok"}

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
        "runtime": get_uptime(),
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
    uvicorn.run(app, host="0.0.0.0", port=8000)