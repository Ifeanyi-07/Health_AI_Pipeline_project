"""
Blood Work Analysis - Streamlit App
------------------------------------
Recreates the two-stage LLM pipeline from the uploaded notebook:
  Stage 1: Extract test values from a raw blood report and classify each
           as HIGH / LOW / NORMAL against the reference range.
  Stage 2: Generate a short health summary + an Indian diet plan based
           on the extracted values.

Run with:
    streamlit run app.py

Requires a Google API key for Gemini, set as the GOOGLE_API_KEY environment
variable (in a local .env file, or as a Railway/host environment variable
in production). The key is never shown or editable in the UI.
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------
st.set_page_config(page_title="Blood Work Analyzer", page_icon="🩸", layout="wide")
st.title("🩸 Blood Work Analysis")
st.caption("Upload or paste a blood report to get extracted values, a health summary, and a diet plan.")

# ----------------------------------------------------------------------
# Sidebar: model settings only — no API key field. The key is read purely
# from the environment (GOOGLE_API_KEY), so it's never displayed, editable,
# or shared across users/devices.
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    model_name = st.text_input("Gemini model", value="gemini-3.6-flash")
    st.divider()
    st.markdown(
        "**Disclaimer:** This tool is for informational purposes only and "
        "is not a substitute for professional medical advice."
    )


@st.cache_resource(show_spinner=False)
def get_llm(model_name: str, api_key: str):
    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)


# ----------------------------------------------------------------------
# Input: upload a .txt file or paste the report text
# ----------------------------------------------------------------------
st.subheader("1. Provide the blood report")

tab_upload, tab_paste = st.tabs(["Upload .txt file", "Paste text"])

blood_report = ""

with tab_upload:
    uploaded = st.file_uploader("Blood report (.txt)", type=["txt"])
    if uploaded is not None:
        blood_report = uploaded.read().decode("utf-8", errors="ignore")
        st.text_area("Preview", blood_report, height=200, disabled=True)

with tab_paste:
    pasted = st.text_area("Paste the raw blood report text here", height=200)
    if pasted.strip():
        blood_report = pasted

run_button = st.button("Run analysis", type="primary", disabled=not blood_report.strip())

# ----------------------------------------------------------------------
# Prompts (kept close to the original notebook)
# ----------------------------------------------------------------------
EXTRACTION_PROMPT_TEMPLATE = """
You are a medical data extraction assistant.

From the blood report below, extract all test values and classify each one as HIGH, LOW, or NORMAL based on the reference ranges provided in the report.

Format your response as:
- Test Name: value | Status: HIGH/LOW/NORMAL | Reference: range

Blood Report:
{report}
"""

DIET_PROMPT_TEMPLATE = """
You are a clinical nutritionist specializing in Indian dietary habits.

Based on the blood work analysis below, write:
1. A short health summary in 3 lines explaining the patient's condition in simple language
2. A short, practical Indian diet plan having only two sections (1) foods to avoid (2) foods to eat more of.
Do not include any other sections in the diet plan.

Blood Work Analysis:
{analysis}
"""

# ----------------------------------------------------------------------
# Run pipeline
# ----------------------------------------------------------------------
if run_button:
    if not os.getenv("GOOGLE_API_KEY"):
        st.error(
            "GOOGLE_API_KEY is not set. Add it as an environment variable "
            "(a .env file locally, or a Railway/host variable in production)."
        )
        st.stop()

    try:
        llm = get_llm(model_name, os.environ["GOOGLE_API_KEY"])
    except Exception as e:
        st.error(f"Could not initialize the model: {e}")
        st.stop()

    st.subheader("2. Extracted values")
    with st.spinner("Extracting and classifying test values..."):
        try:
            extraction_response = llm.invoke(EXTRACTION_PROMPT_TEMPLATE.format(report=blood_report))
            extracted_values = extraction_response.content if hasattr(extraction_response, "content") else str(extraction_response)
        except Exception as e:
            st.error(f"Extraction step failed: {e}")
            st.stop()
    st.markdown(extracted_values)
    st.session_state["extracted_values"] = extracted_values

    st.subheader("3. Health summary & diet plan")
    with st.spinner("Generating health summary and diet plan..."):
        try:
            diet_response = llm.invoke(DIET_PROMPT_TEMPLATE.format(analysis=extracted_values))
            diet_plan = diet_response.content if hasattr(diet_response, "content") else str(diet_response)
        except Exception as e:
            st.error(f"Diet plan step failed: {e}")
            st.stop()
    st.markdown(diet_plan)

    st.download_button(
        "Download full report (Markdown)",
        data=f"## Extracted Values\n\n{extracted_values}\n\n## Health Summary & Diet Plan\n\n{diet_plan}",
        file_name="blood_work_report.md",
        mime="text/markdown",
    )
else:
    st.info("Provide a report above and click **Run analysis** to get started.")
