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
          - Customer Satisfaction (CSAT) Debt
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
        - **Benefit categories you can include to offset costs**
          - Revenue Acceleration
          - Customer Satisfaction / Net Promoter Score (NPS)
          - Deployment Speed
          - Compliance / Audit Savings
          - Security Risk Reduction
          - Time-to-Market
          - Competitive Advantage
          - Employee Retention
          - Reduced 3rd party support spend
          - Other
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

with st.expander("How the calculations work"):
    st.markdown(
        """
        The calculator turns your engineering inputs into business metrics. Here’s exactly how:

        - **Tasks per year**  
          `tasks_per_year = changes_per_month × 12`

        - **Time saved per change (hours)**  
          `hours_saved_per_change = (manual_total_minutes − auto_total_minutes) ÷ 60`

        - **Effective automated changes/year**  
          `effective_changes_per_year = tasks_per_year × (automation_coverage_% ÷ 100)`

        - **Annual hours saved**  
          `annual_hours_saved = hours_saved_per_change × effective_changes_per_year`

        - **Annual cost savings (time)**  
          `annual_cost_savings = annual_hours_saved × engineer_hourly_rate`

        - **Additional benefits (optional)**  
          Sum of any checked benefit categories.  
          `annual_additional_benefits = Σ benefit_annual_value`

        - **Total annual benefit**  
          `annual_total_benefit = annual_cost_savings + annual_additional_benefits`

        - **Annual run cost (effective)**  
          Includes ongoing run cost plus optional debts (scaled by non‑automated scope).  
          `annual_run_cost_effective = annual_run_cost + tech_debt_annual_after + csat_debt_annual_after`

        - **Annual net benefit**  
          `annual_net_benefit = annual_total_benefit − annual_run_cost_effective`

        - **Project cost (Year 0)**  
          One‑time Buy/Build cost, plus any one‑time remediation.  
          `project_cost_effective = project_cost + tech_debt_remediation_one_time + csat_debt_remediation_one_time`

        - **Cash flows (Year 0..N)**  
          Year 0 is the investment (negative), followed by N years of annual net benefit.  
          `cash_flows = [−project_cost_effective] + [annual_net_benefit] × years`

        - **Net Present Value (NPV)**  
          Uses your discount (hurdle) rate `r` to reflect time value of money.  
          `NPV = Σ ( CF_t ÷ (1 + r)^t ), t = 0..years`

        - **Payback period (undiscounted)**  
          Years until cumulative cash ≥ 0; if it happens mid‑year, we interpolate a fraction.

        - **Internal Rate of Return (IRR)**  
          The discount rate where NPV = 0. If IRR > your discount rate, the project clears the financial bar.

        - **Cumulative checkpoints (1/3/5 yrs)**  
          Simple running totals to show progress recovering the initial investment.

        - **Sign convention**  
          Benefits are positive (returns). Costs are investments and appear as negative cash flows.
        """
    )
