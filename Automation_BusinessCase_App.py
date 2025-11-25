#!/usr/bin/env python3

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Automation Business Case App",
    page_icon="images/EIA_Favicon.png",
    layout="wide",
)

cols = st.columns([1, 5, 1])
with cols[2]:
    st.image("images/EIA Logo FINAL small_Dark Background.png", width=160)

st.title("Automation Business Case App")

st.caption(f"Loaded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown(
    """
This app helps you build a defensible business case for Network Automation, quantify costs and benefits, and generate a CXO-ready Markdown report.

### What you can do here
- **Business Case Calculator**: Enter your volumes, time savings, Buy vs Build costs, and (optional) Debts & Risk (Technical Debt and CSAT Debt). The app computes NPV, IRR, Payback, and generates a Markdown report. You can download a ZIP with the report and a timestamped JSON scenario.
- **Business Case Comparison**: Upload two saved JSON scenarios (e.g., Buy vs Build) and compare key metrics side-by-side with deltas.

### How to get started
1. Open the calculator to input your assumptions and generate a scenario + report.
2. Download the combined ZIP (Markdown + JSON) with a scenario slug (e.g., "buy" or "build").
3. Use the comparison page to upload two JSON files and benchmark outcomes.

### Navigate to a page
- 🧮 **Business Case Calculator**

- 📊 **Business Case Comparison**

Tip: You can always come back to this page from the sidebar to choose a different task.
"""
)

# Streamlit's page links (visible when running as a multipage app with a /pages directory)
st.page_link("pages/01_Business_Case_Calculator.py", label="🧮 Open Business Case Calculator", icon="🧮")
st.page_link("pages/02_Business_Case_Comparison.py", label="📊 Open Business Case Comparison", icon="📊")
