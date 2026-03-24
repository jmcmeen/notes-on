# Introduction to Retrieval-Augmented Generation (RAG)

## Table of Contents

- [What is RAG](#what-is-rag)
- [Core Components](#core-components)
- [Document Loading](#document-loading)
- [Chunking Strategies](#chunking-strategies)
- [Embeddings](#embeddings)
- [Vector Stores](#vector-stores)
- [Retrieval](#retrieval)
- [Generation](#generation)
- [Evaluation](#evaluation)
- [Advanced Patterns](#advanced-patterns)
- [Production Considerations](#production-considerations)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is RAG

Retrieval-Augmented Generation (RAG) is an architecture pattern that enhances LLM responses by retrieving relevant information from an external knowledge base before generating an answer. Instead of relying solely on the model's training data, RAG grounds responses in specific, up-to-date documents.

```python
# RAG at its simplest: retrieve then generate
def simple_rag(question: str, knowledge_base: list[str]) -> str:
    """The basic RAG pattern in pseudocode."""
    # Step 1: Find relevant documents from the knowledge base
    relevant_docs = retrieve(question, knowledge_base, top_k=3)

    # Step 2: Build a prompt with the retrieved context
    context = "\n\n".join(relevant_docs)
    prompt = f"""Answer the question based on the provided context.

Context:
{context}

Question: {question}

Answer:"""

    # Step 3: Generate an answer grounded in the context
    answer = llm.generate(prompt)
    return answer
```

**Why RAG vs fine-tuning**:

```python
# RAG advantages:
# - No training required; just index your documents
# - Easy to update: add/remove documents without retraining
# - Source attribution: you can cite which documents were used
# - Cost-effective: no GPU training costs
# - Data privacy: documents stay in your infrastructure

# Fine-tuning advantages:
# - Better for learning new formats, styles, or behaviors
# - Lower latency (no retrieval step)
# - Can learn patterns not easily expressed as retrieval

# Use RAG when:
# - You need up-to-date information (docs, knowledge bases)
# - You need source attribution and verifiability
# - Your data changes frequently
# - You want to start quickly without training infrastructure

# Use fine-tuning when:
# - You need to change the model's style or format
# - The task requires specialized reasoning patterns
# - Retrieval adds too much latency
# - The knowledge is stable and well-defined
```

Architecture overview:

```python
# The RAG pipeline has two phases:
#
# INDEXING PHASE (offline, done once per document set):
#   Documents -> Chunking -> Embedding -> Vector Store
#
# QUERY PHASE (online, per user query):
#   User Query -> Embedding -> Similarity Search -> Top-K Chunks
#   -> Prompt Construction -> LLM Generation -> Response

# Both phases share the same embedding model for consistency
```

---

## Core Components

The RAG pipeline consists of several interconnected components.

```python
# End-to-end RAG pipeline using LangChain
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_anthropic import ChatAnthropic
from langchain.chains import RetrievalQA

# 1. Load documents
loader = TextLoader("knowledge_base.txt")
documents = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # characters per chunk
    chunk_overlap=200,     # overlap between chunks for continuity
    separators=["\n\n", "\n", ". ", " ", ""]  # split hierarchy
)
chunks = splitter.split_documents(documents)

# 3. Create embeddings and store in vector database
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(chunks, embeddings)

# 4. Create retrieval chain
llm = ChatAnthropic(model="claude-sonnet-4-20250514")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True  # include sources in response
)

# 5. Query
result = qa_chain.invoke({"query": "What is the refund policy?"})
print(result["result"])                # the generated answer
print(result["source_documents"])      # the retrieved chunks
```

---

## Document Loading

Loading documents from various sources is the first step in building a RAG pipeline.

```python
# Loading plain text files
from langchain_community.document_loaders import TextLoader

loader = TextLoader("docs/manual.txt", encoding="utf-8")
documents = loader.load()
# Each document has: page_content (str) and metadata (dict)
print(documents[0].page_content[:200])  # first 200 chars
print(documents[0].metadata)            # {"source": "docs/manual.txt"}
```

```python
# Loading PDF files
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("docs/report.pdf")
pages = loader.load()  # one Document per page
for page in pages:
    print(f"Page {page.metadata['page']}: {page.page_content[:100]}...")
```

```python
# Loading HTML files and web pages
from langchain_community.document_loaders import BSHTMLLoader, WebBaseLoader

# Local HTML file
html_loader = BSHTMLLoader("docs/page.html")
html_docs = html_loader.load()

# Web page (fetches and parses)
web_loader = WebBaseLoader("https://docs.example.com/guide")
web_docs = web_loader.load()
```

```python
# Loading code files with metadata
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# Load all Python files from a directory
code_loader = DirectoryLoader(
    "src/",
    glob="**/*.py",           # match pattern for files
    loader_cls=TextLoader,    # loader to use for each file
    show_progress=True        # display progress bar
)
code_docs = code_loader.load()

# Each document includes the file path in metadata
for doc in code_docs:
    print(f"File: {doc.metadata['source']}, Length: {len(doc.page_content)}")
```

```python
# Loading from multiple sources and combining
from langchain.schema import Document

def load_knowledge_base(config: dict) -> list[Document]:
    """Load documents from multiple configured sources."""
    all_docs = []

    # Load text files
    for path in config.get("text_files", []):
        loader = TextLoader(path)
        docs = loader.load()
        all_docs.extend(docs)

    # Load PDFs
    for path in config.get("pdf_files", []):
        loader = PyPDFLoader(path)
        docs = loader.load()
        all_docs.extend(docs)

    # Add custom metadata to all documents
    for doc in all_docs:
        doc.metadata["indexed_at"] = "2025-01-15"
        doc.metadata["version"] = config.get("version", "1.0")

    return all_docs
```

---

## Chunking Strategies

How you split documents into chunks significantly affects retrieval quality.

```python
# Fixed-size chunking: simple but can split mid-sentence
from langchain.text_splitter import CharacterTextSplitter

fixed_splitter = CharacterTextSplitter(
    chunk_size=500,       # 500 characters per chunk
    chunk_overlap=50,     # 50 character overlap between chunks
    separator="\n"        # prefer splitting on newlines
)
chunks = fixed_splitter.split_documents(documents)
```

```python
# Recursive chunking: tries multiple separators in order
from langchain.text_splitter import RecursiveCharacterTextSplitter

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=[
        "\n\n",   # first try: paragraph breaks
        "\n",     # then: line breaks
        ". ",     # then: sentence boundaries
        ", ",     # then: clause boundaries
        " ",      # then: word boundaries
        ""        # last resort: character-level
    ]
)
chunks = recursive_splitter.split_documents(documents)

# This produces more semantically coherent chunks
# because it respects natural text boundaries
```

```python
# Semantic chunking: split based on meaning, not just size
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# Uses embeddings to find semantic boundaries
semantic_splitter = SemanticChunker(
    embeddings=OpenAIEmbeddings(),
    breakpoint_threshold_type="percentile",  # how to detect topic shifts
    breakpoint_threshold_amount=95           # sensitivity (higher = fewer splits)
)
semantic_chunks = semantic_splitter.split_documents(documents)
# Chunks will align with topic boundaries in the text
```

```python
# Code-specific chunking: respects code structure
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=1500,
    chunk_overlap=200
)
# Splits on: class definitions, function definitions, then general separators
code_chunks = python_splitter.split_documents(code_documents)
```

```python
# Custom chunking strategy with overlap control
def chunk_by_section(text: str, max_chunk_size: int = 1000) -> list[str]:
    """Split text by markdown headers, respecting size limits."""
    import re

    # Split on markdown headers (## or ###)
    sections = re.split(r'\n(?=#{2,3}\s)', text)

    chunks = []
    for section in sections:
        if len(section) <= max_chunk_size:
            chunks.append(section.strip())
        else:
            # Section is too large, split further by paragraphs
            paragraphs = section.split("\n\n")
            current_chunk = ""
            for para in paragraphs:
                if len(current_chunk) + len(para) > max_chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = para
                else:
                    current_chunk += "\n\n" + para
            if current_chunk:
                chunks.append(current_chunk.strip())

    return chunks
```

Chunk size considerations:

```python
# Chunk size tradeoffs:
# - Too small (100-200 chars): loses context, many irrelevant results
# - Too large (2000+ chars): dilutes relevance, wastes context window
# - Sweet spot: 500-1500 characters for most use cases

# Overlap tradeoffs:
# - No overlap (0): risk of splitting important info across chunks
# - Some overlap (10-20%): ensures continuity between chunks
# - Too much overlap (50%+): wastes storage and computation

# Practical guidance by content type:
CHUNK_CONFIGS = {
    "documentation": {"size": 1000, "overlap": 200},   # structured, reference material
    "articles":      {"size": 1500, "overlap": 300},   # narrative, flowing text
    "code":          {"size": 1500, "overlap": 200},   # function/class boundaries
    "chat_logs":     {"size": 500,  "overlap": 100},   # short, conversational
    "legal":         {"size": 800,  "overlap": 200},   # precise language matters
}
```

---

## Embeddings

Embeddings convert text into numerical vectors that capture semantic meaning.

```python
# OpenAI embeddings (popular choice, high quality)
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # cost-effective, 1536 dimensions
    # model="text-embedding-3-large"  # higher quality, 3072 dimensions
)

# Embed a single text
vector = embeddings.embed_query("What is machine learning?")
print(f"Embedding dimensions: {len(vector)}")   # 1536
print(f"First 5 values: {vector[:5]}")           # [-0.012, 0.034, ...]

# Embed multiple texts (batch processing, more efficient)
texts = ["first document", "second document", "third document"]
vectors = embeddings.embed_documents(texts)
print(f"Embedded {len(vectors)} documents")
```

```python
# Open-source embeddings with sentence-transformers
from langchain_community.embeddings import HuggingFaceEmbeddings

# Runs locally, no API costs
local_embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",  # fast, good quality, 384 dimensions
    # model_name="all-mpnet-base-v2"  # better quality, 768 dimensions
    model_kwargs={"device": "cpu"},   # or "cuda" for GPU
    encode_kwargs={"normalize_embeddings": True}  # L2 normalization
)

vector = local_embeddings.embed_query("What is machine learning?")
print(f"Dimensions: {len(vector)}")  # 384
```

```python
# Choosing an embedding model
# Key factors: quality, speed, cost, dimensionality

# Model comparison (approximate):
# | Model                    | Dims | Speed  | Cost      | Quality |
# |--------------------------|------|--------|-----------|---------|
# | text-embedding-3-small   | 1536 | Fast   | $0.02/1M  | Good    |
# | text-embedding-3-large   | 3072 | Fast   | $0.13/1M  | Better  |
# | all-MiniLM-L6-v2         | 384  | V.Fast | Free      | Good    |
# | all-mpnet-base-v2        | 768  | Fast   | Free      | Better  |

# IMPORTANT: use the SAME embedding model for indexing and querying
# Mixing models will produce meaningless similarity scores
```

---

## Vector Stores

Vector stores are specialized databases for storing and searching embeddings efficiently.

```python
# FAISS: fast, in-memory vector store (by Meta)
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create from documents
vector_store = FAISS.from_documents(chunks, embeddings)

# Save to disk for persistence
vector_store.save_local("faiss_index")

# Load from disk
loaded_store = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True  # required for pickle-based loading
)

# Search
results = vector_store.similarity_search("refund policy", k=3)
for doc in results:
    print(f"Source: {doc.metadata['source']}")
    print(f"Content: {doc.page_content[:150]}...")
    print()
```

```python
# ChromaDB: easy-to-use vector store with built-in persistence
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create with persistence directory
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db",     # auto-persists to disk
    collection_name="my_knowledge_base"
)

# Search with scores (lower distance = more similar)
results_with_scores = vector_store.similarity_search_with_score(
    "how to reset password",
    k=5
)
for doc, score in results_with_scores:
    print(f"Score: {score:.4f} | {doc.page_content[:100]}...")
```

```python
# Pinecone: managed cloud vector database (for production)
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
import os

os.environ["PINECONE_API_KEY"] = "your-api-key"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Create or connect to an existing index
vector_store = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name="my-rag-index"
)

# Pinecone handles scaling, replication, and persistence automatically
results = vector_store.similarity_search("billing question", k=5)
```

```python
# Adding and deleting documents after initial indexing
# Works with FAISS, Chroma, and Pinecone

from langchain.schema import Document

# Add new documents
new_docs = [
    Document(page_content="New policy effective 2025.", metadata={"source": "policy_v2"}),
    Document(page_content="Updated pricing information.", metadata={"source": "pricing"})
]
vector_store.add_documents(new_docs)

# Delete by IDs (Chroma and Pinecone)
# vector_store.delete(ids=["doc_id_1", "doc_id_2"])
```

---

## Retrieval

Retrieval is the process of finding the most relevant chunks for a given query.

```python
# Basic similarity search: find nearest neighbors by cosine similarity
results = vector_store.similarity_search(
    query="What are the shipping options?",
    k=5  # return top 5 most similar chunks
)

# Similarity search with relevance scores
results_with_scores = vector_store.similarity_search_with_relevance_scores(
    query="What are the shipping options?",
    k=5,
    score_threshold=0.7  # only return results above this relevance
)
for doc, score in results_with_scores:
    print(f"Relevance: {score:.2f} | {doc.page_content[:80]}...")
```

```python
# MMR (Maximal Marginal Relevance): balance relevance with diversity
# Prevents returning 5 chunks that all say the same thing
results = vector_store.max_marginal_relevance_search(
    query="What are the shipping options?",
    k=5,                    # return 5 results
    fetch_k=20,             # consider top 20 candidates
    lambda_mult=0.5         # 0=max diversity, 1=max relevance
)
# MMR iteratively selects documents that are relevant to the query
# but dissimilar to already-selected documents
```

```python
# Hybrid search: combine semantic search with keyword search
# Useful when exact terms matter (product names, codes, IDs)

from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# BM25: keyword-based retriever (like traditional search)
bm25_retriever = BM25Retriever.from_documents(chunks, k=5)

# Vector: semantic retriever
vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Combine both retrievers
hybrid_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]  # 40% keyword, 60% semantic
)

results = hybrid_retriever.invoke("order #12345 shipping status")
# BM25 catches the exact order number
# Vector search catches semantic meaning of "shipping status"
```

```python
# Reranking: use a cross-encoder to re-score initial results
# Cross-encoders are more accurate but slower than bi-encoders
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

# First retrieve with fast vector search, then rerank
base_retriever = vector_store.as_retriever(search_kwargs={"k": 20})

reranker = CohereRerank(
    model="rerank-english-v3.0",
    top_n=5  # keep top 5 after reranking
)

reranking_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=base_retriever
)

# The reranker scores query-document pairs more accurately
results = reranking_retriever.invoke("What is the cancellation policy?")
```

---

## Generation

The generation step combines retrieved context with the user's question to produce a grounded answer.

```python
# Basic RAG prompt construction
def build_rag_prompt(question: str, retrieved_docs: list) -> str:
    """Build a RAG prompt with retrieved context."""
    # Format retrieved documents with source info
    context_parts = []
    for i, doc in enumerate(retrieved_docs, 1):
        source = doc.metadata.get("source", "unknown")
        context_parts.append(f"[Source {i}: {source}]\n{doc.page_content}")

    context = "\n\n---\n\n".join(context_parts)

    return f"""Answer the user's question based on the provided context.

INSTRUCTIONS:
- Only use information from the provided context
- If the context doesn't contain the answer, say "I don't have enough information to answer this question"
- Cite your sources using [Source N] notation
- Be concise but complete

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""
```

```python
# Generation with source attribution
import anthropic
import json

client = anthropic.Anthropic()

def rag_generate(question: str, retrieved_docs: list) -> dict:
    """Generate an answer with source citations."""
    prompt = build_rag_prompt(question, retrieved_docs)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        temperature=0.0,  # deterministic for factual answers
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.content[0].text

    return {
        "answer": answer,
        "sources": [
            {
                "content": doc.page_content[:200],
                "source": doc.metadata.get("source", "unknown")
            }
            for doc in retrieved_docs
        ],
        "tokens_used": response.usage.input_tokens + response.usage.output_tokens
    }
```

Grounding and faithfulness:

```python
# Strategies to keep the LLM grounded in retrieved context

# 1. Explicit grounding instructions in the prompt
grounding_prompt = """You are a helpful assistant that ONLY answers based on
the provided context. You must follow these rules strictly:

- If the answer is in the context, provide it with [Source N] citations
- If the answer is PARTIALLY in the context, share what you can and note
  what information is missing
- If the answer is NOT in the context, respond: "Based on the available
  documents, I cannot answer this question."
- NEVER use your training knowledge to fill gaps
- NEVER make up information not present in the context"""

# 2. Ask the model to quote relevant passages before answering
quote_first_prompt = """First, quote the specific passages from the context
that are relevant to the question. Then provide your answer based on
those quotes.

RELEVANT QUOTES:
(extract exact quotes from the context)

ANSWER:
(answer based on the quotes above)"""

# 3. Structured output for verifiability
structured_output_prompt = """Respond in JSON format:
{
  "answer": "your answer here",
  "confidence": "high|medium|low",
  "supporting_quotes": ["exact quote 1", "exact quote 2"],
  "source_ids": [1, 3],
  "information_gaps": ["what info was missing, if any"]
}"""
```

---

## Evaluation

Evaluating RAG systems requires measuring both retrieval quality and generation quality.

```python
# Retrieval evaluation metrics

def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """What fraction of retrieved docs are relevant?"""
    retrieved_k = retrieved[:k]
    relevant_count = sum(1 for doc in retrieved_k if doc in relevant)
    return relevant_count / k

def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    """What fraction of relevant docs were retrieved?"""
    retrieved_k = set(retrieved[:k])
    found = len(relevant.intersection(retrieved_k))
    return found / len(relevant) if relevant else 0.0

def mrr(retrieved: list[str], relevant: set[str]) -> float:
    """Mean Reciprocal Rank: how early is the first relevant result?"""
    for i, doc in enumerate(retrieved, 1):
        if doc in relevant:
            return 1.0 / i
    return 0.0

# Example evaluation
retrieved_docs = ["doc_a", "doc_c", "doc_b", "doc_d", "doc_e"]
relevant_docs = {"doc_b", "doc_c", "doc_f"}

print(f"Precision@3: {precision_at_k(retrieved_docs, relevant_docs, 3):.2f}")  # 0.67
print(f"Recall@3: {recall_at_k(retrieved_docs, relevant_docs, 3):.2f}")        # 0.67
print(f"MRR: {mrr(retrieved_docs, relevant_docs):.2f}")                         # 0.50
```

```python
# Generation quality evaluation using LLM-as-judge

def evaluate_faithfulness(question: str, context: str, answer: str) -> dict:
    """Evaluate if the answer is faithful to the provided context."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        temperature=0.0,
        messages=[{
            "role": "user",
            "content": f"""Evaluate the faithfulness of this answer.

Question: {question}
Context: {context}
Answer: {answer}

Is every claim in the answer supported by the context?
Identify any claims that are NOT supported.

Respond in JSON:
{{
  "faithful": true/false,
  "score": 0.0-1.0,
  "unsupported_claims": ["list of claims not in context"],
  "reasoning": "brief explanation"
}}"""
        }]
    )
    return json.loads(response.content[0].text)

def evaluate_relevance(question: str, answer: str) -> dict:
    """Evaluate if the answer actually addresses the question."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        temperature=0.0,
        messages=[{
            "role": "user",
            "content": f"""Evaluate if this answer addresses the question.

Question: {question}
Answer: {answer}

Respond in JSON:
{{
  "relevant": true/false,
  "score": 0.0-1.0,
  "reasoning": "brief explanation"
}}"""
        }]
    )
    return json.loads(response.content[0].text)
```

---

## Advanced Patterns

Techniques that improve RAG quality beyond the basic pipeline.

```python
# Multi-query retrieval: generate multiple search queries for better recall
def multi_query_retrieve(question: str, vector_store, k: int = 5) -> list:
    """Generate multiple query variations and combine results."""
    # Use LLM to generate alternative queries
    response = client.messages.create(
        model="claude-haiku-4-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"""Generate 3 different search queries that would help
answer this question. Each query should approach the topic from a
different angle.

Question: {question}

Return one query per line, no numbering:"""
        }]
    )

    queries = [question]  # include original query
    queries.extend(response.content[0].text.strip().split("\n"))

    # Retrieve for each query and deduplicate
    seen_contents = set()
    all_results = []
    for query in queries:
        results = vector_store.similarity_search(query.strip(), k=k)
        for doc in results:
            content_hash = hash(doc.page_content)
            if content_hash not in seen_contents:
                seen_contents.add(content_hash)
                all_results.append(doc)

    return all_results[:k * 2]  # return more results for diversity
```

```python
# HyDE (Hypothetical Document Embeddings)
# Generate a hypothetical answer first, then search for similar real documents
def hyde_retrieve(question: str, vector_store, k: int = 5) -> list:
    """Use HyDE: embed a hypothetical answer instead of the question."""
    # Generate a hypothetical answer (doesn't need to be accurate)
    response = client.messages.create(
        model="claude-haiku-4-20250514",
        max_tokens=256,
        messages=[{
            "role": "user",
            "content": f"Write a short paragraph answering: {question}"
        }]
    )
    hypothetical_answer = response.content[0].text

    # Search using the hypothetical answer as the query
    # This often retrieves better results because the hypothetical answer
    # is in the same "language" as the stored documents
    results = vector_store.similarity_search(hypothetical_answer, k=k)
    return results
```

```python
# Parent-child chunking: retrieve small chunks, return larger context
from langchain.storage import InMemoryStore
from langchain.retrievers import ParentDocumentRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Create two splitters: large parents and small children
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)

# Document store for full parent chunks
docstore = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vector_store,
    docstore=docstore,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter
)

# Index documents (stores child chunks in vector store, parents in docstore)
retriever.add_documents(documents)

# When querying: searches child chunks, but returns parent chunks
# This gives you precise matching with full context
results = retriever.invoke("What is the cancellation policy?")
```

```python
# Contextual compression: compress retrieved docs to only relevant parts
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Use an LLM to extract only the relevant parts of each retrieved document
compressor = LLMChainExtractor.from_llm(
    llm=ChatAnthropic(model="claude-haiku-4-20250514")
)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vector_store.as_retriever(search_kwargs={"k": 10})
)

# Returns compressed chunks containing only query-relevant information
# This reduces noise and saves context window space
compressed_results = compression_retriever.invoke("refund policy details")
```

---

## Production Considerations

Deploying RAG systems to production requires attention to operational concerns.

```python
# Indexing pipeline: handle document updates efficiently
import hashlib
from datetime import datetime

class IndexingPipeline:
    """Manage document indexing with change detection."""

    def __init__(self, vector_store, embeddings, splitter):
        self.vector_store = vector_store
        self.embeddings = embeddings
        self.splitter = splitter
        self.document_hashes = {}  # track indexed documents

    def compute_hash(self, content: str) -> str:
        """Compute hash for change detection."""
        return hashlib.sha256(content.encode()).hexdigest()

    def index_document(self, doc_id: str, content: str, metadata: dict):
        """Index a document, skipping if unchanged."""
        content_hash = self.compute_hash(content)

        # Skip if document hasn't changed
        if self.document_hashes.get(doc_id) == content_hash:
            return {"status": "skipped", "reason": "unchanged"}

        # Remove old version if it exists
        if doc_id in self.document_hashes:
            self.vector_store.delete(ids=[doc_id])

        # Chunk and index the new version
        from langchain.schema import Document
        doc = Document(page_content=content, metadata={**metadata, "doc_id": doc_id})
        chunks = self.splitter.split_documents([doc])
        self.vector_store.add_documents(chunks)

        # Update tracking
        self.document_hashes[doc_id] = content_hash

        return {"status": "indexed", "chunks": len(chunks)}

    def remove_document(self, doc_id: str):
        """Remove a document from the index."""
        if doc_id in self.document_hashes:
            self.vector_store.delete(ids=[doc_id])
            del self.document_hashes[doc_id]
```

```python
# Monitoring and observability for RAG pipelines
import logging
import time

logger = logging.getLogger("rag_pipeline")

class RAGMonitor:
    """Monitor RAG pipeline performance and quality."""

    def __init__(self):
        self.queries = []

    def log_query(self, question: str, retrieved_docs: list,
                  answer: str, latency_ms: float):
        """Log a RAG query for monitoring."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "num_retrieved": len(retrieved_docs),
            "answer_length": len(answer),
            "latency_ms": latency_ms,
            "sources": [d.metadata.get("source") for d in retrieved_docs]
        }
        self.queries.append(entry)

        # Alert on potential issues
        if latency_ms > 5000:
            logger.warning("Slow RAG query: %.0fms for '%s'", latency_ms, question[:50])
        if len(retrieved_docs) == 0:
            logger.warning("No documents retrieved for: '%s'", question[:50])

    def get_metrics(self) -> dict:
        """Get aggregate metrics."""
        if not self.queries:
            return {}
        latencies = [q["latency_ms"] for q in self.queries]
        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
            "zero_retrieval_rate": sum(
                1 for q in self.queries if q["num_retrieved"] == 0
            ) / len(self.queries)
        }
```

---

## Practice Exercises

1. **Basic RAG**: Build a RAG system over a set of text files. Use recursive chunking (1000 chars, 200 overlap), OpenAI embeddings, and FAISS. Answer questions about the documents.

2. **Chunking comparison**: Take a single long document and chunk it using fixed-size, recursive, and semantic strategies. Compare retrieval quality for 5 test questions.

3. **Hybrid retrieval**: Implement hybrid search combining BM25 and vector search. Test on queries that contain specific terms (product codes, names) alongside semantic queries.

4. **Evaluation pipeline**: Create a test set of 10 question-answer pairs with source documents. Measure precision@5, recall@5, and faithfulness of generated answers.

5. **Multi-query RAG**: Implement multi-query retrieval that generates 3 query variations. Compare recall against single-query retrieval on your test set.

6. **Production pipeline**: Build an indexing pipeline that can add, update, and delete documents. Include change detection and monitoring.

---

## Summary

RAG enables LLMs to answer questions grounded in specific knowledge bases. Key takeaways:

- **Architecture**: documents are chunked, embedded, and stored in vector databases; queries retrieve relevant chunks to augment LLM generation
- **Chunking**: recursive splitting with overlap is a good default; semantic chunking works well for topic-diverse documents
- **Embeddings**: use the same model for indexing and querying; choose based on quality, cost, and latency needs
- **Vector stores**: FAISS for prototyping, ChromaDB for local persistence, Pinecone for production scale
- **Retrieval**: MMR adds diversity, hybrid search combines keyword and semantic matching, reranking improves precision
- **Generation**: ground the LLM in context with explicit instructions, require citations, and handle missing information gracefully
- **Evaluation**: measure retrieval (precision, recall, MRR) and generation (faithfulness, relevance) separately
- **Advanced patterns**: multi-query, HyDE, parent-child chunking, and contextual compression each address specific quality issues

---

## Next Steps

- Start with a simple RAG prototype using FAISS and test on your own documents
- Experiment with different chunk sizes and measure the impact on quality
- Add hybrid retrieval for queries that mix semantic and keyword needs
- Build an evaluation pipeline to measure your system objectively
- Explore reranking to improve precision without changing your index
- Plan for production with document update pipelines and monitoring

---

## Additional Resources

- [LangChain RAG Documentation](https://python.langchain.com/docs/tutorials/rag/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai)
- [Anthropic RAG Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [FAISS Documentation](https://faiss.ai)
- [ChromaDB Documentation](https://docs.trychroma.com)
- [Pinecone Documentation](https://docs.pinecone.io)
- [MTEB Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard)
- [RAG Survey Paper (Gao et al., 2024)](https://arxiv.org/abs/2312.10997)
