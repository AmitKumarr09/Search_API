from fastapi import FastAPI, Query
import json

app = FastAPI()

# Load video data
with open("video.json", "r") as file:
    videos = json.load(file)

@app.get("/search/")
def search_video(q: str = Query(..., title="Search Query")):
    """Search for videos by title"""
    results = [video for video in videos if q.lower() in video["title"].lower()]
    return {"results": results}

# Run with: uvicorn search_api:app --reload
