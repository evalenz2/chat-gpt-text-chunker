import streamlit as st

# Constants
MAX_CHARS = 139000  # Max characters per chunk

def split_text_by_chars(text, max_chars=MAX_CHARS):
    chunks = []
    for i in range(0, len(text), max_chars):
        chunk = text[i:i + max_chars]
        chunks.append(chunk)
    return chunks

# UI
st.title("📚 ChatGPT Text Chunker (139,000 Character Chunks)")
st.markdown("Split large text into ChatGPT-ready chunks. Each chunk includes the instruction `just answer ok:` and optional source info.")

# Input Fields
text_input = ""
text_input_area = st.text_area("Paste your full text here", height=300)
uploaded_file = st.file_uploader("Or upload a .txt file", type=["txt"])
source_info = st.text_input("Optional: Add source information (e.g., document title or link)")

# Load input
if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")
else:
    text_input = text_input_area

# Process
if text_input:
    st.info("🔄 Splitting text by characters...")
    chunks = split_text_by_chars(text_input)

    total_chars = len(text_input)
    avg_chars = total_chars / len(chunks)

    st.success(f"✅ Split into {len(chunks)} chunk(s)")
    st.markdown(f"**Total characters:** {total_chars:,}")
    st.markdown(f"**Average characters per chunk:** {int(avg_chars):,}")
    st.markdown("---")

    formatted_chunks = []

    for i, chunk in enumerate(chunks):
        final_chunk = f"just answer ok:\n{chunk}"
        if source_info.strip():
            final_chunk += f"\n\nSource: {source_info.strip()}"
        formatted_chunks.append(final_chunk)

        st.markdown(f"**Chunk {i+1} — {len(chunk):,} characters**")
        st.code(final_chunk[:1000] + ("..." if len(chunk) > 1000 else ""), language="markdown")
        st.button(f"📋 Copy Chunk {i+1}", key=f"copy_{i}", help="Use Ctrl+C to copy from the box above")

    # Download all chunks
    full_text = "\n\n---\n\n".join(formatted_chunks)
    st.download_button("📥 Download All Chunks", full_text, file_name="gpt_chunks.txt")
