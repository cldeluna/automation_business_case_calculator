#!/usr/bin/python3 -tt
# Project: automation_business_case_calculator
# Filename: 01_Business_Case_Calculator.py
# claudiadeluna
# PyCharm

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "11/25/25"
__copyright__ = "Copyright (c) 2025 Claudia"
__license__ = "Python"


import utils

import streamlit as st
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from io import BytesIO
import zipfile


# ---------- Financial helper functions ----------


def compute_payback_period(cash_flows: List[float]) -> Optional[float]:
    """
    Simple (undiscounted) payback period in years.
    Returns fractional years, or None if payback never happens.
    """
    cumulative = 0.0
    for t in range(len(cash_flows)):
        prev_cumulative = cumulative
        cumulative += cash_flows[t]
        if cumulative >= 0:
            if t == 0:
                return 0.0
            cash_this_year = cash_flows[t]
            if cash_this_year == 0:
                return float(t)
            fraction = (0 - prev_cumulative) / cash_this_year
            return (t - 1) + fraction
    return None


def compute_irr(
    cash_flows: List[float], guess_low: float = -0.9, guess_high: float = 10.0
) -> Optional[float]:
    """
    Very simple IRR calculation using binary search.

    Returns the rate r such that NPV(r) ~= 0, or None if it cannot find a solution.
    """

    def npv_at(rate: float) -> float:
        return utils.compute_npv(rate, cash_flows)

    npv_low = npv_at(guess_low)
    npv_high = npv_at(guess_high)

    # Need sign change to have a root in [low, high]
    if npv_low * npv_high > 0:
        return None

    for _ in range(100):
        mid = (guess_low + guess_high) / 2
        npv_mid = npv_at(mid)
        if abs(npv_mid) < 1e-6:
            return mid
        if npv_low * npv_mid < 0:
            guess_high = mid
            npv_high = npv_mid
        else:
            guess_low = mid
            npv_low = npv_mid

    return (guess_low + guess_high) / 2


# ---------- NABCD(E) summary builder ----------


def build_nabcde_summary(
    years: int,
    automation_title: str,
    automation_description: str,
    tasks_per_year: float,
    automation_coverage_pct: float,
    manual_total_minutes: float,
    annual_hours_saved: float,
    annual_total_benefit: float,
    project_cost: float,
    annual_run_cost: float,
    npv: float,
    payback: Optional[float],
    irr: Optional[float],
    acquisition_strategy: str,
) -> str:
    """
    Build a short NABCD(E) summary in plain markdown.
    """

    title = automation_title or "Network Automation Initiative"
    payback_text = (
        f"{payback:.2f} years" if payback is not None else "beyond the modeled period"
    )
    irr_text = f"{irr*100:.2f}%" if irr is not None and irr > -1 else "not meaningful"

    desc_block = (
        f" ({automation_description.strip()})" if automation_description.strip() else ""
    )

    # Approach string varies by Buy vs Build to show consequences
    if (acquisition_strategy or "").lower().startswith("buy"):
        approach_line = (
            f"**Approach** – Buy: implement network automation to handle ~{automation_coverage_pct:.1f}% of changes end-to-end "
            f"(execution, config assembly, ITSM integration, validation). One-time project ~${project_cost:,.0f}; ongoing ~${annual_run_cost:,.0f}/year "
            f"(licenses/support). Consequences: faster time-to-value, less internal engineering, vendor dependency, predictable support SLAs."
        )
    else:
        approach_line = (
            f"**Approach** – Build: implement in-house automation to handle ~{automation_coverage_pct:.1f}% of changes end-to-end "
            f"(execution, config assembly, ITSM integration, validation). One-time project ~${project_cost:,.0f}; ongoing ~${annual_run_cost:,.0f}/year "
            f"(support/maintenance). Consequences: greater control and fit, skill growth, longer time-to-value, internal opportunity cost."
        )

    summary = f"""**Need** – Manual changes for **{title}**{desc_block} consume about {manual_total_minutes:.1f} minutes per change across ~{tasks_per_year:,.0f} changes/year, tying up roughly {annual_hours_saved:,.0f} engineer-hours and exposing the business to avoidable risk, delay, and inconsistency.

{approach_line}

**Benefits** – Combined financial impact of roughly ${annual_total_benefit:,.0f}/year from engineer-time savings and additional business benefits (revenue, customer experience, risk reduction, and speed). Over {years} years this produces an NPV of about ${npv:,.0f}, an IRR of {irr_text}, and payback in about {payback_text}.

**Competitiveness** – Faster, safer, and more consistent change delivery than manual alternatives, freeing engineers for higher-value work and improving time-to-market versus teams that still rely on ad-hoc CLI changes.

**Defensibility** – Standardized, repeatable workflows reduce human error, enforce policy/compliance, and create a clear audit trail for every change.

**Exit / Ask** – Approve ~${project_cost:,.0f} in initial funding plus ~${annual_run_cost:,.0f}/year to make automated change the default operating model, capturing the quantified savings, risk reduction, and customer experience benefits described above.
"""
    return summary


# ---------- Markdown report builder ----------


