from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_openai import OpenAIEmbeddings
from ecommerce.data_converter import DataConverter
from ecommerce.config import Config

class DataIngestor: #this will convert document to embeddings, creating vector store, storing embedding in vector store
    def __init__(self):
        #self.embedding = HuggingFaceEndpointEmbeddings(model = Config.EMBEDDING_MODEL)
        self.embedding = OpenAIEmbeddings(model = Config.EMBEDDING_MODEL)

        self.vstore = AstraDBVectorStore(
            embedding = self.embedding,
            collection_name = "ecommerce_database",
            api_endpoint = Config.ASTRA_DB_API_ENDPOINT,
            token = Config.ASTRA_DB_APPLICATION_TOKEN,
            namespace = Config.ASTRA_DB_KEYSPACE
        )

    def ingest(self, load_existing=True): #load_existing is true means if vector store is already there then load it, if false then create new vector store. If changes on vector store or changes to data, then set it to False
        if load_existing == True:
            return self.vstore
        
        docs = DataConverter(file_path="data/flipkart_product_review.csv").convert()

        self.vstore.add_documents(docs)
        return self.vstore
    
if __name__ == "__main__":
    ingestor = DataIngestor()
    ingestor.ingest(load_existing=False)    
