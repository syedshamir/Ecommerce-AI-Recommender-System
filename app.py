''' Backend code for the ecommerce product recommendation system '''

from flask import render_template, Flask, request, Response
from prometheus_client import Counter, generate_latest

from ecommerce.data_ingestion import DataIngestor
from ecommerce.rag_chain import RAGChainBuilder

from dotenv import load_dotenv
load_dotenv()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Request") #custom metric to count total number of http requests

def create_app(): 
    ''' Create and configure the Flask application '''

    app = Flask(__name__)

    vector_store = DataIngestor().ingest(load_existing=True) #load_existing is true means if vector store is already there then load it, if false then create new vector store. If changes on vector store or changes to data, then set it to False
    # we alread ingested the data and created vector store, so we are loading existing vector store, thus setting it to True

    rag_chain = RAGChainBuilder(vector_store).build_chain() #build the RAG chain using vector store

    @app.route("/")
    def index():
        ''' Render the main page '''
        REQUEST_COUNT.inc() #each time if index page (home page) is loaded, increment the request count
        return render_template("index.html") #loading UI page
    
    @app.route("/get", methods=["POST"])

    def get_response():
        ''' Get response from the RAG chain '''
        user_input = request.form["msg"]

        response = rag_chain.invoke(
            { "input": user_input},
              config = {"configurable": {"session_id":"user-session"}}
        )["answer"]

        return response
    @app.route("/metrics")

    def metrics():
        ''' Expose Prometheus metrics '''
        return Response(generate_latest(), mimetype = "text/plain")   
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(host = "0.0.0.0", port = 5000, debug=True)    