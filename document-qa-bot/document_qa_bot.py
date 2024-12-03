
############ QA bot form Text file #################

from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings


# Load the data
loader = TextLoader("speech.txt")
data = loader.load()

# Split the data into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(data)

# Create a vectordb
embedding=OllamaEmbeddings(model = "llama3")
vectordb=Chroma.from_documents(documents=splits,embedding=embedding)


## query it
query = "What does the speaker believe is the main reason the United States should enter the war?"
docs = vectordb.similarity_search(query)
docs[0].page_content


## Saving to the disk
vectordb=Chroma.from_documents(documents=splits, embedding=embedding,persist_directory="./chroma_db")



# load from disk
db2 = Chroma(persist_directory="./chroma_db", embedding_function=embedding)
docs=db2.similarity_search(query)
print(docs[0].page_content)


## similarity Search With Score
docs = vectordb.similarity_search_with_score(query)
print(docs)


### Retriever option
retriever=vectordb.as_retriever()
retriever.invoke(query)[0].page_content


#################### QA bot form PDF file ####################

## Reading a PDf File
from langchain_community.document_loaders import PyPDFLoader
loader=PyPDFLoader('attention.pdf')
docs=loader.load()

# Split the data into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(docs)

# Create a vectordb
embedding=OllamaEmbeddings(model = "llama3")
vectordb=Chroma.from_documents(documents=splits,embedding=embedding)

## query it
query = "what is main abstract?"
docs = vectordb.similarity_search(query)
print(docs[0].page_content)




