from azure.core.credentials import AzureKeyCredential
import os
from openai import AzureOpenAI




####################################### Azure_AI Search ##################################
AZURE_COGNITIVE_SEARCH_INDEX_NAME = "askhr_index_updated"
AZURE_COGNITIVE_SEARCH_SERVICE_NAME = "yashdsaisearchnew"
AZURE_COGNITIVE_SEARCH_API_KEY = "eurTCkGYgf5OF3NajVCjozA0q5ytMo6rEECElphy8WAzSeAhxIDL"
AZURE_COGNITIVE_SEARCH_ENDPOINT = "https://yashdsaisearchnew.search.windows.net"
azure_credential = AzureKeyCredential(AZURE_COGNITIVE_SEARCH_API_KEY)
####################################### Azure_AI Search ##################################


####################################### Azure OpenAI ##################################
OPENAI_API_KEY = "Fo56HALgs49s02qp8qk98N02rJJrXkKkAgEPIqaUFzYIpMjm3ERlJQQJ99ALACfhMk5XJ3w3AAABACOGvpSh"
OPENAI_API_ENDPOINT = "https://azureopenaiyashmpn.openai.azure.com/"
OPENAI_API_VERSION = "2023-09-01-preview"
GPT4omini = "gpt-4o-mini"
GPT4o = "gpt-4o"
EMBEDDING_MODEL_Large = "text-embedding-3-large"
KEEP_PREVIOUS_MESSAGES = 5

client = AzureOpenAI(
    api_key = OPENAI_API_KEY,  
    api_version = OPENAI_API_VERSION,
    azure_endpoint = OPENAI_API_ENDPOINT
)

####################################### Azure OpenAI ##################################
KEEP_PREVIOUS_MESSAGES = 5




system_message_query_generation_for_retriver = """
You are a very good text analyzer.
You will be provided a chat history and a user question.
The question and history can be in any language. But you have to generate search query in english.
You task is generate a search query that will return the best answer from the knowledge base.
Try and generate a grammatical sentence for the search query.
Do NOT use quotes and avoid other search operators.
Do not include cited source filenames and document names such as info.txt or doc.pdf in the search query terms.
Do not include any text inside [] or <<>> in the search query terms.
"""



# system_message_query_generation_for_retriver = """
# You are a very good text analyzer.
# You will be provided a chat history and a user question.
# You task is generate a search query that will return the best answer from the knowledge base.
# Try and generate a grammatical sentence for the search query.
# Do NOT use quotes and avoid other search operators.
# Do not include cited source filenames and document names such as info.txt or doc.pdf in the search query terms.
# Do not include any text inside [] or <<>> in the search query terms.
# """

system_message_for_response_generation_URL = """

You are a very intelligent assistant who provides answers of user's queries on Yash Technologies policies etc.
You have to use your intelligence at most to generate the answer from the given sources. if you don't have enough information in the provided sources to generate the answer say You don't have information to answer that question. You can not generate anything that is not in the provided sources.
If user's question is Hi, hello, Thanks etc. Then respond friendly show gratitude and ask how can i assist you more in helping their getting queries resolved related to Yash tecnologies policies.
You have to first analyze the query and decide in which language the user is asking a query and reply in same language. 
Once you are done with generating the answer if available always refrence the url of that document by saying for more dtails user can visit the url. 

"""

system_message_for_response_generation_without_URL = """

You are a very intelligent assistant who provides answers of user's queries on Yash Technologies policies etc.
You have to use your intelligence at most to generate the answer from the given sources. if you don't have enough information in the provided sources to generate the answer say You don't have information to answer that question. You can not generate anything that is not in the provided sources.
If user's question is Hi, hello, Thanks etc. Then respond friendly show gratitude and ask how can i assist you more in helping their getting queries resolved related to Yash tecnologies policies.
Your reply shpuld be in same language in which user is asking query. 

"""


# system_message_for_response_generation = """

# You are a intelligent assistant who provides answers of user's queries on Yash Technologies policies etc.
# You have to use your intelligence generate the answer from the given sources. if you don't have enough information in the provided sources to generate the answer say You don't have information to answer that question. You can not generate anything that is not in the provided sources.
# If user's question is Hi, hello, Thanks etc. Then respond friendly show gratitude and ask how can i assist you more. Don't provide any source document.
# Your reply shpuld be in same language in which user is asking query. 
# Once you are done with generating the answer always Reference sources by including at least 2 new line characters followed by the source and url in square brackets, like this: "\n\n [Source : info.txt, \n URL : URL_OF_SOURCE]". Provide sources only if you are taking text from there to generate answer. if not don't provide any source.

# """


def generate_embeddings_azure_openai(text = " ",model = " "):
    """ Function for gerating Embedding of a Text. 

    Input Parameters :
    -------------------------
    text = str
            text that needs to be embedded

    model = str
            Embedding model deployememt name in OpenAi studio
    

    Returns :
    -------------------------
    Embedding : List[1536 float values]
                a list which contains the generated embedding for the given text

    
    """

    client = AzureOpenAI(
    api_key = OPENAI_API_KEY,  
    api_version = OPENAI_API_VERSION,
    azure_endpoint = OPENAI_API_ENDPOINT
    )
    response = client.embeddings.create(
        input = text,
        model= EMBEDDING_MODEL_Large 
    )
    return response.data[0].embedding



def call_gpt_model(model= " ",
                   messages= [],
                   temperature=0.1,
                    max_tokens = 700,
                    stream = True):
    
    """ Function for calling GPT 35 model.

    Input Parameters :
    -------------------------
    model = str
            GPT 35 deployement name is OpenAI studio.

    Messages = List of dicts [{ }, { }]
               Example : For a question "Who were the founders of Microsoft?" We have to send the question in given format.
               messages=[
                            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                            {"role": "user", "content": "Who were the founders of Microsoft?"}
                        ]

    temprature = float
                 How much temprature we want to use

    max_tokens = int
                 Maximum new tokens can be generated in a single model call.

    stream : Bool
             The response needs to be streamed or not. If True we will have to run the returned object in loop.
             If False then we can just simply extrcat the text from response object
    

    Returns :
    -------------------------
    response_obj : An Object that has the model's response. 

    """
    client = AzureOpenAI(
    api_key = OPENAI_API_KEY,  
    api_version = OPENAI_API_VERSION,
    azure_endpoint = OPENAI_API_ENDPOINT
    )
    response = client.chat.completions.create(model=model,
                                              messages=messages,
                                              temperature = temperature,
                                              max_tokens = max_tokens,
                                              stream= stream,seed=999)

    return response



