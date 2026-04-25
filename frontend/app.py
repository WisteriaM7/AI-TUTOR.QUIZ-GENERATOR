import streamlit as st
import requests
import os

st.set_page_config(
    page_title="LearnSphere AI Tutor",
    page_icon="📚",
    layout="wide"
)

st.title("📚 LearnSphere AI Tutor & Quiz Generator")
st.markdown("Powered by **Mistral / LLaMA 2 via Ollama** · FastAPI backend · Streamlit frontend")
st.caption("For LearnSphere Academy — Supporting educators and learners")
st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    model_choice = st.selectbox(
        "Select LLM Model:",
        options=["mistral", "llama2"],
        index=0,
        help="Both models support text simplification and quiz generation."
    )

    st.divider()
    st.subheader("📂 Load Sample Lesson")
    sample_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "sample_lesson.txt"
    )
    if st.button("📖 Load Water Cycle Lesson", use_container_width=True):
        try:
            with open(sample_path, "r") as f:
                st.session_state["lesson_text"] = f.read()
            st.success("Sample lesson loaded!")
        except FileNotFoundError:
            st.error("Sample file not found.")

    uploaded_file = st.file_uploader(
        "Or upload a .txt lesson file:",
        type=["txt"],
    )
    if uploaded_file:
        st.session_state["lesson_text"] = uploaded_file.read().decode("utf-8")
        st.success(f"Loaded: {uploaded_file.name}")

    st.divider()
    st.subheader("📌 What Gets Generated")
    st.markdown("""
- 🧠 **Simplified Explanation** — student-friendly language
- 📝 **5-Question Quiz** — mixed MCQ & short-answer, with answers
- 🔑 **Key Concepts** — 8–10 terms with definitions
    """)

# Main text area
default_text = st.session_state.get("lesson_text", "")

lesson_text = st.text_area(
    "Paste lesson content, textbook paragraph, or lecture notes here:",
    value=default_text,
    height=280,
    placeholder="e.g. Photosynthesis is the process by which plants use sunlight to...",
)

if lesson_text.strip():
    wc = len(lesson_text.split())
    cc = len(lesson_text)
    st.caption(f"📊 Words: {wc:,} · Characters: {cc:,}")
    if cc > 40000:
        st.error("❌ Content exceeds 40,000 character limit. Please shorten the text.")

col1, _ = st.columns([1, 5])
with col1:
    generate_btn = st.button("🚀 Generate Learning Aids", type="primary", use_container_width=True)

if generate_btn:
    if not lesson_text.strip():
        st.warning("⚠️ Please paste or upload some lesson content first.")
    elif len(lesson_text) > 40000:
        st.error("❌ Content too large. Please reduce to under 40,000 characters.")
    else:
        with st.spinner(f"Generating with **{model_choice}** — running 3 tasks..."):
            try:
                response = requests.post(
                    "http://localhost:8000/generate/",
                    data={"text": lesson_text, "model": model_choice},
                    timeout=360
                )

                if response.status_code == 200:
                    output = response.json()

                    # Metadata
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Model", output.get("model_used", model_choice).upper())
                    m2.metric("Words Processed", f"{output.get('word_count', 0):,}")
                    m3.metric("Outputs Generated", "3")

                    st.divider()

                    # Three tabs for outputs
                    tab1, tab2, tab3 = st.tabs(
                        ["🧠 Simplified Explanation", "📝 Quiz", "🔑 Key Concepts"]
                    )

                    with tab1:
                        st.subheader("🧠 Student-Friendly Explanation")
                        st.info(output.get("explanation", "No explanation generated."))
                        st.download_button(
                            "⬇️ Download Explanation (.txt)",
                            data=output.get("explanation", ""),
                            file_name="learnsphere_explanation.txt",
                            mime="text/plain"
                        )

                    with tab2:
                        st.subheader("📝 Quiz Questions & Answers")
                        st.markdown(output.get("quiz", "No quiz generated."))
                        st.download_button(
                            "⬇️ Download Quiz (.txt)",
                            data=output.get("quiz", ""),
                            file_name="learnsphere_quiz.txt",
                            mime="text/plain"
                        )

                    with tab3:
                        st.subheader("🔑 Key Concepts for Revision")
                        st.markdown(output.get("concepts", "No concepts extracted."))
                        st.download_button(
                            "⬇️ Download Key Concepts (.txt)",
                            data=output.get("concepts", ""),
                            file_name="learnsphere_concepts.txt",
                            mime="text/plain"
                        )

                    st.divider()

                    # Full study pack download
                    study_pack = (
                        f"LEARNSPHERE ACADEMY — AI STUDY PACK\n"
                        f"Model: {output.get('model_used', model_choice).upper()}\n"
                        f"{'=' * 60}\n\n"
                        f"SIMPLIFIED EXPLANATION\n{'-' * 40}\n{output.get('explanation', '')}\n\n"
                        f"QUIZ QUESTIONS & ANSWERS\n{'-' * 40}\n{output.get('quiz', '')}\n\n"
                        f"KEY CONCEPTS FOR REVISION\n{'-' * 40}\n{output.get('concepts', '')}\n"
                    )
                    st.download_button(
                        label="⬇️ Download Full Study Pack (.txt)",
                        data=study_pack,
                        file_name="learnsphere_study_pack.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                elif response.status_code == 400:
                    st.error(f"❌ {response.json().get('detail', 'Bad request.')}")
                elif response.status_code == 413:
                    st.error("❌ Content too large. Please limit to 40,000 characters.")
                elif response.status_code == 503:
                    st.error("❌ Ollama is not running. Start it with `ollama serve`.")
                else:
                    st.error(f"❌ Server error {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot reach the backend. Run `uvicorn backend.main:app --reload`.")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Try a shorter text passage.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

st.divider()
st.caption(
    "Ensure Ollama is running (`ollama serve`), your model is pulled "
    "(`ollama pull mistral` or `ollama pull llama2`), "
    "and the backend is active (`uvicorn backend.main:app --reload`)."
)
