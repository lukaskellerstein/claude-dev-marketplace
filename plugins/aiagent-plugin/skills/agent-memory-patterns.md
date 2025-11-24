---
name: agent-memory-patterns
description: Auto-invoked when implementing agent memory systems to ensure proper memory architecture, retrieval, and management
allowed-tools: Read, Grep, Glob
---

# Agent Memory Architecture Best Practices

This skill provides guidance on implementing effective memory systems for AI agents including conversation history, semantic memory, and context management.

## When Active

This skill activates when you:
- Implement agent memory systems
- Design conversation history management
- Work with vector databases for agent memory
- Implement RAG for agents
- Handle long-running conversations
- Optimize context usage
- Build multi-agent systems with shared memory
- Debug memory-related issues

## Memory Types and When to Use Them

### 1. Short-Term Memory (Conversation Buffer)

**For:** Recent conversation context (last few turns)

```python
# Good: Simple conversation buffer
class ConversationBuffer:
    def __init__(self, max_turns=10):
        self.messages = []
        self.max_turns = max_turns

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

        # Keep only recent messages
        if len(self.messages) > self.max_turns * 2:  # * 2 for user + assistant
            self.messages = self.messages[-self.max_turns * 2:]

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []

# Usage
memory = ConversationBuffer(max_turns=10)
memory.add_message("user", "What is Python?")
memory.add_message("assistant", "Python is a programming language...")

# Send to agent with context
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=memory.get_messages()
)
```

**Best Practices:**
- Limit to 10-20 message turns
- Include both user and assistant messages
- Clear when context is no longer relevant
- Monitor token usage
- Prune when approaching context limit

### 2. Sliding Window Memory

**For:** Long conversations with bounded context

```python
# Good: Sliding window with token tracking
from anthropic import Anthropic

class SlidingWindowMemory:
    def __init__(self, max_tokens=8000):
        self.messages = []
        self.max_tokens = max_tokens
        self.client = Anthropic()

    def count_tokens(self, text: str) -> int:
        """Estimate token count (use actual tokenizer in production)"""
        return len(text) // 4  # Rough estimate

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._prune_old_messages()

    def _prune_old_messages(self):
        """Remove oldest messages to stay under token limit"""
        total_tokens = sum(
            self.count_tokens(msg["content"]) for msg in self.messages
        )

        while total_tokens > self.max_tokens and len(self.messages) > 2:
            # Keep at least 1 user + 1 assistant message
            removed = self.messages.pop(0)
            total_tokens -= self.count_tokens(removed["content"])

    def get_messages(self):
        return self.messages

# Usage
memory = SlidingWindowMemory(max_tokens=8000)

for turn in range(100):  # Many conversation turns
    memory.add_message("user", user_input)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=memory.get_messages()
    )
    memory.add_message("assistant", response.content[0].text)
```

**Best Practices:**
- Track actual token counts (use tokenizer)
- Keep most recent messages
- Preserve system prompts
- Log when pruning occurs
- Consider conversation coherence when pruning

### 3. Summary Memory

**For:** Very long conversations with history compression

```python
# Good: Conversation summarization
class SummaryMemory:
    def __init__(self, summary_threshold=20):
        self.messages = []
        self.summary = None
        self.summary_threshold = summary_threshold
        self.client = Anthropic()

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

        # Summarize when threshold reached
        if len(self.messages) > self.summary_threshold:
            self._create_summary()

    def _create_summary(self):
        """Create summary of old messages"""
        # Messages to summarize (keep recent ones)
        to_summarize = self.messages[:-10]

        # Create conversation text
        conversation = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in to_summarize
        ])

        # Generate summary
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",  # Use Haiku for cost
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Summarize this conversation concisely:\n\n{conversation}"
            }]
        )

        new_summary = response.content[0].text

        # Append to existing summary
        if self.summary:
            self.summary = f"{self.summary}\n\nContinued: {new_summary}"
        else:
            self.summary = new_summary

        # Keep only recent messages
        self.messages = self.messages[-10:]

    def get_context(self):
        """Get context including summary and recent messages"""
        if self.summary:
            # Inject summary as system context
            return [
                {"role": "user", "content": f"Previous conversation summary:\n{self.summary}"},
                {"role": "assistant", "content": "I understand the previous context."},
                *self.messages
            ]
        return self.messages

# Usage
memory = SummaryMemory(summary_threshold=20)

for turn in range(100):
    memory.add_message("user", user_input)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=memory.get_context()
    )
    memory.add_message("assistant", response.content[0].text)
```

