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


def main():
    st.title('Service Call Summarizer')
    st.write('Upload text files to generate a summary and identify the next action items.')

    uploaded_files = st.file_uploader('Upload Files', type=['txt'], accept_multiple_files=True)

    if uploaded_files:
        summaries = []
        customer_action_items = []
        executive_action_items = []

        files = []
        for uploaded_file in uploaded_files:
            file_info = {
                'name': uploaded_file.name,
                'content': uploaded_file.read().decode('utf-8')
            }
            files.append(file_info)

        # Sort files based on the file names
        files.sort(key=lambda x: ('raised' in x['name'], 'followup' in x['name'], 'settled' not in x['name']))

        for file_info in files:
            content = file_info['content']
            summary = generate_summary(content)
            summaries.append(summary)

            file_customer_action_items, file_executive_action_item = get_next_action_items(summary)
            customer_action_items.extend(file_customer_action_items)
            if file_executive_action_item:
                executive_action_items.append(file_executive_action_item)

        final_summary = '\n'.join(summaries)

        st.header('Summary')
        st.write(final_summary)

        st.header('Action Items')
        if len(customer_action_items) > 0:
            st.subheader('For the Customer')
            for item in customer_action_items:
                st.write(f'- {item}')
        else:
            st.write('No customer action items identified.')

        if len(executive_action_items) > 0:
            st.subheader('For the Executive')
            for item in executive_action_items:
                st.write(f'- {item}')
        else:
            st.write('No executive action items identified.')

if __name__ == '__main__':
    main()
