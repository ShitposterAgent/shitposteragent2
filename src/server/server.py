from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from datetime import datetime
import os
from automation.automation_module import Automation  # Updated import
from vision import Vision
from nlp import NLP
from config_manager import ConfigManager
from server.storage import PostStorage

app = FastAPI(title="Shitposter Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components with config asynchronously
# Moved initialization to startup event

class Post(BaseModel):
    content: str
    platform: str
    schedule_time: Optional[datetime] = None

class AnalysisRequest(BaseModel):
    text: str
    context: Optional[str] = None

automation = None  # Global variable to hold Automation instance

async def process_scheduled_posts(config):
    """Process any pending scheduled posts"""
    while True:
        try:
            pending_posts = post_storage.get_pending_posts()
            for post in pending_posts:
                try:
                    await automation.social_automator.post_update(post['content'])  # Await the async method
                    post_storage.mark_post_completed(post['id'])
                except Exception as e:
                    post_storage.mark_post_failed(post['id'], str(e))
        except Exception as e:
            print(f"Error processing scheduled posts: {e}")
        await asyncio.sleep(60)  # Check every minute

@app.on_event("startup")
async def startup_event():
    """Start background tasks when server starts"""
    global automation
    config_manager = ConfigManager(config_path=os.path.expanduser("~/shitposter.json"))
    config = config_manager.config
    post_storage = PostStorage(config)
    vision = Vision(config.vision, config)  # Pass VisionConfig directly

    automation = await Automation.create(config)  # Asynchronously create Automation instance

    asyncio.create_task(process_scheduled_posts(config))  # Start background task

@app.get("/status")
async def get_status():
    """Get the current status of the agent"""
    return {"status": "running"}

@app.post("/post")
async def create_post(post: Post):
    """Schedule or immediately create a social media post"""
    try:
        if post.schedule_time:
            post_id = post_storage.add_post(post.platform, post.content, post.schedule_time)
            return {"status": "scheduled", "post_id": post_id, "time": post.schedule_time}
        else:
            await automation.social_automator.post_update(post.content)  # Await the async method
            return {"status": "posted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts/scheduled")
async def get_scheduled_posts():
    """Get all scheduled posts"""
    try:
        posts = post_storage.get_pending_posts()
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    """Analyze text using Ollama"""
    try:
        analysis = vision.analyze_with_ollama(request.text, context=request.context)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/platforms/{platform}/status")
async def get_platform_status(platform: str):
    """Get status of specific platform"""
    try:
        await automation.social_automator.check_platforms([platform])  # Await the async method
        return {"status": "checked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)