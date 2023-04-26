from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

class Item(BaseModel):
    chat: str

# koElectra-base-v3
classifier1 = pipeline(
    "text-classification",
    model="classifier1",
    return_all_scores=True,
)

# kcbert-Base
classifier2 = pipeline(
    "text-classification",
    model="classifier2",
    return_all_scores=True,
)


@app.post("/")
async def root(item: Item):
    print(item.chat)
    labels = classifier1(item.chat)
    general_score = labels[0][0]['score']
    others_score = labels[0][1]['score']
    if general_score > others_score:
        return {"message": "일반"}
    else:
        labels = classifier2(item.chat)
        question_score = labels[0][0]['score']
        request_score = labels[0][1]['score']
        if question_score > request_score:
            return {"message": "질문"}
        else:
            return {"message": "요청"}

