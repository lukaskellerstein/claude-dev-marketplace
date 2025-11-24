---
description: Build a production-ready RAG (Retrieval Augmented Generation) system with Langchain, vector databases, and advanced retrieval strategies
---

Build a comprehensive RAG system with proper document ingestion, retrieval, and generation using Langchain and best practices.

## Process

Follow these steps:

1. **Analyze Requirements**: Understand the RAG system goals and constraints
   - Document corpus (type, size, update frequency)
   - Query types and complexity
   - Expected accuracy and quality
   - Latency requirements
   - Scale requirements (users, queries per second)
   - Budget constraints
   - Review existing data and infrastructure

2. **Launch Langchain Expert**: Use the `langchain-expert` agent to:
   - Design document ingestion pipeline
   - Choose chunking strategy
   - Select embedding model
   - Choose vector database
   - Design retrieval strategy
   - Design reranking approach
   - Plan query transformation
   - Design generation approach

3. **Agent Integration** (if needed): Use `claude-agent-expert` or `agent-orchestration-expert` for:
   - Complex multi-step retrieval with agents
   - Query decomposition and routing
   - Multi-agent collaboration for research

4. **Implementation Guide**: Provide:
   - Complete RAG implementation
   - Document ingestion code
   - Retrieval chain
   - Evaluation framework
   - Deployment guide

## Output

Present a comprehensive RAG system implementation including:

### System Architecture
- High-level RAG architecture diagram
- Components and data flow
- Document ingestion pipeline
- Query processing flow
- Generation approach
- Why this architecture fits requirements

### Document Ingestion Pipeline
- Document sources and types
- Loading strategy (batch, streaming)
- Preprocessing and cleaning
- Chunking strategy and configuration
- Metadata extraction
- Embedding generation
- Vector store indexing
- Pipeline implementation code

### Chunking Strategy
- Chunking method (fixed-size, semantic, recursive)
- Chunk size and overlap
- Chunking configuration
- Why this strategy for the data
- Code implementation

```python
# Document loading
# Text splitting configuration
# Chunk processing
# Metadata handling
```

### Embedding Configuration
- Embedding model selection (OpenAI, Cohere, local)
- Embedding dimensions
- Embedding generation strategy (batch, streaming)
- Caching strategy
- Cost per million tokens
- Performance characteristics

### Vector Database Setup
- Vector database choice (Pinecone, Weaviate, Qdrant, Chroma)
- Index configuration
- Distance metric (cosine, euclidean, dot product)
- Why this database for requirements
- Setup and initialization code
- Backup and recovery strategy

### Retrieval Strategy
- Retrieval method (similarity, MMR, multi-query)
- Number of documents to retrieve (top-K)
- Similarity threshold
- Metadata filtering
- Hybrid search configuration (if applicable)
- Query transformation approach
- Retrieval implementation code

```python
# Vector store initialization
# Retriever configuration
# Query preprocessing
# Document retrieval
# Result post-processing
```

### Reranking (Optional)
- Reranking model selection (Cohere, Cross-encoder)
- Reranking configuration
- When to use reranking
- Cost and latency impact
- Implementation code

### Query Processing
- Query preprocessing
- Query expansion/transformation
- Query routing (if multi-index)
- Query validation
- Implementation code

### Generation Chain
- LLM selection (Claude, GPT-4, local)
- Prompt template design
- Context injection approach
- Source citation strategy
- Output parsing
- Streaming configuration
- Generation implementation code

```python
# Prompt template
# LLM configuration
# RAG chain setup
# Streaming response
# Source attribution
```

### Advanced Features

#### Multi-Query Retrieval
- Generate multiple query variations
- Retrieve for each variation
- Aggregate and deduplicate results

#### Parent-Document Retrieval
- Retrieve small chunks for relevance
- Return parent documents for context
- Better context preservation

#### Contextual Compression
- Compress retrieved documents
- Remove irrelevant information
- Improve context quality

#### Hypothetical Document Embeddings (HyDE)
- Generate hypothetical answer
- Use answer for retrieval
- Improve retrieval for abstract queries

### Evaluation Framework
- Retrieval metrics (precision, recall, MRR, NDCG)
- Generation metrics (accuracy, relevance, faithfulness)
- End-to-end evaluation
- Test dataset creation
- Evaluation code and scripts
- Baseline comparison

