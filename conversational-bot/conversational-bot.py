# how to design and implement an LLM-powered chatbot. This chatbot will be able to have a conversation and remember previous interactions.
# 
# Note that this chatbot that we build will only use the language model to have a conversation. There are several other related concepts that you may be looking for:
# 
# - Conversational RAG: Enable a chatbot experience over an external source of data
# - Agents: Build a chatbot that can take actions

import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage,trim_messages
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
load_dotenv(".env") ## aloading all the environment variable

groq_api_key=os.getenv("GROQ_API_KEY")

model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

#### first method of invoking the model
model.invoke([HumanMessage(content="Hi , My name is Raushan and I am a Senior Data Scientist")])
model.invoke(
    [
        HumanMessage(content="Hi , My name is Raushan and I am a Senior Data Scientist"),
        AIMessage(content="Hello Raushan! It's nice to meet you. \n\nAs a Senior Data Scientist, what kind of projects are you working on these days? \n\nI'm always eager to learn more about the exciting work being done in the field of AI.\n"),
        HumanMessage(content="Hey What's my name and what do I do?")
    ]
)


#### Second method of invoking the model

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

trimmer=trim_messages(
    max_tokens=200,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human"
)
messages = [
    SystemMessage(content="you're a good assistant"),
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]
trimmer.invoke(messages)
chain=(
    RunnablePassthrough.assign(messages=itemgetter("messages")|trimmer)
    | prompt
    | model)

response=chain.invoke(
    {
    "messages":messages + [HumanMessage(content="What ice cream do i like")],
    "language":"Hindi"
    }
)
response.content

response = chain.invoke(
    {
        "messages": messages + [HumanMessage(content="what math problem did i ask")],
        "language": "English",
    }
)
response.content

