from langchain_community.document_loaders.csv_loader import CSVLoader
import os
from langchain.chat_models import ChatOpenAI

from transformers import GenerationConfig, pipeline
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from langchain.text_splitter import RecursiveCharacterTextSplitter

import torch


def chat():
    loader = CSVLoader(file_path='/opt/data/train/integ_data_0.csv')#保存済みのfile、encodingを変える
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 20,
    )

    docs = text_splitter.split_documents(pages)



    embed_model = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents=docs, embedding=embed_model , collection_name="openai_embed")
    from transformers import AutoTokenizer, AutoModelForCausalLM

    model_name = "elyza/ELYZA-japanese-Llama-2-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")

    if torch.cuda.is_available():
        model = model.to("cuda")
        



    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=256,
        temperature=0.6,
        top_p=0.95,
        repetition_penalty=1.2
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)
    query = "ワイン庫の出し方は?"#userの質問
    results = vectorstore.similarity_search(query, k=4)
    source_knowledge = "\n".join([x.page_content for x in results])
    template = """あなたは役にたつ助手です、あなたは検索で得られた全ての情報を整えます.下記のcontextsに基づいて,queryに関わる'備考'も含めて全ての情報を人間の言葉で簡潔で答えてください.

    contexts:
    {source_knowledge}

    query:
    {query}"""

    prompt = PromptTemplate(template=template, input_variables=["source_knowledge", "query"])

    llm_chain = LLMChain(prompt=prompt,
                        llm=local_llm
                        )

    print(llm_chain.run({"source_knowledge":source_knowledge ,"query" : query }))
    
if __name__ == "__main__":
    chat()