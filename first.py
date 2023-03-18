import streamlit as st
from main import page1
from page2 import page2

def main():
    st.set_page_config(page_title='My Streamlit App')
    st.title('Welcome')
    menu = ['Page 1', 'Page 2']
    choice = st.sidebar.selectbox('Select a page', menu)
    if choice == 'Page 1':
        page1()
    elif choice == 'Page 2':
        page2()

if __name__ == '__main__':
    main()
