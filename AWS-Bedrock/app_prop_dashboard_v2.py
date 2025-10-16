import streamlit as st
import json
import pandas as pd
from pathlib import Path
import base64
import importlib.util
import sys
import os
import io
import contextlib
import time

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="AI Property Valuation Dashboard", layout="wide")

# ----------------------------------------------------
# IMPORT AGENT FUNCTION SCRIPT
# ----------------------------------------------------
AGENT_FUN_PATH = Path("C:/Dip/Study/Programming/Fannie_Mae_code/agent_functions_v3.py")

if not AGENT_FUN_PATH.exists():
    st.error(f"❌ agent_functions_v3.py not found at: {AGENT_FUN_PATH}")
    st.stop()

spec = importlib.util.spec_from_file_location("agent_functions_v3", AGENT_FUN_PATH)
agent_funcs = importlib.util.module_from_spec(spec)
sys.modules["agent_functions_v3"] = agent_funcs
spec.loader.exec_module(agent_funcs)

# ----------------------------------------------------
# FILE PATHS
# ----------------------------------------------------
BASE_DIR = Path("C:/Dip/Study/Programming/Fannie_Mae_code")
OUTPUT_DIR = BASE_DIR / "processed_reports"
OUTPUT_DIR.mkdir(exist_ok=True)

# Predefined PDFs
APPRAISAL_PDF = OUTPUT_DIR / "appraisal.pdf"
BPO_PDF = OUTPUT_DIR / "bpo.pdf"
ZILLOW_PDF = OUTPUT_DIR / "redfin.pdf"  # renamed third-party source

# ----------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------
def display_pdf(pdf_path):
    """Embed a PDF with download option."""
    if not pdf_path.exists():
        st.error(f"❌ PDF not found: {pdf_path}")
        return
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    st.download_button("📥 Download PDF", data=pdf_bytes, file_name=pdf_path.name, mime="application/pdf")
    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def display_json(json_path):
    """Show JSON and tabular format."""
    if not json_path.exists():
        st.warning("⚠️ JSON file not found.")
        return
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    with st.expander("🧠 Raw JSON"):
        st.json(data)
    st.divider()
    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=["Feature", "Value"])
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        st.warning("⚠️ Unsupported JSON structure.")
        return
    st.subheader("📊 Tabular Summary")
    st.dataframe(df, use_container_width=True)


def display_summary(summary_path, title="📝 Summary"):
    """Show LLM-generated summary text."""
    st.subheader(title)
    if summary_path.exists():
        text = summary_path.read_text(encoding="utf-8")
        st.text_area(title, text, height=300, disabled=False)
    else:
        st.warning("⚠️ Summary not found.")


# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------
st.sidebar.title("🏠 Property Valuation Review")
st.sidebar.markdown("### Step 1: Click below to process saved PDFs")

process_button = st.sidebar.button("🚀 Process All Documents")

# ----------------------------------------------------
# MAIN EXECUTION
# ----------------------------------------------------
if process_button:
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_box = st.empty()
    start_time = time.time()

    with st.spinner("🧠 Running AI Vision Pipeline..."):
        # Step 1: Set PDF paths
        status_text.text("📂 Locating saved PDF files...")
        pdf_paths = [str(APPRAISAL_PDF), str(BPO_PDF), str(ZILLOW_PDF)]

        # Step 2: Run agent_functions_v3
        status_text.text("⚙️ Running agent_functions_v3.main() on local PDFs...")
        agent_funcs.PDF_FILES = pdf_paths
        os.chdir(OUTPUT_DIR)

        log_stream = io.StringIO()
        with contextlib.redirect_stdout(log_stream):
            agent_funcs.main()  # Run main() from your processing script

        logs = log_stream.getvalue()
        log_box.text_area("📜 Execution Logs", logs, height=250)
        progress_bar.progress(70)

        # Step 3: Load output paths
        status_text.text("📊 Loading processed results...")
        appraisal_json = OUTPUT_DIR / "appraisal_vision_report.json"
        bpo_json = OUTPUT_DIR / "bpo_vision_report.json"
        zillow_json = OUTPUT_DIR / "zillow_vision_report.json"

        appraisal_summary = OUTPUT_DIR / "appraisal_summary.txt"
        bpo_summary = OUTPUT_DIR / "bpo_summary.txt"
        zillow_summary = OUTPUT_DIR / "zillow_summary.txt"
        comparison_summary = OUTPUT_DIR / "comparison_summary.txt"
        progress_bar.progress(100)

    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    st.success(f"✅ All 3 reports processed successfully in {total_time} seconds!")
    st.info(f"📁 Files saved permanently in: {OUTPUT_DIR}")

    # ----------------------------------------------------
    # DISPLAY RESULTS
    # ----------------------------------------------------
    tabs = st.tabs(["📘 Appraisal", "📗 BPO", "📙 Third-Party (Redfin)", "📊 Comparison Summary"])

    with tabs[0]:
        col1, col2 = st.columns([2, 1])
        with col1:
            display_pdf(APPRAISAL_PDF)
            display_summary(appraisal_summary)
        with col2:
            display_json(appraisal_json)

    with tabs[1]:
        col1, col2 = st.columns([2, 1])
        with col1:
            display_pdf(BPO_PDF)
            display_summary(bpo_summary)
        with col2:
            display_json(bpo_json)

    with tabs[2]:
        col1, col2 = st.columns([2, 1])
        with col1:
            display_pdf(ZILLOW_PDF)
            display_summary(zillow_summary)
        with col2:
            display_json(zillow_json)

    with tabs[3]:
        st.header("📊 Multi-Source Comparison Summary")
        display_summary(comparison_summary)
        if comparison_summary.exists():
            st.download_button(
                label="📥 Download Comparison Summary",
                data=comparison_summary.read_text(encoding="utf-8"),
                file_name="comparison_summary.txt"
            )

else:
    st.info("👈 Click **Process All Documents** to run the AI pipeline on saved PDFs.")
