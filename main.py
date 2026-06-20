from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Sentences(BaseModel):
    sentences: list[str]

class ResultItem(BaseModel):
    sentence: str
    sentiment: str

class Result(BaseModel):
    results: list[ResultItem]

# Strong keywords that override TextBlob if found
HAPPY_WORDS = [
    "love", "loved", "loving", "great", "excellent", "amazing", "awesome",
    "fantastic", "wonderful", "happy", "joyful", "excited", "best", "beautiful",
    "perfect", "brilliant", "superb", "delightful", "glad", "enjoy", "enjoyed",
    "fun", "incredible", "grateful", "thankful", "pleased", "cheerful",
    "outstanding", "terrific", "yay", "hooray", "smile", "laughing", "thrilled",
    "ecstatic", "overjoyed", "blessed", "positive", "like", "liked",

    "adore", "adored", "adorable", "affectionate", "appreciate", "appreciated",
    "astonishing", "attractive", "beatific", "beloved", "breathtaking",
    "captivating", "celebrate", "celebrated", "charming", "comforting",
    "confident", "content", "cool", "creative", "cute", "dazzling",
    "decent", "dreamy", "eager", "easy", "effective", "efficient",
    "encouraging", "energetic", "enjoyable", "enthusiastic", "epic",
    "fabulous", "faithful", "favorite", "fine", "flourishing", "fortunate",
    "friendly", "generous", "genius", "genuine", "gifted", "good",
    "gorgeous", "graceful", "heartwarming", "helpful", "honest", "hopeful",
    "impressive", "inspiring", "jolly", "kind", "legendary", "lively",
    "lovely", "lucky", "magnificent", "marvelous", "motivated", "nice",
    "optimistic", "outperform", "peaceful", "phenomenal", "pleasant",
    "popular", "priceless", "productive", "prosperous", "proud", "radiant",
    "refreshing", "rejoice", "remarkable", "respected", "rewarding",
    "satisfying", "sensational", "spectacular", "splendid", "stellar",
    "stunning", "successful", "sunny", "supportive", "sweet", "talented",
    "thankyou", "thriving", "top", "trustworthy", "valuable", "vibrant",
    "victorious", "warm", "welcoming", "win", "winner", "winning",
    "wisdom", "worthy", "wow", "yes", "yummy", "zealous"
]

SAD_WORDS = [
    "hate", "hated", "terrible", "awful", "horrible", "bad", "worst", "sad",
    "disappointed", "disappointing", "upset", "angry", "frustrated", "annoyed",
    "miserable", "depressed", "crying", "cry", "dreadful", "disgusting",
    "dislike", "unfortunately", "failed", "fail", "failure", "poor", "useless",
    "broken", "hurt", "pain", "suffering", "regret", "sorry", "waste",
    "pathetic", "disaster", "ugly", "boring", "dull", "tired", "exhausted",
    "unfortunate", "tragic", "devastated", "hopeless", "helpless", "furious",

    "abysmal", "aggravating", "alarming", "ashamed", "atrocious", "avoid",
    "bitter", "bleak", "buggy", "chaotic", "cheap", "collapse", "complain",
    "confused", "corrupt", "cruel", "damaged", "dangerous", "dark",
    "defeated", "defective", "despair", "destroyed", "difficult", "dirty",
    "discouraged", "disturbing", "doomed", "drained", "embarrassed",
    "empty", "error", "evil", "fake", "faulty", "fear", "fearful",
    "foolish", "garbage", "gloomy", "gross", "guilty", "hard", "harmful",
    "harsh", "heartbroken", "hostile", "humiliated", "ignored", "impossible",
    "inadequate", "inferior", "injured", "insulting", "irritating", "jealous",
    "lonely", "loser", "loss", "mad", "mess", "mistake", "negative",
    "nervous", "nightmare", "offensive", "outrageous", "overwhelmed",
    "painful", "pessimistic", "pitiful", "problem", "rage", "rejected",
    "risky", "rotten", "ruined", "scam", "scared", "shame", "shocked",
    "sick", "stress", "stressed", "struggling", "terrified", "toxic",
    "trouble", "unfair", "unhappy", "unreliable", "unsafe", "weak",
    "weary", "worthless", "wounded", "wrong", "yell", "zero", "failured",
    "catastrophe", "bankrupt", "meltdown", "nightmarish", "destructive"
]

def get_sentiment(text):
    lower = text.lower()

    # Count keyword hits
    happy_score = sum(1 for w in HAPPY_WORDS if w in lower.split())
    sad_score   = sum(1 for w in SAD_WORDS   if w in lower.split())

    # Get TextBlob polarity (-1 to +1)
    polarity = TextBlob(text).sentiment.polarity

    # Combine: keywords vote + textblob vote
    if happy_score > sad_score:
        keyword_vote = "happy"
    elif sad_score > happy_score:
        keyword_vote = "sad"
    else:
        keyword_vote = "neutral"

    if polarity > 0.1:
        textblob_vote = "happy"
    elif polarity < -0.1:
        textblob_vote = "sad"
    else:
        textblob_vote = "neutral"

    # If both agree, confident answer
    if keyword_vote == textblob_vote:
        return keyword_vote

    # If keywords found a strong signal, trust them
    if happy_score > 0 or sad_score > 0:
        return keyword_vote

    # Otherwise trust TextBlob
    return textblob_vote

@app.post("/sentiment", response_model=Result)
def sentiment_analysis(data: Sentences):
    results = []
    for sentence in data.sentences:
        sentiment = get_sentiment(sentence)
        results.append({"sentence": sentence, "sentiment": sentiment})
    return {"results": results}
