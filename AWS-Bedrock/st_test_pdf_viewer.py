# import streamlit as st
# import json
# import pandas as pd
# from pathlib import Path
# from streamlit_pdf_viewer import pdf_viewer

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
# BPO_PDF = BASE_DIR / "BPO_Report_Sample.pdf"
# BPO_JSON = BASE_DIR / "property_BPO.json"
# BPO_SUMMARY = BASE_DIR / "BPO_summary.txt"

# # --- Zillow ---
# ZILLOW_PDF = BASE_DIR / "property_Zillow.pdf"
# ZILLOW_JSON = BASE_DIR / "property_zillow.json"
# ZILLOW_SUMMARY = BASE_DIR / "property_summary_zillow.txt"

# # --- Comparison ---
# COMPARISON_SUMMARY = BASE_DIR / "multi_source_comparison_summary.txt"

# # ----------------------------------------------------
# # HELPER FUNCTIONS
# # ----------------------------------------------------
# def load_json(file_path):
#     """Load a JSON file safely."""
#     if not file_path.exists():
#         return None
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             return json.load(f)
#     except Exception as e:
#         st.error(f"Error reading JSON: {e}")
#         return None


# def display_summary(summary_file):
#     """Show the summary text below the PDF."""
#     st.subheader("📝 Summary of Report")
#     if summary_file.exists():
#         with open(summary_file, "r", encoding="utf-8") as f:
#             summary_text = f.read()
#         st.text_area("LLM-Generated Summary", summary_text, height=300, disabled=True)
#     else:
#         st.warning(f"⚠️ Summary file not found: {summary_file}")


# def display_json(json_file):
#     """Show JSON and table."""
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

# # ----------------------------------------------------
# # SIDEBAR NAVIGATION (with Tabs)
# # ----------------------------------------------------
# st.sidebar.title("🏠 Property Valuation Dashboard")
# tab1, tab2, tab3, tab4 = st.sidebar.tabs(["📘 Appraisal", "📗 BPO", "📙 Zillow", "📊 Comparison"])

# # ----------------------------------------------------
# # MAIN CONTENT
# # ----------------------------------------------------
# col1, col2 = st.columns([2, 1])

# # --- TAB 1: APPRAISAL ---
# with tab1:
#     with col1:
#         st.header("📘 Appraisal Report")
#         pdf_viewer(str(APPRAISAL_PDF),     
#         width=900,          # width of viewer area
#         height=1000,        # height controls scroll length
#         key="appraisal_pdf")      # enable scrolling in viewer)  # native viewer (scrollable, unlimited)
#         st.divider()
#         display_summary(APPRAISAL_SUMMARY)
#     with col2:
#         display_json(APPRAISAL_JSON)

# # --- TAB 2: BPO ---
# with tab2:
#     with col1:
#         st.header("📗 Broker Price Opinion (BPO) Report")
#         pdf_viewer(str(BPO_PDF),
#         width=900,          # width of viewer area)
#         height=1000,        # height controls scroll length
#         key="bpo_pdf")      # enable scrolling in viewer
#         st.divider()
#         display_summary(BPO_SUMMARY)
#     with col2:
#         display_json(BPO_JSON)

# # --- TAB 3: ZILLOW ---
# with tab3:
#     with col1:
#         st.header("📙 Third-Party Source (Zillow) Report")
#         pdf_viewer(str(ZILLOW_PDF), 
#         width=900,          # width of viewer area
#         height=1000,        # height controls scroll length
#         key="zillow_pdf")      # enable scrolling in viewer
#         st.divider()
#         display_summary(ZILLOW_SUMMARY)
#     with col2:
#         display_json(ZILLOW_JSON)
        

