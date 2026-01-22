import streamlit as st
from data.mock_requirements import MOCK_REQUIREMENTS

st.set_page_config(layout="wide", page_title="BRD Analyzer")

# --- Session State ---
if "step" not in st.session_state:
    st.session_state.step = "empty"

# --- Sidebar ---
st.sidebar.title("🤖 BRD Analyzer")
uploaded = st.sidebar.file_uploader("Upload BRD", type=["pdf", "docx"])

if uploaded:
    st.session_state.step = "processing"
    st.session_state.filename = uploaded.name

# --- Processing ---
if st.session_state.step == "processing":
    st.header(f"Analyzing {st.session_state.filename}")
    progress = st.progress(0)
    for i in range(100):
        progress.progress(i + 1)
    st.session_state.step = "results"
    st.rerun()

# --- Empty ---
if st.session_state.step == "empty":
    st.title("Welcome to BRD Analyzer")
    st.info("Upload BRD document to start")

# --- Results ---
if st.session_state.step == "results":
    st.title(st.session_state.filename)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", len(MOCK_REQUIREMENTS))
    col2.metric("Clear", sum(r["status"] == "Clear" for r in MOCK_REQUIREMENTS))
    col3.metric("Unclear", sum(r["status"] == "Unclear" for r in MOCK_REQUIREMENTS))

    tab_all, tab_unclear, tab_clear = st.tabs(["All", "Needs Review", "Clear"])

    def render(items):
        for r in items:
            with st.expander(f"#{r['id']} | {r['category']}"):
                st.write(r["text"])
                if r["status"] == "Clear":
                    st.success("Clear Requirement")
                    if r.get("testCase"):
                        st.code(r["testCase"], language="gherkin")
                else:
                    st.warning("Unclear Requirement")
                    st.write("**Issue:**", r["issue"])
                    st.write("**AI Suggestion:**", r["suggestion"])
                    st.text_area("Edit Requirement", value=r["text"])

    with tab_all:
        render(MOCK_REQUIREMENTS)
    with tab_unclear:
        render([r for r in MOCK_REQUIREMENTS if r["status"] == "Unclear"])
    with tab_clear:
        render([r for r in MOCK_REQUIREMENTS if r["status"] == "Clear"])
