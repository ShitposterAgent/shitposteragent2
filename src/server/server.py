from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os

from automation.automation_module import Automation
from config_manager import ConfigManager

# Initialize components at module level
config_manager = ConfigManager()
config = config_manager.config
automation = None

app = FastAPI(title="Shitposter Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    content: str
    platform: str
    schedule_time: Optional[datetime] = None

@app.on_event("startup")
async def startup():
    global automation
    automation = await Automation.create(config)

@app.on_event("shutdown")
async def shutdown():
    if automation:
        await automation.close()

@app.get("/status")
async def get_status():
    return {"status": "running"}

@app.post("/post")
async def create_post(post: Post):
    try:
        await automation.social_automator.post_update(post.content)
        return {"status": "posted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/platforms/{platform}/status")
async def get_platform_status(platform: str):
    try:
        await automation.social_automator.check_platforms([platform])
        return {"status": "checked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)