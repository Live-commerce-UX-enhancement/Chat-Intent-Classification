from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import json
import classifier
from multiprocessing import Pool

app = FastAPI()
num_cores = 4
pool = Pool(num_cores)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()

            preprocessed_data = classifier.preprocess(data)

            result_list = pool.map(classifier.classify, preprocessed_data)

            # 의도 분류 결과
            response_data = {
                'chat_data': result_list
            }

            await websocket.send_text(json.dumps(response_data, ensure_ascii=False))
    except WebSocketDisconnect:
        await websocket.close()
