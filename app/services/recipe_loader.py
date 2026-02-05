'''
from fastapi import FastAPI

app = FastAPI(
    title="Recipe Search API",
    version="0.1.0",
    description="REST API for searching recipes based on ingredients or free-text queries."
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
'''
import json
from pathlib import Path
from typing import Iterator, Dict

DATA_PATH = Path("data/20170107-061401-recipeitems.json")

def load_recipes() -> Iterator[Dict]:
    """
    Stream recipes from JSONL file.
    Each line is one JSON object.
    """
    with DATA_PATH.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            yield json.loads(line)