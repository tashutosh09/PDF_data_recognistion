
import streamlit as st
from call_llm import generate_resume_answer
from helper import read_file_robust
from pdf_parser import pdf_to_markdown_pymupdf4llm
import tempfile
import os

def main():
    # Page config
    st.set_page_config(page_title="📄 Resume Q&A Bot", page_icon="🤖", layout="wide")
    st.title("📄 Resume Q&A Bot")
    st.markdown("Upload your resume (PDF), convert it to Markdown, then ask questions based only on your resume.")
    st.divider()

    # Initialize session state
    if "markdown_loaded" not in st.session_state:
        st.session_state.markdown_loaded = False
        st.session_state.markdown_data = ""

    api_key = "AIzaSyA8ss5VY86BI8Hg2Mlk_5RsXl5tEG8frOE"

    # Upload PDF section
    st.subheader("📤 Upload Resume PDF")
    uploaded_file = st.file_uploader("Select your resume PDF", type=["pdf"])

    if uploaded_file and not st.session_state.markdown_loaded:
        if st.button("🔄 Convert Resume to Markdown"):
            # Save uploaded PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(uploaded_file.getbuffer())
                pdf_path = tmp_pdf.name

            # Convert to Markdown
            try:
                output_md = os.path.splitext(uploaded_file.name)[0] + ".md"
                pdf_to_markdown_pymupdf4llm(pdf_path, output_path=output_md, write_images=True)
                markdown_data, _ = read_file_robust(output_md)
                if markdown_data is None:
                    st.error("❌ Failed to read the converted Markdown.")
                else:
                    st.session_state.markdown_loaded = True
                    st.session_state.markdown_data = markdown_data
                    st.success("✅ Resume successfully converted to Markdown!")
            except Exception as e:
                st.error(f"Error converting PDF: {e}")
            finally:
                os.remove(pdf_path)

    # Question section (only after markdown loaded)
    if st.session_state.markdown_loaded:
        st.subheader("❓ Ask a Question")
        question = st.text_input("What would you like to know about your resume?")

        if st.button("🚀 Get Answer"):
            if not question.strip():
                st.error("❌ Please enter a valid question!")
            else:
                st.info("🤖 Generating answer from resume...")
                try:
                    answer = generate_resume_answer(
                        resume_markdown=st.session_state.markdown_data,
                        topic=question.strip(),
                        api_key=api_key
                    )
                    st.success("✅ Answer generated successfully!")
                    st.subheader("💬 Response:")
                    st.markdown(answer)
                    st.download_button(
                        "💾 Download Answer",
                        data=answer,
                        file_name="resume_answer.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error generating answer: {e}")

    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("Upload a PDF resume, convert it to Markdown, then ask questions about your resume content.")
        st.header("💡 Tips")
        st.markdown("""
        - Convert your resume first, then ask questions.
        - Use clear headings in your resume for best results.
        """)
    
if __name__ == "__main__":
    main()

