import json
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


def classifier(chat_list):
    result_list = list()
    for chat in chat_list:
        labels = classifier1(chat)
        general_score = labels[0][0]['score']
        others_score = labels[0][1]['score']
        if general_score > others_score:
            result_list.append([chat, "일반"])
        else:
            labels = classifier2(chat)
            question_score = labels[0][0]['score']
            request_score = labels[0][1]['score']
            if question_score > request_score:
                result_list.append([chat, "질문"])
            else:
                result_list.append([chat, "요청"])
    return result_list


def preprocess(data_list):
    message_list = list()
    data_json = json.loads(data_list)
    for chat_data in data_json['list']:
        message_list.append(chat_data["message"])
    return message_list
