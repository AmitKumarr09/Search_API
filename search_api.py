from fastapi import FastAPI, Query, HTTPException
import pyodbc
from rapidfuzz import process, fuzz  # Fuzzy search

app = FastAPI()

# Establish SQL Server connection
def get_db_connection():
    conn = pyodbc.connect("DRIVER={SQL Server};SERVER=your_server;DATABASE=VideoDB;UID=your_username;PWD=your_password")
    return conn

# Fetch video data from SQL Server dynamically
def fetch_video_titles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Title FROM Videos")  # Query SQL Server
    titles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return titles

# Improved search function with fuzzy matching
def search_videos(query):
    if not query:
        return [{"message": "Please provide a valid search query."}]

    query_lower = query.lower()
    titles = fetch_video_titles()  # Load data from SQL Server

    # Find best matches using fuzzy search
    matches = process.extract(query_lower, titles, limit=5, scorer=fuzz.partial_ratio)

    results = []
    for matched_title, score, _ in matches:  # Corrected unpacking (ignored index)
        if score > 60:  # Only return matches with confidence above 60%
            results.append({"title": matched_title, "confidence_score": score})

    return results if results else [{"message": "No matching videos found."}]

@app.get("/search")
async def search(query: str = Query(None, alias="q", description="Search query")):
    if query is None:
        raise HTTPException(status_code=400, detail="Error: Search query is required.")

    videos = search_videos(query)
    return {"query": query, "results": videos}
