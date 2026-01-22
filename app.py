# app.py
import streamlit as st
import pandas as pd

# ===== IMPORT BACKEND (ของคุณจาก Colab) =====
from backend.extract import extract_text_from_pdf
from backend.group_llm import group_requirements_with_llm
from backend.ml_predict import predict_clear_unclear
from backend.llm_review import analyze_unclear_with_llm

# ===========================================
# CONFIG
# ===========================================
st.set_page_config(
    page_title="BRD Analyzer",
    layout="wide"
)

# ===========================================
# SESSION STATE
# ===========================================
if "step" not in st.session_state:
    st.session_state.step = "empty"   # empty | processing | results

if "results" not in st.session_state:
    st.session_state.results = []

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

# ===========================================
# SIDEBAR (UPLOAD)
# ===========================================
with st.sidebar:
    st.title("🤖 BRD Analyzer")

    uploaded_file = st.file_uploader(
        "Upload BRD (PDF)",
        type=["pdf"]
    )

    if uploaded_file:
        st.session_state.file_name = uploaded_file.name
        st.session_state.step = "ready"

    if st.session_state.step == "ready":
        if st.button("Run Analysis"):
            st.session_state.step = "processing"

# ===========================================
# MAIN AREA
# ===========================================

# -------- EMPTY VIEW --------
if st.session_state.step == "empty":
    st.title("Welcome to BRD Analyzer")
    st.write(
        "Upload a Business Requirement Document (BRD) "
        "to analyze requirement clarity using AI."
    )

# -------- READY (FILE UPLOADED) --------
elif st.session_state.step == "ready":
    st.header(st.session_state.file_name)
    st.info("File uploaded. Click **Run Analysis** to start.")

# -------- PROCESSING VIEW --------
elif st.session_state.step == "processing":

    st.header(f"Analyzing: {st.session_state.file_name}")

    with st.spinner("Running AI pipeline..."):
        # 1️⃣ PDF → Text
        text = extract_text_from_pdf(uploaded_file)

        # 2️⃣ LLM Group Requirement
        grouped_requirements = group_requirements_with_llm(text)

        # 3️⃣ ML Predict Clear / Unclear
        predicted = predict_clear_unclear(grouped_requirements)

        # 4️⃣ LLM Issue + Suggestion (เฉพาะ Unclear)
        final_results = analyze_unclear_with_llm(predicted)

        # save result
        st.session_state.results = final_results
        st.session_state.step = "results"

    st.success("Analysis completed")

# -------- RESULTS VIEW --------
elif st.session_state.step == "results":

    st.header(st.session_state.file_name)

    results = st.session_state.results
    df = pd.DataFrame(results)

    # ===== SUMMARY =====
    total = len(df)
    clear = len(df[df["status"] == "Clear"])
    unclear = len(df[df["status"] == "Unclear"])

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Requirements", total)
    c2.metric("Clear", clear)
    c3.metric("Unclear", unclear)

    st.divider()

    # ===== REQUIREMENT LIST =====
    for r in results:
        with st.expander(f"ID-{r['id']} | {r['status']}"):
            st.write(r["text"])

            if r["status"] == "Unclear":
                st.warning(r["issue"])
                st.text_area(
                    "AI Suggestion",
                    r["suggestion"],
                    key=f"sug_{r['id']}"
                )

            if r.get("test_case"):
                st.subheader("Generated Test Case")
                st.code(r["test_case"], language="gherkin")

    st.divider()

    # ===== EXPORT =====
    st.download_button(
        "⬇ Export Audit Result (CSV)",
        df.to_csv(index=False),
        file_name="brd_audit_result.csv"
    )