def build_markdown_report(
    years: int,
    automation_title: str,
    automation_description: str,
    solution_details_md: str,
    out_of_scope: str,
    switches_per_location: float,
    num_locations: float,
    total_switches: float,
    tasks_per_year: float,
    automation_coverage_pct: float,
    hourly_rate: float,
    manual_total_minutes: float,
    auto_total_minutes: float,
    minutes_saved_per_change: float,
    annual_hours_saved: float,
    annual_cost_savings: float,
    benefits: List[Dict[str, Any]],
    annual_additional_benefits: float,
    annual_total_benefit: float,
    annual_run_cost: float,
    annual_net_benefit: float,
    project_cost: float,
    discount_rate_pct: float,
    cash_flows: List[float],
    npv: float,
    payback: Optional[float],
    irr: Optional[float],
    cum_1: float,
    cum_3: float,
    cum_5: float,
    nabcde_summary: str,
    acquisition_strategy: str,
    cost_breakdown: List[Dict[str, Any]],
    tech_debt_included: bool,
    tech_debt_reduction_pct: Optional[float],
    tech_debt_base_annual: Optional[float],
    tech_debt_impact_pct: Optional[float],
    tech_debt_residual_pct: Optional[float],
    csat_debt_included: bool,
    csat_debt_base_annual: Optional[float],
    csat_debt_impact_pct: Optional[float],
    csat_debt_residual_pct: Optional[float],
) -> str:
    """
    Build a markdown report with a CXO-ready story but using the engineer inputs.
    """

    title = automation_title or "Network Automation Business Case"

    cash_flow_lines = []
    for t, cf in enumerate(cash_flows[: years + 1]):
        cash_flow_lines.append(f"| Year {t} | ${cf:,.2f} USD |")

    cash_flow_table = "\n".join(cash_flow_lines)

    payback_text = (
        f"{payback:.2f} years"
        if payback is not None
        else "Not reached within model horizon (beyond model years)"
    )
    irr_text = (
        f"{irr*100:.2f}%"
        if irr is not None and irr > -1
        else "Not meaningful / not found"
    )

    scope_lines = ""
    if switches_per_location > 0:
        scope_lines += (
            f"- **Switches per location (avg):** {switches_per_location:,.1f}\n"
        )
    if num_locations > 0:
        scope_lines += f"- **Locations impacted:** {num_locations:,.0f}\n"
    if total_switches > 0:
        scope_lines += (
            f"- **Estimated total switches/devices in scope:** {total_switches:,.0f}\n"
        )

    desc_block = (
        f"\n\n**Description / Scope**  \n{automation_description.strip()}\n"
        if automation_description.strip()
        else ""
    )

    # Optional long-form sections (Markdown supported)
    solution_details_block = (
        f"\n\n## Detailed Solution Description\n\n{solution_details_md.strip()}\n"
        if solution_details_md.strip()
        else ""
    )
    out_of_scope_block = (
        f"\n\n## Out of Scope / Not Automated\n\n{out_of_scope.strip()}\n"
        if out_of_scope.strip()
        else ""
    )

    # Build detailed benefit lines
    if benefits:
        benefit_lines = []
        for b in benefits:
            name = b.get("name") or b.get("category")
            category = b.get("category", "Benefit")
            value = b.get("annual_value", 0.0)
            methodology = b.get("methodology", "").strip() or "Not documented"
            typical = b.get("typical", "").strip() or "Not documented"

            benefit_lines.append(
                f"- **{name}** (Category: **{category}**) – ${value:,.2f} USD/year  \n"
                f"  - **Methodology:** {methodology}  \n"
                f"  - **Typical values / assumptions:** {typical}"
            )
        benefits_block = "\n".join(benefit_lines)
    else:
        benefits_block = (
            "No additional benefits beyond engineer time-savings were specified."
        )

    # Build Cost Modeling table
    if cost_breakdown:
        cb_lines = ["| Cost item | Timing | Amount (USD) |", "|---|---|---|"]
        for item in cost_breakdown:
            cb_lines.append(
                f"| {item.get('name','')} | {item.get('timing','')} | ${item.get('amount',0.0):,.2f} |"
            )
        cost_modeling_table = "\n".join(cb_lines)
    else:
        cost_modeling_table = "No itemized cost breakdown provided."

    # Determine if CSAT debt is present in cost breakdown (amount > 0)
    csat_present = any(
        (
            isinstance(item, dict)
            and str(item.get("name", "")).lower().startswith("csat debt")
            and item.get("amount", 0.0) > 0
        )
        for item in cost_breakdown
    )

    # Compose positive impacts list with conditional CSAT and technical debt items
    tech_line = ""
    if tech_debt_included:
        if tech_debt_reduction_pct is not None:
            tech_line = f"- Reduced technical debt (remediated by {tech_debt_reduction_pct:.0f}%)  "
        else:
            tech_line = "- Reduced technical debt  "

    items = [
        "- Deferring or avoiding incremental hiring for repetitive work  ",
        (
            "- Improved customer satisfaction (included in this model), reducing churn/credits/support  "
            if csat_present
            else ""
        ),
        tech_line,
        "- Reduced delays on other initiatives due to freed engineer capacity  ",
        "- Higher team morale by shifting work toward higher-value tasks  ",
        "- Smaller skills gaps as staff gain time to learn and cross-train  ",
    ]
    positive_impacts_lines = "\n".join([s for s in items if s]).strip()

    # Precompute Approach text to avoid backslashes in f-string expressions
    is_buy = (acquisition_strategy or "").lower().startswith("buy")
    approach_decision = "Buy" if is_buy else "Build"
    if is_buy:
        approach_consequences = "Buy – faster time-to-value, less internal engineering, vendor dependency, predictable support SLAs."
        approach_intro = "Implement a network automation solution that handles the repetitive parts of the workflow:"
        annual_run_label = "licenses/support"
    else:
        approach_consequences = "Build – greater control and fit, team skill growth, longer time-to-value, internal opportunity cost."
        approach_intro = "Implement in-house automation that handles the repetitive parts of the workflow:"
        annual_run_label = "support/maintenance"

    # Build optional Intangible/Soft Benefits section in the report if provided
    soft_benefits_section = ""
    try:
        if soft_benefits_selected:
            lines = [
                "## Intangible / Soft Benefits",
                "These qualitative impacts strengthen the narrative and stakeholder confidence. While not directly modeled in cash flows, they often influence funding, prioritization, and long‑term success:",
            ]
            for sb in soft_benefits_selected:
                lines.append(f"\n### {sb.get('name','')}")
                details = sb.get("details", [])
                for d in details:
                    lines.append(f"- {d}")
            soft_benefits_section = "\n" + "\n".join(lines) + "\n"
    except Exception:
        soft_benefits_section = ""

    report = f"""# {title} – Network Automation Business Case

## NABCD(E) One-Page Summary

{nabcde_summary}

---

## Summary

- **Time horizon:** {years} years  
- **Changes per year (this change type):** {tasks_per_year:,.0f} changes/year  
- **Percent of changes automated:** {automation_coverage_pct:.1f}% of changes/year  
- **Engineer fully-loaded cost:** ${hourly_rate:,.2f} USD/hour
 - **Acquisition strategy:** {acquisition_strategy}

{scope_lines}{desc_block}{solution_details_block}{out_of_scope_block}
## Need

Manual change handling for this activity is consuming significant engineer time and slowing delivery:

- **Manual time per change:** {manual_total_minutes:.1f} minutes/change  
- **Automated time per change (target):** {auto_total_minutes:.1f} minutes/change  
- **Time saved per change:** {minutes_saved_per_change:.1f} minutes/change  

Across the volume of work:

- **Annual hours saved (engineer time):** {annual_hours_saved:,.1f} hours/year  
- **Annual gross cost savings (time):** ${annual_cost_savings:,.2f} USD/year  

## Approach

{approach_decision} decision and consequences:

{approach_consequences}
{approach_intro}

1. Obtain change details (intent, devices impacted)  
2. Develop command payload  
3. Quantify impact  
4. Initiate change management, scheduling, and notifications  
5. Current state analysis and verification  
6. Execute change  
7. Test and verification QA  
8. Documentation, notification, and close out  

Assumptions:

- **Automation coverage:** {automation_coverage_pct:.1f}% of these changes  
- **One-time project cost (Year 0):** ${project_cost:,.2f} USD  
- **Annual run cost ({annual_run_label}):** ${annual_run_cost:,.2f} USD/year  
- **Discount rate (hurdle rate):** {discount_rate_pct:.1f}%  

## Benefits (Financial)

### Breakdown of Annual Benefits

- **Operational efficiency (time saved):** ${annual_cost_savings:,.2f} USD/year  

**Additional quantified benefits (only included if explicitly checked):**

{benefits_block}

- **Total of additional benefits:** ${annual_additional_benefits:,.2f} USD/year  
- **Total annual benefit (time + additional):** ${annual_total_benefit:,.2f} USD/year  

#### Totals (Sign Convention)
- Benefits are shown as positive amounts (returns / pluses).
- Costs are treated as investments and appear as negative cash flows (see Cost Modeling and Cash Flows sections).  

### Net Benefit After Run Costs

- **Annual net benefit (total benefits − run cost):** ${annual_net_benefit:,.2f} USD/year  

### Cash Flows (Year 0 to {years})

| Year | Cash Flow (USD) |
|------|-----------------|
{cash_flow_table}

### Financial Metrics

| Metric | Value | Definition | Tip |
|---|---|---|---|
| Discount rate (hurdle rate) | {discount_rate_pct:.1f}% | Your required annual return used to discount future cash; reflects cost of capital and risk. | Use the same rate across projects; higher rate = stricter bar. |
| Net Present Value (NPV, {years} years) | ${npv:,.2f} | Today's value of all project cash flows using the discount rate; > $0 means the project adds value. | Compare NPV across projects of similar size; higher is better. |
| Payback period (undiscounted) | {payback_text} | Years until cumulative cash turns positive (ignores time value of money). | Quick storytelling metric; many teams target ≤ 2–3 years. |
| Internal Rate of Return (IRR) | {irr_text} | Return rate where NPV = $0; compare to discount rate. | Bigger spread above the discount rate = better. |

#### Interpretation (plain English)
- Rule of thumb: If IRR is above the discount rate and NPV is > $0, the project is financially attractive.  
- Sensitivity: Higher discount rate or lower annual benefits reduce NPV/IRR and lengthen payback.  
- Narrative: Pair these numbers with outcomes: fewer outages, consistent changes, faster delivery.  

### Cumulative Cash Flow Checkpoints

- **After 1 year:** ${cum_1:,.2f} USD  
- **After 3 years:** ${cum_3:,.2f} USD  
- **After 5 years:** ${cum_5:,.2f} USD  

(Interpreting positive values: you've recovered the initial investment and created headroom. Beyond net cash generation, this can also enable:)
{positive_impacts_lines}

### Debt & Risk modeling details

Applied automation coverage: {automation_coverage_pct:.1f}% → debt impact applied: {100 - automation_coverage_pct:.1f}%

{('- Technical debt: base at 100% = $' + f"{(tech_debt_base_annual or 0):,.2f}" + 
   (', applied impact = ' + f"{(tech_debt_impact_pct or 0)*100:.0f}%" if tech_debt_impact_pct is not None else '') + 
   (', residual after remediation = ' + f"{(tech_debt_residual_pct or 0):.0f}%" if tech_debt_residual_pct is not None else '')
  ) if tech_debt_included else ''}

{('- CSAT debt: base at 100% = $' + f"{(csat_debt_base_annual or 0):,.2f}" + 
   (', applied impact = ' + f"{(csat_debt_impact_pct or 0)*100:.0f}%" if csat_debt_impact_pct is not None else '') + 
   (', residual after remediation = ' + f"{(csat_debt_residual_pct or 0):.0f}%" if csat_debt_residual_pct is not None else '')
  ) if csat_debt_included else ''}

## Cost Modeling

- **Selected strategy:** {acquisition_strategy}

{cost_modeling_table}

- **One-time project cost (Year 0):** ${project_cost:,.2f} USD  
- **Annual run cost:** ${annual_run_cost:,.2f} USD/year  
- **First-year total cost:** ${project_cost + annual_run_cost:,.2f} USD  

## Competitiveness

- Faster, safer changes vs. fully manual operations.  
- More consistent implementation across devices and sites.  
- Engineers can focus on higher-value design and troubleshooting instead of repetitive command-line work.  

## Defensibility (Risk & Compliance)

- Built-in repeatability and compliance: automation enforces standard patterns.  
- Reduced human error lowers outage risk and rework.  
- Clear audit trail for changes (via ITSM and automation logs).  
{soft_benefits_section}

## Exit / Ask

Based on this {years}-year model:

- **NPV** of ${npv:,.2f} and **IRR** of {irr_text} indicate a financially attractive initiative.  
- **Payback** in {payback_text} shows when the project becomes cash-positive.  

**Ask:** Approve funding of **${project_cost:,.2f} USD** for the initial automation delivery, with an ongoing budget of **${annual_run_cost:,.2f} USD/year** for run and maintenance, to secure the time, risk, and customer-impact benefits quantified above.
"""
    return report


