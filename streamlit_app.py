import openai
import streamlit as st

# Configure OpenAI API
openai.api_key = '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'

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
    action_items = []
    sentences = summary.split('. ')
    for sentence in sentences:
        sentence = sentence.strip()
        if 'customer' in sentence.lower():
            action_items.append(sentence)
        if 'executive' in sentence.lower():
            action_items.append(sentence)
    return action_items

def main():
    st.title('Text Summarizer')
    st.write('Upload a text file to generate a summary and identify next action items.')

    uploaded_file = st.file_uploader('Upload File', type=['txt'])

    if uploaded_file is not None:
        content = uploaded_file.read().decode('utf-8')
        summary = generate_summary(content)
        action_items = get_next_action_items(summary)

        st.header('Summary')
        st.write(summary)

        st.header('Next Action Items')
        if len(action_items) > 0:
            for item in action_items:
                st.write(f'- {item}')
        else:
            st.write('No action items identified.')

if __name__ == '__main__':
    main()
