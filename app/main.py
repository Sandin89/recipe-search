from fastapi import FastAPI
from app.services.recipe_loader import load_recipes

API_VERSION = "0.1.0"

app = FastAPI(
    title="Recipe Search API",
    version=API_VERSION,
    description="REST API for searching recipes based on ingredients or free-text queries.",
)

# Loaded once at startup to avoid re-parsing the large dataset per request
RECIPES = []


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
