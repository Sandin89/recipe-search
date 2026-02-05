from typing import Dict, List, Tuple, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import json
from pathlib import Path

_MODEL_NAME = "all-MiniLM-L6-v2"

_SYNONYMS_PATH = Path("app/core/synonyms.json")

def load_query_synonyms() -> dict:
    if not _SYNONYMS_PATH.exists():
        return {}
    with _SYNONYMS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

_QUERY_SYNONYMS = load_query_synonyms()

def translate_query(text: str) -> str:
    t = (text or "").lower().strip()
    return _QUERY_SYNONYMS.get(t, text)

#

def build_recipe_document(recipe: Dict) -> str:
    name = recipe.get("name", "") or ""
    ingredients = recipe.get("ingredients", "") or ""
    return f"{name}\n{ingredients}".strip()

class SemanticIndex:
    def __init__(self) -> None:
        self.model = SentenceTransformer(_MODEL_NAME)
        self.recipe_ids: List[int] = []
        self.embeddings: Optional[np.ndarray] = None

    def build(self, recipes: List[Dict]) -> None:
        docs = [build_recipe_document(r) for r in recipes]
        embs = self.model.encode(docs, convert_to_numpy=True, show_progress_bar=True)

        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        embs = embs / norms

        self.recipe_ids = list(range(len(recipes)))
        self.embeddings = embs

    def query(self, recipes: List[Dict], text: str, top_k: int = 50) -> List[Tuple[float, Dict]]:
        if self.embeddings is None or not self.recipe_ids:
            return []

        q = self.model.encode(text, convert_to_numpy=True)
        q_norm = np.linalg.norm(q)
        if q_norm == 0:
            return []

        q = q / q_norm

        sims = np.dot(self.embeddings, q)  
        top_k = max(1, min(top_k, len(sims)))

        idxs = np.argpartition(-sims, top_k - 1)[:top_k]
        idxs = idxs[np.argsort(-sims[idxs])]

        return [(float(sims[i]), recipes[i]) for i in idxs]