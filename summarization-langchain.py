# GPU size
# gpu_info = !nvidia-smi
# gpu_info = '\n'.join(gpu_info)
# if gpu_info.find('failed') >= 0:
#   print('Not connected to a GPU')
# else:
#   print(gpu_info)
  
# Memory size  
# from psutil import virtual_memory
# ram_gb = virtual_memory().total / 1e9
# print('Your runtime has {:.1f} gigabytes of available RAM\n'.format(ram_gb))

# if ram_gb < 20:
#   print('Not using a high-RAM runtime')
# else:
#   print('You are using a high-RAM runtime!') 
  
  
# import gradio at first before importing other langchain libraries
#!pip install gradio
import gradio as gr
print(gr.__version__)
  
  
#!pip install -q transformers einops accelerate langchain bitsandbytes
#!huggingface-cli login 
#!pip install pypdfium2
  

from langchain import HuggingFacePipeline
from transformers import AutoTokenizer
from langchain.chains import RetrievalQA
from langchain import PromptTemplate
from langchain import LLMChain
from langchain import PromptTemplate
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI

from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFium2Loader
import transformers
import torch

model = "meta-llama/Llama-2-7b-chat-hf"

tokenizer = AutoTokenizer.from_pretrained(model)

pipeline = transformers.pipeline(
    "text-generation", #task
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    max_length=1000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id
)
  
  
llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0})

def summarize_pdf(pdf_filepath):
    loader = PyPDFium2Loader(pdf_filepath)
    data = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts_FM1 = text_splitter.split_documents(data)

    template = """
              Write a concise summary of the following text delimited by triple backquotes.
              Return your response in bullet points which covers the key points of the text.
              ```{text}```
              BULLET POINT SUMMARY:
           """

    prompt = PromptTemplate(template=template, input_variables=["text"])

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    return llm_chain.run(texts_FM1)

pdf_filepath = '/content/drive/MyDrive/Colab Notebooks/GenerativeAI-projects/6_extracted_FM-esg-report-2022.pdf'
print(summarize_pdf(pdf_filepath))


# Setting up the Interface using Gradio:

input_pdf_path = gr.components.Textbox(label="Provide the PDF file path")
output_summary = gr.components.Textbox(label="Summary")

interface = gr.Interface(
    fn=summarize_pdf,
    inputs=input_pdf_path,
    outputs=output_summary,
    title="PDF Summarizer",
    description="Provide PDF file path to get the summary."
).queue().launch(share=True, debug = True)

# Summarizing Large Documents Using Map Reduce

# !pip install pdfreader
# !pip install PyPDF2

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from typing_extensions import Concatenate

def summarize_large_pdf(pdf_filepath):
    
    # provide the path of  pdf file/files.
    pdfreader = PdfReader(pdf_filepath)

    # read text from pdf
    text = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            text += content
    llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0})
    print(f"The number of tokens: {llm.get_num_tokens(text)}")

    ## Splittting the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
    chunks = text_splitter.create_documents([text])
    print(f"length of chunks: {len(chunks)}")
    chain = load_summarize_chain(llm,chain_type='map_reduce',verbose=False)
    summary = chain.run(chunks)
    return summary 


pdf_filepath2 = "/content/drive/MyDrive/Colab Notebooks/GenerativeAI-projects/1_updated_FM-esg-report-2022.pdf"
summarize_large_pdf(pdf_filepath2)