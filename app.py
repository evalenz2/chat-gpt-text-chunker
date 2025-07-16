import streamlit as st
import json
from streamlit.components.v1 import html

# ── Configuration ──────────────────────────────────────────────────────────────
MAX_CHARS = 139_000            # characters per chunk

# ── Helpers ────────────────────────────────────────────────────────────────────
def split_text_by_chars(text: str, max_chars: int = MAX_CHARS):
    """Return a list of raw‑text chunks ≤ max_chars each."""
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

def copy_button(label: str, text_to_copy: str, key: str):
    """
    Render an HTML button that copies text_to_copy to the clipboard.
    Uses JS clipboard API; works in Streamlit ≥1.26.
    """
    escaped = json.dumps(text_to_copy)          # safe JS string literal
    html(
        f"""
        <button onclick='navigator.clipboard.writeText({escaped})'
                style="padding:6px 12px;margin:4px 0;border-radius:6px;
                       border:1px solid #888;background:#eee;cursor:pointer;">
            📋 {label}
        </button>
        """,
        height=38,
        key=key,
    )

# ── UI ─────────────────────────────────────────────────────────────────────────
st.title("📚 ChatGPT Text Chunker (139 000‑Character Blocks)")
st.markdown(
    "Paste text or upload a **.txt** file and I’ll split it into chunks no longer "
    "than **139 000 characters**.  Each chunk is prefixed with `just answer ok:`."
)

# Input widgets
textarea_content = st.text_area("Paste your full text here", height=300)
uploaded_file = st.file_uploader("…or upload a .txt file", type=["txt"])
source_info = st.text_input("Optional: source info (title, link, etc.)")

# Determine final input
text_input = uploaded_file.read().decode() if uploaded_file else textarea_content

# ── Processing ────────────────────────────────────────────────────────────────
if text_input:
    st.info("🔄 Splitting text…")
    raw_chunks = split_text_by_chars(text_input)

    total_chars = len(text_input)
    st.success(f"✅ Split into **{len(raw_chunks)}** chunk(s)")
    st.markdown(f"**Total characters:** {total_chars:,}")
    st.markdown("---")

    all_chunks_with_headers = []

    for idx, raw_chunk in enumerate(raw_chunks, start=1):
        final_chunk = f"just answer ok:\n{raw_chunk}"
        if source_info.strip():
            final_chunk += f"\n\nSource: {source_info.strip()}"

        all_chunks_with_headers.append(final_chunk)

        # Display & copy
        st.markdown(f"### Chunk {idx} — {len(final_chunk):,} chars")
        st.code(final_chunk, language="markdown")
        copy_button(f"Copy Chunk {idx}", final_chunk, key=f"copy_{idx}")

        # Optional per‑chunk download
        st.download_button(
            f"💾 Download Chunk {idx}",
            final_chunk,
            file_name=f"chunk_{idx}.txt",
            mime="text/plain",
            key=f"dl_{idx}",
        )

        st.markdown("---")

    # Download all chunks in one file
    combined = "\n\n---\n\n".join(all_chunks_with_headers)
    st.download_button(
        "📥 Download **all** chunks",
        combined,
        file_name="gpt_chunks.txt",
        mime="text/plain",
    )
