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



col1, col2 = st.columns([1, 3])

# # # Display the logo in the first column
# with col1:
#     st.image('scg_logo.jpg', width=100)

# # # Display the text in the second column
with col2:
    st.subheader("Hello! There, How can I help you Today-  :)")
       
    
    st.caption(":violet[what a] :orange[good day] :violet[to share what SCG is offering right now!]")
    
    
    st.set_page_config(page_title="Chat with the Streamlit docs, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
    st.title("KMUTT & SCG Chatbot")




# # add sidebar filters
# # st.sidebar.slider("Slider", 0, 100, 50)
# # st.sidebar.date_input("Date Input")
# # openai.api_key = st.secrets.openai_key
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
        
        service_context = ServiceContext.from_defaults(llm = Gemini(model="models/gemini-ultra"), embed_model=embed_model,)
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

# # for message in st.session_state.messages:
# #     with st.container():
# #         if message["role"] == "assistant":
# #             st.image('scg_logo.jpg', width=30)
# #             st.write("ChatBot:", message["content"])
# #         else:
# #             st.write("You:", message["content"])

# # If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history


# import streamlit as st
# import openai
# from llama_index.llms.openai import OpenAI
# from llama_index.llms.gemini import Gemini
# from llama_index.embeddings.gemini import GeminiEmbedding
# from llama_index.core import (
#     VectorStoreIndex, 
#     ServiceContext, 
#     Document, 
#     SimpleDirectoryReader
# )
# from streamlit_extras.app_logo import add_logo
# import google.generativeai as genai
# from llama_index.llms.huggingface import HuggingFaceLLM
# import torch
# import dotenv
# import os
# from llama_index.core import Settings
# from llama_index.core import PromptTemplate

# dotenv.load_dotenv()

# st.set_page_config(
#     page_title="SCG&KMUTT chatbot", 
#     page_icon=r"scg_logo.jpg", 
#     layout="centered", 
#     initial_sidebar_state="auto", 
#     menu_items=None
# )

# st.markdown(
#     """
#     <style>
#     body {
#         background-color: #e6f7ff;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# col1, col2 = st.columns([5, 1])

# with col1:
#     st.image('scg_logo.jpg', width=120)
#     st.header(":violet[SCG & KMUTT Chat]Bot", divider='rainbow', help="This bot is designed by Ujjwal Deep to address all of your questions hehe")

# st.subheader("Hello! There, How can I help you Today-  :)")
# st.caption(":violet[what a] :orange[good day] :violet[to share what SCG is offering right now!]")

# GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
# genai.configure(api_key=GOOGLE_API_KEY)

# if "messages" not in st.session_state.keys():
#     st.session_state.messages = [
#         {"role": "assistant", "content": "Ask me a question about Concrete technology"}
#     ]

# @st.cache_resource(show_spinner=False)
# def load_data():
#     with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
#         reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
#         docs = reader.load_data()
        
#         embed_model = GeminiEmbedding(
#             model_name="models/embedding-001", title="this is a document"
#         )

#         system_prompt = """# StableLM Tuned (Alpha version)
# - StableLM is a helpful and harmless open-source AI language model developed by StabilityAI.
# - StableLM is excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
# - StableLM is more than just an information source, StableLM is also able to write poetry, short stories, and make jokes.
# - StableLM will refuse to participate in anything that could harm a human.
# """

#         # This will wrap the default prompts that are internal to llama-index
#         query_wrapper_prompt = PromptTemplate("{query_str}")
#         llm = HuggingFaceLLM(
#             context_window=4096,
#             max_new_tokens=256,
#             generate_kwargs={"temperature": 0.7, "do_sample": False},
#             system_prompt=system_prompt,
#             query_wrapper_prompt=query_wrapper_prompt,
#             tokenizer_name="StabilityAI/stablelm-tuned-alpha-3b",
#             model_name="StabilityAI/stablelm-tuned-alpha-3b",
#             device_map="auto",
#             stopping_ids=[50278, 50279, 50277, 1, 0],
#             tokenizer_kwargs={"max_length": 4096},
#         )

#         # Set the embedding model and LLM in the Settings
#         Settings.embed_model = embed_model
#         Settings.llm = llm

#         # Initialize the vector store index with the embedding model
#         index = VectorStoreIndex.from_documents(docs)

#         return index

# index = load_data()

# if "chat_engine" not in st.session_state.keys():
#     st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# if prompt := st.chat_input("Your question"):
#     st.session_state.messages.append({"role": "user", "content": prompt})

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             response = st.session_state.chat_engine.chat(st.session_state.messages[-1]["content"])
#             st.write(response.response)
#             st.session_state.messages.append({"role": "assistant", "content": response.response})

