import json
from transformers import pipeline

# koElectra-base-v3
classifier1 = pipeline(
    "text-classification",
    model="model Path",
    return_all_scores=True,
)

# kcbert-Base
classifier2 = pipeline(
    "text-classification",
    model="model Path",
    return_all_scores=True,
)


def classify(chat):
    message = chat['message']
    labels = classifier1(message)
    general_score = labels[0][0]['score']
    others_score = labels[0][1]['score']
    if general_score > others_score:
        chat['result'] = '일반'
    else:
        labels = classifier2(message)
        question_score = labels[0][0]['score']
        request_score = labels[0][1]['score']
        if question_score > request_score:
            chat['result'] = '질문'
        else:
            chat['result'] = '요청'

    return chat


def preprocess(data_list):
    message_list = list()
    data_json = json.loads(data_list)
    for chat_data in data_json['list']:
        message_list.append({'commentNo': chat_data["commentNo"], 'message': chat_data["message"]})
    return message_list
