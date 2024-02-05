# Summarize pdf document using OpenAI API and Langchain and Gradio UI

# import the required libraries
import gradio as gr
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFium2Loader
from langchain.llms import OpenAI

import openai
from configparser import ConfigParser

# Get the OpenAI API key in a config object:
config_object = ConfigParser()
config_object.read("config_genai.ini")
openai.api_key = config_object["OPENAI"]["openai_api_key"]

# LLM model:
llm = OpenAI(openai_api_key=openai.api_key, temperature=0)

# create the summarize function:
def summarize_pdf(pdf_file_path, custom_prompt=""):
    loader = PyPDFium2Loader(pdf_file_path)
    docs = loader.load_and_split()
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    return summary

def main():
    input_pdf_path = gr.components.Textbox(label="Enter the PDF file path")
    output_summary = gr.components.Textbox(label="Summary")

    iface = gr.Interface(
        fn=summarize_pdf,
        inputs=input_pdf_path,
        outputs=output_summary,
        title="PDF Summarizer",
        description="Enter the path to a PDF file and get its summary.",
    )

    iface.queue().launch(share=True, debug = False)
    
    
if __name__ == "__main__":
    main()