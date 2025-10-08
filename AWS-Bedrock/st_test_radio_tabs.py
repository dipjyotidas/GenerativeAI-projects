# code for working with Radio buttons

# import streamlit as st
# import json
# import pandas as pd
# from pathlib import Path
# import base64

# # ----------------------------------------------------
# # PAGE CONFIG
# # ----------------------------------------------------
# st.set_page_config(page_title="Property Valuation Dashboard", layout="wide")

# # ----------------------------------------------------
# # FILE PATHS
# # ----------------------------------------------------
# BASE_DIR = Path("C:/Dip/Study/Programming/Fannie_Mae_code")

# # --- Appraisal ---
# APPRAISAL_PDF = BASE_DIR / "Appraisal_Report_Sample.pdf"
# APPRAISAL_JSON = BASE_DIR / "property_appraisal.json"
# APPRAISAL_SUMMARY = BASE_DIR / "appraisal_report_summary.txt"

# # --- BPO ---
# BPO_PDF = BASE_DIR / "sample_UAD.pdf"
# BPO_JSON = BASE_DIR / "property_BPO.json"
# BPO_SUMMARY = BASE_DIR / "BPO_summary.txt"

# # --- Zillow (Third-party) ---
# ZILLOW_PDF = BASE_DIR / "sample_UAD.pdf"
# ZILLOW_JSON = BASE_DIR / "property_zillow.json"
# ZILLOW_SUMMARY = BASE_DIR / "property_summary_zillow.txt"

# # --- Comparison ---
# COMPARISON_SUMMARY = BASE_DIR / "multi_source_comparison_summary.txt"

# # ----------------------------------------------------
# # HELPER FUNCTIONS
# # ----------------------------------------------------
# def load_json(file_path):
#     if not file_path.exists():
#         return None
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception as e:
#         st.error(f"Error reading JSON: {e}")
#         return None

# def display_pdf(pdf_path):
#     """Embed a PDF with download option."""
#     if not pdf_path.exists():
#         st.error(f"❌ File not found: {pdf_path}")
#         return
#     with open(pdf_path, "rb") as f:
#         pdf_bytes = f.read()
#     st.download_button("📥 Download PDF", data=pdf_bytes, file_name=pdf_path.name, mime="application/pdf")
#     base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
#     pdf_display = f"""
#         <iframe src="data:application/pdf;base64,{base64_pdf}"
#                 width="100%" height="850"
#                 type="application/pdf"></iframe>
#     """
#     st.markdown(pdf_display, unsafe_allow_html=True)

# def display_summary(summary_file):
#     """Display the LLM-generated summary text."""
#     st.subheader("📝 Summary of Report")
#     if summary_file.exists():
#         with open(summary_file, "r", encoding="utf-8") as f:
#             summary_text = f.read()
#         st.text_area("LLM Summary", summary_text, height=300, disabled=False)
#     else:
#         st.warning(f"⚠️ Summary file not found: {summary_file}")

# def display_json(json_file):
#     """Display JSON and its tabular representation."""
#     st.header("🧠 Extracted JSON Data")
#     data = load_json(json_file)
#     if not data:
#         st.warning(f"⚠️ JSON file not found: {json_file}")
#         return
#     with st.expander("📋 View Raw JSON"):
#         st.json(data, expanded=False)
#     st.divider()
#     if isinstance(data, dict):
#         df = pd.DataFrame(list(data.items()), columns=["Feature", "Value"])
#         st.subheader("📊 Tabular Summary")
#         st.dataframe(df, use_container_width=True)
#     elif isinstance(data, list):
#         df = pd.DataFrame(data)
#         st.subheader("📊 Tabular Summary")
#         st.dataframe(df, use_container_width=True)
#     else:
#         st.warning("⚠️ Unsupported JSON structure.")


#######################################################################################################
# ----------------------------------------------------
# SIDEBAR NAVIGATION WITH RADIO BUTTONS
# ----------------------------------------------------
# st.sidebar.title("🏠 Property Valuation Review Assistant")
# report_choice = st.sidebar.radio(
#     "Select Report Type:",
#     ["Appraisal Report", "BPO Report", "Third-Party (Zillow)", "📊 Comparison Summary"],
# )


# # ----------------------------------------------------
# # MAIN CONTENT (layout shared across all reports)
# # ----------------------------------------------------
# col1, col2 = st.columns([2, 1])

# if report_choice == "Appraisal Report":
#     with col1:
#         st.header("📘 Appraisal Report")
#         display_pdf(APPRAISAL_PDF)
#         st.divider()
#         display_summary(APPRAISAL_SUMMARY)
#     with col2:
#         display_json(APPRAISAL_JSON)

# elif report_choice == "BPO Report":
#     with col1:
#         st.header("📗 Broker Price Opinion (BPO) Report")
#         display_pdf(BPO_PDF)
#         st.divider()
#         display_summary(BPO_SUMMARY)
#     with col2:
#         display_json(BPO_JSON)

# elif report_choice == "Third-Party (Zillow)":
#     with col1:
#         st.header("📙 Third-Party Source (Zillow) Report")
#         display_pdf(ZILLOW_PDF)
#         st.divider()
#         display_summary(ZILLOW_SUMMARY)
#     with col2:
#         display_json(ZILLOW_JSON)
        
