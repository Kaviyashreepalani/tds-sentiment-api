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
async def health():
    return {"status": "ok"}


@app.post("/")
@app.post("/sentiment")
async def sentiment(request: SentimentRequest):

    positive_words = {
        "love","great","excellent","good","happy","awesome","amazing",
        "fantastic","wonderful","best","like","nice","perfect","enjoy",
        "brilliant","outstanding","superb","excited","delighted",
        "pleased","satisfied","positive","success","successful",
        "beautiful","fun","joy","joyful","smile","glad"
    }

    negative_words = {
        "hate","terrible","bad","awful","sad","worst","horrible",
        "angry","disappointed","poor","useless","boring","annoying",
        "disgusting","pathetic","failure","unhappy","upset",
        "miserable","depressed","frustrated","negative","problem",
        "broken","fail","failed","loss","losing","pain","cry",
        "crying","regret","regrettable"
    }

    results = []

    for sentence in request.sentences:
        text = sentence.lower()

        pos = sum(1 for word in positive_words if word in text)
        neg = sum(1 for word in negative_words if word in text)

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
