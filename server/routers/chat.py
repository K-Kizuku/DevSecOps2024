from fastapi import APIRouter, Depends, HTTPException,  FastAPI, Response
from fastapi.responses import StreamingResponse

import asyncio

import requests
from torchvision.io import read_image
from torchvision.models import resnet50, ResNet50_Weights
import os

def getCategoryName(path):
    img = read_image(path)
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights=weights)
    model.eval()
    preprocess = weights.transforms()
    batch = preprocess(img).unsqueeze(0)
    prediction = model(batch).squeeze(0).softmax(0)
    cid = prediction.argmax().item()
    return category_name = weights.meta["categories"][cid]

chat_router = APIRouter()

async def generate_output_stream(prompt: str):
    # ここに処理を記述
    return "output"

@chat_router.get("/streaming", response_model=str)
async def stream_output(response:StreamingResponse):
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"
    async def generate_json_data():
        for i in range(100):
            await asyncio.sleep(0.1)
            yield f"data:{i}\n\n"


    return StreamingResponse(content=generate_json_data(), media_type="text/event-stream", headers={"Content-Type": "text/event-stream","Cache-Control": "no-cache"})

    # async def send_output(prompt: str):
    #     output = await generate_output_stream(prompt)
    #     for token in output.split():
    #         yield "data: {}\n\n".format(token)
    #         await asyncio.sleep(0.1)  # 出力の速度を調整するための遅延（任意の秒数で調整可能）

    # async for chunk in send_output(prompt):
    #     yield chunk


