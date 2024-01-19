#!/usr/bin/env python
# coding: utf-8

# #### Document summarization application Falcon LLM using Sagemaker Jumpstart

### Author : Dipjyoti Das
### Last Edited : Jan 19, 2024

### This script provides an example for how to use Sagemaker Jumpstart -for text summarization use case. It used Falcon 7B open source model 
### from Jumsptart model hub with Langchain.

# #### Prerequisites

#### AWS Innovation Sandbox should be installed and Domain created in Sagemaker

# #### Deploy Falcon 7B using Sagemaker Jumpstart

# To deploy your model, complete the following steps:
# 
# 1. Navigate to your SageMaker Studio environment from the SageMaker console.
# 2. Within the IDE, under SageMaker JumpStart in the navigation pane, choose Models, notebooks, solutions.
# 3. Deploy the Falcon 7B Instruct model to an endpoint for inference
# 4. Choose Open notebook.
# 5. Run the first four cells of the notebook to deploy the Falcon 7B Instruct endpoint.You can see your deployed JumpStart models on the Launched JumpStart assets page.
# 6. In the navigation pane, under SageMaker Jumpstart, choose Launched JumpStart assets.
# 7. Choose the Model endpoints tab to view the status of your endpoint.

## If you get ResouceLimitExceeded error for deplying the model endpoint for a particular instance (ex : 'ml.g5.2xlarge' etc), 
## please contatct AWS admin to raise a ticket and raise the account level service limit Instances.

# In[41]:


# Import the Boto3 and JSON modules
import json
import boto3

import warnings
warnings.filterwarnings('ignore')


# In[40]:


# define a function that will call the endpoint. This function takes a dictionary payload and uses it to invoke the SageMaker runtime client. 
# Then it deserializes the response and prints the input and generated text.

newline, bold, unbold = '\n', '\033[1m', '\033[0m'

# get the endpoint after the model is deployed in Jumpstart
endpoint_name ='hf-llm-falcon-7b-instruct-bf16-2024-01-19-14-57-58-026'

def query_endpoint(payload):
    client = boto3.client('runtime.sagemaker')
    response = client.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/json', Body=json.dumps(payload).encode('utf-8'))
    model_predictions = json.loads(response['Body'].read())
    generated_text = model_predictions[0]['generated_text']
    print (
        f"Input Text: {payload['inputs']}{newline}"
        f"Generated Text: {bold}{generated_text}{unbold}{newline}")


# In[24]:


# payload includes the prompt as inputs, together with the inference parameters that will be passed to the model.
# We can use these parameters with the prompt to tune the output of the model for your use case:
payload = {
    "inputs": "Girafatron is obsessed with giraffes, the most glorious animal on the face of this Earth. Giraftron believes all other animals are irrelevant when compared to the glorious majesty of the giraffe.\nDaniel: Hello, Girafatron!\nGirafatron:",
    "parameters":{
        "max_new_tokens": 50,
        "return_full_text": False,
        "do_sample": True,
        "top_k":10
        }
}


# #### Query with a summarization prompt

# In[ ]:


# Create a sample text document (document to summarize) in your present directory - document.txt


# In[25]:


#  create a function that uses prompt engineering techniques to summarize document.txt

def summarize(text_to_summarize):
    summarization_prompt = """Process the following text and then perform the instructions that follow:

{text_to_summarize}

Provide a short summary of the preceeding text.

Summary:"""
    payload = {
        "inputs": summarization_prompt,
        "parameters":{
            "max_new_tokens": 150,
            "return_full_text": False,
            "do_sample": True,
            "top_k":10
            }
    }
    response = query_endpoint(payload)


# * For longer documents, an error might appear. Falcon and all other LLMs, has a limit on the number of tokens passed as input. We can get around this limit using LangChain’s enhanced summarization capabilities, which allows for a much larger input to be passed to the LLM.

# In[27]:


def summarize(text_to_summarize):
    summarization_prompt = """Process the following text and then perform the instructions that follow:

{text_to_summarize}

Provide a short summary of the preceeding text.

Summary:"""
    payload = {
        "inputs": summarization_prompt,
        "parameters":{
            "max_new_tokens": 150,
            "return_full_text": False,
            "do_sample": True,
            "top_k":10
            }
    }
    response = query_endpoint(payload)
    print(response)
    
with open("document.txt") as f:
    text_to_summarize = f.read()


# In[28]:


summarize(text_to_summarize)


# * For longer documents, an error might appear. Falcon and all other LLMs, has a limit on the number of tokens passed as input. We can get around this limit using LangChain’s enhanced summarization capabilities, which allows for a much larger input to be passed to the LLM.

# #### Import and run a summarization chain

# In[42]:


get_ipython().system('pip install langchain')
get_ipython().system('pip install transformers')


# In[26]:


ls


# In[30]:


# Import the relevant modules and break down the long document into chunks:
import langchain
from langchain import SagemakerEndpoint, PromptTemplate
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size = 500,
                    chunk_overlap  = 20,
                    separators = [" "],
                    length_function = len
                )
input_documents = text_splitter.create_documents([text_to_summarize])


# In[31]:


# To make LangChain work effectively with Falcon, we need to define the default content handler classes for valid input and output:

class ContentHandlerTextSummarization(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs={}) -> bytes:
        input_str = json.dumps({"inputs": prompt, **model_kwargs})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> json:
        response_json = json.loads(output.read().decode("utf-8"))
        generated_text = response_json[0]['generated_text']
        return generated_text.split("summary:")[-1]
    
content_handler = ContentHandlerTextSummarization()


# In[32]:


# We can define custom prompts as PromptTemplate objects, the main vehicle for prompting with LangChain, for the map-reduce summarization approach.
# This is an optional step because mapping and combine prompts are provided by default if the parameters within the call to load the summarization chain
# (load_summarize_chain) are undefined.

map_prompt = """Write a concise summary of this text in a few complete sentences:

{text}

Concise summary:"""

map_prompt_template = PromptTemplate(
                        template=map_prompt, 
                        input_variables=["text"]
                      )


combine_prompt = """Combine all these following summaries and generate a final summary of them in a few complete sentences:

{text}

Final summary:"""

combine_prompt_template = PromptTemplate(
                            template=combine_prompt, 
                            input_variables=["text"]
                          ) 


# In[33]:


# LangChain supports LLMs hosted on SageMaker inference endpoints, so instead of using the AWS Python SDK, we can initialize the
# connection through LangChain for greater accessibility:
summary_model = SagemakerEndpoint(
                    endpoint_name = endpoint_name,
                    region_name= "us-east-1",
                    model_kwargs= {},
                    content_handler=content_handler
                )


# In[39]:


# load in a summarization chain and run a summary on the input documents using the following code:
summary_chain = load_summarize_chain(llm=summary_model,
                                     chain_type="map_reduce", 
                                     map_prompt=map_prompt_template,
                                     combine_prompt=combine_prompt_template,
                                     verbose=False
                                    ) 
summary = summary_chain({"input_documents": input_documents, 'token_max': 700}, return_only_outputs=True)
print(summary["output_text"])  


# In[37]:


endpoint_name


# In[ ]:


# delete the inference endpoint to avoid incurring unnecessary costs 
client = boto3.client('runtime.sagemaker')
client.delete_endpoint(EndpointName=endpoint_name)

