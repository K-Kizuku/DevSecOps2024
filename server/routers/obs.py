from fastapi import APIRouter, Depends, HTTPException,  FastAPI, Response
from fastapi.responses import StreamingResponse

from starlette.websockets import WebSocket
import json
import subprocess

import asyncio
obs_router = APIRouter()

DEFAULT_ATTRIBUTES = (
    'pid',
    'name',
    'vram',
)

def get_gpu_info(nvidia_smi_path='nvidia-smi', no_units=True):
    cmd = 'nvidia-smi   --query-compute-apps=pid,process_name,used_memory --format=csv,noheader'
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode().split('\n')
    lines = [ line.strip() for line in lines if line.strip() != '' ]

    return [ { k: v for k, v in zip(DEFAULT_ATTRIBUTES, line.split(', ')) } for line in lines ]

@obs_router.get("/obs", response_model=str)
async def websocket_endpoint(ws: WebSocket, pid: int = 0):
    await ws.accept()
    key = ws.headers.get('sec-websocket-key')
    clients[key] = ws

    try:
        while True:
            message_data = get_gpu_info()
            # pidによるフィルタリング
            query = []
            for d in message_data:
                if(int(d['pid']) == pid):
                    query += [d['vram']] 
            # 全クライアントにメッセージを送信
            json_data = {
                "key": key,
                "vram_usage": query,
            }
            for client in clients.values():
                await client.send_text(json.dumps(json_data))

    except:
        await ws.close()
        del clients[key]

