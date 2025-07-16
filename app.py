import streamlit as st
import json
import streamlit.components.v1 as components
import tiktoken

# ── Configuration ──────────────────────────────────────────────────────────────
MAX_TOKENS = 27_000           # tokens per chunk
MODEL_NAME = "gpt-4"

# Initialize tokenizer once
enc = tiktoken.encoding_for_model(MODEL_NAME)

# ── Helpers ────────────────────────────────────────────────────────────────────
def split_text_by_tokens(text: str, max_tokens: int = MAX_TOKENS):
    """
    Return a list of (chunk_str, token_count) tuples,
    each with ≤ max_tokens GPT‑4 tokens.
    """
    words = text.split()
    chunks, current_chunk, current_tokens = [], [], 0

    for word in words:
        tok_len = len(enc.encode(" " + word))
        if current_tokens + tok_len > max_tokens:
            chunk_text = " ".join(current_chunk)
            chunks.append((chunk_text, current_tokens))
            current_chunk, current_tokens = [word], tok_len
        else:
            current_chunk.append(word)
            current_tokens += tok_len

    if current_chunk:
        chunks.append((" ".join(current_chunk), current_tokens))

    return chunks

def copy_button(label: str, text_to_copy: str):
    """HTML/JS button that copies text_to_copy to the clipboard."""
    escaped = json.dumps(text_to_copy)          # safe JS string
    components.html(
        f"""
        <button onclick='navigator.clipboard.writeText({escaped})'
                style="padding:6px 12px;border-radius:6px;border:1px solid #888;
                       background:#eee;cursor:pointer;">
            📋 {label}
        </button>
        """,
        height=40,
    )

# ── UI ─────────────────────────────────────────────────────────────────────────
st.title("📚 ChatGPT Text Chunker (27 000‑Token Blocks)")
st.markdown(
    "Paste text or upload a .txt file and I’ll split it into chunks of no more "
    "than 27 000 GPT‑4 tokens.  Each chunk is prefixed with `just answer ok:`."
)

# Inputs
textarea_content = st.text_area("Paste your full text here", height=300)
uploaded_file    = st.file_uploader("…or upload a .txt file", type=["txt"])
source_info      = st.text_input("Optional: source info (title, link, etc.)")

text_input = uploaded_file.read().decode() if uploaded_file else textarea_content

# ── Processing ────────────────────────────────────────────────────────────────
if text_input:
    st.info("Splitting text into token‑sized chunks…")
    token_chunks = split_text_by_tokens(text_input)
    total_tokens = sum(tok for _, tok in token_chunks)

    st.success(f"Split into {len(token_chunks)} chunk(s)")
    st.markdown(f"Total tokens: {total_tokens:,}")
    st.markdown("---")

    all_chunks = []

    for idx, (chunk_body, tok_count) in enumerate(token_chunks, start=1):
        final_chunk = f"just answer ok:\n{chunk_body}"
        if source_info.strip():
            final_chunk += f"\n\nSource: {source_info.strip()}"

        all_chunks.append(final_chunk)

        with st.expander(f"Chunk {idx} — {tok_count} tokens", expanded=False):
            # Show only a preview of the chunk to keep the page light
            preview = final_chunk[:800] + ("…" if len(final_chunk) > 800 else "")
            s
