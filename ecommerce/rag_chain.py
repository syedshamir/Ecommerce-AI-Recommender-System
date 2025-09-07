from langchain_groq import ChatGroq #use to generate conversational response from groq llm
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from ecommerce.config import Config

class RAGChainBuilder:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.model = ChatGroq(model=Config.RAG_MODEL, temperature= 0.5)
        self.history_store={} #stores chat history based on session id

    def _get_history(self, session_id:str) -> BaseChatMessageHistory:  #to get chat history based on session id
        if session_id not in self.history_store:
            self.history_store[session_id] = ChatMessageHistory()
        return self.history_store[session_id]

    def build_chain(self):
        #first convert vector store to retriever
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3}) # k = 3 means top 3 similar documents.. use of retirever is to fetch relevant documents from vector store or query over vector store based on user query

        ''' this prompt rewrites user question based on chat history to make it standalone question'''

        context_prompt = ChatPromptTemplate.from_messages([
            ("system", "Given the chat history and user question, rewrite it as a standalone question."),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """You're an e-commerce bot answering product-related queries using reviews and titles.
                          Stick to context. Be concise and helpful.\n\nCONTEXT:\n{context}\n\nQUESTION: {input}"""),
            MessagesPlaceholder(variable_name="chat_history"), 
            ("human", "{input}")  
        ])

        history_aware_retriever = create_history_aware_retriever(
            self.model,
            retriever ,
            context_prompt,
        )

        question_answer_chain = create_stuff_documents_chain(
            self.model, qa_prompt

        )

        rag_chain = create_retrieval_chain(
            history_aware_retriever,
            question_answer_chain
        )

        return RunnableWithMessageHistory(
            rag_chain,
            get_session_history=self._get_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )