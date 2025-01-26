from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from datetime import datetime
import os
from automation import SocialMediaAutomator
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

# Initialize components with config
config_manager = ConfigManager(config_path=os.path.expanduser("~/shitposter.json"))
config = config_manager.config
vision = Vision(config.vision.dict(), config)
automator = SocialMediaAutomator(
    social_media_config=config.social_media,
    ollama_config=config.ollama,
    tesseract_config=config.tesseract,
    playwright_config=config.playwright
)
post_storage = PostStorage(config)

class Post(BaseModel):
    content: str
    platform: str
    schedule_time: Optional[datetime] = None

class AnalysisRequest(BaseModel):
    text: str
    context: Optional[str] = None

async def process_scheduled_posts(background_tasks: BackgroundTasks, config):
    """Process any pending scheduled posts"""
    while True:
        try:
            pending_posts = post_storage.get_pending_posts()
            for post in pending_posts:
                try:
                    automator.post_update(post['content'])
                    post_storage.mark_post_completed(post['id'])
                except Exception as e:
                    post_storage.mark_post_failed(post['id'], str(e))
        except Exception as e:
            print(f"Error processing scheduled posts: {e}")
        await asyncio.sleep(60)  # Check every minute

@app.on_event("startup")
async def startup_event():
    """Start background tasks when server starts"""
    background_tasks = BackgroundTasks()
    background_tasks.add_task(process_scheduled_posts, config)

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
            automator.post_update(post.content)
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
        automator.check_platforms([platform])
        return {"status": "checked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def start_server():
    """Start the FastAPI server"""
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    start_server()