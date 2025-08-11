# Contextual Customer Answer RAG

A RAG (Retrieval-Augmented Generation) system for providing contextual customer answers using Airbnb listing data.

## Description

This project implements a RAG system that can retrieve relevant information from Airbnb listing data and generate contextual answers for customer queries using **Mistral Large LLM**.

## Features

- **Vector Database**: ChromaDB for efficient similarity search
- **Document Processing**: Automatic text chunking and embedding
- **Mistral LLM Integration**: Intelligent response generation using Mistral Large
- **REST API**: FastAPI-based web interface
- **Docker Support**: Easy deployment with Docker
- **Real-time Search**: Semantic search capabilities
- **Metadata Tracking**: Document source and chunk information
- **LLM-Powered Responses**: Human-like answers based on retrieved context

## Quick Start with Docker

### Prerequisites

- Docker
- Docker Compose

### Deployment

1. **Clone and navigate to the project:**
   ```bash
   cd ContextualCustomerAnswerRAG
   ```

2. **Set up environment variables:**
   ```bash
   # Copy the environment template
   cp .env_template .env
   
   # Edit .env file with your actual Mistral API key
   # MISTRAL_API_KEY=your_actual_api_key_here
   ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose -f docker-compose.yml up --build
   ```

3. **Run test inside Docker Compose:**
   ```bash
   docker-compose -f docker-compose.test.yml up --build
   ```

4. **Access the application:**
   - API: http://localhost:8000
   - **Interactive API Documentation**: http://localhost:8000/docs (Swagger UI)
   - **ReDoc Documentation**: http://localhost:8000/redoc (Alternative view)
   - Health check: http://localhost:8000/health

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with system information
- `GET /health` - Health check
- `GET /info` - Vector database collection information
- `POST /search` - Search for relevant documents
- `POST /search-with-llm` - Search with LLM-powered response generation
- `GET /llm-status` - Check Mistral LLM integration status
- `POST /load-documents` - Load documents from file
- `GET /sample-queries` - Get sample queries for testing

### OpenAPI Specification

The API follows OpenAPI 3.0 specification and provides comprehensive documentation at `/docs` endpoint.

#### Request/Response Models

##### QueryRequest
```json
{
  "query": "string",
  "n_results": "integer (default: 5, max: 5)"
}
```

##### SearchResponse
```json
{
  "query": "string",
  "results": [
    {
      "text": "string",
      "distance": "number (optional)"
    }
  ],
  "total_results": "integer"
}
```

##### LLMSearchResponse
```json
{
  "query": "string",
  "llm_response": "string",
  "results": [
    {
      "text": "string",
      "distance": "number (optional)"
    }
  ],
  "error": "string (optional)"
}
```

##### CollectionInfo
```json
{
  "collection_name": "string",
  "document_count": "integer"
}
```

##### LLMStatus
```json
{
  "status": "string",
  "message": "string (optional)"
}
```

#### Endpoint Details

##### GET /
**Description**: Root endpoint providing system overview and available endpoints  
**Response**: System information, version, and endpoint list  
**Status Codes**: 200 OK

##### GET /health
**Description**: Health check endpoint for monitoring and load balancers  
**Response**: Service health status  
**Status Codes**: 200 OK

##### GET /info
**Description**: Retrieve vector database collection information  
**Response**: Collection name and document count  
**Status Codes**: 200 OK, 500 Internal Server Error

##### POST /search
**Description**: Search for relevant documents using semantic similarity  
**Request Body**: QueryRequest  
**Response**: SearchResponse with ranked results  
**Status Codes**: 200 OK, 400 Bad Request, 500 Internal Server Error

##### POST /search-with-llm
**Description**: Enhanced search with LLM-powered response generation  
**Request Body**: QueryRequest  
**Response**: LLMSearchResponse with AI-generated answer  
**Status Codes**: 200 OK, 400 Bad Request, 500 Internal Server Error

##### GET /llm-status
**Description**: Check Mistral LLM integration status  
**Response**: LLM service status and any error messages  
**Status Codes**: 200 OK, 500 Internal Server Error

##### POST /load-documents
**Description**: Load and process documents from airbnblisting.txt file  
**Response**: Success message with document count  
**Status Codes**: 200 OK, 500 Internal Server Error

##### GET /sample-queries
**Description**: Get sample queries for testing and demonstration  
**Response**: List of example queries  
**Status Codes**: 200 OK

#### Error Handling

The API uses standard HTTP status codes and provides detailed error messages:

- **400 Bad Request**: Invalid input parameters or validation errors
- **500 Internal Server Error**: Server-side errors with descriptive messages
- **422 Unprocessable Entity**: Request validation failures (FastAPI automatic)

#### Rate Limiting

Currently no rate limiting is implemented, but the system is designed to handle multiple concurrent requests efficiently.

#### Authentication

No authentication is required for the current endpoints. All endpoints are publicly accessible.

#### OpenAPI Schema

The complete OpenAPI 3.0 specification is available at:
- **JSON Schema**: http://localhost:8000/openapi.json
- **YAML Schema**: http://localhost:8000/openapi.yaml

This allows developers to:
- Generate client SDKs in various programming languages
- Import the API specification into tools like Postman or Insomnia
- Validate API requests and responses
- Generate comprehensive API documentation

### Search Examples

#### Basic Search
```bash
curl -X POST "http://localhost:8000/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What amenities are available in the apartment?",
       "n_results": 3
     }'
```

#### LLM-Powered Search
```bash
curl -X POST "http://localhost:8000/search-with-llm" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "Can you summarize the main features of this apartment?",
       "n_results": 5
     }'
```

#### Check LLM Status
```bash
curl -X GET "http://localhost:8000/llm-status"
```

### Sample Queries

#### Basic Information
- "What amenities are available in the apartment?"
- "What are the check-in and check-out times?"
- "Is there parking available?"
- "What are the house rules?"
- "How far is the apartment from the metro?"
- "What is the WiFi password?"
- "Are pets allowed?"
- "What is the maximum number of guests?"

#### LLM-Enhanced Queries
- "Can you summarize the main features of this apartment?"
- "What makes this apartment special or unique?"
- "What are the nearby attractions and transportation options?"
- "How would you describe the overall experience of staying here?"
- "What are the best features for families with children?"

## Mistral LLM Integration

The system now includes integration with **Mistral Large LLM** for enhanced response generation:

### How It Works

1. **Retrieval**: The system searches the vector database for relevant documents
2. **Context Building**: Retrieved documents are formatted as context for the LLM
3. **LLM Generation**: Mistral Large generates human-like responses based on the context
4. **Response Delivery**: Both the LLM response and retrieved documents are returned


## Data Processing

The system automatically processes the `airbnblisting.txt` file:

1. **Text Cleaning**: Removes extra whitespace and normalizes text
2. **Chunking**: Splits text into overlapping chunks (500 chars with 50 char overlap)
3. **Embedding**: Generates embeddings using sentence transformers
4. **Storage**: Stores in ChromaDB with metadata

## Development

### Adding New Data

1. Replace or update `airbnblisting.txt` with new content
2. Call the `/reload` endpoint to reprocess the data
3. The system will automatically update the vector database

### Customizing the RAG System

- Modify `rag_system.py` for core RAG functionality
- Update `main.py` for API endpoints
- Adjust chunking parameters in `RAGHandler.chunk_text()`


## License

[Add your license information here]