**Best Practices:**
- Use cheaper model (Haiku) for summarization
- Keep recent messages unsummarized
- Preserve critical information in summaries
- Test summary quality regularly
- Store summaries in database
- Allow summary regeneration

### 4. Semantic Memory (Vector Store)

**For:** Long-term facts, documents, and knowledge retrieval

```python
# Good: Semantic memory with vector database
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from anthropic import Anthropic

class SemanticMemory:
    def __init__(self, collection_name="agent_memory"):
        self.client = QdrantClient(host="localhost", port=6333)
        self.anthropic = Anthropic()
        self.collection_name = collection_name

        # Create collection if not exists
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )
        except:
            pass  # Collection already exists

    def get_embedding(self, text: str):
        """Get embedding using Voyage AI or OpenAI"""
        # Use embedding model (placeholder - use actual embedding API)
        import requests
        response = requests.post(
            "https://api.voyageai.com/v1/embeddings",
            json={"input": text, "model": "voyage-2"},
            headers={"Authorization": f"Bearer {VOYAGE_API_KEY}"}
        )
        return response.json()["data"][0]["embedding"]

    def store(self, text: str, metadata: dict = None):
        """Store text in semantic memory"""
        embedding = self.get_embedding(text)

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": text,
                "timestamp": datetime.utcnow().isoformat(),
                **(metadata or {})
            }
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

    def retrieve(self, query: str, limit: int = 5):
        """Retrieve relevant memories"""
        query_embedding = self.get_embedding(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )

        return [
            {
                "text": hit.payload["text"],
                "score": hit.score,
                "metadata": hit.payload
            }
            for hit in results
        ]

    def get_relevant_context(self, query: str):
        """Get relevant context for agent"""
        memories = self.retrieve(query, limit=3)

        if not memories:
            return ""

        context = "Relevant memories:\n"
        for i, mem in enumerate(memories, 1):
            context += f"\n{i}. {mem['text']}"

        return context

# Usage
semantic_memory = SemanticMemory()

# Store facts during conversation
semantic_memory.store(
    "User prefers Python over JavaScript",
    metadata={"type": "preference", "user_id": "123"}
)

semantic_memory.store(
    "User is working on a machine learning project",
    metadata={"type": "context", "user_id": "123"}
)

# Retrieve relevant memories
query = "What programming languages does the user like?"
relevant_context = semantic_memory.get_relevant_context(query)

# Use in agent call
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"{relevant_context}\n\nQuestion: {query}"}
    ]
)
```

**Best Practices:**
- Use specialized embedding models (Voyage, OpenAI)
- Store metadata for filtering
- Implement relevance threshold
- Regularly clean old memories
- Index for fast retrieval
- Consider hybrid search (vector + keyword)
- Store source and timestamp
- Implement memory importance scoring

### 5. Entity Memory

**For:** Tracking entities (people, places, things) and relationships

