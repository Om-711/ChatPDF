import streamlit as st
from function_chatbot_pdf import loader_fuc, retriever_fuc
import time
import tempfile
import base64
from streamlit_pdf_viewer import pdf_viewer

# consider st.session_state as a variable to store all the things page, content and
if "page" not in st.session_state:
    st.session_state.page = "home"

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "chat_history" not in st.session_state:#
    st.session_state.chat_history = []

def go_to_chat():
    st.session_state.page = "chat"

st.set_page_config(layout="wide")

if st.session_state.page == "home":
    st.title("Chat with PDF")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded_file is not None:
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(uploaded_file.getbuffer())
            file_path = tmp.name

        st.write(f"File saved at: {file_path}")
        st.session_state.uploaded_file = file_path
        with st.spinner("Loading...."):
            time.sleep(1.5)
            go_to_chat()
            st.rerun()

elif st.session_state.page == "chat":
    # st.title("Chat with PDF Bot")

    if st.session_state.uploaded_file is None:
        st.warning("Please upload a PDF first.")
        st.session_state.page = "home"
        st.rerun()
    
    else:

        col1, col2 = st.columns([1, 1])

        file_path = st.session_state.uploaded_file

        with col1:

            pdf_viewer(
                st.session_state.uploaded_file,
                width=700,
                height=800,
                zoom_level=1.0,                   
                viewer_align="center",             
                show_page_separator=True           
            )

        with col2:
            st.subheader("Ask Questions about your PDF")

            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])



            question = st.chat_input("Type your question here...")

        
            if question:
                if "doc_data" not in st.session_state:
                    with st.spinner("Thinking..."):
                        embeddings, chunks, doc = loader_fuc(st.session_state.uploaded_file)
                        st.session_state.doc_data = (embeddings, chunks, doc)

                embeddings, chunks, doc = st.session_state.doc_data

                st.session_state.chat_history.append({"role": "user", "content": question})

                
                with st.spinner("Thinking..."):
                    response = retriever_fuc(embeddings, chunks, doc, question)
                    # with st.chat_message("assistant"):
                    #     st.markdown(response)
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
            
            if st.button("New Chat"):
                st.session_state.chat_history = []
                st.rerun()
                    
                  
    # if st.button("Back to Home"):
    #     st.session_state.page = "home"
    #     st.rerun()
