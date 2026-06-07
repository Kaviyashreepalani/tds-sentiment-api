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

positive_words = {
    "love","great","awesome","excellent","amazing","good","happy",
    "wonderful","fantastic","best","like","enjoy","nice","perfect"
}

negative_words = {
    "hate","bad","terrible","awful","horrible","sad","worst",
    "angry","poor","disappointed","disappointing","boring","ugly"
}

def detect_sentiment(text: str) -> str:
    t = text.lower()

    pos = sum(1 for w in positive_words if w in t)
    neg = sum(1 for w in negative_words if w in t)

    if pos > neg:
        return "happy"
    elif neg > pos:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment")
def sentiment(req: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": detect_sentiment(sentence)
            }
            for sentence in req.sentences
        ]
    }

@app.get("/")
def root():
    return {"message": "Sentiment API running"}
