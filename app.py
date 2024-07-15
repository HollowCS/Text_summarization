import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    ChatMessage
    )
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.globals import set_llm_cache, get_llm_cache
import streamlit as st


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(api_key=api_key, model="Gemma-7b-It")


def get_text_from_user(speech):
    chat_message = [
        SystemMessage(content="You are an expert with an expertise in summarizing"),
        HumanMessage(content=f"please provide a short and concise summary of a following speech:\n text: {speech}")
    ]
    genericPromptTemplate = """
        Write a summary of the follwing speech : {speech}
        Translate the precise summary to {language}"""

    prompt = PromptTemplate(
        input_variables=['speech', 'language'],
        template=genericPromptTemplate
    )
    prompt.format(speech='speech', language='bengali')
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    summary = llm_chain.run({'speech':speech, 'language': 'bengali'})

    return summary


st.header("summarize AI")

# initializing session state

if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Paste here: ")
if prompt:

    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response =""
        response_generator = get_text_from_user(prompt)
        for word in response_generator:
            response += word
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})