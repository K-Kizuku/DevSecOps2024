import logging
import os
import sys

from llama_index import (
    LLMPredictor,
    PromptTemplate,
    ServiceContext,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.llms import LlamaCPP

def hoge():
    # ログレベルの設定
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True)

    documents = SimpleDirectoryReader("/opt/data/train").load_data()

    # LLMのセットアップ
    model_path = f"mo/ELYZA-japanese-Llama-2-7b-fast-instruct-gguf/ELYZA-japanese-Llama-2-7b-fast-instruct-q8_0.gguf"
    llm = LlamaCPP(
        model_path=model_path,
        temperature=0.1,
        model_kwargs={"n_ctx": 4096, "n_gpu_layers": 32},
    )
    llm_predictor = LLMPredictor(llm=llm)
        
    # 埋め込みモデルの初期化  
        # 埋め込みモデルの計算を実行するデバイスを指定。今回は埋め込みモデルをCPUで実施しないとVRAMに収まりきらないので、CPUで実施する。
    # "cpu","cuda","mps"から指定する。
    EMBEDDING_DEVICE = "cpu"

    # 実行するモデルの指定とキャッシュフォルダの指定
    embed_model_name = ("intfloat/multilingual-e5-large",)
    cache_folder = "./sentence_transformers"

    # 埋め込みモデルの作成
    embed_model = HuggingFaceEmbedding(
        model_name="intfloat/multilingual-e5-large",
        cache_folder=cache_folder,
        device=EMBEDDING_DEVICE,
    )

    # ServiceContextのセットアップ
    ## debug用 Callback Managerのセットアップ
    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    callback_manager = CallbackManager([llama_debug])

    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        embed_model=embed_model,
        chunk_size=500,
        chunk_overlap=20,
        callback_manager=callback_manager,
    )

    # インデックスの生成
    index = VectorStoreIndex.from_documents(
        documents,
        service_context=service_context,
    )

if __name__ == "__main__":
    hoge()