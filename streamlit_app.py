import openai
import streamlit as st
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from PIL import Image

# Configure OpenAI API
llm = OpenAI(api_token=st.secrets["chat_gpt_key"])
pandas_ai = PandasAI(llm, conversational=False)

image = Image.open('exl.png')

with st.sidebar:
    st.image(image, width = 150)
    st.header('Service Call Summarizer')

def generate_summary(text):
    prompt = "summarize the conversation in bullet points and also suggest one action item for the Customer and the Executive:\n\n"
    prompt += text
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        temperature=0.5,
        n=1,
        stop=None,
        top_p=None,
        frequency_penalty=0.2,
        presence_penalty=0.8
    )
    summary = response.choices[0].text.strip()
    summary = summary.replace("Summarized Conversation:\n\n", "")  # Remove the title
    return summary

def get_next_action_items(summary):
    customer_action_item = ""
    executive_action_item = ""

    sentences = summary.split('. ')
    for sentence in sentences:
        sentence = sentence.strip()
        if 'customer' in sentence.lower() and not sentence.startswith("Summary"):
            customer_action_item = sentence
            break
        if 'executive' in sentence.lower() and not sentence.startswith("Summary"):
            executive_action_item = sentence
            break
    return customer_action_item.strip('*'), executive_action_item.strip('*')
