#!/usr/bin/python3 -tt
# Project: automation_business_case_calculator
# Filename: Automation_BusinessCase_App.py
# claudiadeluna
# PyCharm

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "11/25/25"
__copyright__ = "Copyright (c) 2025 Claudia"
__license__ = "Python"

import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Automation Business Case App",
    page_icon="images/EIA_Favicon.png",
    layout="wide",
)

cols = st.columns([1, 5, 1])
with cols[2]:
    st.image("images/EIA Logo FINAL Large_Dark Background.png")

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
"""
)

# Streamlit's page links (visible when running as a multipage app with a /pages directory)
st.page_link(
    "pages/01_Business_Case_Calculator.py",
    label=" Open Business Case Calculator",
    icon="🧮",
)
st.page_link(
    "pages/02_Business_Case_Comparison.py",
    label=" Open Business Case Comparison",
    icon="📊",
)

st.info(
    "Tip: You can always come back to this page from the sidebar to choose a different task."
)

with st.expander("Checklist: Values you’ll need"):
    st.markdown(
        """
        - **Initiative basics**
          - [ ] Title
          - [ ] Short description/scope
        - **Volume & cost assumptions**
          - [ ] Switches per location (avg)
          - [ ] Number of locations (or total devices)
          - [ ] Changes per month for this change type
          - [ ] Percent of these changes automated (%)
          - [ ] Engineer fully-loaded cost (USD/hour)
        - **Acquisition strategy (choose one)**
          - Buy tool(s)
            - [ ] One-time: license(s)
            - [ ] One-time: integration/implementation
            - [ ] One-time: training
            - [ ] Annual: ongoing support & maintenance
          - Build in-house
            - [ ] One-time: development effort
            - [ ] One-time: staff opportunity cost
            - [ ] One-time: training
            - [ ] Annual: ongoing support & maintenance
        - **Debts & Risk (optional; applied to non-automated scope)**
          - Technical Debt
            - [ ] Annual cost at 100% impact (USD/year)
            - [ ] One-time remediation cost (optional)
            - [ ] Residual technical debt after remediation (%)
          - CSAT Debt
            - [ ] Annual cost at 100% impact (USD/year)
            - [ ] One-time remediation cost (optional)
            - [ ] Residual CSAT debt after remediation (%)
        - **Manual vs Automated time per change (minutes per step)**
          - [ ] Obtain change details (intent, devices)
          - [ ] Develop command payload
          - [ ] Quantify impact
          - [ ] Change management, scheduling, notifications
          - [ ] Current state analysis and verification
          - [ ] Execute change
          - [ ] Test and verification QA
          - [ ] Documentation, notification, close out
        - **Additional Benefits (optional; per checked category)**
          - [ ] Annual value (USD/year)
          - [ ] Methodology (how estimated)
          - [ ] Typical values/assumptions
        - **Finance**
          - [ ] Discount rate / hurdle rate (%)
        """
    )
    st.markdown(
        """
            ---
            ### Intangible / Soft Benefits (context)
            Some outcomes are hard to price precisely but still matter for funding and prioritization. In the calculator’s sidebar you can select relevant categories (not monetized by default), such as:
            - Relationship and Trust
            - Demand and Alignment
            - Organizational Behavior
            - Financial and Political Capital
            - Culture and Talent
            - Risk and Resilience
            - Reputation and Influence
            """
    )
