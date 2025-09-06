from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
# from langchain.chains import RunnableWithHistory
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import tempfile

load_dotenv()

def loader_fuc(path_location):
    loader = PyPDFLoader(path_location)

    doc = loader.load()

    t = [f"{idx}:{t.page_content}" for idx,t in enumerate(doc)]
    text = "".join(t) # bhai ye se string me text join kiya tune bhul mat jana
    
    # If you just split by page or fixed characters ( every 1000 characters), you may cut in the middle of a heading, sentence, or bullet point ..-> making chunks harder for embeddings to capture meaning.
    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=150)

    chunks = splitter.create_documents([text])

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    return embedding, chunks, doc


def retriever_fuc(embedding, chunks, doc, question):

    vector_store = FAISS.from_documents(chunks, embedding)

    retriever = vector_store.as_retriever(search_type = "mmr", search_kwargs={"k" : 15})

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    
    prompt = PromptTemplate(
        template= """

            You are a helpfull assistant.
            Answer all the questions using only the  content.If the context is insufficient to answer the question Just say, answer not 
            found in the context.Along with answering the question also give the reference from which you have answered the question like pages number
            or same context from the pdf. Answer according to for question like Hi, Hello, etc like starting gesture types.

        
            Context: {content}

            chat_history : {chat_history}
            Questions : {question}
            Answer :
        """,
        input_variables=["chat_history", "content", "question"]
    )
    # 
    retriever_doc = retriever.invoke("Give me complete context of the pdf! and what is the topic of the pdf")

    content = "".join(docs.page_content for docs in doc)

    chat_history = "Empty"

    final_prompt = prompt.invoke({"chat_history":chat_history,'content':content, 'question':question})

    parser = StrOutputParser()

    memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")
    chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

    response = chain.invoke({'content' : content, 'question' : question})

    return response['text']


