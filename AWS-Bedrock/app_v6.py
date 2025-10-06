import streamlit as st
import json
import base64
from pathlib import Path

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="Multi-Source Property Valuation Review", layout="wide")

# ----------------------------------------------------
# FILE PATHS
# ----------------------------------------------------
BASE_DIR = Path("C:/Dip/Study/Programming/Fannie_Mae_code")

# --- Appraisal ---
APPRAISAL_PDF = BASE_DIR / "Appraisal_Report_Sample.pdf"
APPRAISAL_JSON = BASE_DIR / "property_appraisal.json"
APPRAISAL_SUMMARY = BASE_DIR / "appraisal_report_summary.txt"

# --- BPO ---
BPO_PDF = BASE_DIR / "BPO_Report_Sample.pdf"
BPO_JSON = BASE_DIR / "property_BPO.json"
BPO_SUMMARY = BASE_DIR / "BPO_summary.txt"

# --- Zillow ---
ZILLOW_PDF = BASE_DIR / "property_Zillow.pdf"
ZILLOW_JSON = BASE_DIR / "property_zillow.json"
ZILLOW_SUMMARY = BASE_DIR / "property_summary_zillow.txt"

# --- Prompt ---
PROMPT_FILE = BASE_DIR / "prompt.txt"

# --- Comparison Summary ---
COMPARISON_SUMMARY = BASE_DIR / "multi_source_comparison_summary.txt"

# ----------------------------------------------------
# HELPERS
# ----------------------------------------------------
def load_json(file_path: Path):
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error reading JSON file: {e}")
    else:
        st.warning(f"File not found: {file_path}")
    return None


def load_text(file_path: Path):
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        st.warning(f"File not found: {file_path}")
    return None


def show_pdf_download_button(file_path: Path):
    if file_path.exists():
        with open(file_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name=file_path.name)
    else:
        st.error(f"PDF not found: {file_path}")

# ----------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------
st.sidebar.title("🏠 Property Valuation Review Assistant")

valuation_type = st.sidebar.radio(
    "Select View:",
    [
        "Appraisal",
        "Broker Price Opinion (BPO)",
        "Zillow",
        "🧩 Comparison Summary",
        "💬 Prompt Review"
    ]
)

section = st.sidebar.radio(
    "Select Section:",
    ["📄 Property PDF", "🧠 JSON Output", "📝 Summary"],
    index=2 if "Summary" in valuation_type else 0
)

# ----------------------------------------------------
# MAIN DISPLAY LOGIC
# ----------------------------------------------------
def display_section(pdf_path, json_path, summary_path, label):
    st.header(f"{label} - {section}")

    # PDF Section
    if section == "📄 Property PDF":
        st.subheader(f"{label} Report PDF")
        show_pdf_download_button(pdf_path)

    # JSON Section
    elif section == "🧠 JSON Output":
        st.subheader(f"{label} - JSON Data")
        data = load_json(json_path)
        if data:
            st.json(data, expanded=False)
        else:
            st.warning(f"No JSON data found for {label}.")

    # Summary Section
    elif section == "📝 Summary":
        st.subheader(f"{label} - Summary")
        summary_text = load_text(summary_path)
        if summary_text:
            st.text_area("Summary", summary_text, height=400)
        else:
            st.warning(f"No summary file found for {label}.")


# ----------------------------------------------------
# ROUTING BASED ON USER SELECTION
# ----------------------------------------------------
if valuation_type == "Appraisal":
    display_section(APPRAISAL_PDF, APPRAISAL_JSON, APPRAISAL_SUMMARY, "Appraisal Report")

elif valuation_type == "Broker Price Opinion (BPO)":
    display_section(BPO_PDF, BPO_JSON, BPO_SUMMARY, "Broker Price Opinion Report")

elif valuation_type == "Zillow":
    display_section(ZILLOW_PDF, ZILLOW_JSON, ZILLOW_SUMMARY, "Zillow Report")

elif valuation_type == "🧩 Comparison Summary":
    st.header("🧩 Multi-Source Valuation Comparison Summary")
    comparison_text = load_text(COMPARISON_SUMMARY)
    if comparison_text:
        st.text_area("Comparison Summary", comparison_text, height=600)
    else:
        st.warning("Comparison summary file not found.")

elif valuation_type == "💬 Prompt Review":
    st.header("💬 Prompt Review Text")
    prompt_text = load_text(PROMPT_FILE)
    if prompt_text:
        st.text_area("Prompt", prompt_text, height=400)
    else:
        st.warning("Prompt file not found.")
