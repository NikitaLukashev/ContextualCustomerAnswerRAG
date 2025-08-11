"""
Pydantic models for the RAG system API
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    n_results: Optional[int] = 5


class SearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    total_results: int


class CollectionInfo(BaseModel):
    collection_name: str
    document_count: int


class LLMSearchResponse(BaseModel):
    query: str
    llm_response: str
    results: List[Dict[str, Any]]


class LLMStatus(BaseModel):
    llm_available: bool
    llm_model: Optional[str]
    llm_error: Optional[str]
