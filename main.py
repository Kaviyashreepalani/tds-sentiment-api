from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

@app.get("/")
@app.head("/")
async def root():
    return {"status": "ok"}

@app.post("/sentiment")
async def sentiment(req: SentimentRequest):
    results = []

    positive_words = {
        "love","great","excellent","good","happy","awesome",
        "amazing","fantastic","wonderful","best","like"
    }

    negative_words = {
        "sad","bad","terrible","awful","hate","worst",
        "poor","horrible","angry","disappointed"
    }

    for sentence in req.sentences:
        text = sentence.lower()

        pos = sum(word in text for word in positive_words)
        neg = sum(word in text for word in negative_words)

        if pos > neg:
            label = "happy"
        elif neg > pos:
            label = "sad"
        else:
            label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": label
        })

    return {"results": results}
