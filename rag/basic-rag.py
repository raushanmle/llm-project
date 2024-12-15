# RAG
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
load_dotenv(".env")
groq_api_key = os.getenv("GROQ_API_KEY")

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

llm = ChatGroq(groq_api_key=groq_api_key, model="Llama3-8b-8192")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents, embedding=embeddings)
retriever = vectorstore.as_retriever(
    search_type="similarity", search_kwargs={"k": 1})

vectorstore.similarity_search("cat")
retriever.batch(["cat", "dog"])

message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""
prompt = ChatPromptTemplate.from_messages([("human", message)])
rag_chain = {"context": retriever,
             "question": RunnablePassthrough()} | prompt | llm
response = rag_chain.invoke("tell me about cat")
print(response.content)
