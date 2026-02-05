from typing import List, Dict, Optional


def _normalize(text: str) -> str:
    return (text or "").lower().strip()


def _recipe_text(recipe: Dict) -> str:
    name = recipe.get("name", "")
    ingredients = recipe.get("ingredients", "")
    return f"{name} {ingredients}".lower()


def _matches_query(recipe: Dict, query: Optional[str]) -> bool:
    q = _normalize(query)
    if not q:
        return True
    return q in _recipe_text(recipe)


def _contains_excluded(recipe: Dict, exclude: List[str]) -> bool:
    text = _recipe_text(recipe)
    return any(_normalize(word) and _normalize(word) in text for word in exclude)


def _include_score(recipe: Dict, include: List[str]) -> int:
    text = _recipe_text(recipe)
    score = 0
    for word in include:
        w = _normalize(word)
        if w and w in text:
            score += 1
    return score


def search_recipes(
    recipes: List[Dict],
    query: Optional[str],
    include: List[str],
    exclude: List[str],
    limit: int,
    offset: int,
) -> List[Dict]:
    results = []

    for recipe in recipes:
        if not _matches_query(recipe, query):
            continue
        if exclude and _contains_excluded(recipe, exclude):
            continue

        score = _include_score(recipe, include) if include else 0
        results.append((score, recipe))

    results.sort(key=lambda x: x[0], reverse=True)

    offset = max(0, offset)
    limit = max(1, min(100, limit))  # skydd: 1..100, borde räcka för denna uppgift, i annat fall ökar jag gränsen.

    sliced = results[offset : offset + limit]
    return [recipe for _, recipe in sliced]
