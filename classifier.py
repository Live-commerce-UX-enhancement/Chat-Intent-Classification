import json
import datetime
from transformers import pipeline

# koElectra-base-v3
classifier1 = pipeline(
    "text-classification",
    model="/Users/yuseogi/Desktop/work/학교/4-1/캡스톤/Auto-Chat-Classification-and-Answers-for-Live-Commerce/classifier1",
    return_all_scores=True,
)

# kcbert-Base
classifier2 = pipeline(
    "text-classification",
    model="/Users/yuseogi/Desktop/work/학교/4-1/캡스톤/Auto-Chat-Classification-and-Answers-for-Live-Commerce/classifier2",
    return_all_scores=True,
)


def classifier(chat):
    message = chat[1]
    labels = classifier1(message)
    general_score = labels[0][0]['score']
    others_score = labels[0][1]['score']
    if general_score > others_score:
        return [chat, "일반"]
    else:
        labels = classifier2(message)
        question_score = labels[0][0]['score']
        request_score = labels[0][1]['score']
        if question_score > request_score:
            return [chat, "질문"]
        else:
            return [chat, "요청"]


def preprocess(data_list):
    message_list = list()
    data_json = json.loads(data_list)
    for chat_data in data_json['list']:
        message_list.append([chat_data["commentNo"], chat_data["message"]])
    return message_list, data_json['time']
