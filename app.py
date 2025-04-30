import streamlit as st
import tiktoken

# Set near-maximum token limit for GPT-4o
MAX_TOKENS = 127000
enc = tiktoken.encoding_for_model("gpt-4")

def split_text_by_tokens(text, max_tokens=MAX_TOKENS):
    words = text.split()
    chunks = []
    current_chunk = []
    current_tokens = 0

    for word in words:
        token_count = len(enc.encode(" " + word))
        if current_tokens + token_count > max_tokens:
            chunk_text = " ".join(current_chunk)
            chunks.append((chunk_text, current_tokens))
            current_chunk = [word]
            current_tokens = token_count
        else:
            current_chunk.append(word)
            current_tokens += token_count

    if current_chunk:
        chunks.append((" ".join(current_chunk), current_tokens))

    return chunks

# Streamlit UI
st.title("GPT-4o Max Token Text Splitter")

text_input = st.text_area("Paste your full text here", height=300)
uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])

if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")

if text_input:
    chunks = split_text_by_tokens(text_input)
    st.success(f"✅ Text split into {len(chunks)} chunk(s), each close to {MAX_TOKENS} tokens.")

    for i, (chunk, token_count) in enumerate(chunks):
        st.text_area(f"Chunk {i+1} — {token_count} tokens", value=chunk, height=250)

    st.download_button("📥 Download All Chunks", "\n\n---\n\n".join(chunk for chunk, _ in chunks), file_name="chunks.txt")