# elif report_choice == "📊 Comparison Summary":
#     with col1:
#         st.header("📊 Multi-Source Comparison Summary")
#         if COMPARISON_SUMMARY.exists():
#             summary_text = COMPARISON_SUMMARY.read_text(encoding="utf-8")
#             st.text_area("Comparison Summary", summary_text, height=500, disabled=False)
#         else:
#             st.warning(f"⚠️ Comparison summary file not found: {COMPARISON_SUMMARY}")
            
            
# The above with Radio buttons is working and displaying all pdfs and we can scroll through them.


#############################################################################################################

# New code for working with sidebar tabs


import streamlit as st
import json
import pandas as pd
from pathlib import Path
import base64

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------
st.set_page_config(page_title="Property Valuation Dashboard", layout="wide")

# ----------------------------------------------------
# FILE PATHS
# ----------------------------------------------------
BASE_DIR = Path("C:/Dip/Study/Programming/Fannie_Mae_code")

# --- Appraisal ---
APPRAISAL_PDF = BASE_DIR / "Appraisal_Report_Sample.pdf"
APPRAISAL_JSON = BASE_DIR / "property_appraisal.json"
APPRAISAL_SUMMARY = BASE_DIR / "appraisal_report_summary.txt"

# --- BPO ---
BPO_PDF = BASE_DIR / "sample_UAD.pdf"
BPO_JSON = BASE_DIR / "property_BPO.json"
BPO_SUMMARY = BASE_DIR / "BPO_summary.txt"

# --- Zillow (Third-party) ---
ZILLOW_PDF = BASE_DIR / "sample_UAD.pdf"
ZILLOW_JSON = BASE_DIR / "property_zillow.json"
ZILLOW_SUMMARY = BASE_DIR / "property_summary_zillow.txt"

# --- Comparison ---
COMPARISON_SUMMARY = BASE_DIR / "multi_source_comparison_summary.txt"

# ----------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------
def load_json(file_path):
    if not file_path.exists():
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error reading JSON: {e}")
        return None

    
    
def display_pdf(pdf_path, key_prefix: str):
    """Embed a PDF with a unique download button."""
    if not pdf_path.exists():
        st.error(f"❌ File not found: {pdf_path}")
        return
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    # ✅ Give each button a unique key
    st.download_button(
        label=f"📥 Download {pdf_path.name}",
        data=pdf_bytes,
        file_name=pdf_path.name,
        mime="application/pdf",
        key=f"{key_prefix}_download_button"
    )


def display_summary(summary_file):
    """Display the LLM-generated summary text."""
    st.subheader("📝 Summary of Report")
    if summary_file.exists():
        with open(summary_file, "r", encoding="utf-8") as f:
            summary_text = f.read()
        st.text_area("LLM Summary", summary_text, height=300, disabled=False)
    else:
        st.warning(f"⚠️ Summary file not found: {summary_file}")

def display_json(json_file):
    """Display JSON and its tabular representation."""
    st.header("🧠 Extracted JSON Data")
    data = load_json(json_file)
    if not data:
        st.warning(f"⚠️ JSON file not found: {json_file}")
        return
    with st.expander("📋 View Raw JSON"):
        st.json(data, expanded=False)
    st.divider()
    if isinstance(data, dict):
        df = pd.DataFrame(list(data.items()), columns=["Feature", "Value"])
        st.subheader("📊 Tabular Summary")
        st.dataframe(df, use_container_width=True)
    elif isinstance(data, list):
        df = pd.DataFrame(data)
        st.subheader("📊 Tabular Summary")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Unsupported JSON structure.")








# ----------------------------------------------------
# SIDEBAR NAVIGATION (with Tabs)
# ----------------------------------------------------
st.sidebar.title("🏠 Property Valuation Dashboard")
tab1, tab2, tab3, tab4 = st.sidebar.tabs(["📘 Appraisal", "📗 BPO", "📙 Zillow", "📊 Comparison Summary"])

# ----------------------------------------------------
# MAIN CONTENT
# ----------------------------------------------------
col1, col2 = st.columns([2, 1])



# --- TAB 1: APPRAISAL ---
with tab1:
    with col1:
        st.header("📘 Appraisal Report")
        display_pdf(APPRAISAL_PDF, key_prefix="appraisal")
        #pdf_viewer(str(APPRAISAL_PDF))  # native viewer (scrollable, unlimited)
        st.divider()
        display_summary(APPRAISAL_SUMMARY)
    with col2:
        display_json(APPRAISAL_JSON)

# --- TAB 2: BPO ---
with tab2:
    with col1:
        st.header("📗 Broker Price Opinion (BPO) Report")
        display_pdf(BPO_PDF, key_prefix="bpo")
        #pdf_viewer(str(BPO_PDF))
        st.divider()
        display_summary(BPO_SUMMARY)
    with col2:
        display_json(BPO_JSON)

# --- TAB 3: ZILLOW ---
with tab3:
    with col1:
        st.header("📙 Third-Party Source (Zillow) Report")
        display_pdf(ZILLOW_PDF, key_prefix="zillow")
        #pdf_viewer(str(ZILLOW_PDF))
        st.divider()
        display_summary(ZILLOW_SUMMARY)
    with col2:
        display_json(ZILLOW_JSON)
        
# --- COMPARISON TAB ---
with tab4:
    st.header("📊 Multi-Source Comparison Summary")
    if COMPARISON_SUMMARY.exists():
        summary_text = COMPARISON_SUMMARY.read_text(encoding="utf-8")
        st.text_area("Comparison Summary", summary_text, height=500, disabled=False)
    else:
        st.warning(f"⚠️ Comparison summary file not found: {COMPARISON_SUMMARY}")

#############################################################################################################