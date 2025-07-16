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
        st.code(final_chunk[:1000] + ("..." if len(chunk) > 1000 else ""), language="markdown")  # Preview
        st.button(f"📋 Copy Chunk {i+1}", key=f"copy_{i}", help="Use Ctrl+C to copy from the box above")

    # Download button for all chunks combined
    full_text = "\n\n---\n\n".join(formatted_chunks)
    st.download_button("📥 Download All Chunks", full_text, file_name="gpt_chunks.txt")
