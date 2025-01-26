from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime
import asyncio
from ..automation import SocialMediaAutomator
from ..vision import Vision
from ..nlp import NLP

app = FastAPI(title="Shitposter Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config
config_path = os.path.expanduser('~/shitposter.json')
with open(config_path) as f:
    config = json.load(f)

# Initialize components
vision = Vision(config['vision'])
automator = SocialMediaAutomator(
    social_media_config=config['social_media'],
    ollama_config=config['ollama'],
    tesseract_config=config['tesseract'],
    playwright_config=config['playwright']
)

class Post(BaseModel):
    content: str
    platform: str
    schedule_time: Optional[datetime] = None

class AnalysisRequest(BaseModel):
    text: str
    context: Optional[str] = None

@app.get("/status")
async def get_status():
    """Get the current status of the agent"""
    return {"status": "running"}

@app.post("/post")
async def create_post(post: Post):
    """Schedule or immediately create a social media post"""
    try:
        if post.schedule_time:
            # Store scheduled post
            # Implementation needed for persistent storage
            return {"status": "scheduled", "time": post.schedule_time}
        else:
            # Post immediately
            automator.post_update(post.content)
            return {"status": "posted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    """Analyze text using Ollama"""
    try:
        analysis = vision.analyze_with_ollama(request.text)
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