from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import json
import classifier

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            preprocessed_data = classifier.preprocess(data)
            result_list = classifier.classifier(preprocessed_data)
            await websocket.send_text(json.dumps(result_list, ensure_ascii=False))
    except WebSocketDisconnect:
        await websocket.close()
