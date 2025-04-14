from fastapi import FastAPI, Query, HTTPException
import json
import os

app = FastAPI()

# Load video data safely
video_data = []
file_path = "video.json"

if os.path.exists(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            video_data = json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error: Invalid JSON format in 'video.json'")
else:
    raise HTTPException(status_code=500, detail="Error: 'video.json' not found!")

# Autocomplete function (Search-As-You-Type)
@app.get("/autocomplete")
async def autocomplete(query: str = Query(None, alias="q", description="Autocomplete query")):
    if not query:
        return {"suggestions": []}

    suggestions = [video["title"] for video in video_data if video["title"].lower().startswith(query.lower())]

    return {"query": query, "suggestions": suggestions[:5]}  # Limit to 5 suggestions
