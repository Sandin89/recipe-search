## Kör lokalt

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload



När servern är uppe, open:
- http://127.0.0.1:8000/docs (interactive Swagger UI)
- http://127.0.0.1:8000/health

```

Arbetsprovet byggdes steg för steg med målet att alltid ha en fungerande lösning. Jag började med en enkel FastAPI  bas i main och jobbade sedan vidare i separata branches som testades innan de slogs ihop.

Tidigt märkte jag att datasetet inte var vanlig JSON utan JSONL, vilket först orsakade problem vid inläsning. Det löstes genom att läsa filen rad för rad, vilket också blev en bättre lösning för ett så stort dataset.

När grunden var på plats förbättrades sökningen successivt med include/exclude, pagination och tydligare validering för att undvika oväntade fel.

I ett senare steg lades semantisk sök till för att göra fritextsökningar mer träffsäkra. Den används som ett stöd ovanpå den befintliga logiken, med fallback till klassisk sök om den inte ger resultat.

Fokus genom hela arbetet har varit på fungerande kod, tydliga steg och att lösa riktiga problem på ett rimligt sätt.

Jag föröskte hålla mig till att enbart göra uppgiften och inte "over-do" it med HTML/Jinja, utan hålla mig til lramen av uppgiften.
Då uppgiften skulel vara inne under "kommande vecka" så tog jag min tid, testade och lät det hellre ta en dag extra än att skynda mig och kasta in det samma eftermiddag.

Då alla bolag arbetar olika, vissa integrerar generativ AI och andra får absolut inte använda det, så valde jag att inte koppla på eng enerativ AI i uppgiften, för att få lite mer personliga svar via tokens. (Samt att detta kostar och skulle kräva att jag anger min personliga nyckel i koden, vilket är totalt nej!)


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



![OMAI](bilder/omai_F46B63.png)

# ARBETSPROV - Recept

## Uppgift
Din uppgift är att bygga ett REST-baserat API som kan söka efter recept, givet ett antal ingredienser eller en beskrivning av vad man vill laga. 

Till din hjälp finns en receptsamling i JSON-format 20170107-061401-recipeitems.json.zip.

Här är ett exempel:
```json
{
   "_id": {
       "$oid": "54f3bb3696cc622a52715210"
   },
   "name": "Coconut fish curry",
   "ingredients": "2 red chillies\npinch dried chilli\n2 tbsp vegetable oil\n½ lemon\nhandful fresh coriander\n2 tbsp vegetable oil\n½ onion\n1 garlic\n1 handful peeled and chopped sweet potato\n1 tsp curry powder\n1 tsp cumin\n85g/3oz cod or pollack\n½ tin coconut milk\n1 handful baby spinach\n½ lime\n, to taste salt\n2 tbsp chopped fresh coriander",
   "url": "http://www.bbc.co.uk/food/recipes/coconutfishcurry_89979",
   "ts": {
       "$date": 1425259318950
   },
   "cookTime": "PT30M",
   "source": "bbcfood",
   "recipeYield": "Serves 1",
   "prepTime": "PT30M"
}
```

## Krav
- Det ska tydligt framgå hur programmet startas, vilka beroenden den har och eventuella stödsystem
- API:ets ska kunna hantera indata på flera språk men behöver bara svara med receptet på engelska
- Dokumentera vilka aspekter av AI du använt och varför
- Godkända programmeringspråk är: Java, C#, JavaScript/TypeScript, Python

## Utvärderingskriterier
- Kodkvalitet 
- Lösningens robusthet
- Arkitektur
- Användningen av AI-teknologier

## Leverans
- Zip-fil med källkod och dokumentation eller - 
- länk till ett Github repo.
- Om du gjort en lösning deployad i molnet en länk till tjänsten

## Tips
- Hur kan systemet hantera negativa sökord, t.ex. kyckling men inte vitlök?
- Om du vill använda en vektordatabas är [Chroma](https://cookbook.chromadb.dev/running/running-chroma/#docker) ett bra alternativ som också går att köra lokalt i Docker. 

Lycka till!
