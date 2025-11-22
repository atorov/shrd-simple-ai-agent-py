# Simple AI Agent (Python)

A lightweight, extensible AI agent implementation in Python that leverages local Large Language Models (LLMs) via [Ollama](https://ollama.com/). This agent is capable of performing file system operations and executing system commands to accomplish complex tasks autonomously.

## 🚀 Features

- **Local LLM Integration**: Uses Ollama for privacy-focused, local inference (defaulting to `qwen3`).
- **Tool-Use Capabilities**:
  - 📂 **File System**: List directories and read file contents.
  - ✏️ **File Editing**: Modify files by replacing text segments.
  - 💻 **Shell Execution**: Run bash commands directly from the agent.
- **Simple Architecture**: Easy to understand loop-based agent structure.

## 📋 Prerequisites

Before running the agent, ensure you have the following installed:

- **Python 3.8+**
- **[Ollama](https://ollama.com/)**: The backend for running the LLM.
- **Qwen3 Model**: You need to pull the specific model used by the agent.

  ```bash
  ollama pull qwen3
  ```

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd shrd-simple-ai-agent-py
   ```

2. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Usage

1. Ensure the Ollama service is running in the background.
2. Run the agent:

   ```bash
   python main.py
   ```

## ⚠️ Security Disclaimer

This agent has access to **run bash commands** and **modify files** on your system.

- Run it in a controlled environment (like a container or sandbox) if possible.
- Review the code in `main.py` to understand the tools available to the model.
- Use with caution.
