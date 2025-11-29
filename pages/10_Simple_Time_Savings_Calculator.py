#!/usr/bin/python3 -tt
# Project: automation_business_case_calculator
# Filename: 10_Simple_Time_Savings_Calculator.py
# Minimal stub page to estimate simple time savings

import streamlit as st


def main():
    st.set_page_config(page_title="Simple Time Savings Calculator", page_icon="⏱️", layout="wide")

    st.title("Simple Time Savings Calculator")
    st.caption("Quickly estimate annual hours and cost savings from automating a task.")

    with st.expander("About", expanded=False):
        st.markdown(
            """
            This lightweight calculator helps you estimate time and cost savings:
            - Enter manual vs automated minutes per interaction.
            - Specify how many interactions happen per month and the automation coverage.
            - Provide engineer fully-loaded cost per hour.
            """
        )

    col1, col2 = st.columns(2)
    with col1:
        manual_minutes = st.number_input("Manual minutes per interaction", min_value=0.0, value=30.0, step=5.0, key="sts_manual_min")
        auto_minutes = st.number_input("Automated minutes per interaction (target)", min_value=0.0, value=5.0, step=1.0, key="sts_auto_min")
        changes_per_month = st.number_input("Interactions per month", min_value=0.0, value=100.0, step=10.0, key="sts_cpm")

    with col2:
        automation_coverage_pct = st.number_input("Automation coverage (%)", min_value=0.0, max_value=100.0, value=75.0, step=5.0, key="sts_cov")
        hourly_rate = st.number_input("Engineer fully-loaded cost (USD/hour)", min_value=0.0, value=100.0, step=5.0, key="sts_rate")
        years = st.number_input("Model horizon (years)", min_value=1, value=5, step=1, key="sts_years")

    minutes_saved = max(0.0, manual_minutes - auto_minutes)
    tasks_per_year = changes_per_month * 12.0
    effective_changes = tasks_per_year * (automation_coverage_pct / 100.0)
    annual_hours_saved = (minutes_saved / 60.0) * effective_changes
    annual_cost_savings = annual_hours_saved * hourly_rate

    st.markdown("**Results**")
    st.info(
        f"Minutes saved/interaction: {minutes_saved:.1f}\n\n"
        f"Changes/year: {tasks_per_year:,.0f}\n\n"
        f"Effective automated changes/year: {effective_changes:,.0f}\n\n"
        f"Annual hours saved: {annual_hours_saved:,.1f} hours\n\n"
        f"Annual cost savings: ${annual_cost_savings:,.2f}"
    )

    st.caption("Tip: Use the Business Case Calculator for full NPV/IRR/payback modeling.")
    try:
        st.page_link("pages/20_Business_Case_Calculator.py", label="Open Business Case Calculator", icon="🧮")
    except Exception:
        pass


if __name__ == "__main__":
    main()
