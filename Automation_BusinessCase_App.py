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


def main():

    st.set_page_config(
        page_title="Automation Business Case App",
        page_icon="images/EIA_Favicon.png",
        layout="wide",
    )

    cols = st.columns([1, 5, 1])
    with cols[0]:
        st.image("images/naf_icon.png", use_container_width=True)
        st.markdown("[🏠](https://networkautomation.forum/)")
    with cols[2]:
        st.image("images/EIA Logo FINAL Large_Dark Background.png")
        st.markdown("[🏠](https://eianow.com)")

    st.title("Automation Business Case App")

    st.caption(f"Loaded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    st.markdown(
        """
    This app helps you build a defensible business case for Network Automation, quantify costs and benefits, and generate a CXO-ready Markdown report. It also includes a Solution Wizard to describe your automation approach aligned to the NAF Automation Framework.
    
    ### What you can do here
    - **Business Case Calculator**: Enter your volumes, time savings, Buy vs Build costs, and (optional) Debts & Risk (Technical Debt and CSAT Debt). The app computes NPV, IRR, Payback, and generates a Markdown report. You can download a ZIP with the report and a timestamped JSON scenario.
    - **Business Case Comparison**: Upload two saved JSON scenarios (e.g., Buy vs Build) and compare key metrics side-by-side with deltas.
    - **Solution Wizard**: Describe an automation solution aligned to the Network Automation Forum (NAF) Automation Framework. Capture choices for Presentation, Intent, Observability, Orchestration, Collector, and Executor, and preview a clear narrative per section.
    
    ### How to get started
    1. Use the Solution Wizard to outline your automation solution (optional, can be done anytime).
    2. Open the calculator to input your assumptions and generate a scenario + report.
    3. Download the combined ZIP (Markdown + JSON) with a scenario slug (e.g., "buy" or "build").
    4. Use the comparison page to upload two JSON files and benchmark outcomes.
    
    ### Navigate to a page
    """
    )

    # Streamlit's page links (visible when running as a multipage app with a /pages directory)
    st.page_link(
        "pages/20_Business_Case_Calculator.py",
        label=" Open Business Case Calculator",
        icon="🧮",
    )
    st.page_link(
        "pages/30_Business_Case_Comparison.py",
        label=" Open Business Case Comparison",
        icon="📊",
    )
    st.page_link(
        "pages/40_Solution_Wizard.py",
        label=" Open Solution Wizard",
        icon="🧭",
    )

    # About the Solution Wizard (NAF Framework)
    st.markdown("---")
    st.subheader("About the Solution Wizard (NAF Framework)")
    try:
        st.page_link(
            "pages/40_Solution_Wizard.py",
            label="Open Solution Wizard",
            icon="🧭",
        )
    except Exception:
        st.caption("Open the 'Solution Wizard' from the left navigation.")

    st.markdown(
        """
        ### Purpose of the Wizard
        The wizard serves as a structured thinking tool and a second set of eyes to ensure you haven’t overlooked any key aspects of your automation project. It helps you organize your approach by prompting you to clarify what your automation system will do, who it will serve, and how it will be built and supported. This ensures you have a comprehensive understanding before making investment or development decisions.

        ### When to Use the Wizard
        - If you want to validate your project plan and make sure all components are addressed, the wizard is a helpful resource.
        - If you’ve already thought through the NAF Framework and have your business case details, you can skip the wizard and use the Business Case Calculator directly.
        - The wizard can also assist in generating text for the "Detailed solution description" box, helping you articulate your automation system clearly.

        ### Key Points to Remember
        - A thorough grasp of your automation system’s purpose, target users, build/support strategy, and integration points is essential for filling out the Business Case Calculator effectively.
        - The NAF Framework is flexible and inclusive, allowing you to use your own tools and operational practices while ensuring your automation solution is well-structured and future-proof.
        - This wizard and the underlying NAF Framework are here to help you build robust, maintainable, and business-aligned network automation solutions.
        """
    )

    st.info(
        "Tip: You can always come back to this page from the sidebar to choose a different task."
    )

    st.caption(
        "Solution Wizard content is informed by the Network Automation Forum's Automation Framework: "
        "https://github.com/Network-Automation-Forum/reference/tree/main/docs/Framework"
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

    with st.expander("Resources", expanded=False):
        st.subheader("Technical Debt")
        st.markdown(
            "- How to measure technical debt: https://ltsgroup.tech/blog/how-to-measure-technical-debt/"
        )
        st.markdown(
            "- How to calculate the cost of tech debt (9 metrics): https://www.pragmaticcoders.com/blog/how-to-calculate-the-cost-of-tech-debt-9-metrics-to-use"
        )


if __name__ == "__main__":
    main()
