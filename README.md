# ChatGPT Text Chunker

A simple Streamlit app to split long text into optimized chunks for ChatGPT, especially GPT-4o, supporting up to 127,000 tokens per chunk. Perfect for RAG pipelines, prompt engineering, or loading large context into multi-turn conversations.

---

## 🔍 Features

- Paste text or upload `.txt` files
- Splits using OpenAI's `tiktoken` tokenizer
- Displays token count per chunk
- Targets up to 127k tokens per chunk (GPT-4o compatible)
- Download chunks as a single `.txt` file

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/chat-gpt-text-chunker.git
cd chat-gpt-text-chunker
