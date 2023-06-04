import streamlit as st

# Define the table data
table_data = [
    ['2023-05-28', 'John Doe', 'Health Insurance', 'Claim description 1', 'Action item 1', '$1000', 'In progress'],
    ['2023-05-29', 'Jane Smith', 'Auto Insurance', 'Claim description 2', 'Action item 2', '$2000', 'Approved'],
    ['2023-05-30', 'Mike Johnson', 'Home Insurance', 'Claim description 3', 'Action item 3', '$1500', 'Denied']
]

def display_table():
    st.title('Claim Management System')
    st.header('Claims')
    
    # Display the table
    st.table(table_data)

def main():
    st.set_page_config(page_title='Service Call Summarizer')
    st.sidebar.title('Sidebar')
    st.sidebar.image('logo.png', width=150)
    page = st.sidebar.radio('Navigation', ['Summary', 'Claims'])
    
    if page == 'Summary':
        st.title('Service Call Summarizer')
        st.write('Upload text files to generate a summary and identify the next action items.')

        uploaded_files = st.file_uploader('Upload Files', type=['txt'], accept_multiple_files=True)
        # Rest of the code for generating summary and action items
    elif page == 'Claims':
        display_table()

if __name__ == '__main__':
    main()
