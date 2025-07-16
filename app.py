import streamlit as st
import json
import streamlit.components.v1 as components   # renamed for clarity

# ── Configuration ──────────────────────────────────────────────────────────────
MAX_CHARS = 139_000

# ── Helpers ────────────────────────────────────────────────────────────────────
def split_text_by_chars(text: str, max_chars: int = MAX_CHARS):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

def copy_button(label: str, text_to_copy: str):
    """
    Render a tiny HTML button that copies `text_to_copy` to the clipboard.
    No 'key' param (avoids TypeError).
    """
    escaped = json.dumps(text_to_copy)  # safe JS string
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
st.title("📚 ChatGPT Text Chunker (139 000‑Character Blocks)")
st.markdown(
    "Split large text into chunks no longer than **139 000 characters**. "
    "Each chunk is prefixed with `just answer ok:` &nbsp;and can be copied or downloaded."
)

textarea_content = st.text_area("Paste your full text here", height=300)
uploaded_file  = st.file_uploader("…or upload a .txt file", type=["txt"])
source_info    = st.text_input("Optional: source info (title, link, etc.)")

text_input = uploaded_file.read().decode() if uploaded_file else textarea_content

# ── Processing ────────────────────────────────────────────────────────────────
if text_input:
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

        with st.expander(f"Chunk {idx} — {len(final_chunk):,} chars", expanded=False):
            # Preview first 800 chars so the expander isn't overwhelming
            st.code(final_chunk[:800] + ("…" if len(final_chunk) > 800 else ""), language="markdown")
            copy_button("Copy this chunk", final_chunk)
            st.download_button(
                "💾 Download this chunk",
                final_chunk,
                file_name=f"chunk_{idx}.txt",
                mime="text/plain",
                key=f"dl_{idx}",
            )

    # Combined download
    combined = "\n\n---\n\n".join(all_chunks_with_headers)
    st.download_button(
        "📥 Download **all** chunks",
        combined,
        file_name="gpt_chunks.txt",
        mime="text/plain",
    )