```python
# Evaluation dataset
# Retrieval evaluation
# Generation evaluation
# Metrics calculation
# Results analysis
```

### Performance Optimization
- Embedding caching
- Vector store optimization
- Query caching
- Parallel retrieval
- Batch operations
- Prompt compression
- Response streaming

### Cost Analysis
- Embedding costs (per million tokens)
- Vector database costs (storage, queries)
- LLM costs (per million tokens)
- Total cost per query
- Cost optimization opportunities
- Monthly cost estimates

### Error Handling
- Failed document ingestion
- Embedding generation errors
- Vector store unavailability
- Retrieval failures
- LLM API errors
- Fallback strategies
- Error logging and alerting

### Monitoring and Observability
- Key metrics to track
  - Query latency (p50, p95, p99)
  - Retrieval quality metrics
  - Generation quality metrics
  - Error rates
  - Cost per query
  - Document freshness
- Logging strategy
- LangSmith integration
- Custom dashboards
- Alerting rules

### Testing Strategy
- Unit tests for components
- Integration tests for pipeline
- End-to-end RAG tests
- Retrieval quality tests
- Generation quality tests
- Edge case testing
- Load testing

### Deployment Guide
- Infrastructure requirements
- Vector database deployment
- Application deployment
- Worker scaling strategy
- High availability setup
- CI/CD pipeline
- Configuration management
- Secrets management

### Maintenance and Updates
- Document reindexing strategy
- Incremental updates
- Version management
- Data cleanup
- Monitoring data quality
- Performance tuning

## Examples

### Documentation RAG System
```
/build-rag-system

Build a RAG system for technical documentation with:
- 1,000 markdown documents
- Semantic chunking for code blocks
- Hybrid search (vector + keyword)
- Claude Sonnet for generation
- Source citations with links
- Sub-second query response
```

### Enterprise Knowledge Base
```
/build-rag-system

Create an enterprise knowledge base with:
- 50,000 documents (PDF, Word, HTML)
- Multi-tenant with access control
- Metadata filtering by department
- Reranking for precision
- Streaming responses
- 1,000 concurrent users
```

### Research Assistant RAG
```
/build-rag-system

Build a research assistant with:
- Academic papers (arXiv, PubMed)
- Multi-query retrieval for comprehensiveness
- Parent-document retrieval for context
- Claude Opus for analysis
- Citation tracking
- Export to bibliography format
```

### Customer Support RAG
```
/build-rag-system

Create customer support RAG with:
- Product docs, FAQs, ticket history
- Query routing by product category
- Fast retrieval (<500ms)
- Haiku for cost-effective responses
- Escalation to human if low confidence
- Multi-language support
```

### Code Search RAG
```
/build-rag-system

Build code search and explanation with:
- GitHub repositories
- Code-specific chunking
- Metadata (language, file path, author)
- Claude Sonnet for code explanation
- Inline code examples in responses
- IDE integration
```

## RAG Architectures

### Basic RAG
- Simple similarity search
- Single LLM call with context
- No reranking
- Fast and cost-effective

### Advanced RAG
- Multi-query retrieval
- Reranking for precision
- Query transformation
- Better quality, higher cost

### Agentic RAG
- Agent decides retrieval strategy
- Iterative retrieval and reasoning
- Multi-step research
- Highest quality, highest cost

### Hybrid RAG
- Vector + keyword search
- Multiple embedding models
- Fusion of results
- Best accuracy

## Best Practices Applied

- **Semantic Chunking**: Preserve meaning in chunks
- **Metadata**: Rich metadata for filtering
- **Hybrid Search**: Combine vector and keyword
- **Reranking**: Improve top-K quality
- **Streaming**: Better UX for long responses
- **Caching**: Reduce costs and latency
- **Monitoring**: Track quality and performance
- **Testing**: Comprehensive evaluation
- **Documentation**: Clear system docs
- **Security**: Access control and validation

## Integration with Other Systems

- **Vector Databases**: Primary storage for embeddings
- **Databases**: For document metadata and tracking
- **Object Storage**: For original documents (S3, GCS)
- **APIs**: Document source integrations
- **Monitoring**: Observability platforms
- **Auth Systems**: User authentication
- **Search Engines**: Hybrid search with Elasticsearch

Provide production-ready RAG implementations with comprehensive evaluation, monitoring, and operational excellence.
