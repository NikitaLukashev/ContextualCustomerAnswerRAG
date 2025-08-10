# Performance monitoring - Metrics and performance tracking
"""
API routes for the RAG system
"""

from fastapi import APIRouter, HTTPException
from models import QueryRequest, SearchResponse, CollectionInfo, LLMSearchResponse, LLMStatus
from .llm_handler import MistralLLM
from .rag_handler import RAGHandler
# Create router
router = APIRouter()

# Global variable for RAG system (will be set by main.py)
rag_handler = None


def set_rag_handler(rag):
    """Set the RAG system instance for the routes to use"""
    global rag_handler
    rag_handler = rag

@router.get("/")
async def root():
    """
    Root endpoint
    """
    response = {
        "message": "Airbnb Listing RAG System with Mistral LLM",
        "version": "2.0.0",
        "endpoints": {
            "health": "/health",
            "info": "/info",
            "search": "/search",
            "search-with-llm": "/search-with-llm",
            "llm-status": "/llm-status",
            "docs": "/docs"
        }
    }
    return response


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    response = {"status": "healthy", "service": "rag-system"}
    return response


@router.get("/info", response_model=CollectionInfo)
async def get_collection_info():
    """
    Get information about the vector database collection
    """
    try:
        info = rag_handler.get_collection_info()
        return CollectionInfo(**info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving collection info: {str(e)}")


@router.post("/search", response_model=SearchResponse)
async def search_documents(request: QueryRequest):
    """
    Search for relevant documents based on a query
    """
    
    try:
        results = rag_handler.search(request.query, request.n_results)
        
        return SearchResponse(
            query=request.query,
            results=results,
            total_results=len(results)
        )
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during search")


@router.post("/load-documents")
async def load_documents():
    """
    Load documents from the airbnblisting.txt file
    """
    
    try:
        documents = rag_handler.process_airbnb_listing("data/airbnblisting.txt")
        
        rag_handler.add_documents(documents)
        
        return {
            "message": "Documents reloaded successfully",
            "documents_added": len(documents)
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error loading documents: {str(e)}")


@router.post("/search-with-llm", response_model=LLMSearchResponse)
async def search_with_llm(request: QueryRequest):
    """
    Search for relevant documents and generate LLM response using Mistral
    """
    
    try:
        results = rag_handler.search_with_llm(request.query, request.n_results)
        
        return LLMSearchResponse(**results)
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during LLM search")


@router.get("/llm-status", response_model=LLMStatus)
async def get_llm_status():
    """
    Get the status of the LLM service
    """
    
    try:
        status = rag_handler.get_llm_status()
        print(status)
        return LLMStatus(**status)
        print('status')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving LLM status: {str(e)}")


@router.get("/sample-queries")
async def get_sample_queries():
    """
    Get sample queries for testing the RAG system
    """
    sample_queries = [
        "What amenities are available in the apartment?",
        "What are the check-in and check-out times?",
        "Is there parking available?",
        "What are the house rules?",
        "How far is the apartment from the metro?",
        "What is the WiFi password?",
        "Are pets allowed?",
        "What is the maximum number of guests?",
        "What kitchen appliances are available?",
        "What are the safety features?",
        "Can you summarize the main features of this apartment?",
        "What makes this apartment special or unique?",
        "What are the nearby attractions and transportation options?"
    ]
    
    return {
        "sample_queries": sample_queries
    }
