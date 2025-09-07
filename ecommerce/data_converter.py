import pandas as pd
from langchain_core.documents import Document

class DataConverter: #convert data to documents
    def __init__(self, file_path:str):
        self.file_path = file_path

    def convert(self):
        df = pd.read_csv(self.file_path)[["product_title", "review"]] #convert csv to pandas and only two columns to read

        docs = [
            Document(page_content=row['review'], metadata={"product_name": row["product_title"]}) # Document has page_content which is having review, and metadata  is a dictionary which is having product name
            for _, row in df.iterrows()  #iterrows is used to iterate over each row of the dataframe  . each row will be a document     
        ]
        return docs
