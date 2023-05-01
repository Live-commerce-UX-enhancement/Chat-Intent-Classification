import nest_asyncio
from transformers import pipeline
import re
import asyncio
from requests_html import pyppeteer
import json

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
    labels = classifier1(chat)
    general_score = labels[0][0]['score']
    others_score = labels[0][1]['score']
    if general_score > others_score:
        return "일반"
    else:
        labels = classifier2(chat)
        question_score = labels[0][0]['score']
        request_score = labels[0][1]['score']
        if question_score > request_score:
            return "질문"
        else:
            return "요청"


stream_url = "https://view.shoppinglive.naver.com/lives/953276?tr=lim&fm=shoppinglive&sn=home"
nest_asyncio.apply()

async def main():
    browser = await pyppeteer.launch(
        headless=True,
        args=['--no-sandbox'],
        autoClose=False
    )
    page = await browser.newPage()
    await page.goto(stream_url)
    cdp = await page.target.createCDPSession()
    await cdp.send('Network.enable')
    await cdp.send('Page.enable')

    def printResponse(response):
        data_list = re.sub(r'^\d+', '', response["response"]["payloadData"])
        data_list = data_list[2:-2].split('","')

        if data_list[0] == "broadcast_chat":
            data_json = json.loads(data_list[1].replace("\\", ""))
            for chat_data in data_json["list"]:
                message = chat_data["message"]
                print(f'채팅: {message}, 분류: {classifier(message)}')

    cdp.on('Network.webSocketFrameReceived', printResponse)  # Calls printResponse when a websocket is received


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
