# Rate limiting - API throttling and request management
from fastapi import FastAPI
import uvicorn
from controller import RAGHandler
from controller.route import set_rag_handler
import os
from controller import router
from controller.db import DBConnector
from mistralai import Mistral

app = FastAPI(
    title="Airbnb Listing RAG System",
    description="A RAG (Retrieval-Augmented Generation) system for Airbnb listing data",
    version="1.0.0"
)

# Global variable for RAG system
rag_handler = None



@app.on_event("startup")
async def startup_event():
    """
    Initialize the RAG system on startup
    """
    global rag_handler
    
    # Initialize RAG system with external ChromaDB
    chroma_host = os.getenv('CHROMA_SERVER_HOST', None)
    chroma_port = int(os.getenv('CHROMA_SERVER_PORT', 8000))

    # Create ChromaDB client
    db_connector = DBConnector(chroma_host, chroma_port)
    chroma_client = db_connector.connect()
    
    # Create Mistral client
    api_key = os.getenv('MISTRAL_API_KEY')
    mistral_client = Mistral(api_key)

    rag_handler = RAGHandler(chroma_client, mistral_client)
    
    # Check if airbnblisting.txt exists
    if os.path.exists("data/airbnblisting.txt"):
        documents = rag_handler.process_airbnb_listing("data/airbnblisting.txt")
        
        # Check if collection is empty
        collection_info = rag_handler.get_collection_info()
        if collection_info['document_count'] == 0:
            rag_handler.add_documents(documents)
    
    set_rag_handler(rag_handler)
    # Set the RAG system in the routes
    #
    #set_rag_handler(rag_handler)

# Include the router with all endpoints
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000
    )