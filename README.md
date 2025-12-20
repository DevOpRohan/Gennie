# Gennie 🧞
**Your Local AI Super-Assistant**

Gennie is an intelligent, agentic local assistant that doesn't just chat—it **does** things. It watches your files, executes code, manages your tasks, and remembers your context.

> [!TIP]
> **Want the deep dive?** Read [How Gennie Works](./documentation.md) for a technical tour of the architecture.

## ✨ Key Features

*   **👀 Real-Time File Ecosystem**: Watches your working directory. Drop a file, and Gennie knows about it instantly—no uploads required.
*   **🧠 Agentic Reasoning**: Uses a ReAct loop to plan, execute, and verify tasks rather than just spitting out text.
*   **🐍 Python Code Interpreter**: A stateful environment to run data analysis, math, or file manipulation scripts.
*   **✅ Integrated Task Manager**: Remembers your ToDos and manages them via a built-in SQL database.
*   **🔍 Multimodal Memory**: Search your local knowledge base using text or even images.

## 🚀 Quick Start

### Prerequisites
*   Python 3.10+
*   An OpenAI API Key (or compatible LLM endpoint)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Gennie.git
    cd Gennie
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Export your OpenAI API key:
    ```bash
    export OPENAI_API_KEY="sk-..."
    ```

### Running Gennie

Start the Streamlit interface:

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`, point Gennie to your working directory, and start building.
