from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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
async def sentiment(request: SentimentRequest):
    positive_words = [
        "love", "great", "excellent", "good", "happy",
        "awesome", "amazing", "fantastic", "wonderful",
        "best", "like"
    ]

    negative_words = [
        "hate", "terrible", "bad", "awful", "sad",
        "worst", "horrible", "angry", "disappointed",
        "poor"
    ]

    results = []

    for sentence in request.sentences:
        text = sentence.lower()

        pos = sum(word in text for word in positive_words)
        neg = sum(word in text for word in negative_words)

        if pos > neg:
            sentiment = "happy"
        elif neg > pos:
            sentiment = "sad"
        else:
            sentiment = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}
