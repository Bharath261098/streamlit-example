def main():
    st.title('Service Call Summarizer')
    st.write('Upload text files to generate a summary and identify the next action items.')

    uploaded_files = st.file_uploader('Upload Files', type=['txt'], accept_multiple_files=True)

    if uploaded_files:
        summaries = []
        customer_action_items = []
        executive_action_items = []

        for uploaded_file in uploaded_files:
            content = uploaded_file.read().decode('utf-8')
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
