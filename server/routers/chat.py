from fastapi import FastAPI, Response
from gpt import GPT  # 仮のライブラリ名
import asyncio

app = FastAPI()

# GPTモデルの初期化
gpt_model = GPT()

async def generate_output_stream(prompt: str) -> str:
    output = gpt_model.generate(prompt)  # LLMからの出力を生成する関数（仮定）
    return output

@app.get("/stream")
async def stream_output(response: Response, prompt: str):
    response.headers["Content-Type"] = "text/event-stream"
    response.headers["Cache-Control"] = "no-cache"

    async def send_output(prompt: str):
        output = await generate_output_stream(prompt)
        for token in output.split():
            yield "data: {}\n\n".format(token)
            await asyncio.sleep(0.1)  # 出力の速度を調整するための遅延（任意の秒数で調整可能）

    async for chunk in send_output(prompt):
        yield chunk
