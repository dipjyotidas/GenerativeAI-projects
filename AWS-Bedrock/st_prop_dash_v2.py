import streamlit as st
import json
import pandas as pd
from pathlib import Path
import base64
import importlib.util
import sys
import io
import contextlib
import time
import os

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="AI Property Valuation Dashboard", layout="wide")

# ----------------------------------------------------
# BASE DIRECTORIES
# ----------------------------------------------------
BASE_DIR = Path("/home/sagemaker-user/lqc-process/st-integration-v2")
OUTPUT_DIR = BASE_DIR / "processed_reports"
OUTPUT_DIR.mkdir(exist_ok=True)

# ----------------------------------------------------
# AGENT FUNCTION PATHS
# ----------------------------------------------------
APPRAISAL_FUN = BASE_DIR / "appraisal_function.py"
BPO_FUN = BASE_DIR / "bpo_function.py"
REDFIN_FUN = BASE_DIR / "redfin_function.py"
COMPARE_FUN = BASE_DIR / "compare_fun.py"

# ----------------------------------------------------
# UTILITY: DYNAMIC SCRIPT IMPORT
# ----------------------------------------------------
def import_script(script_path):
    """Dynamically import a Python module from a given path."""
    if not Path(script_path).exists():
        st.error(f"❌ Script not found: {script_path}")
        return None
    spec = importlib.util.spec_from_file_location("dynamic_module", script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["dynamic_module"] = module
    spec.loader.exec_module(module)
    return module

# ----------------------------------------------------
# DISPLAY HELPERS
# ----------------------------------------------------
def display_pdf(pdf_path):
    """Render PDF in the Streamlit UI."""
    if not pdf_path.exists():
        st.warning(f"⚠️ PDF not found: {pdf_path}")
        return
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700"></iframe>',
        unsafe_allow_html=True,
    )

def display_json(json_file):
    """Display JSON output and table view."""
    if not json_file.exists():
        st.warning(f"⚠️ JSON file not found: {json_file}")
        return
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    st.subheader("🧠 Extracted JSON Data")
    with st.expander("📋 Raw JSON View"):
        st.json(data, expanded=False)
    st.divider()
    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=["Feature", "Value"])
    elif isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        st.warning("⚠️ Unsupported JSON format.")
        return
    st.dataframe(df, use_container_width=True)

def display_summary(summary_file):
    """Display summary text file."""
    st.subheader("📝 Summary")
    if summary_file.exists():
        text = summary_file.read_text(encoding="utf-8")
        st.text_area("Summary Output", text, height=250, disabled=False)
    else:
        st.warning("⚠️ Summary text not found.")

# ----------------------------------------------------
# EXECUTION FUNCTION
# ----------------------------------------------------
def run_processing(script_path, pdf_path=None):
    """Run the corresponding processing script quietly with progress and timer."""
    module = import_script(script_path)
    if not module:
        return

    start_time = time.time()
    progress = st.progress(0)
    status = st.empty()

    progress.progress(20)
    status.info(f"🚀 Processing {pdf_path.name if pdf_path else 'Comparison'}...")

    with contextlib.redirect_stdout(io.StringIO()):  # suppress internal print logs
        try:
            if pdf_path:
                module.main(str(pdf_path))
            else:
                module.main()
        except Exception as e:
            st.error(f"❌ Error during processing: {e}")
            return

    elapsed = round(time.time() - start_time, 2)
    progress.progress(100)
    status.success(f"✅ Processing completed in {elapsed} seconds.")

# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("🏠 AI Property Valuation Dashboard")
st.markdown("Select and process Appraisal, BPO, 3rd Party, and Comparison reports using AI agent workflows.")

tabs = st.tabs(["📘 Appraisal", "📗 BPO", "📙 3rd Party (Zillow/Redfin)", "📊 Comparison Summary"])

# ----------------------------------------------------
# TAB 1 - APPRAISAL
# ----------------------------------------------------
with tabs[0]:
    st.header("📘 Appraisal Report")
    pdf_files = list(BASE_DIR.glob("*.pdf"))
    selected_pdf = st.selectbox("Select a PDF to parse:", pdf_files, key="appraisal_select")

    col1, col2 = st.columns([2, 1])
    with col1:
        display_pdf(selected_pdf)
    with col2:
        if st.button("⚙️ Process Appraisal PDF", key="process_appraisal"):
            run_processing(APPRAISAL_FUN, selected_pdf)
            display_json(OUTPUT_DIR / "appraisal_vision_report.json")
            display_summary(OUTPUT_DIR / "appraisal_summary.txt")

# ----------------------------------------------------
# TAB 2 - BPO
# ----------------------------------------------------
with tabs[1]:
    st.header("📗 Broker Price Opinion (BPO) Report")
    pdf_files = list(BASE_DIR.glob("*.pdf"))
    selected_pdf = st.selectbox("Select a PDF to parse:", pdf_files, key="bpo_select")

    col1, col2 = st.columns([2, 1])
    with col1:
        display_pdf(selected_pdf)
    with col2:
        if st.button("⚙️ Process BPO PDF", key="process_bpo"):
            run_processing(BPO_FUN, selected_pdf)
            display_json(OUTPUT_DIR / "bpo_vision_report.json")
            display_summary(OUTPUT_DIR / "bpo_summary.txt")

# ----------------------------------------------------
# TAB 3 - 3RD PARTY (Zillow/Redfin)
# ----------------------------------------------------
with tabs[2]:
    st.header("📙 Third-Party Source (Zillow/Redfin) Report")
    pdf_files = list(BASE_DIR.glob("*.pdf"))
    selected_pdf = st.selectbox("Select a PDF to parse:", pdf_files, key="redfin_select")

    col1, col2 = st.columns([2, 1])
    with col1:
        display_pdf(selected_pdf)
    with col2:
        if st.button("⚙️ Process 3rd Party PDF", key="process_redfin"):
            run_processing(REDFIN_FUN, selected_pdf)
            display_json(OUTPUT_DIR / "redfin_vision_report.json")
            display_summary(OUTPUT_DIR / "redfin_summary.txt")

# ----------------------------------------------------
# TAB 4 - COMPARISON
# ----------------------------------------------------
with tabs[3]:
    st.header("📊 Multi-Source Comparison Summary")
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("⚙️ Run Comparison", key="process_comparison"):
            run_processing(COMPARE_FUN)
    with col2:
        display_summary(OUTPUT_DIR / "comparison_summary.txt")

    st.divider()

    # ✅ Read comparison JSON report and show only "Differences"
    llm_json_path = OUTPUT_DIR / "llm_comparison_report.json"
    if llm_json_path.exists():
        try:
            with open(llm_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            differences = data.get("Differences", {})
            if not differences:
                st.warning("⚠️ No 'Differences' section found in LLM comparison report.")
            else:
                st.subheader("🔍 Differences Across Reports")
                rows = []
                for key, val in differences.items():
                    if isinstance(val, list):
                        for item in val:
                            rows.append({"Category": key, "Detail": item})
                    else:
                        rows.append({"Category": key, "Detail": str(val)})

                df_diff = pd.DataFrame(rows)
                st.dataframe(df_diff, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error reading comparison JSON: {e}")
    else:
        st.info("ℹ️ Comparison report not found. Please run the comparison first.")
