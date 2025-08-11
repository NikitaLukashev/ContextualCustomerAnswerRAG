# Contextual Customer Answer RAG

A RAG (Retrieval-Augmented Generation) system for providing contextual customer answers using Airbnb listing data.

## Description

This project implements a RAG system that can retrieve relevant information from Airbnb listing data and generate contextual answers for customer queries using **Mistral Large LLM**. The system uses:

- **ChromaDB** as the vector database
- **Sentence Transformers** for embeddings
- **Mistral Large LLM** for intelligent response generation
- **FastAPI** for the web API
- **Docker** for containerization

## Project Structure

```
ContextualCustomerAnswerRAG/
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── .dockerignore       # Docker ignore file
├── main.py             # FastAPI application
├── rag_system.py       # Core RAG system
├── airbnblisting.txt   # Airbnb listing data
└── data/               # Vector database storage
```

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
   cp env_template.txt .env
   
   # Edit .env file with your actual Mistral API key
   # MISTRAL_API_KEY=your_actual_api_key_here
   ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with system information
- `GET /health` - Health check
- `GET /info` - Vector database collection information
- `POST /search` - Search for relevant documents
- `POST /search-with-llm` - Search with LLM-powered response generation
- `GET /llm-status` - Check Mistral LLM integration status
- `POST /reload` - Reload documents from file
- `GET /sample-queries` - Get sample queries for testing

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

### Benefits

- **Intelligent Answers**: More natural and contextual responses
- **Better Understanding**: LLM can synthesize information from multiple documents
- **User Experience**: More engaging and helpful customer interactions
- **Fallback Support**: Works even if LLM is unavailable

### Configuration

The Mistral API key is configured via environment variable in a `.env` file:

1. **Create a `.env` file** in the project root:
   ```bash
   cp env_template.txt .env
   ```

2. **Update the `.env` file** with your actual Mistral API key:
   ```bash
   MISTRAL_API_KEY=your_actual_api_key_here
   ```

3. **The `.env` file is automatically loaded** by Docker Compose and the API key will be available to your application.

**Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

## Vector Database

The system uses ChromaDB as the vector database with the following features:

- **Persistent Storage**: Data is stored in the `./data` directory
- **Cosine Similarity**: Uses cosine similarity for vector search
- **Automatic Embeddings**: Sentence transformers for text embeddings
- **Metadata Support**: Tracks document source and chunk information

## Data Processing

The system automatically processes the `airbnblisting.txt` file:

1. **Text Cleaning**: Removes extra whitespace and normalizes text
2. **Chunking**: Splits text into overlapping chunks (500 chars with 50 char overlap)
3. **Embedding**: Generates embeddings using sentence transformers
4. **Storage**: Stores in ChromaDB with metadata

## Configuration

### Environment Variables

- `CHROMA_DB_IMPL`: ChromaDB implementation (default: duckdb+parquet)
- `PERSIST_DIRECTORY`: Vector database storage directory (default: ./data)

### Docker Configuration

The Docker setup includes:
- Volume mounting for persistent data
- Port mapping (8000:8000)
- Automatic restart policy
- Hot reload for development

## Development

### Adding New Data

1. Replace or update `airbnblisting.txt` with new content
2. Call the `/reload` endpoint to reprocess the data
3. The system will automatically update the vector database

### Customizing the RAG System

- Modify `rag_system.py` for core RAG functionality
- Update `main.py` for API endpoints
- Adjust chunking parameters in `RAGHandler.chunk_text()`

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `docker-compose.yml`
2. **Memory issues**: Increase Docker memory allocation
3. **Data not loading**: Check if `airbnblisting.txt` exists

### Logs

View Docker logs:
```bash
docker-compose logs -f
```

## License

[Add your license information here]
