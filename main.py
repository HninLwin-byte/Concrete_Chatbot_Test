import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import (
    VectorStoreIndex, 
    ServiceContext, 
    Document, 
    SimpleDirectoryReader
)
from streamlit_extras.app_logo import add_logo
import google.generativeai as genai

import dotenv,os
dotenv.load_dotenv()


st.set_page_config(page_title="SCG&KMUTT", page_icon=r"scg_logo.jpg", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.markdown(
    """
    <style>
    body {
        background-color: #e6f7ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([5, 1])

# Display the logo in the first column
with col1:
    st.image('scg_logo.jpg', width=120)
    
    
    st.header(":violet[SCG & KMUTT Chat]Bot",divider='rainbow', help = "This bot is designed by Ujjwal Deep to address all of your questions hehe")




    st.subheader("Hello! There, How can I help you Today-  :)")
       
    
    st.caption(":violet[what a] :orange[good day] :violet[to share what SCG is offering right now!]")
    
    
 



GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
# # openai.api_key = st.secrets.openai_key


if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Concrete technology"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        # llm = OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert o$
        # index = VectorStoreIndex.from_documents(docs)
        # service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."))
        embed_model = GeminiEmbedding(
            model_name="models/embedding-001", title="this is a document"
            )
        
        service_context = ServiceContext.from_defaults(llm = Gemini(model="models/gemini-pro"), embed_model=embed_model,)
        #service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python library. Keep your answers technical and based on facts – do not hallucinate features."))
        #service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=None)
       

        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


# # If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history


