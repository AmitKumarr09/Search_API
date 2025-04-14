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
        raise HTTPException(status_code=500, detail="Error: Invalid JSON format in 'videos.json'")
else:
    raise HTTPException(status_code=500, detail="Error: 'videos.json' not found!")

# Improved search function
def search_videos(query):
    if not query:
        return [{"message": "Please provide a valid search query."}]

    query_lower = query.lower()
    results = []

    for video in video_data:
        title_lower = video["title"].lower()
        match_score = sum(1 for word in query_lower.split() if word in title_lower)  # Count matching words

        if match_score > 0:
            results.append({"title": video["title"], "match_score": match_score})

    # Sort by relevance (higher match score first)
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:5] if results else [{"message": "No matching videos found."}]

@app.get("/search")
async def search(query: str = Query(None, alias="q", description="Search query")):
    if query is None:
        raise HTTPException(status_code=400, detail="Error: Search query is required.")

    videos = search_videos(query)
    return {"query": query, "results": videos}
