# Introduction to LLM Application Engineering

## Table of Contents

- [What is LLM Application Engineering](#what-is-llm-application-engineering)
- [LLM Fundamentals](#llm-fundamentals)
- [API Basics](#api-basics)
- [Prompt Design Patterns](#prompt-design-patterns)
- [Structured Output](#structured-output)
- [Building Pipelines](#building-pipelines)
- [Context Management](#context-management)
- [Evaluation](#evaluation)
- [Error Handling](#error-handling)
- [Cost Optimization](#cost-optimization)
- [Common Architectures](#common-architectures)
- [Observability](#observability)
- [Practice Exercises](#practice-exercises)
- [Summary](#summary)
- [Next Steps](#next-steps)
- [Additional Resources](#additional-resources)

---

## What is LLM Application Engineering

LLM Application Engineering is the discipline of building reliable, production-grade software systems powered by large language models. It sits at the intersection of software engineering and AI, focusing on how to effectively integrate LLMs into applications.

Key concerns include:

- **Reliability**: LLMs are non-deterministic; engineering around this uncertainty
- **Cost management**: optimizing token usage and model selection
- **Latency**: managing response times for real-time applications
- **Safety**: handling harmful outputs, prompt injection, and data privacy
- **Evaluation**: measuring quality when outputs are subjective
- **Scalability**: serving many users with rate-limited APIs

```python
# A minimal LLM application - the building block of everything else
import anthropic

# Initialize the client with your API key
client = anthropic.Anthropic()

# Make a simple completion request
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is LLM application engineering?"}
    ]
)

# Extract the text response
print(response.content[0].text)
```

---

## LLM Fundamentals

Understanding key concepts is essential for building effective LLM applications.

**Tokens** are the basic units of text processing:

```python
# Tokens are subword units, not whole words
# "Hello world" -> ["Hello", " world"] (2 tokens)
# "unbelievable" -> ["un", "believ", "able"] (3 tokens)

# Token counting matters for cost and context limits
import anthropic

# Approximate token counting (rule of thumb)
# English: ~4 characters per token, or ~0.75 words per token
text = "This is an example sentence for token estimation."
approx_tokens = len(text) / 4  # rough estimate: ~12.5 tokens

# Most APIs report token usage in the response
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[{"role": "user", "content": text}]
)
print(f"Input tokens: {response.usage.input_tokens}")   # actual input count
print(f"Output tokens: {response.usage.output_tokens}")  # actual output count
```

**Context windows** define how much text the model can process:

```python
# Context window = input tokens + output tokens
# Claude Sonnet: 200K token context window
# This means the total of your prompt + response must fit

# Context window considerations:
# - Larger context = more information available
# - But: cost scales with token count
# - And: very long contexts can reduce quality ("lost in the middle")

# Calculate remaining space for output
max_context = 200000
input_tokens = response.usage.input_tokens
remaining_for_output = max_context - input_tokens
print(f"Remaining for output: {remaining_for_output} tokens")
```

**Temperature and Top-p** control randomness in outputs:

```python
# Temperature controls randomness (0.0 = deterministic, 1.0 = creative)
# Use low temperature for factual/analytical tasks
factual_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    temperature=0.0,  # deterministic output for consistent results
    messages=[{"role": "user", "content": "What is the capital of France?"}]
)

# Use higher temperature for creative tasks
creative_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    temperature=0.8,  # more varied and creative output
    messages=[{"role": "user", "content": "Write a haiku about programming."}]
)

# Top-p (nucleus sampling) is an alternative to temperature
# top_p=0.9 means consider tokens comprising the top 90% probability mass
# Generally, adjust temperature OR top-p, not both
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    top_p=0.9,  # nucleus sampling
    messages=[{"role": "user", "content": "Suggest a project name."}]
)
```

---

## API Basics

Most LLM APIs follow a chat completions pattern with message-based conversations.

```python
import anthropic

client = anthropic.Anthropic()

# The messages format: a list of role/content pairs
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful Python tutor.",  # system prompt sets behavior
    messages=[
        # User message: the human's input
        {"role": "user", "content": "Explain list comprehensions."},
        # Assistant message: Claude's previous response (for multi-turn)
        {"role": "assistant", "content": "List comprehensions provide a concise way..."},
        # User follow-up
        {"role": "user", "content": "Show me a complex example."}
    ]
)
```

Understanding the three roles:

```python
# System role: sets overall behavior, persona, and constraints
# - Processed once at the start
# - Not visible in conversation history
# - Ideal for: instructions, persona, output format, guardrails

# User role: represents the human's messages
# - Contains questions, tasks, data to process
# - Can include structured data, code, documents

# Assistant role: represents the AI's responses
# - Used in multi-turn to provide conversation history
# - Can be "prefilled" to guide the response format

# Prefilling example: guide Claude to respond in JSON
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=256,
    messages=[
        {"role": "user", "content": "List 3 Python frameworks as JSON."},
        {"role": "assistant", "content": "{"}  # prefill to force JSON output
    ]
)
# Claude will continue from "{" and produce valid JSON
```

Streaming responses for better user experience:

```python
# Streaming returns tokens as they are generated
# Essential for chat interfaces and real-time applications
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain async programming in Python."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)  # print each token as it arrives

print()  # newline after streaming completes

# Get the final message object with usage stats
final_message = stream.get_final_message()
print(f"Total tokens used: {final_message.usage.input_tokens + final_message.usage.output_tokens}")
```

---

## Prompt Design Patterns

Effective prompts follow repeatable patterns that improve output quality.

```python
# Few-shot prompting: provide examples to guide behavior
few_shot_messages = [
    {"role": "user", "content": """Classify the sentiment of each review.

Examples:
Review: "This product is amazing, I love it!" -> Positive
Review: "Terrible quality, broke after one day." -> Negative
Review: "It's okay, nothing special." -> Neutral

Now classify:
Review: "Best purchase I've made this year, highly recommend!"
"""}
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=64,
    messages=few_shot_messages
)
```

Chain-of-thought prompting:

```python
# Chain-of-thought: ask the model to reason step by step
cot_response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": """Solve this step by step:

A store has 45 apples. They sell 60% on Monday and half of the
remaining on Tuesday. How many apples are left?

Think through this step by step before giving the final answer."""
    }]
)
# The model will show its reasoning, reducing errors in the final answer
```

Role prompting:

```python
# Role prompting via system message
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="""You are a senior security engineer performing a code review.
Focus on: SQL injection, XSS, authentication flaws, and data exposure.
For each issue found, rate severity (Critical/High/Medium/Low) and
provide a specific fix.""",
    messages=[{
        "role": "user",
        "content": f"Review this code:\n\n```python\n{code_to_review}\n```"
    }]
)
```

Structured prompt template:

```python
# A reusable prompt template with clear sections
def build_analysis_prompt(code: str, language: str, focus_areas: list[str]) -> str:
    """Build a structured code analysis prompt."""
    focus_list = "\n".join(f"- {area}" for area in focus_areas)
    return f"""Analyze the following {language} code.

<code>
{code}
</code>

<focus_areas>
{focus_list}
</focus_areas>

<output_format>
For each issue found:
1. Line number(s)
2. Issue description
3. Severity (Critical/High/Medium/Low)
4. Suggested fix with code
</output_format>

Provide your analysis:"""

# Use the template
prompt = build_analysis_prompt(
    code="def login(user, pwd): return db.query(f'SELECT * FROM users WHERE name={user}')",
    language="Python",
    focus_areas=["SQL injection", "Input validation", "Error handling"]
)
```

---

## Structured Output

Getting LLMs to produce machine-readable structured output is critical for building pipelines.

```python
# JSON mode: instruct the model to output valid JSON
import json

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=512,
    system="Always respond with valid JSON. No markdown, no explanation.",
    messages=[{
        "role": "user",
        "content": """Extract entities from this text and return JSON:

"Apple Inc. CEO Tim Cook announced a new product at their
Cupertino headquarters on March 15, 2025."

Schema: {"entities": [{"text": str, "type": "PERSON|ORG|LOCATION|DATE"}]}"""
    }]
)

# Parse the JSON response
entities = json.loads(response.content[0].text)
print(entities)
# {"entities": [
#   {"text": "Apple Inc.", "type": "ORG"},
#   {"text": "Tim Cook", "type": "PERSON"},
#   {"text": "Cupertino", "type": "LOCATION"},
#   {"text": "March 15, 2025", "type": "DATE"}
# ]}
```

Function calling / tool use:

```python
# Tool use lets the model call functions you define
# The model decides WHEN to call a tool and with WHAT arguments

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    ],
    messages=[
        {"role": "user", "content": "What's the weather like in Seattle?"}
    ]
)

# Check if the model wants to use a tool
for block in response.content:
    if block.type == "tool_use":
        tool_name = block.name       # "get_weather"
        tool_input = block.input     # {"location": "Seattle, WA"}
        tool_use_id = block.id       # unique ID for this tool call

        # Execute the function and return results
        weather_data = get_weather(**tool_input)  # your implementation

        # Send tool result back to continue the conversation
        followup = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=[...],  # same tool definitions
            messages=[
                {"role": "user", "content": "What's the weather like in Seattle?"},
                {"role": "assistant", "content": response.content},
                {
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": json.dumps(weather_data)
                    }]
                }
            ]
        )
```

Using Pydantic for response validation:

```python
from pydantic import BaseModel, ValidationError

# Define expected response structure
class SentimentResult(BaseModel):
    text: str
    sentiment: str  # "positive", "negative", "neutral"
    confidence: float  # 0.0 to 1.0
    key_phrases: list[str]

def analyze_sentiment(text: str) -> SentimentResult:
    """Analyze sentiment with structured, validated output."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=256,
        system="Respond with valid JSON matching the schema exactly.",
        messages=[{
            "role": "user",
            "content": f"""Analyze the sentiment of this text:
"{text}"

JSON schema: {SentimentResult.model_json_schema()}"""
        }]
    )

    # Parse and validate with Pydantic
    try:
        result = SentimentResult.model_validate_json(response.content[0].text)
        return result
    except ValidationError as e:
        raise ValueError(f"Model returned invalid structure: {e}")
```

---

## Building Pipelines

Real applications chain multiple LLM calls and processing steps into pipelines.

```python
# Sequential pipeline: each step feeds into the next
def document_qa_pipeline(document: str, question: str) -> dict:
    """Answer a question about a document with citation."""

    # Step 1: Extract relevant passages
    extraction = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Extract passages from this document that are relevant
to the question: "{question}"

Document:
{document}

Return only the relevant passages, numbered."""
        }]
    )
    relevant_passages = extraction.content[0].text

    # Step 2: Generate answer from passages
    answer = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": f"""Based on these passages, answer the question.
Include passage numbers as citations.

Passages:
{relevant_passages}

Question: {question}

Answer with citations:"""
        }]
    )

    return {
        "passages": relevant_passages,
        "answer": answer.content[0].text,
        "input_tokens": extraction.usage.input_tokens + answer.usage.input_tokens,
        "output_tokens": extraction.usage.output_tokens + answer.usage.output_tokens
    }
```

Routing pattern:

```python
# Router: use a fast/cheap model to decide which specialized pipeline to use
def route_request(user_input: str) -> str:
    """Route user input to the appropriate handler."""
    routing = client.messages.create(
        model="claude-haiku-4-20250514",  # fast, cheap model for routing
        max_tokens=32,
        system="""Classify the user request into exactly one category:
- CODE: code generation, debugging, or review
- ANALYSIS: data analysis or summarization
- CREATIVE: creative writing or brainstorming
- QA: factual questions
Respond with only the category name.""",
        messages=[{"role": "user", "content": user_input}]
    )

    category = routing.content[0].text.strip()

    # Route to specialized handler with appropriate model and prompt
    handlers = {
        "CODE": handle_code_request,
        "ANALYSIS": handle_analysis_request,
        "CREATIVE": handle_creative_request,
        "QA": handle_qa_request,
    }

    handler = handlers.get(category, handle_qa_request)  # default to QA
    return handler(user_input)
```

Fallback pattern:

```python
# Fallback: try a cheaper model first, escalate if needed
def generate_with_fallback(prompt: str, max_retries: int = 2) -> str:
    """Try cheaper model first, fall back to more capable model."""
    models = [
        "claude-haiku-4-20250514",   # cheapest, try first
        "claude-sonnet-4-20250514",  # mid-tier fallback
    ]

    for model in models:
        try:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.content[0].text

            # Validate output quality (application-specific check)
            if is_quality_sufficient(result):
                return result
            # If quality is insufficient, try next model

        except anthropic.APIError as e:
            continue  # try next model on API errors

    raise RuntimeError("All models failed to produce acceptable output")
```

---

## Context Management

Managing context effectively is crucial when dealing with the finite context window.

```python
# Chunking: split large documents into processable pieces
def chunk_text(text: str, chunk_size: int = 4000, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks by character count."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # overlap prevents cutting mid-sentence
    return chunks

# Process each chunk and combine results
def summarize_long_document(document: str) -> str:
    """Summarize a document that exceeds the context window."""
    chunks = chunk_text(document, chunk_size=8000, overlap=500)

    # Step 1: Summarize each chunk individually
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=512,
            messages=[{
                "role": "user",
                "content": f"Summarize this section (part {i+1}/{len(chunks)}):\n\n{chunk}"
            }]
        )
        chunk_summaries.append(response.content[0].text)

    # Step 2: Combine chunk summaries into final summary
    combined = "\n\n".join(chunk_summaries)
    final = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Combine these section summaries into one coherent summary:\n\n{combined}"
        }]
    )
    return final.content[0].text
```

Sliding window for conversations:

```python
# Sliding window: keep recent messages, summarize older ones
class ConversationManager:
    """Manage conversation history with a sliding window."""

    def __init__(self, max_messages: int = 20):
        self.messages = []          # full history
        self.max_messages = max_messages
        self.summary = ""           # summary of older messages

    def add_message(self, role: str, content: str):
        """Add a message and compact history if needed."""
        self.messages.append({"role": role, "content": content})

        if len(self.messages) > self.max_messages:
            self._compact()

    def _compact(self):
        """Summarize older messages to free up context space."""
        # Take the oldest half of messages to summarize
        split = len(self.messages) // 2
        old_messages = self.messages[:split]

        # Summarize old messages
        history_text = "\n".join(
            f"{m['role']}: {m['content']}" for m in old_messages
        )
        response = client.messages.create(
            model="claude-haiku-4-20250514",  # cheap model for summarization
            max_tokens=256,
            messages=[{
                "role": "user",
                "content": f"Summarize this conversation concisely:\n\n{history_text}"
            }]
        )
        self.summary = response.content[0].text
        self.messages = self.messages[split:]  # keep recent messages

    def get_messages(self) -> list[dict]:
        """Get messages with summary context for API call."""
        messages = []
        if self.summary:
            # Inject summary as context at the beginning
            messages.append({
                "role": "user",
                "content": f"[Previous conversation summary: {self.summary}]"
            })
            messages.append({
                "role": "assistant",
                "content": "I understand the context from our previous discussion."
            })
        messages.extend(self.messages)
        return messages
```

---

## Evaluation

Evaluating LLM outputs is essential for quality assurance and improvement.

```python
# Automated metrics for measurable outputs
from difflib import SequenceMatcher

def evaluate_extraction(predicted: dict, expected: dict) -> dict:
    """Evaluate structured extraction against ground truth."""
    metrics = {
        "exact_match": predicted == expected,
        "field_accuracy": 0.0,
        "missing_fields": [],
        "extra_fields": []
    }

    # Check field-by-field accuracy
    all_fields = set(expected.keys()) | set(predicted.keys())
    correct = sum(1 for k in expected if predicted.get(k) == expected[k])
    metrics["field_accuracy"] = correct / len(expected) if expected else 0
    metrics["missing_fields"] = [k for k in expected if k not in predicted]
    metrics["extra_fields"] = [k for k in predicted if k not in expected]

    return metrics
```

LLM-as-judge:

```python
# Use an LLM to evaluate another LLM's output
def llm_judge(question: str, answer: str, criteria: list[str]) -> dict:
    """Use Claude as a judge to evaluate an answer."""
    criteria_text = "\n".join(f"- {c}" for c in criteria)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        system="You are an impartial judge evaluating AI-generated answers.",
        messages=[{
            "role": "user",
            "content": f"""Evaluate this answer on the given criteria.

Question: {question}
Answer: {answer}

Criteria:
{criteria_text}

For each criterion, provide a score (1-5) and brief justification.
Respond in JSON: {{"scores": [{{"criterion": str, "score": int, "reason": str}}], "overall": int}}"""
        }]
    )

    import json
    return json.loads(response.content[0].text)

# Usage
scores = llm_judge(
    question="Explain Python decorators",
    answer=model_output,
    criteria=["Accuracy", "Completeness", "Clarity", "Code examples"]
)
```

Building an evaluation suite:

```python
# Evaluation dataset: pairs of inputs and expected outputs
eval_dataset = [
    {
        "input": "What is the capital of France?",
        "expected": "Paris",
        "type": "factual"
    },
    {
        "input": "Classify: 'I love this!' -> sentiment",
        "expected": "positive",
        "type": "classification"
    },
]

def run_eval_suite(dataset: list[dict], model: str) -> dict:
    """Run an evaluation suite and compute metrics."""
    results = {"correct": 0, "total": len(dataset), "errors": []}

    for item in dataset:
        response = client.messages.create(
            model=model,
            max_tokens=128,
            temperature=0.0,  # deterministic for evaluation
            messages=[{"role": "user", "content": item["input"]}]
        )
        output = response.content[0].text.strip().lower()
        expected = item["expected"].lower()

        if expected in output:
            results["correct"] += 1
        else:
            results["errors"].append({
                "input": item["input"],
                "expected": expected,
                "got": output
            })

    results["accuracy"] = results["correct"] / results["total"]
    return results
```

---

## Error Handling

Robust error handling is essential for production LLM applications.

```python
import anthropic
import time

def call_with_retry(
    messages: list[dict],
    max_retries: int = 3,
    base_delay: float = 1.0
) -> anthropic.types.Message:
    """Call the API with exponential backoff retry logic."""

    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=messages
            )
            return response

        except anthropic.RateLimitError:
            # Rate limited: wait with exponential backoff
            if attempt == max_retries:
                raise
            delay = base_delay * (2 ** attempt)  # 1s, 2s, 4s
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)

        except anthropic.APIStatusError as e:
            # Server errors (500, 503): retry
            if e.status_code >= 500 and attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                print(f"Server error {e.status_code}. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise  # client errors (400, 401, 403) should not be retried

        except anthropic.APIConnectionError:
            # Network issues: retry
            if attempt == max_retries:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Connection error. Retrying in {delay}s...")
            time.sleep(delay)
```

Content filtering and safety:

```python
def safe_generate(user_input: str) -> dict:
    """Generate a response with content safety checks."""

    # Pre-processing: basic input validation
    if len(user_input) > 50000:
        return {"error": "Input too long", "output": None}

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system="You are a helpful assistant. Refuse harmful requests politely.",
            messages=[{"role": "user", "content": user_input}]
        )

        # Check stop reason
        if response.stop_reason == "end_turn":
            return {"output": response.content[0].text, "error": None}
        elif response.stop_reason == "max_tokens":
            return {"output": response.content[0].text, "error": "truncated"}
        else:
            return {"output": None, "error": f"Unexpected stop: {response.stop_reason}"}

    except anthropic.BadRequestError as e:
        return {"output": None, "error": f"Bad request: {e.message}"}
```

---

## Cost Optimization

Controlling costs is critical for sustainable LLM applications.

```python
# Model selection: choose the right model for each task
MODEL_TIERS = {
    "simple": "claude-haiku-4-20250514",     # classification, routing, extraction
    "standard": "claude-sonnet-4-20250514",  # general tasks, code, analysis
    "complex": "claude-opus-4-20250514",     # complex reasoning, nuanced tasks
}

def select_model(task_complexity: str) -> str:
    """Select the most cost-effective model for the task."""
    return MODEL_TIERS.get(task_complexity, MODEL_TIERS["standard"])

# Prompt caching: reuse common prefixes to reduce costs
# Anthropic supports prompt caching for repeated system prompts
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": large_system_prompt,     # this gets cached after first call
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": user_query}]
)

# Prompt compression: reduce token count without losing meaning
def compress_prompt(context: str, max_chars: int = 8000) -> str:
    """Compress context to fit within budget."""
    if len(context) <= max_chars:
        return context

    # Use a cheap model to summarize the context
    response = client.messages.create(
        model="claude-haiku-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Summarize this text, preserving all key facts:\n\n{context}"
        }]
    )
    return response.content[0].text

# Token budget tracking
class TokenBudget:
    """Track and limit token usage across requests."""

    def __init__(self, daily_limit: int = 1_000_000):
        self.daily_limit = daily_limit
        self.tokens_used = 0

    def check_budget(self, estimated_tokens: int) -> bool:
        """Check if we have budget for this request."""
        return (self.tokens_used + estimated_tokens) <= self.daily_limit

    def record_usage(self, response):
        """Record token usage from a response."""
        self.tokens_used += response.usage.input_tokens + response.usage.output_tokens
```

---

## Common Architectures

Standard patterns for LLM-powered applications.

```python
# 1. Chatbot: multi-turn conversation with memory
class Chatbot:
    """Simple chatbot with conversation history."""

    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.history = []

    def chat(self, user_message: str) -> str:
        """Send a message and get a response."""
        self.history.append({"role": "user", "content": user_message})

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.history
        )

        assistant_message = response.content[0].text
        self.history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

# 2. Agent: LLM with tool use in a loop
def agent_loop(user_task: str, tools: list[dict], max_steps: int = 10) -> str:
    """Run an agent loop: think -> act -> observe -> repeat."""
    messages = [{"role": "user", "content": user_task}]

    for step in range(max_steps):
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # Check if the model is done (no more tool calls)
        if response.stop_reason == "end_turn":
            return response.content[0].text

        # Process tool calls
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)  # your implementation
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })
        messages.append({"role": "user", "content": tool_results})

    return "Agent reached maximum steps without completing."

# 3. RAG: Retrieve context, then generate
def rag_query(question: str, vector_store) -> str:
    """Simple RAG: retrieve relevant docs, then answer."""
    # Retrieve relevant documents
    docs = vector_store.similarity_search(question, k=5)
    context = "\n\n".join(doc.page_content for doc in docs)

    # Generate answer grounded in retrieved context
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""Answer based on the provided context only.

Context:
{context}

Question: {question}

If the context doesn't contain the answer, say so."""
        }]
    )
    return response.content[0].text
```

---

## Observability

Monitoring and debugging LLM applications in production.

```python
import logging
import time
from dataclasses import dataclass, field

# Structured logging for LLM calls
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger("llm_app")

@dataclass
class LLMCallTrace:
    """Record details of an LLM API call for observability."""
    request_id: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    status: str = "pending"
    error: str = ""
    metadata: dict = field(default_factory=dict)

def traced_call(messages: list[dict], model: str, trace_id: str, **kwargs) -> tuple:
    """Make an API call with full tracing."""
    trace = LLMCallTrace(request_id=trace_id, model=model)
    start_time = time.time()

    try:
        response = client.messages.create(
            model=model,
            messages=messages,
            **kwargs
        )
        trace.input_tokens = response.usage.input_tokens
        trace.output_tokens = response.usage.output_tokens
        trace.status = "success"
        trace.latency_ms = (time.time() - start_time) * 1000

        logger.info(
            "LLM call completed | id=%s model=%s input=%d output=%d latency=%.0fms",
            trace.request_id, trace.model,
            trace.input_tokens, trace.output_tokens, trace.latency_ms
        )
        return response, trace

    except Exception as e:
        trace.status = "error"
        trace.error = str(e)
        trace.latency_ms = (time.time() - start_time) * 1000
        logger.error("LLM call failed | id=%s error=%s", trace.request_id, str(e))
        raise

# Monitoring dashboard metrics
class LLMMetrics:
    """Aggregate metrics for monitoring dashboards."""

    def __init__(self):
        self.total_calls = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_errors = 0
        self.latencies = []

    def record(self, trace: LLMCallTrace):
        """Record metrics from a traced call."""
        self.total_calls += 1
        self.total_input_tokens += trace.input_tokens
        self.total_output_tokens += trace.output_tokens
        self.latencies.append(trace.latency_ms)
        if trace.status == "error":
            self.total_errors += 1

    def summary(self) -> dict:
        """Get summary metrics."""
        return {
            "total_calls": self.total_calls,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "error_rate": self.total_errors / max(self.total_calls, 1),
            "avg_latency_ms": sum(self.latencies) / max(len(self.latencies), 1),
            "p95_latency_ms": sorted(self.latencies)[int(len(self.latencies) * 0.95)]
            if self.latencies else 0,
        }
```

---

## Practice Exercises

1. **Basic API call**: Write a function that takes a question and returns Claude's response. Handle rate limits and log token usage.

2. **Structured extraction**: Build a pipeline that extracts structured data (name, email, phone) from unstructured text and validates with Pydantic.

3. **Multi-step pipeline**: Create a pipeline that (a) summarizes a document, (b) extracts key topics, (c) generates quiz questions from the topics.

4. **Conversation manager**: Implement a chatbot with sliding window context management that summarizes old messages.

5. **Evaluation harness**: Build an eval suite with 10+ test cases for a classification task. Compare Haiku vs Sonnet accuracy and cost.

6. **Agent with tools**: Build a simple agent that can use a calculator tool and a knowledge base lookup tool to answer questions.

---

## Summary

LLM Application Engineering involves building reliable systems around large language models. Key takeaways:

- **API fundamentals**: understand tokens, context windows, temperature, and message roles
- **Prompt patterns**: few-shot, chain-of-thought, and role prompting improve output quality
- **Structured output**: JSON mode and tool use enable machine-readable responses
- **Pipelines**: chain LLM calls with routing, fallbacks, and sequential processing
- **Context management**: chunking, summarization, and sliding windows handle large inputs
- **Evaluation**: combine automated metrics with LLM-as-judge for quality assurance
- **Error handling**: retries with exponential backoff, content filtering, and graceful degradation
- **Cost optimization**: model tiering, caching, and prompt compression control spend
- **Observability**: structured logging and metrics enable production monitoring

---

## Next Steps

- Build a complete RAG application (see the RAG notes)
- Study prompt engineering techniques in depth (see Prompt Engineering notes)
- Experiment with tool use to build agent-based applications
- Set up an evaluation pipeline for your specific use case
- Implement observability with a tracing tool like Langfuse or LangSmith
- Explore fine-tuning for specialized tasks where prompting is insufficient

---

## Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/en/docs)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com/docs)
- [LlamaIndex Documentation](https://docs.llamaindex.ai)
- [Braintrust Eval Framework](https://www.braintrust.dev)
