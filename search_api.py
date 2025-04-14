from fastapi import FastAPI, Query, HTTPException
import json
import os
from rapidfuzz import process, fuzz  # Correct import

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

# Improved search function with fuzzy matching
def search_videos(query):
    if not query:
        return [{"message": "Please provide a valid search query."}]

    query_lower = query.lower()
    titles = [video["title"].lower() for video in video_data]

    # Find best matches using fuzzy search
    matches = process.extract(query_lower, titles, limit=5, scorer=fuzz.partial_ratio)

    results = []
    for matched_title, score, _ in matches:  # Corrected unpacking (ignored index)
        if score > 60:  # Only return matches with confidence score above 60%
            original_title = next(video["title"] for video in video_data if video["title"].lower() == matched_title)
            results.append({"title": original_title, "confidence_score": score})

    return results if results else [{"message": "No matching videos found."}]

@app.get("/search")
async def search(query: str = Query(None, alias="q", description="Search query")):
    if query is None:
        raise HTTPException(status_code=400, detail="Error: Search query is required.")

    videos = search_videos(query)
    return {"query": query, "results": videos}
