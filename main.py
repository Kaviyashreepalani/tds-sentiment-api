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
async def health_check():
    return {"status": "ok"}


@app.post("/")
@app.post("/sentiment")
async def sentiment(request: SentimentRequest):

    positive_words = {
        "love", "great", "excellent", "good", "happy",
        "awesome", "amazing", "fantastic", "wonderful",
        "best", "like", "nice", "perfect", "enjoy",
        "brilliant", "outstanding", "superb"
    }

    negative_words = {
        "hate", "terrible", "bad", "awful", "sad",
        "worst", "horrible", "angry", "disappointed",
        "poor", "useless", "boring", "annoying",
        "disgusting", "pathetic", "failure"
    }

    results = []

    for sentence in request.sentences:
        text = sentence.lower()

        positive_score = sum(
            1 for word in positive_words if word in text
        )

        negative_score = sum(
            1 for word in negative_words if word in text
        )

        if positive_score > negative_score:
            label = "happy"
        elif negative_score > positive_score:
            label = "sad"
        else:
            label = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": label
        })

    return {"results": results}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
