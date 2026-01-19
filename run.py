#!/usr/bin/env python3
"""
Mauli Industries ERP System - Startup Script
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting Mauli Industries ERP System...")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    )
