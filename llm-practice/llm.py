from langchain_community.llms import Ollama

llm=Ollama(model="llama3.2")

llm.invoke("Come up with 10 names for a song about parrots")

from langchain_ollama import OllamaLLM

model = OllamaLLM(model="llama3")
model.invoke("Come up with 10 names for a song about parrots")


from langchain.embeddings import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="llama3")
text = "This is a sample query."
query_result = embeddings.embed_query(text)
print(query_result)
print(len(query_result))

words = ["cat", "dog", "computer", "animal"]

doc_vectors = embeddings.embed_documents(words)

doc_vectors.__len__()



















