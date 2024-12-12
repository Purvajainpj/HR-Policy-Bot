import os
import time
from creds import system_message_query_generation_for_retriver,system_message_for_response_generation_URL
from creds import call_gpt_model,KEEP_PREVIOUS_MESSAGES,system_message_for_response_generation_without_URL
#from retreive_chroma import get_similiar_content_chromadb
from retrieve_azure_si_search import get_similiar_content_azure


## This file can be used to generate response given a user query. 


def generate_query_for_retriver(user_query = " ",messages = [],model=" "):

    """ Function to generate search query for retriver given a conversation history.

    Input Parameters :
    -------------------------
    user_query = str
                 User's query

    messages = List of dicts [{ }, { }]
               Previous conversation history.
    
    Returns : 
    -------------------------
    query_for_retriver : str
                         Query that can be used to search in Knowledge base. 
    
    """

    start = time.time()
    user_message = """Chat History:
    {chat_history}

    Question:
    {question}

    Search query:"""

    user_message = user_message.format(chat_history=str(messages), question=user_query)

    chat_conversations_for_query_generation_for_retriver = [{"role" : "system", "content" : system_message_query_generation_for_retriver}]
    chat_conversations_for_query_generation_for_retriver.append({"role": "user", "content": user_message })

    try:                                
        response = call_gpt_model(messages = chat_conversations_for_query_generation_for_retriver,model= model,stream=False)
    except:
        if model == "YashGPT35Turbo" :
            response = call_gpt_model(messages = chat_conversations_for_query_generation_for_retriver, model = "YashGPT35Turbo16k",stream=False)
        else :
            response = call_gpt_model(messages = chat_conversations_for_query_generation_for_retriver,model = "YashGPT4_32K",
                                               stream=False)
       
    response = response.choices[0].message.content
    #print("-"*100)
    #print("Generated Query for Retriver in :", time.time()-start,'seconds.')
    print("Generated Query for Retriver is :",response)
    print("-"*100)

    return response


def generate_response_with_memory(user_query=" ", stream=True,model= " ",previous_history = [],Location = " ",retriver = "azure"):


    """Function to generate response given a user's Query.

    Input Parameters :
    -------------------------
    user_query = str
                 User's query
    dropdown_3_prompt = str
                        dropdown_3_prompt
                 
    system_message_for_response_generator = str
                                            Prompt for generating the response
    previous_data_list = []
                         Previous Conversations

    Returns :
    -------------------------
    response_list : model's response.

    
    """
    print("User's Query : ",user_query )
    query_for_retriver = generate_query_for_retriver(user_query=user_query,messages = previous_history,model=model)    
    if retriver == "azure":
        similiar_docs,use_url_prompt = get_similiar_content_azure(query_for_retriver,Location = Location)
    if retriver == "chromadb":
        similiar_docs,use_url_prompt = get_similiar_content_chromadb(query_for_retriver,Location = Location)
        
    user_content = user_query + " \nSOURCES:\n" + similiar_docs
    
    if use_url_prompt : 
        system_message = system_message_for_response_generation_URL
    else : 
        system_message = system_message_for_response_generation_without_URL

    previous_conversations_to_send_for_memory_response =  [{"role" : "system", "content" : system_message}] + previous_history[-10:] + [{"role":"user","content" : user_content}]
    
    #response_from_model = call_gpt_model(messages = previous_conversations_to_send_for_memory_response,model= model)
                                   
    response_from_model = call_gpt_model(messages = previous_conversations_to_send_for_memory_response,model= model)

    return response_from_model,previous_conversations_to_send_for_memory_response
