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

def _contains_all_includes(recipe: Dict, include: List[str]) -> bool:
    text = _recipe_text(recipe)
    for word in include:
        w = _normalize(word)
        if w and w not in text:
            return False
    return True

def search_recipes(
    recipes: List[Dict],
    query: Optional[str],
    include: List[str],
    exclude: List[str],
    limit: int,
    offset: int,
    require_all_includes: bool = False,
) -> List[Dict]:
    results = []

    for recipe in recipes:
        if not _matches_query(recipe, query):
            continue
        if exclude and _contains_excluded(recipe, exclude):
            continue

        # här vill  jag vara extra strikt (t.ex. AI->översatt ingrediens),
        # kräver jag att alla include-termer faktiskt finns i texten.
        if include and require_all_includes and not _contains_all_includes(recipe, include):
            continue

        score = _include_score(recipe, include) if include else 0
        results.append((score, recipe))

    results.sort(key=lambda x: x[0], reverse=True)

    offset = max(0, offset)
    limit = max(1, min(100, limit))  # skydd: 1..100, borde räcka för denna uppgift

    sliced = results[offset: offset + limit]
    return [recipe for _, recipe in sliced]

def to_search_result(recipe: Dict) -> Dict:
    ingredients = recipe.get("ingredients", "") or ""
    ingredients = " ".join(ingredients.split())  # normaliserar whitespace och/eller newlines
    short_ingredients = ingredients[:200]

    if len(ingredients) > 200:
        short_ingredients += "..."

    recipe_id = None
    _id = recipe.get("_id")
    if isinstance(_id, dict):
        recipe_id = _id.get("$oid")

    return {
        "id": recipe_id,
        "name": recipe.get("name"),
        "ingredients": short_ingredients,
        "url": recipe.get("url"),
        "source": recipe.get("source"),
    }