import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.middleware import WafMiddleware
from backend.app.routes import router as api_router
from config.settings import BACKEND_DIR, BASE_DIR

app = FastAPI(title="VSMK-AI-WAF", version="1.0.0")

# 1. Add WAF Middleware (The Core Protection)
app.add_middleware(WafMiddleware)

# 2. Register API Routes
app.include_router(api_router)

# 3. Mount Frontend Static Files
# We serve the frontend directory at /dashboard
FRONTEND_DIR = BASE_DIR / "frontend"
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def root():
    return {"message": "VSMK-AI-WAF is running. Visit /dashboard to view logs."}

@app.get("/dashboard")
async def dashboard_page():
    return FileResponse(FRONTEND_DIR / "dashboard.html")

# Mock Vulnerable Endpoint for Testing
@app.get("/vulnerable")
async def vulnerable_endpoint(q: str = ""):
    return {"status": "success", "data": f"You searched for: {q}"}

@app.post("/vulnerable")
async def vulnerable_post_endpoint(data: dict):
    return {"status": "success", "received": data}

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
