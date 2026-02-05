from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from app.services.recipe_loader import load_recipes
from app.services.search_service import search_recipes

API_VERSION = "0.2.0"

app = FastAPI(
    title="Recipe Search API",
    version=API_VERSION,
)

RECIPES = []


class SearchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: Optional[str] = None
    include: List[str] = []
    exclude: List[str] = []
    limit: int = 10
    offset: int = 0


@app.on_event("startup")
def startup_event():
    global RECIPES
    RECIPES = list(load_recipes())
    print(f"Loaded {len(RECIPES)} recipes")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": API_VERSION,
        "recipes_loaded": len(RECIPES),
    }


@app.post("/search")
def search(request: SearchRequest):
    results = search_recipes(
        recipes=RECIPES,
        query=request.query,
        include=request.include,
        exclude=request.exclude,
        limit=request.limit,
        offset=request.offset,
    )

    return {
        "count": len(results),
        "results": results,
    }
