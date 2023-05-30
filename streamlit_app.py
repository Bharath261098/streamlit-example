import openai
import streamlit as st

from PIL import Image

# Configure OpenAI API
openai.api_key = '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'

image = Image.open('exl.png')

with st.sidebar:
    st.image(image, width = 150)
    st.header('Call Summarizer')

def generate_summary(text):
    prompt = "summarize the conversation provided and also suggest the next action item for the Customer and Executive:\n\n"
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
    return summary

def get_next_action_items(summary):
    customer_action_items = []
    executive_action_item = ""
    sentences = summary.split('. ')
    for sentence in sentences:
        sentence = sentence.strip()
        if 'customer' in sentence.lower():
            customer_action_items.append(sentence)
        if 'executive' in sentence.lower():
            executive_action_item = sentence
    return customer_action_items, executive_action_item

def main():
    st.title('Call Summarizer')
    st.write('Upload a text file to generate a summary and identify the next action items for the customer and executive.')

    uploaded_file = st.file_uploader('Upload File', type=['txt'])

    if uploaded_file is not None:
        content = uploaded_file.read().decode('utf-8')
        summary = generate_summary(content)
        customer_action_items, executive_action_item = get_next_action_items(summary)

        st.header('Summary')
        st.write(summary)

        st.header('Next Action Items')
        if len(customer_action_items) > 0:
            st.subheader('For the Customer')
            for item in customer_action_items:
                st.write(f'- {item}')
        else:
            st.write('No customer action items identified.')

        if executive_action_item:
            st.subheader('For the Executive')
            st.write(f'- {executive_action_item}')
        else:
            st.write('No executive action item identified.')

if __name__ == '__main__':
    main()