```python
# Good: Entity-based memory
class EntityMemory:
    def __init__(self):
        self.entities = {}  # {entity_name: {attributes}}
        self.relationships = []  # [(entity1, relation, entity2)]

    def extract_entities(self, text: str):
        """Extract entities using Claude"""
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"""Extract entities and relationships from this text:

{text}

Return JSON format:
{{
    "entities": [{{"name": "...", "type": "...", "attributes": {{}}}}],
    "relationships": [{{"entity1": "...", "relation": "...", "entity2": "..."}}]
}}"""
            }]
        )

        return json.loads(response.content[0].text)

    def update_entities(self, text: str):
        """Update entity knowledge from text"""
        extracted = self.extract_entities(text)

        # Update entities
        for entity in extracted["entities"]:
            name = entity["name"]
            if name not in self.entities:
                self.entities[name] = entity
            else:
                # Merge attributes
                self.entities[name].update(entity)

        # Add relationships
        self.relationships.extend(extracted["relationships"])

    def get_entity_context(self, entity_name: str):
        """Get context about an entity"""
        if entity_name not in self.entities:
            return ""

        entity = self.entities[entity_name]
        context = f"About {entity_name}:\n"

        # Add attributes
        for key, value in entity.get("attributes", {}).items():
            context += f"- {key}: {value}\n"

        # Add relationships
        related = [
            r for r in self.relationships
            if r["entity1"] == entity_name or r["entity2"] == entity_name
        ]

        if related:
            context += "\nRelationships:\n"
            for rel in related:
                context += f"- {rel['entity1']} {rel['relation']} {rel['entity2']}\n"

        return context

# Usage
entity_memory = EntityMemory()

# Extract and store entities from conversation
entity_memory.update_entities(
    "John works at Google as a software engineer. He reports to Sarah."
)

# Get context about entity
context = entity_memory.get_entity_context("John")
# Returns: "About John:\n- employer: Google\n- role: software engineer\n..."
```

**Best Practices:**
- Use LLM for entity extraction
- Normalize entity names
- Store entity types (person, place, organization)
- Track relationships between entities
- Update entities with new information
- Resolve entity references (coreference)
- Store confidence scores
- Implement entity merging

## Memory Architecture Patterns

### Pattern 1: Hybrid Memory System

**Combine multiple memory types for comprehensive context**

```python
# Good: Hybrid memory combining multiple types
class HybridMemory:
    def __init__(self):
        self.short_term = ConversationBuffer(max_turns=10)
        self.summary = SummaryMemory(summary_threshold=20)
        self.semantic = SemanticMemory()
        self.entities = EntityMemory()

    async def process_turn(self, user_message: str):
        """Process conversation turn with all memory systems"""

        # 1. Retrieve relevant semantic memories
        relevant_context = self.semantic.get_relevant_context(user_message)

        # 2. Extract entities mentioned
        self.entities.update_entities(user_message)
        entity_context = ""
        # Get context for mentioned entities
        # (entity extraction logic here)

        # 3. Build full context
        full_context = []

        # Add relevant semantic memories
        if relevant_context:
            full_context.append({
                "role": "user",
                "content": f"Relevant background:\n{relevant_context}"
            })
            full_context.append({
                "role": "assistant",
                "content": "I'll keep that context in mind."
            })

        # Add entity context if relevant
        if entity_context:
            full_context.append({
                "role": "user",
                "content": f"Entity information:\n{entity_context}"
            })
            full_context.append({
                "role": "assistant",
                "content": "I understand."
            })

        # Add conversation history
        full_context.extend(self.short_term.get_messages())

        # Add current message
        full_context.append({
            "role": "user",
            "content": user_message
        })

        # 4. Call agent with full context
        response = await self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=full_context
        )

        assistant_message = response.content[0].text

        # 5. Update all memory systems
        self.short_term.add_message("user", user_message)
        self.short_term.add_message("assistant", assistant_message)
        self.summary.add_message("user", user_message)
        self.summary.add_message("assistant", assistant_message)

        # Store important facts in semantic memory
        if should_store(assistant_message):
            self.semantic.store(assistant_message)

        return assistant_message
```

### Pattern 2: Multi-Agent Shared Memory

**Shared memory for coordinating multiple agents**