# # --- TAB 4: COMPARISON SUMMARY ---
# with tab4:
#     with col1:
#         st.header("📊 Multi-Source Comparison Summary")
#         if COMPARISON_SUMMARY.exists():
#             summary_text = COMPARISON_SUMMARY.read_text(encoding="utf-8")
#             st.text_area("Comparison Summary", summary_text, height=500, disabled=False)
#         else:
#             st.warning(f"⚠️ Comparison summary file not found: {COMPARISON_SUMMARY}")


##########################################################################################################################
# The above code with pdf viewer has some issues with tabs and the pdf is not showing up

##############################################################################################################

import streamlit as st
import json
import pandas as pd
from pathlib import Path
from streamlit_pdf_viewer import pdf_viewer

st.set_page_config(page_title="Property Valuation Dashboard", layout="wide")

BASE_DIR = Path("C:/Dip/Study/Programming/Fannie_Mae_code")

APPRAISAL_PDF = BASE_DIR / "Appraisal_Report_Sample.pdf"
APPRAISAL_JSON = BASE_DIR / "property_appraisal.json"
APPRAISAL_SUMMARY = BASE_DIR / "appraisal_report_summary.txt"

BPO_PDF = BASE_DIR / "sample_UAD.pdf"
BPO_JSON = BASE_DIR / "property_BPO.json"
BPO_SUMMARY = BASE_DIR / "BPO_summary.txt"

ZILLOW_PDF = BASE_DIR / "sample_UAD.pdf"
ZILLOW_JSON = BASE_DIR / "property_zillow.json"
ZILLOW_SUMMARY = BASE_DIR / "property_summary_zillow.txt"

COMPARISON_SUMMARY = BASE_DIR / "multi_source_comparison_summary.txt"


def load_json(file_path):
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error reading JSON: {e}")
    return None


def display_summary(summary_file):
    st.subheader("📝 Summary of Report")
    if summary_file.exists():
        with open(summary_file, "r", encoding="utf-8") as f:
            summary_text = f.read()
        st.text_area("LLM Summary", summary_text, height=300, disabled=True)
    else:
        st.warning(f"⚠️ Summary file not found: {summary_file}")


def display_json(json_file):
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


# ✅ USE MAIN PAGE TABS (NOT SIDEBAR)
st.sidebar.title("🏠 Property Valuation Dashboard")
tab1, tab2, tab3, tab4 = st.tabs(["📘 Appraisal", "📗 BPO", "📙 Zillow", "📊 Comparison"])

# ----------------------------------------------------
# TAB 1: APPRAISAL
# ----------------------------------------------------
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("📘 Appraisal Report")
        pdf_viewer(str(APPRAISAL_PDF), width=900, height=1000, key="appraisal_pdf")
        st.divider()
        display_summary(APPRAISAL_SUMMARY)
    with col2:
        display_json(APPRAISAL_JSON)

# ----------------------------------------------------
# TAB 2: BPO
# ----------------------------------------------------
with tab2:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("📗 Broker Price Opinion (BPO) Report")
        pdf_viewer(str(BPO_PDF), width=900, height=1000, key="bpo_pdf")
        st.divider()
        display_summary(BPO_SUMMARY)
    with col2:
        display_json(BPO_JSON)

# ----------------------------------------------------
# TAB 3: ZILLOW
# ----------------------------------------------------
with tab3:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("📙 Third-Party (Zillow) Report")
        pdf_viewer(str(ZILLOW_PDF), width=900, height=1000, key="zillow_pdf")
        st.divider()
        display_summary(ZILLOW_SUMMARY)
    with col2:
        display_json(ZILLOW_JSON)

# ----------------------------------------------------
# TAB 4: COMPARISON SUMMARY
# ----------------------------------------------------
with tab4:
    st.header("📊 Multi-Source Comparison Summary")
    if COMPARISON_SUMMARY.exists():
        st.text_area("Comparison Summary", COMPARISON_SUMMARY.read_text(encoding="utf-8"), height=500, disabled=True)
    else:
        st.warning(f"⚠️ Comparison summary file not found: {COMPARISON_SUMMARY}")
