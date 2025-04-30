import streamlit as st
import tiktoken

# Settings
MAX_TOKENS = 27000
MODEL_NAME = "gpt-4"

# Initialize tokenizer
enc = tiktoken.encoding_for_model(MODEL_NAME)

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

# UI
st.title("📚 ChatGPT Text Chunker (27K Token Chunks)")
st.markdown("Split large text into ChatGPT-ready chunks with a 27,000-token limit. Each chunk includes the instruction `just answer ok:` and optionally adds source info.")

# Inputs
text_input = st.text_area("Paste your full text here", height=300)
uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])
source_info = st.text_input("Optional: Add source information (e.g., document title or link)")

if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")

if text_input:
    st.info("🔄 Splitting text...")
    chunks = split_text_by_tokens(text_input)
    
    total_tokens = sum(t for _, t in chunks)
    avg_tokens = total_tokens / len(chunks)
    
    st.success(f"✅ Split into {len(chunks)} chunk(s)")
    st.markdown(f"**Total tokens:** {total_tokens:,}")
    st.markdown(f"**Average tokens per chunk:** {int(avg_tokens):,}")
    st.markdown("---")

    formatted_chunks = []

    for i, (chunk, token_count) in enumerate(chunks):
        final_chunk = f"just answer ok:\n{chunk}"
        if source_info.strip():
            final_chunk += f"\n\nSource: {source_info.strip()}"
        formatted_chunks.append(final_chunk)

        st.markdown(f"**Chunk {i+1} — {token_count} tokens**")
        st.code(final_chunk, language="markdown")
        st.button(f"📋 Copy Chunk {i+1}", key=f"copy_{i}", help="Use Ctrl+C to copy from the box above")

    # Download button for all chunks combined
    full_text = "\n\n---\n\n".join(formatted_chunks)
    st.download_button("📥 Download All Chunks", full_text, file_name="gpt_chunks.txt")