```python
# Good: Shared memory for multi-agent system
class SharedMemory:
    def __init__(self):
        self.global_state = {}
        self.agent_memories = {}  # {agent_id: memory}
        self.message_bus = []
        self.lock = asyncio.Lock()

    async def set_global_state(self, key: str, value: any):
        """Set global state accessible to all agents"""
        async with self.lock:
            self.global_state[key] = {
                "value": value,
                "timestamp": datetime.utcnow(),
                "version": self.global_state.get(key, {}).get("version", 0) + 1
            }

    async def get_global_state(self, key: str):
        """Get global state"""
        return self.global_state.get(key, {}).get("value")

    async def broadcast_message(self, from_agent: str, message: dict):
        """Broadcast message to all agents"""
        async with self.lock:
            self.message_bus.append({
                "from": from_agent,
                "message": message,
                "timestamp": datetime.utcnow()
            })

    async def get_messages_for_agent(self, agent_id: str, since: datetime = None):
        """Get messages for specific agent"""
        messages = [
            msg for msg in self.message_bus
            if msg["from"] != agent_id  # Don't include own messages
        ]

        if since:
            messages = [
                msg for msg in messages
                if msg["timestamp"] > since
            ]

        return messages

    def get_agent_memory(self, agent_id: str):
        """Get or create memory for agent"""
        if agent_id not in self.agent_memories:
            self.agent_memories[agent_id] = ConversationBuffer()
        return self.agent_memories[agent_id]

# Usage in multi-agent system
shared_memory = SharedMemory()

# Agent 1 stores information
await shared_memory.set_global_state("current_task", "Analyze data")
await shared_memory.broadcast_message("agent1", {
    "type": "task_complete",
    "result": "Analysis done"
})

# Agent 2 retrieves information
current_task = await shared_memory.get_global_state("current_task")
messages = await shared_memory.get_messages_for_agent("agent2")
```

## Memory Optimization Techniques

### 1. Prompt Caching (Claude 3.5+)

```python
# Good: Use prompt caching for repeated context
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": large_system_prompt,  # Will be cached
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": large_document,  # Will be cached
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": "What does this document say about X?"  # Not cached
                }
            ]
        }
    ]
)
```

**Caching Benefits:**
- 90% cost reduction for cached tokens
- Faster response times
- Ideal for repeated context (system prompts, documents)

### 2. Context Compression

```python
# Good: Compress old context
def compress_context(messages):
    """Compress old messages to reduce tokens"""
    if len(messages) < 10:
        return messages

    # Keep recent messages (last 5 turns)
    recent = messages[-10:]

    # Compress older messages
    old_messages = messages[:-10]
    compressed_text = compress_conversation(old_messages)

    return [
        {"role": "user", "content": f"Previous context: {compressed_text}"},
        {"role": "assistant", "content": "Understood."},
        *recent
    ]
```

### 3. Selective Memory Storage

```python
# Good: Only store important information
def should_store_in_memory(message: str, response: str) -> bool:
    """Determine if conversation should be stored in long-term memory"""

    # Use Claude to judge importance
    judge_response = client.messages.create(
        model="claude-3-haiku-20240307",  # Use Haiku for cost
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""Is this conversation important to remember long-term?
User: {message}
Assistant: {response}

Answer only: YES or NO"""
        }]
    )

    return "YES" in judge_response.content[0].text.upper()

# Only store important facts
if should_store_in_memory(user_message, assistant_message):
    semantic_memory.store(f"User: {user_message}\nAssistant: {assistant_message}")
```

## Memory Checklist

Before deploying agent memory systems:

**Short-Term Memory**
- [ ] Conversation buffer size limits set
- [ ] Token counting implemented
- [ ] Pruning strategy defined
- [ ] Memory cleared appropriately

**Long-Term Memory**
- [ ] Vector database configured
- [ ] Embedding model selected
- [ ] Retrieval strategy implemented
- [ ] Memory importance scoring
- [ ] Regular cleanup scheduled

**Memory Optimization**
- [ ] Prompt caching enabled (3.5+ models)
- [ ] Context compression implemented
- [ ] Selective memory storage
- [ ] Token usage monitored

**Multi-Agent Memory**
- [ ] Shared state management
- [ ] Message passing implemented
- [ ] Concurrency handled
- [ ] Memory isolation where needed

**Testing**
- [ ] Long conversation tests
- [ ] Memory retrieval accuracy
- [ ] Context limits tested
- [ ] Memory consistency verified

Use these patterns to build effective memory systems for production AI agents.
