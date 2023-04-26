from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

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


@app.get("/{chat}")
async def root(chat: str):
    labels = classifier1(chat)
    general_score = labels[0][0]['score']
    others_score = labels[0][1]['score']
    if general_score > others_score:
        return {"message": "일반"}
    else:
        labels = classifier2(chat)
        question_score = labels[0][0]['score']
        request_score = labels[0][1]['score']
        if question_score > request_score:
            return {"message": "질문"}
        else:
            return {"message": "요청"}

