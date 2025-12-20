# Why Your "Chat with PDF" App is Boring (And How Gennie Fixes It)
*Building a truly agentic local assistant that watches your files, runs code, and actually remembers things.*

---

## The "Chat with Data" Illusion

We've all built it. The "Hello World" of LLM apps:
1.  Upload a PDF.
2.  Chunk it.
3.  Embed it.
4.  Ask "What is this file about?"

It's cool for five minutes. But then you realize: **it's pasive.** It waits for you. It doesn't know what you did five minutes ago. It can't *do* anything other than summarize text.

I wanted something different. I wanted an assistant that:
*   👀 **Watches** my working directory in real-time.
*   🐍 **Executes Python code** to solve complex math or data problems.
*   🧠 **Remembers** our past conversations and learns.
*   ✅ **Manages** my tasks so I don't have to.

So I built **Gennie**.

---

## The Architecture: More Than Just RAG

Gennie isn't just a RAG wrapper. It's an **Agentic Loop** hooked up to a live reliable file system watcher and a stateful code execution environment.

### 1. The Eyes: Real-Time Ingestion (`ingestor/`)
Most apps make you manually upload files. Gennie watches your back.

Using `watchdog`, Gennie monitors your `working_directory`.
*   **Drop a PDF?** It's OCR'd and indexed instantly.
*   **Move a file?** The vector store updates the reference.
*   **Delete a file?** It's gone from the memory.

This happens in `ingestor.py` via the `DirectoryIngestor`:

```python
class DirectoryIngestor(Ingestor):
    # ...
    def start_file_watcher(self, directory_path):
        event_handler = IngestionEventHandler(self)
        observer = Observer()
        observer.schedule(event_handler, directory_path, recursive=True)
        observer.start()
```

It maintains a SQL database (`files` table) to track hashes and paths, ensuring we don't re-index unchanged files.

### 2. The Brain: The ReAct Loop (`agent/gennie.py`)
Gennie doesn't just "chat". It **thinks**.

It uses a custom ReAct (Reasoning + Acting) loop. When you ask a question, Gennie doesn't just generate text. It generates a **Plan**.

The `gennie` function is the heart. It sits in a loop (up to `max_loop_count` times) allowing it to:
1.  **Thought**: "I need to calculate the Fibonacci sequence."
2.  **Action**: Calls `python_interpreter`.
3.  **Observation**: Gets the result.
4.  **Answer**: "The result is..."

```python
# The Loop
while gpt_response_count <= max_loop_count:
    # 1. Ask LLM
    completion = await openai_chat_async(...)
    
    # 2. Check for Tool Calls
    if 'tool_calls' in completion:
        # Execute tools (Search, Python, SQL)
        res = open_ai_tools_execution(...)
        messages.extend(res)
    else:
        # 3. Check if done
        res = parser(assistant_response)
        if res['reply'] != "":
            return res['reply']
```

### 3. The Hands: Tools (`agent/tools.py`)
An agent is only as good as its tools. Gennie has a Swiss Army knife:

#### 🐍 Code Interpreter
Not just a calculator. It's a **stateful Jupyter-like environment**. If you define `x = 5` in one turn, `x` is still `5` in the next.
*   *Use case:* "Read this CSV file I just dropped in the folder and plot a graph."

#### 🗄️ SQL ToDo Manager
A dedicated SQLite database for task management.
*   *Use case:* "Remind me to check the deployment status."
*   Gennie writes the SQL: `INSERT INTO todos (task, status) VALUES ...`

#### 🔍 Semantic Search
Not just text. **Multimodal**.
*   `search`: Detailed text retrieval.
*   `text_to_image_search`: Find slides or diagrams based on descriptions.
*   `image_to_image_search`: Find similar assets.

---

## Why This Matters

Gennie represents a shift from **stateless chatbots** to **stateful agents**.

*   It lives on **your** machine.
*   It works with **your** files.
*   It uses **your** tools.

It's not just "Artificial Intelligence". It's **Augmented Intelligence** for your local workflow. 
