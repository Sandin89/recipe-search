from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from app.services.recipe_loader import load_recipes
from app.services.search_service import search_recipes, to_search_result
from app.services.semantic_search import SemanticIndex, translate_query

API_VERSION = "0.2.0"

app = FastAPI(
    title="Recipe Search API",
    version=API_VERSION,
)

RECIPES = []
SEMANTIC_INDEX = SemanticIndex()


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

    SEMANTIC_INDEX.build(RECIPES)
    print("Semantic index built")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": API_VERSION,
        "recipes_loaded": len(RECIPES),
    }


@app.post("/search")
def search(request: SearchRequest):
    if request.query and request.query.strip():
        q = translate_query(request.query)

        auto_include: List[str] = []
        if q != request.query:
            auto_include.append(q)

        candidates = SEMANTIC_INDEX.query(RECIPES, q, top_k=200)
        candidate_recipes = [r for _, r in candidates]

        results = search_recipes(
            recipes=candidate_recipes,
            query=None,
            include=request.include + auto_include,
            exclude=request.exclude,
            limit=request.limit,
            offset=request.offset,
            require_all_includes=bool(auto_include),
        )

        # Fallback: om semantic gav 0, kör vanlig search
        if not results:
            results = search_recipes(
                recipes=RECIPES,
                query=request.query,
                include=request.include,
                exclude=request.exclude,
                limit=request.limit,
                offset=request.offset,
            )
    else:
        results = search_recipes(
            recipes=RECIPES,
            query=None,
            include=request.include,
            exclude=request.exclude,
            limit=request.limit,
            offset=request.offset,
        )

    return {
        "count": len(results),
        "results": [to_search_result(r) for r in results],
    }
