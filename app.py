import streamlit as st
from creds import GPT4o,GPT4omini,KEEP_PREVIOUS_MESSAGES
from generate_response import generate_response_with_memory
from time import sleep
import tiktoken


def authenticate(email,password):
    valid_password = "sampleapp@123"
    valid_mails = ["user@India.com","user@USA.com","user@German.com","user@Dutch.com","user@Polish.com","user@Swedish.com"]
    if password == valid_password :
        if email in valid_mails:
            Location = email.split("@")[1].split(".")[0]
            st.session_state.Location = Location
        return True
    else: 
        return False
# Session state initialization
if 'logged_in' not in st.session_state:
   st.session_state.logged_in = False
# Login Pages
login = st.sidebar.checkbox("Login")
if login and not st.session_state.logged_in:
   st.sidebar.title("Login")
   email = st.sidebar.text_input("Email")
   password = st.sidebar.text_input("Password", type="password")
   if st.sidebar.button("Login"):
       if authenticate(email,password):
           st.session_state.logged_in = True
           st.experimental_rerun()
       else:
           st.sidebar.error("Invalid Credentials. Please try again..")
# Check if the user is logged in before proceeding
if not st.session_state.logged_in:
   st.warning("Please log in to use the Yash Hr Policy Bot.")
   st.stop()  # Stop further execution if not logged in


            
email = st.sidebar.selectbox('Select Location',("user@India.com","user@USA.com","user@German.com", "user@Dutch.com","user@Polish.com", "user@Swedish.com"))

# Location = email.split("@")[1].split(".")[0]
# st.session_state.Location = Location


    

st.title("Ask-HR Bot")


logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTM5pKR86mq9HfmpD5gDi-gcToaiPblCecAKQ&s"
logo_html = f'<img src="{logo_url}" alt="Logo" height="130" width="250">'
st.sidebar.markdown(f'<div class="logo-container">{logo_html}</div>', unsafe_allow_html=True)



model = st.sidebar.selectbox('Select Model',("GPT4o","GPT-4omini"))

if model == "GPT4o":
    model_to_use  = GPT4o

if model == "GPT-4omini":
    model_to_use  = GPT4omini
    

# retriver = st.sidebar.selectbox('Select VectorDB',("Azure","ChromaDB(Free)"))

# if retriver == "Azure":
#     retriver_to_use  = "azure"

# if retriver == "ChromaDB(Free)":
#     retriver_to_use  = "chromadb"


retriver_to_use =  "azure"                                         
    
use_memory = True
if use_memory:
    #st.session_state.messages = []
    if st.sidebar.button(':red[Clear History]'):
        st.session_state.memory_messages = []
        st.session_state.messages = []
        
if "cost" not in st.session_state:
    st.session_state.cost = 0.00 
if "Prompt_Tokens" not in st.session_state:
    st.session_state.Prompt_Tokens = 0
if "Output_Tokens" not in st.session_state:
    st.session_state.Output_Tokens = 0

if "encoding" not in st.session_state:
    st.session_state.encoding = tiktoken.get_encoding("cl100k_base")     
    
if "memory_messages" not in st.session_state:
    st.session_state.memory_messages = []
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello User From " +st.session_state.Location + ". How can i help you." })
    for message in st.session_state.messages:
        with st.chat_message(message["role"],avatar = "🤖" ):
            st.markdown(message["content"])

else:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            avatar = "🤖"
        else:
            avatar = "🧑‍💻"
        with st.chat_message(message["role"],avatar = avatar ):
            st.markdown(message["content"])
            
            
# User input
if prompt := st.chat_input("Please type your query here.?"):
    # Display user message in chat message container
    st.chat_message("user",avatar = "🧑‍💻").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    user_query = prompt
    if use_memory:
        response,messages = generate_response_with_memory(user_query= user_query,
                                                 stream=True,
                                                 model=model_to_use,
                                                 previous_history = st.session_state.memory_messages[-KEEP_PREVIOUS_MESSAGES:],
                                                 Location = st.session_state.Location)
        

    print("##"*100)

    with st.chat_message("assistant",avatar = "🤖"):
        message_placeholder = st.empty()
        full_response = " "
        for chunk in response:
            if len(chunk.choices) >0:
                if str(chunk.choices[0].delta.content) != "None":                     
                    for char in chunk.choices[0].delta.content:
                        full_response += char
                        sleep(0.00001) 
                    message_placeholder.markdown(full_response + "▌")
                             
        

        prompt_tokens = len(st.session_state.encoding.encode(str(messages))) 
        #print("prompt_tokens :",prompt_tokens)
        
        completion_tokens = len(st.session_state.encoding.encode(full_response))
        
        if chunk.model == "gpt-4o-2024-08-06":
            rate_prompt_tokens_per_1000 = 0.00250 
            rate_completion_tokens_per_1000 = 0.01000
        
        if chunk.model == "gpt-4o-mini":
            rate_prompt_tokens_per_1000 = 0.000150
            rate_completion_tokens_per_1000 = 0.000600

        cost_prompt_tokens = (prompt_tokens / 1000) * rate_prompt_tokens_per_1000

        cost_completion_tokens = (completion_tokens / 1000) * rate_completion_tokens_per_1000

        total_cost = st.session_state.cost + cost_completion_tokens + cost_prompt_tokens
        st.session_state.cost = total_cost 
        
        st.session_state.Prompt_Tokens = st.session_state.Prompt_Tokens + prompt_tokens 
        st.session_state.Output_Tokens = st.session_state.Output_Tokens + completion_tokens

        pricing_string = "\n **Promt Tokens used in this session :** " +str(st.session_state.Prompt_Tokens) + " \n **Completion Tokens used in this session:** " +str(st.session_state.Output_Tokens) + " \n **Cost of this session :** " +"$"+str(st.session_state.cost)[:10]

        message_placeholder.markdown(full_response + "\n" + pricing_string)
  
    st.session_state.memory_messages.append({"role": "user", "content": user_query})
    st.session_state.memory_messages.append({"role": "assistant", "content": full_response})
        
    st.session_state.messages.append({"role": "assistant", "content": full_response+ "\n" + pricing_string})
    
    