# ---------- Streamlit app ----------

BENEFIT_CATEGORIES = [
    ("Revenue Acceleration", "rev"),
    ("Customer Satisfaction / NPS", "nps"),
    ("Deployment Speed", "deploy"),
    ("Compliance / Audit Savings", "compliance"),
    ("Security Risk Reduction", "security"),
    ("Time-to-Market", "ttm"),
    ("Competitive Advantage", "competitive"),
    ("Employee Retention", "retention"),
    ("Reduced 3rd party support spend", "thirdparty_support"),
    ("Other", "other"),
]


def main():
    st.set_page_config(
        page_title="Network Automation Business Case",
        page_icon="images/EIA_Favicon.png",
        layout="wide",
    )

    st.title("Network Automation Business Case Calculator")

    # ---- High-level automation info (title, description) ----
    st.subheader("Automation Initiative Details")

    st.write(
        "Enter the things you already know as a network engineer "
        "(how often, how long, plus optional benefits). "
        "The app converts that into business metrics (NPV, IRR, payback), "
        "a NABCD(E) summary, and a Markdown report you can share with CXOs."
    )

    automation_title = st.text_input(
        "Automation initiative title",
        value="Access VLAN Change Automation",
        help="Example: 'Access VLAN Change Automation', 'Firewall Rule Deployment Automation', etc.",
    )

    automation_description = st.text_area(
        "Short description / scope",
        value=(
            "Automation of access VLAN change workflows across the campus and branch network, "
            "including config generation, deployment, and validation."
        ),
        help="One or two sentences describing what this automation will do and where.",
    )

    solution_details_md = st.text_area(
        "Detailed solution description (Markdown supported)",
        value="",
        help="Provide a longer-form description of the approach, components, workflow, and assumptions. You can use Markdown for formatting.",
    )

    out_of_scope = st.text_area(
        "Out of scope / not automated (Markdown supported)",
        value="",
        help="List anything intentionally excluded or not automated in this solution. Markdown is supported.",
    )

    years = 5

    # Prepare container for soft benefits selections (used across UI and report)
    soft_benefits_selected: List[Dict[str, Any]] = []

    # -------- Sidebar for volume, cost & additional benefits --------
    with st.sidebar:
        st.image("images/EIA Logo FINAL small_Round.png", width=75)
        # st.markdown("---")
        _vol_cost = st.expander("Volume & Cost Assumptions", expanded=True)
        with _vol_cost:
            st.subheader("Volume & Cost Assumptions")

            switches_per_location = st.number_input(
            "Number of switches per location",
            min_value=0,
            value=10,
            step=1,
            help="This can be an average number of network switches (L2 and L3) "
            "or network devices per location.",
            )

        with _vol_cost:
            num_locations = st.number_input(
                "Number of locations",
                min_value=0,
                value=250,
                step=10,
                help="This can be an estimated number of locations which will be impacted "
                "by this operational improvement.",
            )

        total_switches = switches_per_location * num_locations
        with _vol_cost:
            st.metric(
                label="Estimated total switches/devices in scope",
                value=f"{total_switches:,.0f}",
            )

        with _vol_cost:
            tasks_per_month = st.number_input(
                "Changes per month (this type of change across the network)",
                min_value=0.0,
                value=5.0,  # default per your assumption
                step=1.0,
            )
        tasks_per_year = tasks_per_month * 12

        with _vol_cost:
            automation_coverage_pct = st.number_input(
                "Percent of these changes automated (%)",
                min_value=0.0,
                max_value=100.0,
                value=80.0,
                step=5.0,
            )

        with _vol_cost:
            hourly_rate = st.number_input(
            "Engineer fully-loaded cost (USD/hour)",
            min_value=0.0,
            value=75.0,
            step=5.0,
            )

        with _vol_cost:
            discount_rate_pct = st.number_input(
            "Discount rate / hurdle rate (%)",
            min_value=0.0,
            value=10.0,
            step=1.0,
            help=(
                "The required annual return used to discount future cash flows (time value of money). "
                "Used in NPV and as a comparison for IRR. 10% is a common placeholder, "
                "but verify the standard rate with your finance organization."
            ),
            )

        st.markdown("---")
        _acq = st.expander("Acquisition Strategy", expanded=True)
        with _acq:
            st.subheader("Acquisition Strategy")
            st.caption("All amounts below are COSTS (expenses), in USD.")
            acquisition_strategy = st.radio(
                "Will you buy a tool or build in-house?",
                options=["Buy tool(s)", "Build in-house" ],
                index=1,
                help=(
                    "Buy: pay vendor license(s) and integrate.\n"
                    "Build: develop internally; includes engineering time and opportunity cost."
                ),
            )

        # Prepare cost breakdown container to append additional items later
        cost_breakdown: List[Dict[str, Any]] = []

        if acquisition_strategy == "Buy tool(s)":
            with _acq:
                st.caption("Specify one-time and ongoing costs for buying a tool or tools.")
                st.markdown("**One-time costs**")
            with _acq:
                buy_tool_cost = st.number_input(
                "Tool license(s) cost – one-time (USD)",
                min_value=0.0,
                value=35000.0,
                step=5000.0,
                )
            with _acq:
                buy_integration_cost = st.number_input(
                "Integration/implementation cost – one-time (USD)",
                min_value=0.0,
                value=15000.0,
                step=5000.0,
                )
                buy_training_cost = st.number_input(
                "Training cost – one-time (USD)",
                min_value=0.0,
                value=5000.0,
                step=1000.0,
                )
                st.markdown("**Ongoing maintenance costs**")
                buy_ongoing_support = st.number_input(
                "Ongoing support & maintenance – annual (USD/year)",
                min_value=0.0,
                value=6000.0,
                step=1000.0,
                )

            project_cost = buy_tool_cost + buy_integration_cost + buy_training_cost
            annual_run_cost = buy_ongoing_support

            # Itemized breakdown for report/UI
            cost_breakdown = [
                {
                    "name": "Tool license(s)",
                    "timing": "One-time",
                    "amount": buy_tool_cost,
                },
                {
                    "name": "Integration/implementation",
                    "timing": "One-time",
                    "amount": buy_integration_cost,
                },
                {"name": "Training", "timing": "One-time", "amount": buy_training_cost},
                {
                    "name": "Ongoing support & maintenance",
                    "timing": "Annual",
                    "amount": buy_ongoing_support,
                },
            ]

            # Validation: flag zeros to confirm
            zero_fields = []
            if buy_tool_cost == 0:
                zero_fields.append("Tool license(s)")
            if buy_integration_cost == 0:
                zero_fields.append("Integration/implementation")
            if buy_training_cost == 0:
                zero_fields.append("Training")
            if buy_ongoing_support == 0:
                zero_fields.append("Ongoing support & maintenance")
            if zero_fields:
                with _acq:
                    st.warning(
                        "You entered $0 for: "
                        + ", ".join(zero_fields)
                        + ". Confirm these should truly be zero."
                    )

        else:  # Build in-house
            with _acq:
                st.caption("Specify one-time and ongoing costs for building in-house.")
                st.markdown("**One-time costs**")
            with _acq:
                build_dev_effort = st.number_input(
                "Development effort cost – one-time (USD)",
                min_value=0.0,
                value=40000.0,
                step=5000.0,
                help="Engineering time (contractors and/or internal allocation).",
                )
            with _acq:
                build_opportunity = st.number_input(
                "Staff opportunity cost – one-time (USD)",
                min_value=0.0,
                value=10000.0,
                step=2000.0,
                help="Value of in-house staff not doing BAU (Business as Usual or their 'day job') while building.",
                )
                build_training_cost = st.number_input(
                "Training cost – one-time (USD)",
                min_value=0.0,
                value=3000.0,
                step=1000.0,
                )
                st.markdown("**Ongoing maintenance costs**")
                build_ongoing_support = st.number_input(
                "Ongoing support & maintenance – annual (USD/year)",
                min_value=0.0,
                value=8000.0,
                step=1000.0,
                )

            project_cost = build_dev_effort + build_opportunity + build_training_cost
            annual_run_cost = build_ongoing_support

            # Itemized breakdown for report/UI
            cost_breakdown = [
                {
                    "name": "Development effort",
                    "timing": "One-time",
                    "amount": build_dev_effort,
                },
                {
                    "name": "Staff opportunity cost",
                    "timing": "One-time",
                    "amount": build_opportunity,
                },
                {
                    "name": "Training",
                    "timing": "One-time",
                    "amount": build_training_cost,
                },
                {
                    "name": "Ongoing support & maintenance",
                    "timing": "Annual",
                    "amount": build_ongoing_support,
                },
            ]

            # Validation: flag zeros to confirm
            zero_fields = []
            if build_dev_effort == 0:
                zero_fields.append("Development effort")
            if build_opportunity == 0:
                zero_fields.append("Staff opportunity cost")
            if build_training_cost == 0:
                zero_fields.append("Training")
            if build_ongoing_support == 0:
                zero_fields.append("Ongoing support & maintenance")
            if zero_fields:
                st.warning(
                    "You entered $0 for: "
                    + ", ".join(zero_fields)
                    + ". Confirm these should truly be zero."
                )

        # Debts & Risk (Optional) – Technical debt modeled from automation coverage
        st.markdown("---")
        _debts = st.expander("Debts & Risk (Optional)", expanded=False)
        with _debts:
            st.subheader("Debts & Risk (Optional)")
            st.caption(
                "Technical debt is assumed to impact the non-automated portion of the estate."
            )
            include_tech_debt = st.checkbox(
            "Include technical debt as an additional annual cost",
            value=False,
            help=(
                "Annual technical debt cost is scaled by (1 − automation%). "
                "Example: at 80% automation, 20% impact applies."
            ),
            )

        tech_debt_annual_after = 0.0
        tech_debt_remediation_one_time = 0.0
        tech_reduction_pct = None
        tech_debt_base_annual = None
        tech_debt_impact_pct = None
        tech_debt_residual_pct = None
        if include_tech_debt:
            base_tech_debt_annual = _debts.number_input(
                "Technical debt annual cost at 100% impact (USD/year)",
                min_value=0.0,
                value=20000.0,
                step=1000.0,
            )
            impact_pct = max(0.0, 1.0 - (automation_coverage_pct / 100.0))
            tech_debt_base_annual = float(base_tech_debt_annual)
            tech_debt_impact_pct = impact_pct
            tech_debt_annual = base_tech_debt_annual * impact_pct
            _debts.info(
                f"Calculated technical debt (annual): ${tech_debt_annual:,.0f} (impact {impact_pct*100:.0f}%)"
            )

            include_remediation = _debts.checkbox(
                "This automation includes technical debt remediation",
                value=False,
                help=(
                    "Adds a one-time remediation cost in Year 0 and optionally reduces the ongoing annual technical debt."
                ),
            )
            residual_pct = 100.0
            if include_remediation:
                tech_debt_remediation_one_time = _debts.number_input(
                    "One-time remediation cost (USD)",
                    min_value=0.0,
                    value=10000.0,
                    step=1000.0,
                )
                residual_pct = _debts.number_input(
                    "Residual technical debt after remediation (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=5.0,
                    help="Percent of the technical debt that remains annually after remediation (0% = fully remediated).",
                )
                tech_debt_residual_pct = residual_pct

            tech_debt_annual_after = tech_debt_annual * (residual_pct / 100.0)
            if include_remediation:
                tech_reduction_pct = 100.0 - float(residual_pct)
            # Append to cost breakdown for reporting
            cost_breakdown.append(
                {
                    "name": "Technical debt (annual, adjusted by automation)",
                    "timing": "Annual",
                    "amount": tech_debt_annual_after,
                }
            )
            if tech_debt_remediation_one_time > 0:
                cost_breakdown.append(
                    {
                        "name": "Technical debt remediation",
                        "timing": "One-time",
                        "amount": tech_debt_remediation_one_time,
                    }
                )

        # CSAT debt (Optional) – modeled similarly, scaled by non-automated portion
        include_csat_debt = _debts.checkbox(
            "Include CSAT (customer satisfaction) debt as an additional annual cost",
            value=False,
            help=(
                "Annual CSAT debt cost is scaled by (1 − automation%). "
                "Represents churn risk, service credits, extra support load."
            ),
        )

        csat_debt_annual_after = 0.0
        csat_debt_remediation_one_time = 0.0
        csat_debt_base_annual = None
        csat_debt_impact_pct = None
        csat_debt_residual_pct = None
        if include_csat_debt:
            base_csat_debt_annual = _debts.number_input(
                "CSAT debt annual cost at 100% impact (USD/year)",
                min_value=0.0,
                value=15000.0,
                step=1000.0,
            )
            impact_pct = max(0.0, 1.0 - (automation_coverage_pct / 100.0))
            csat_debt_base_annual = float(base_csat_debt_annual)
            csat_debt_impact_pct = impact_pct
            csat_debt_annual = base_csat_debt_annual * impact_pct
            _debts.info(
                f"Calculated CSAT debt (annual): ${csat_debt_annual:,.0f} (impact {impact_pct*100:.0f}%)"
            )

            include_csat_remediation = _debts.checkbox(
                "This automation includes CSAT debt remediation",
                value=False,
                help=(
                    "Adds a one-time CSAT remediation cost in Year 0 and optionally reduces the ongoing annual CSAT debt."
                ),
            )
            csat_residual_pct = 100.0
            if include_csat_remediation:
                csat_debt_remediation_one_time = _debts.number_input(
                    "CSAT remediation cost (one-time USD)",
                    min_value=0.0,
                    value=5000.0,
                    step=1000.0,
                )
                csat_residual_pct = _debts.number_input(
                    "Residual CSAT debt after remediation (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=20.0,
                    step=5.0,
                    help="Percent of the CSAT debt that remains annually after remediation.",
                )
                csat_debt_residual_pct = csat_residual_pct

            csat_debt_annual_after = csat_debt_annual * (csat_residual_pct / 100.0)
            cost_breakdown.append(
                {
                    "name": "CSAT debt (annual, adjusted by automation)",
                    "timing": "Annual",
                    "amount": csat_debt_annual_after,
                }
            )
            if csat_debt_remediation_one_time > 0:
                cost_breakdown.append(
                    {
                        "name": "CSAT debt remediation",
                        "timing": "One-time",
                        "amount": csat_debt_remediation_one_time,
                    }
                )

        # Summary of costs at bottom of section (vertical for readability)
        utils.thick_hr(color="red", thickness=5)

        # Detect if user has not modified any seeded cost inputs (show prompt instead of values)
        using_defaults_costs = False
        if acquisition_strategy == "Buy tool(s)":
            using_defaults_costs = (
                float(buy_tool_cost) == 35000.0
                and float(buy_integration_cost) == 15000.0
                and float(buy_training_cost) == 5000.0
                and float(buy_ongoing_support) == 6000.0
                and not include_tech_debt
                and not include_csat_debt
            )
        else:
            using_defaults_costs = (
                float(build_dev_effort) == 40000.0
                and float(build_opportunity) == 10000.0
                and float(build_training_cost) == 3000.0
                and float(build_ongoing_support) == 8000.0
                and not include_tech_debt
                and not include_csat_debt
            )

        if using_defaults_costs:
            st.info("Update values to your needs to see a cost summary.")
        else:
            st.markdown("**➖ Cost summary (USD)**")
            first_year_total_cost = (
                project_cost
                + annual_run_cost
                + tech_debt_annual_after
                + tech_debt_remediation_one_time
                + csat_debt_annual_after
                + csat_debt_remediation_one_time
            )
            st.write(f"- One-time project cost (Year 0): ${project_cost:,.0f}")
            st.write(f"- Annual run cost (per year): ${annual_run_cost:,.0f}")
            if include_tech_debt:
                st.write(f"- Technical debt (annual): ${tech_debt_annual_after:,.0f}")
                if tech_debt_remediation_one_time:
                    st.write(
                        f"- Technical debt remediation (one-time): ${tech_debt_remediation_one_time:,.0f}"
                    )
            if include_csat_debt:
                st.write(f"- CSAT debt (annual): ${csat_debt_annual_after:,.0f}")
                if csat_debt_remediation_one_time:
                    st.write(
                        f"- CSAT debt remediation (one-time): ${csat_debt_remediation_one_time:,.0f}"
                    )
            st.info(f"First-year total cost: ${first_year_total_cost:,.0f}")
            st.caption(
                "Project cost is incurred in Year 0; annual run cost recurs each year."
            )
        utils.thick_hr(color="red", thickness=5)
        # st.markdown("---")
        _ben = st.expander("Additional Benefits (Optional)", expanded=False)
        with _ben:
            st.header("Additional Benefits (Optional)")
            st.caption(
                "Check any benefit types that apply, then specify the annual dollar value, "
                "methodology, and typical assumptions. Only checked benefits are included "
                "in the calculations."
            )

        benefit_inputs: List[Dict[str, Any]] = []

        for label, key in BENEFIT_CATEGORIES:
            include = _ben.checkbox(label, value=False, key=f"{key}_include")
            if include:
                _ben.markdown(f"**{label}**")

                name = _ben.text_input(
                    f"{label} – Benefit name",
                    value=label,
                    key=f"{key}_name",
                    help="Short, clear description (e.g., 'Faster upsell of managed LAN deals').",
                )

                # Helper calculator for Revenue Acceleration / Deployment Speed:
                typical_str = ""
                suggested_value = None

                if label in ("Revenue Acceleration", "Deployment Speed"):
                    _ben.caption(
                        "Helper: quantify days of 'waiting' you eliminate.\n"
                        "Example: VLAN distribution manually takes 5 business days, "
                        "automation completes in 1 day (4 days saved)."
                    )
                    manual_days = _ben.number_input(
                        f"{label} – Manual duration (days)",
                        min_value=0.0,
                        value=5.0,
                        step=0.5,
                        key=f"{key}_manual_days",
                    )
                    auto_days = _ben.number_input(
                        f"{label} – Automated duration (days)",
                        min_value=0.0,
                        value=1.0,
                        step=0.5,
                        key=f"{key}_auto_days",
                    )
                    sites_per_year = _ben.number_input(
                        f"{label} – Sites/projects per year impacted",
                        min_value=0.0,
                        value=12.0,
                        step=1.0,
                        key=f"{key}_sites_per_year",
                    )
                    value_per_site_day = _ben.number_input(
                        f"{label} – Business value per site per day (USD)",
                        min_value=0.0,
                        value=1000.0,
                        step=500.0,
                        key=f"{key}_value_per_day",
                        help="Rough value of a site being 'fully live' per day "
                        "(revenue, productivity, cost avoidance, etc.)",
                    )

                    days_saved_per_site = max(manual_days - auto_days, 0.0)
                    suggested_value = (
                        days_saved_per_site * value_per_site_day * sites_per_year
                    )

                    _ben.info(
                        f"Suggested annual value from waiting-time reduction: "
                        f"≈ ${suggested_value:,.0f} "
                        f"({days_saved_per_site:.1f} days saved/site × "
                        f"${value_per_site_day:,.0f}/day × "
                        f"{sites_per_year:.0f} sites/year)"
                    )

                    typical_str = (
                        f"Manual duration {manual_days:.1f} days, "
                        f"automated duration {auto_days:.1f} days, "
                        f"{days_saved_per_site:.1f} days saved per site; "
                        f"{sites_per_year:.0f} sites/year; "
                        f"business value ≈ ${value_per_site_day:,.0f} per site per day."
                    )

                annual_value_default = (
                    float(suggested_value) if suggested_value is not None else 0.0
                )

                annual_value = _ben.number_input(
                    f"{label} – Annual value (USD/year)",
                    min_value=0.0,
                    value=annual_value_default,
                    step=5000.0,
                    key=f"{key}_value",
                    help="You can override the suggested value if needed.",
                )

                methodology = _ben.text_area(
                    f"{label} – Methodology (how you calculated it)",
                    key=f"{key}_method",
                    help=(
                        "Example: 'Assume VLAN rollout at 12 sites/year; manual 5 days vs automation 1 day, "
                        "4 days saved × $1,000/day × 12 sites/year'."
                    ),
                )

                if label in ("Revenue Acceleration", "Deployment Speed"):
                    typical = typical_str
                else:
                    typical = _ben.text_area(
                        f"{label} – Typical values / assumptions",
                        key=f"{key}_typical",
                        help="Key assumptions or typical values you used so finance can sanity-check.",
                    )

                benefit_inputs.append(
                    {
                        "category": label,
                        "name": name,
                        "annual_value": annual_value,
                        "methodology": methodology,
                        "typical": typical,
                    }
                )

        # Benefits summary just like Cost summary
        utils.thick_hr(color="green", thickness=5)
        st.markdown("**➕ Benefits summary (USD)**")
        if benefit_inputs:
            for b in benefit_inputs:
                cat = b.get("category", "Benefit")
                nm = b.get("name", cat)
                amt = float(b.get("annual_value", 0.0))
                st.write(f"- {nm} ({cat}): ${amt:,.0f}/year")
            total_addl = sum(float(b.get("annual_value", 0.0)) for b in benefit_inputs)
            st.info(f"Total of additional benefits: ${total_addl:,.0f}/year")
            st.caption("Sign convention: benefits are positive (+ returns).")
        else:
            st.caption("No additional benefits selected.")
        utils.thick_hr(color="green", thickness=5)
        # Intangible/Soft Benefits (Optional) — moved to last in sidebar
        # st.markdown("---")
        _soft = st.expander("Intangible / Soft Benefits (Optional)", expanded=False)
        with _soft:
            st.subheader("Intangible / Soft Benefits (Optional)")
        try:
            with open("soft_benefits.json", "r", encoding="utf-8") as f:
                soft_data = json.load(f)
            categories = soft_data.get("categories", [])
            for idx, cat in enumerate(categories):
                checked = _soft.checkbox(
                    cat.get("name", f"Category {idx+1}"), key=f"soft_ben_{idx}"
                )
                if checked:
                    soft_benefits_selected.append(
                        {
                            "name": cat.get("name", ""),
                            "details": cat.get("details", []),
                        }
                    )
        except Exception as e:
            st.info(f"Soft benefits file not loaded: {e}")

    # -------- Main inputs: manual vs automated time --------
    st.subheader("Manual vs Automated Time per Change (in minutes)")
    cols_img = st.columns([1, 3, 1])
    with cols_img[1]:
        st.image("images/AnatomyOfNetChange.png", use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Manual today**")

        manual_obtain_details = st.number_input(
            "1. Obtain change details – manual (minutes/change)",
            min_value=0,
            value=10,
            step=1,
            help="Change intent and devices impacted.",
        )
        manual_develop_payload = st.number_input(
            "2. Develop command payload – manual (minutes/change)",
            min_value=0,
            value=15,
            step=1,
        )
        manual_quantify_impact = st.number_input(
            "3. Quantify impact – manual (minutes/change)",
            min_value=0,
            value=10,
            step=1,
        )
        manual_change_mgmt = st.number_input(
            "4. Change management, scheduling, notification – manual (minutes/change)",
            min_value=0,
            value=15,
            step=1,
        )
        manual_state_analysis = st.number_input(
            "5. Current state analysis & verification – manual (minutes/change)",
            min_value=0,
            value=15,
            step=1,
        )
        manual_execute = st.number_input(
            "6. Execute change – manual (minutes/change)",
            min_value=0,
            value=10,
            step=1,
        )
        manual_test_qa = st.number_input(
            "7. Test & verification QA – manual (minutes/change)",
            min_value=0,
            value=15,
            step=1,
        )
        manual_document = st.number_input(
            "8. Documentation, notification, close out – manual (minutes/change)",
            min_value=0,
            value=10,
            step=1,
        )

    with col2:
        st.markdown("**After automation**")

        auto_obtain_details = st.number_input(
            "1. Obtain change details – automated (minutes/change)",
            min_value=0,
            value=5,
            step=1,
            help="Time to capture intent / inputs into automation.",
        )
        auto_develop_payload = st.number_input(
            "2. Develop command payload – automated (minutes/change)",
            min_value=0,
            value=5,
            step=1,
        )
        auto_quantify_impact = st.number_input(
            "3. Quantify impact – automated (minutes/change)",
            min_value=0,
            value=5,
            step=1,
        )
        auto_change_mgmt = st.number_input(
            "4. Change management, scheduling, notification – automated (minutes/change)",
            min_value=0,
            value=5,
            step=1,
        )
        auto_state_analysis = st.number_input(
            "5. Current state analysis & verification – automated (minutes/change)",
            min_value=0,
            value=5,
            step=1,
        )
        auto_execute = st.number_input(
            "6. Execute change – automated (minutes/change)",
            min_value=0,
            value=5,
            step=1,
        )
        auto_test_qa = st.number_input(
            "7. Test & verification QA – automated (minutes/change)",
            min_value=0,
            value=5,
            step=1,
        )
        auto_document = st.number_input(
            "8. Documentation, notification, close out – automated (minutes/change)",
            min_value=0,
            value=5,
            step=1,
        )

    # Show live totals just above the Calculate button
    manual_total_preview = (
        manual_obtain_details
        + manual_develop_payload
        + manual_quantify_impact
        + manual_change_mgmt
        + manual_state_analysis
        + manual_execute
        + manual_test_qa
        + manual_document
    )

    auto_total_preview = (
        auto_obtain_details
        + auto_develop_payload
        + auto_quantify_impact
        + auto_change_mgmt
        + auto_state_analysis
        + auto_execute
        + auto_test_qa
        + auto_document
    )

    tcol1, tcol2 = st.columns(2)
    with tcol1:
        st.metric(
            label="Total manual minutes per change", value=f"{manual_total_preview}"
        )
    with tcol2:
        st.metric(
            label="Total automated minutes per change", value=f"{auto_total_preview}"
        )

    if st.button("Calculate Business Case"):
        # --- Time & operational savings ---

        manual_total_minutes = (
            manual_obtain_details
            + manual_develop_payload
            + manual_quantify_impact
            + manual_change_mgmt
            + manual_state_analysis
            + manual_execute
            + manual_test_qa
            + manual_document
        )

        auto_total_minutes = (
            auto_obtain_details
            + auto_develop_payload
            + auto_quantify_impact
            + auto_change_mgmt
            + auto_state_analysis
            + auto_execute
            + auto_test_qa
            + auto_document
        )

        minutes_saved_per_change = manual_total_minutes - auto_total_minutes
        hours_saved_per_change = minutes_saved_per_change / 60.0

        automation_coverage = automation_coverage_pct / 100.0
        effective_changes_per_year = tasks_per_year * automation_coverage
        annual_hours_saved = hours_saved_per_change * effective_changes_per_year

        annual_cost_savings = annual_hours_saved * hourly_rate  # engineer-time savings

        # --- Additional benefits (sum only checked ones) ---

        annual_additional_benefits = sum(
            b.get("annual_value", 0.0) for b in benefit_inputs
        )

        # Total annual benefit (time + additional)
        annual_total_benefit = annual_cost_savings + annual_additional_benefits

        # Net after run cost
        # Adjust costs with technical debt if included
        project_cost += tech_debt_remediation_one_time + csat_debt_remediation_one_time
        annual_run_cost_effective = (
            annual_run_cost + tech_debt_annual_after + csat_debt_annual_after
        )
        annual_net_benefit = annual_total_benefit - annual_run_cost_effective

        discount_rate = discount_rate_pct / 100.0

        # Cash flows: Year 0..5
        years_list = years
        year0_cf = -project_cost
        cash_flows = [year0_cf]
        for _ in range(years_list):
            cash_flows.append(annual_net_benefit)

        npv = utils.compute_npv(discount_rate, cash_flows)
        payback = compute_payback_period(cash_flows)
        irr = compute_irr(cash_flows)

        def cumulative_up_to_year(n: int) -> float:
            return sum(cash_flows[: n + 1])

        cum_1 = cumulative_up_to_year(1)
        cum_3 = cumulative_up_to_year(3)
        cum_5 = cumulative_up_to_year(5)

        # --- Build NABCD(E) summary ---

        nabcde_summary = build_nabcde_summary(
            years=years_list,
            automation_title=automation_title,
            automation_description=automation_description,
            tasks_per_year=tasks_per_year,
            automation_coverage_pct=automation_coverage_pct,
            manual_total_minutes=manual_total_minutes,
            annual_hours_saved=annual_hours_saved,
            annual_total_benefit=annual_total_benefit,
            project_cost=project_cost,
            annual_run_cost=annual_run_cost_effective,
            npv=npv,
            payback=payback,
            irr=irr,
            acquisition_strategy=acquisition_strategy,
        )

        # --- Display results ---

        st.markdown("---")
        st.subheader("Business Case Summary (USD)")

        mcol1, mcol2 = st.columns(2)

        with mcol1:
            st.write(
                f"**Initiative title:** {automation_title or 'Network Automation Initiative'}"
            )
            if automation_description.strip():
                st.write(f"**Description:** {automation_description}")
            st.write(f"**Switches per location (avg):** {switches_per_location:,.1f}")
            st.write(f"**Locations impacted:** {num_locations:,.0f}")
            st.write(f"**Estimated total switches/devices:** {total_switches:,.0f}")
            st.write(f"**Changes per year:** {tasks_per_year:,.0f} changes/year")
            st.write(
                f"**Automation coverage:** {automation_coverage_pct:.1f}% of changes/year"
            )
            st.write(f"**Engineer hourly cost:** ${hourly_rate:,.2f} USD/hour")
            st.write(
                f"**Manual time per change:** {manual_total_minutes:.1f} minutes/change"
            )
            st.write(
                f"**Automated time per change:** {auto_total_minutes:.1f} minutes/change"
            )
            st.write(
                f"**Time saved per change:** {minutes_saved_per_change:.1f} minutes/change"
            )

            st.write(f"**Annual hours saved:** {annual_hours_saved:,.1f} hours/year")

        with mcol2:
            st.write("**Annual benefit breakdown:**")
            st.write(
                f"- Operational efficiency (time): ${annual_cost_savings:,.2f} USD/year"
            )
            st.write(
                f"- Additional benefits (sum of checked items): ${annual_additional_benefits:,.2f} USD/year"
            )
            if benefit_inputs:
                st.write("  - Included benefit categories:")
                cats = sorted({b["category"] for b in benefit_inputs})
                for c in cats:
                    st.write(f"    • {c}")
            st.write(
                f"**➕ Total annual benefit:** ${annual_total_benefit:,.2f} USD/year"
            )
            st.write(f"**Annual run cost:** ${annual_run_cost_effective:,.2f} USD/year")
            st.write(f"**Annual net benefit:** ${annual_net_benefit:,.2f} USD/year")
            st.write(f"**Initial project cost (Year 0):** ${project_cost:,.2f} USD")
            st.write(f"**Discount rate:** {discount_rate_pct:.1f}%")
            st.caption(
                "Sign convention: benefits are positive (+ returns); costs are investments and modeled as negative cash flows."
            )

        # Cost modeling breakdown display
        st.subheader("Cost Modeling (Selected strategy)")
        st.write(f"**Acquisition strategy:** {acquisition_strategy}")
        cb_rows = []
        for item in cost_breakdown:
            cb_rows.append(
                {
                    "Cost item": item.get("name", ""),
                    "Timing": item.get("timing", ""),
                    "Amount (USD)": f"${item.get('amount', 0.0):,.2f}",
                }
            )
        st.table(cb_rows)
        st.write(f"**One-time project cost (Year 0):** ${project_cost:,.2f} USD")
        st.write(f"**Annual run cost:** ${annual_run_cost_effective:,.2f} USD/year")
        st.write(
            f"**First-year total cost:** ${project_cost + annual_run_cost_effective:,.2f} USD"
        )

        st.subheader("Cash Flows (Year 0–5)")

        cash_rows = []
        for t, cf in enumerate(cash_flows):
            cash_rows.append({"Year": t, "Cash Flow (USD)": f"{cf:,.2f}"})
        st.table(cash_rows)

        st.subheader("Key Financial Metrics")

        payback_text = (
            f"{payback:.2f} years"
            if payback is not None
            else "Not reached within model horizon (beyond model years)"
        )
        irr_text = (
            f"{irr*100:.2f}%"
            if irr is not None and irr > -1
            else "Not meaningful / not found"
        )

        metrics_rows = [
            {
                "Metric": "Discount rate (hurdle rate)",
                "Value": f"{discount_rate_pct:.1f}%",
                "Definition": "Your required annual return used to discount future cash; reflects cost of capital and risk.",
                "Tip": "Use the same rate across projects; higher rate = stricter bar.",
            },
            {
                "Metric": f"Net Present Value (NPV, {years_list} years)",
                "Value": f"${npv:,.2f}",
                "Definition": "Today's value of all project cash flows using the discount rate; > $0 means the project adds value.",
                "Tip": "> $0 adds value; compare NPV across projects of similar size.",
            },
            {
                "Metric": "Payback period (undiscounted)",
                "Value": payback_text,
                "Definition": "Years until cumulative cash turns positive (ignores time-value-of-money). Shorter is better.",
                "Tip": "Quick storytelling metric; common targets are ≤ 2–3 years.",
            },
            {
                "Metric": "Internal Rate of Return (IRR)",
                "Value": irr_text,
                "Definition": "Return rate where NPV = $0. If IRR is above your discount rate, the project is attractive.",
                "Tip": "Bigger spread above the discount rate = better.",
            },
        ]

        st.table(metrics_rows)

        # Friendly explanations for non-finance readers
        with st.expander("What these metrics mean (with examples)"):
            st.markdown(
                """
                #### Discount rate (hurdle rate)
                - **What it is:** The minimum annual return your org expects for projects. Used to convert future dollars into today's dollars.
                - **Typical range:** 8%–15% in many enterprises. Higher if riskier.
                - **Good example:** Setting a realistic rate (e.g., 10%) that matches finance guidance. Ensures apples-to-apples across projects.
                - **Red flag:** Using 0% (or very low) makes every project look better than it actually is.

                #### Net Present Value (NPV)
                - **What it is:** The value today of all cash you expect from the project after subtracting the upfront cost, using the discount rate.
                - **Rule of thumb:** If NPV > $0, the project creates value; higher is better when comparing similar-sized projects.
                - **Good example:** NPV = +$250,000 over {years_list} years at {discount_rate_pct:.1f}%. Indicates strong value creation.
                - **Red flag:** NPV close to $0 or negative suggests benefits/run-costs are too low/high, or the project is too risky/slow.

                #### Payback period (undiscounted)
                - **What it is:** How many years until the project has paid back the initial investment (ignores time value of money).
                - **Rule of thumb:** Shorter is better. Many teams target ≤ 2–3 years, but it depends on strategy and budget.
                - **Good example:** Payback in 1.8 years—easy to explain and fits typical budget cycles.
                - **Red flag:** Payback beyond the modeled period (e.g., > {years_list} years) means it never turns positive in this horizon.

                #### Internal Rate of Return (IRR)
                - **What it is:** The return rate where NPV becomes $0. Compare IRR to your discount rate.
                - **Rule of thumb:** IRR above the discount rate is attractive. The higher the spread, the better.
                - **Good example:** IRR = 24% with a 10% discount rate → strong case (spread = 14%).
                - **Red flag:** IRR not meaningful (no sign change in cash flows) or below the discount rate.

                ---
                #### Tips and sanity checks
                - **Sensitivity:**
                  - Raising the discount rate lowers NPV and can reduce IRR.
                  - Lowering annual benefits or increasing run costs worsens NPV/IRR and lengthens payback.
                - **Apples-to-apples:** Use the same discount rate across projects when comparing options.
                - **Narrative:** Pair these numbers with operational outcomes: fewer outages, consistent changes, faster delivery.
                """
            )

        st.subheader("Cumulative Cash Flow Checkpoints")
        st.write(f"**After 1 year:** ${cum_1:,.2f} USD")
        st.write(f"**After 3 years:** ${cum_3:,.2f} USD")
        st.write(f"**After 5 years:** ${cum_5:,.2f} USD")
        caption_lines = [
            "Positive values mean you've recovered the initial investment and created headroom. In practice this can also mean:",
            "- Deferring/avoiding incremental hiring for repetitive changes",
        ]
        if include_csat_debt and csat_debt_annual_after > 0:
            caption_lines.append(
                "- Improved customer satisfaction (included in this model)"
            )
        if include_tech_debt and tech_debt_annual_after > 0:
            if tech_reduction_pct is not None:
                caption_lines.append(
                    f"- Reduced technical debt (remediated by {tech_reduction_pct:.0f}%)"
                )
            else:
                caption_lines.append("- Reduced technical debt")
        caption_lines.extend(
            [
                "- Reduced delays on adjacent initiatives from freed capacity",
                "- Increased team morale and engagement",
                "- Reduced skills gaps as staff gain time to learn and cross-train",
            ]
        )
        st.caption("\n".join(caption_lines))

        # Intangible / Soft Benefits (UI output) — moved below Cumulative section
        if soft_benefits_selected:
            st.subheader("Intangible / Soft Benefits")
            for sb in soft_benefits_selected:
                st.markdown(f"**{sb.get('name','')}**")
                for d in sb.get("details", []):
                    st.markdown(f"- {d}")

        # --- Assumption sanity-check panel ---

        st.markdown("---")
        st.subheader("Assumption Sanity-Check (per switch, per site, per change)")

        hours_per_switch_per_year = (
            annual_hours_saved / total_switches if total_switches > 0 else None
        )
        hours_per_site_per_year = (
            annual_hours_saved / num_locations if num_locations > 0 else None
        )
        benefit_per_switch_per_year = (
            annual_total_benefit / total_switches if total_switches > 0 else None
        )
        benefit_per_site_per_year = (
            annual_total_benefit / num_locations if num_locations > 0 else None
        )
        benefit_per_change = (
            annual_total_benefit / tasks_per_year if tasks_per_year > 0 else None
        )

        sanity_rows = []

        sanity_rows.append(
            {
                "Metric": "Hours saved per change",
                "Value": f"{hours_saved_per_change:.2f} hours/change",
            }
        )
        sanity_rows.append(
            {
                "Metric": "Hours saved per year (total)",
                "Value": f"{annual_hours_saved:,.2f} hours/year",
            }
        )
        if hours_per_switch_per_year is not None:
            sanity_rows.append(
                {
                    "Metric": "Hours saved per switch per year",
                    "Value": f"{hours_per_switch_per_year:.3f} hours/switch/year",
                }
            )
        if hours_per_site_per_year is not None:
            sanity_rows.append(
                {
                    "Metric": "Hours saved per site per year",
                    "Value": f"{hours_per_site_per_year:.3f} hours/site/year",
                }
            )
        if benefit_per_switch_per_year is not None:
            sanity_rows.append(
                {
                    "Metric": "Total benefit per switch per year",
                    "Value": f"${benefit_per_switch_per_year:,.2f} USD/switch/year",
                }
            )
        if benefit_per_site_per_year is not None:
            sanity_rows.append(
                {
                    "Metric": "Total benefit per site per year",
                    "Value": f"${benefit_per_site_per_year:,.2f} USD/site/year",
                }
            )
        if benefit_per_change is not None:
            sanity_rows.append(
                {
                    "Metric": "Total benefit per change",
                    "Value": f"${benefit_per_change:,.2f} USD/change",
                }
            )

        st.table(sanity_rows)
        st.caption(
            "Gut-check these numbers to see if they feel realistic before sharing with CXOs or finance."
        )

        # --- NABCD(E) Summary section ---

        st.markdown("---")
        st.subheader("NABCD(E) Summary (Copy-Paste Ready)")
        st.markdown(nabcde_summary)
        st.code(nabcde_summary, language="markdown")

        # --- Markdown report download ---

        markdown_report = build_markdown_report(
            years=years_list,
            automation_title=automation_title,
            automation_description=automation_description,
            solution_details_md=solution_details_md,
            out_of_scope=out_of_scope,
            switches_per_location=switches_per_location,
            num_locations=num_locations,
            total_switches=total_switches,
            tasks_per_year=tasks_per_year,
            automation_coverage_pct=automation_coverage_pct,
            hourly_rate=hourly_rate,
            manual_total_minutes=manual_total_minutes,
            auto_total_minutes=auto_total_minutes,
            minutes_saved_per_change=minutes_saved_per_change,
            annual_hours_saved=annual_hours_saved,
            annual_cost_savings=annual_cost_savings,
            benefits=benefit_inputs,
            annual_additional_benefits=annual_additional_benefits,
            annual_total_benefit=annual_total_benefit,
            annual_run_cost=annual_run_cost,
            annual_net_benefit=annual_net_benefit,
            project_cost=project_cost,
            discount_rate_pct=discount_rate_pct,
            cash_flows=cash_flows,
            npv=npv,
            payback=payback,
            irr=irr,
            cum_1=cum_1,
            cum_3=cum_3,
            cum_5=cum_5,
            nabcde_summary=nabcde_summary,
            acquisition_strategy=acquisition_strategy,
            cost_breakdown=cost_breakdown,
            tech_debt_included=bool(
                include_tech_debt
                and (tech_debt_annual_after > 0 or tech_debt_remediation_one_time > 0)
            ),
            tech_debt_reduction_pct=tech_reduction_pct,
            tech_debt_base_annual=tech_debt_base_annual,
            tech_debt_impact_pct=tech_debt_impact_pct,
            tech_debt_residual_pct=tech_debt_residual_pct,
            csat_debt_included=bool(
                include_csat_debt
                and (csat_debt_annual_after > 0 or csat_debt_remediation_one_time > 0)
            ),
            csat_debt_base_annual=csat_debt_base_annual,
            csat_debt_impact_pct=csat_debt_impact_pct,
            csat_debt_residual_pct=csat_debt_residual_pct,
        )

        st.markdown("---")
        st.subheader("⬇️ Downloads")
        st.markdown("**📄 Download Markdown Report Only**")

        # Slug is derived from acquisition strategy only (no user input)
        _is_buy = (acquisition_strategy or "").lower().startswith("buy")
        slug = "Buy" if _is_buy else "Build"

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="📄 Download business case as Markdown",
            data=markdown_report,
            file_name=f"BusinessCaseReport_{slug}_{ts}.md",
            mime="text/markdown",
        )

        # --- SaveScenarios (JSON) ---
        st.markdown("***OR***")
        st.markdown("📦 Download Markdown Report and Scenario JSON")

        # Removed comparison tabs; keeping report & scenario actions only

        # Helper to assemble current scenario JSON
        def build_scenario_payload() -> Dict[str, Any]:
            return {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "version": "1.0",
                # Inputs
                "years": years_list,
                "automation_title": automation_title,
                "automation_description": automation_description,
                "solution_details_md": solution_details_md,
                "out_of_scope": out_of_scope,
                "switches_per_location": switches_per_location,
                "num_locations": num_locations,
                "total_switches": total_switches,
                "tasks_per_year": tasks_per_year,
                "automation_coverage_pct": automation_coverage_pct,
                "hourly_rate": hourly_rate,
                "manual_total_minutes": manual_total_minutes,
                "auto_total_minutes": auto_total_minutes,
                "minutes_saved_per_change": minutes_saved_per_change,
                "acquisition_strategy": acquisition_strategy,
                "cost_breakdown": cost_breakdown,
                # Intangible / Soft Benefits selections
                "soft_benefits": soft_benefits_selected,
                # Debts
                "include_tech_debt": bool(include_tech_debt),
                "tech_debt_base_annual": tech_debt_base_annual,
                "tech_debt_impact_pct": tech_debt_impact_pct,
                "tech_debt_residual_pct": tech_debt_residual_pct,
                "tech_debt_annual_after": tech_debt_annual_after,
                "tech_debt_remediation_one_time": tech_debt_remediation_one_time,
                "include_csat_debt": bool(include_csat_debt),
                "csat_debt_base_annual": csat_debt_base_annual,
                "csat_debt_impact_pct": csat_debt_impact_pct,
                "csat_debt_residual_pct": csat_debt_residual_pct,
                "csat_debt_annual_after": csat_debt_annual_after,
                "csat_debt_remediation_one_time": csat_debt_remediation_one_time,
                # Benefits
                "benefits": benefit_inputs,
                "annual_additional_benefits": annual_additional_benefits,
                # Outputs
                "annual_hours_saved": annual_hours_saved,
                "annual_cost_savings": annual_cost_savings,
                "annual_total_benefit": annual_total_benefit,
                "annual_run_cost_effective": annual_run_cost_effective,
                "annual_net_benefit": annual_net_benefit,
                "project_cost": project_cost,
                "discount_rate_pct": discount_rate_pct,
                "cash_flows": cash_flows,
                "npv": npv,
                "payback": payback,
                "irr": irr,
                "cum_1": cum_1,
                "cum_3": cum_3,
                "cum_5": cum_5,
            }

        scenario_json_str = json.dumps(build_scenario_payload(), indent=2)

        # Combined ZIP (Markdown + JSON) single button with shared timestamp
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"BusinessCaseReport_{slug}_{ts}.md", markdown_report)
            zf.writestr(f"BusinessCaseScenario_{slug}_{ts}.json", scenario_json_str)
        zip_bytes = zip_buffer.getvalue()
        st.download_button(
            label="📄 Download report + 🗂️ JSON scenario (ZIP)",
            data=zip_bytes,
            file_name=f"BusinessCaseArtifacts_{slug}_{ts}.zip",
            mime="application/zip",
        )

        # Inform user where files are saved and list filenames
        md_name = f"BusinessCaseReport_{slug}_{ts}.md"
        zip_name = f"BusinessCaseArtifacts_{slug}_{ts}.zip"
        zip_md_name = f"BusinessCaseReport_{slug}_{ts}.md"
        zip_json_name = f"BusinessCaseScenario_{slug}_{ts}.json"
        st.info(
            "Downloads are saved by your browser to its default download folder (e.g., 'Downloads').\n\n"
            f"Files created now:\n"
            f"- {md_name}\n"
            f"- {zip_name} (contains {zip_md_name} and {zip_json_name})"
        )

        show_preview = False
        if show_preview:
            # Show a preview (truncated if long)
            preview = markdown_report[:1500]
            if len(markdown_report) > 1500:
                preview += "\n...\n"
            st.code(preview, language="markdown")


# Standard call to the main() function.
if __name__ == "__main__":
    main()
