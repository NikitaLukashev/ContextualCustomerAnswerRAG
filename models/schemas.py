# Basic schemas - Pydantic models for API validation
"""
Pydantic models for the RAG system API
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, validator


class QueryRequest(BaseModel):
    query: str = Field(description="Search query text")
    n_results: Optional[int] = Field(default=5, ge=1, le=10, description="Number of results to return (1-10)")
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()


class SearchResponse(BaseModel):
    query: str = Field(description="Original search query")
    results: List[Dict[str, Any]] = Field(description="List of search results")
    total_results: int = Field(ge=0, description="Total number of results found")
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()



class CollectionInfo(BaseModel):
    collection_name: str = Field(description="Name of the vector database collection")
    document_count: int = Field(ge=0, description="Number of documents in the collection")


class LLMSearchResponse(BaseModel):
    query: str = Field(description="Original search query")
    llm_response: str = Field(description="AI-generated response from the LLM")
    results: List[Dict[str, Any]] = Field(description="List of retrieved documents")
    error: Optional[str] = Field(None, description="Error message if LLM processing failed")

    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError('Query cannot be empty or whitespace only')
        return v.strip()


class LLMStatus(BaseModel):
    llm_available: bool = Field(description="Whether the LLM service is available")
    llm_model: Optional[str] = Field(None, description="The LLM model being used")
    llm_error: Optional[str] = Field(None, description="Error message if LLM is not available")
