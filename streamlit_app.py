import openai
import re
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

def extract_claim_number(file_name):
    match = re.search(r'claim(\d+)', file_name)
    if match:
        return int(match.group(1))
    return 0

def main():
    st.title('Service Call Summarizer')
    st.write('Upload text files to generate a summary and identify the next action items.')

    uploaded_files = st.file_uploader('Upload Files', type=['txt'], accept_multiple_files=True)
    uploaded_files = sorted(uploaded_files, key=lambda file: extract_claim_number(file.name))

    if uploaded_files:
        content = ""
        for file in uploaded_files:
            content += file.read().decode('utf-8') + "\n"

        summary = generate_summary(content)
        customer_action_item, executive_action_item = get_next_action_items(summary)

        st.header('Summary')
        st.write(summary)

        st.header('Action Items')
        if customer_action_item:
            st.subheader('For the Customer')
            st.write(f'- {customer_action_item}')
        else:
            st.write('No customer action item identified.')

        if executive_action_item:
            st.subheader('For the Executive')
            st.write(f'- {executive_action_item}')
        else:
            st.write('No executive action item identified.')

if __name__ == '__main__':
    main()
