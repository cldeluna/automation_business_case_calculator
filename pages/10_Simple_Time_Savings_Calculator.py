#!/usr/bin/python3 -tt
"""
Simple Time Savings Calculator

Purpose
- Quick, lightweight estimator for annual hours and cost savings from automating an interaction workflow.

Key features
- Inputs in sidebar: interactions/month, automation coverage %, hourly rate, implement hours (one-time), maintain hours/year.
- Detailed per-step minutes (manual vs automated) in a collapsed expander; totals appear above.
- Results table (minutes saved/interaction, volumes, hours and cost savings, one-year project cost, quick ROI).
- Summary Narrative (plain text) with scenario-specific values.
- Save results as JSON with filename format: "SimpleROI_<shortTitle>_<YYYYMMDD_HHM MZ>.json".
- Load a saved SimpleROI_*.json from the sidebar to restore a scenario for this session.

Notes
- “Interaction” wording is used consistently (not “change”).
- Quick ROI is a simple one-year estimate: ROI = (Benefit − Cost) / Cost × 100%,
  where Benefit = annual cost savings, Cost = (implement hours + maintain hours) × hourly rate.
- Results and narrative are hidden until you change at least one default input.
"""
# Project: automation_business_case_calculator
# Filename: 10_Simple_Time_Savings_Calculator.py
# Minimal stub page to estimate simple time savings

import streamlit as st
import utils
import json
from datetime import datetime


def main():

    st.set_page_config(
        page_title="Simple Time Savings Calculator/Estimator",
        page_icon="images/EIA_Favicon.png",
        layout="wide",
    )

    # Sidebar logo (left nav pane)
    try:
        st.sidebar.image("images/EIA Logo FINAL small_Round.png", width=75)
    except Exception:
        pass

    # Colors
    hr_color_dict = utils.hr_colors()

    # Header
    st.title("Simple Time Savings Calculator")
    st.caption("Quickly estimate annual hours and cost savings from automating a task.")

    # One-time success notice after applying uploaded JSON (post-rerun)
    if st.session_state.get("simple_upload_applied", False):
        st.success(
            "Loaded values from JSON into this session. Scroll to review, update, and save if needed."
        )
        del st.session_state["simple_upload_applied"]

    with st.expander("About", expanded=True):
        st.markdown(
            """
            This lightweight calculator helps you estimate time and cost savings:
            - Enter manual vs automated minutes per interaction.
            - Specify how many interactions happen per month and the automation coverage.
            - Provide engineer fully-loaded cost per hour.
            
            An interaction can be a change, submission, calculation, analysis, troubleshooting, or other task that requires network device interaction and execution (logging in, determing state, executing commands, verifying results, etc.).
            
            Note: This simple calculator uses a fixed one-year horizon for costs and ROI calculations.
            """
        )

    # Load saved Simple ROI JSON (applies to current session) BEFORE instantiating widgets
    with st.sidebar.expander("Load Saved Simple ROI", expanded=False):
        uploaded = st.file_uploader(
            "Upload SimpleROI_*.json", type=["json"], key="simple_upload_json"
        )
        processed_name = st.session_state.get("simple_upload_processed_name")
        if uploaded is not None:
            # Validate filename pattern first
            if not uploaded.name.startswith("SimpleROI_"):
                st.error(
                    "Invalid file. Please upload a file that starts with 'SimpleROI_' and is a JSON export from this tool."
                )
                st.caption(
                    "Tip: Use the 'Save results as JSON' button in this page to generate a compatible file."
                )
            else:
                already_loaded = processed_name == uploaded.name
                load_btn = st.button(
                    "Load uploaded JSON",
                    type="primary",
                    disabled=already_loaded,
                    key="simple_apply_upload_btn",
                    help=(
                        "This file is already loaded."
                        if already_loaded
                        else "Apply the uploaded values to this session."
                    ),
                )
                if load_btn and not already_loaded:
                    try:
                        data = json.load(uploaded)
                        proj = data.get("project", {})
                        assump = data.get("assumptions", {})
                        tpi = data.get("timePerInteraction", {})

                        # Title/description
                        if proj.get("title"):
                            st.session_state["simple_project_title"] = proj.get(
                                "title", ""
                            )
                        if proj.get("description"):
                            st.session_state["simple_project_desc"] = proj.get(
                                "description", ""
                            )

                        # Assumptions
                        if "interactionsPerMonth" in assump:
                            st.session_state["sts_ipm"] = (
                                float(assump["interactionsPerMonth"]) or 0.0
                            )
                        if "automationCoveragePct" in assump:
                            st.session_state["sts_cov"] = (
                                float(assump["automationCoveragePct"]) or 0.0
                            )
                        if "hourlyRate" in assump:
                            st.session_state["sts_rate"] = (
                                float(assump["hourlyRate"]) or 0.0
                            )
                        if "implementHoursOneTime" in assump:
                            st.session_state["sts_impl_hours"] = (
                                float(assump["implementHoursOneTime"]) or 0.0
                            )
                        if "maintainHoursPerYear" in assump:
                            st.session_state["sts_maint_hours"] = (
                                float(assump["maintainHoursPerYear"]) or 0.0
                            )

                        # Time per interaction steps
                        m_steps = tpi.get("manualStepsMinutes", []) or []
                        a_steps = tpi.get("automatedStepsMinutes", []) or []
                        for i, val in enumerate(m_steps, start=1):
                            st.session_state[f"simple_time_m{i}"] = int(val)
                        for i, val in enumerate(a_steps, start=1):
                            st.session_state[f"simple_time_a{i}"] = int(val)

                        # Mark applied and rerun so widgets pick up values without mutation errors
                        st.session_state["simple_upload_processed_name"] = uploaded.name
                        st.session_state["simple_upload_applied"] = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to load JSON: {e}")

    # Assumptions (moved to sidebar)
    with st.sidebar.expander("Volume & Cost Assumptions", expanded=True):
        interactions_per_month = st.number_input(
            "Interactions per month",
            min_value=0.0,
            value=100.0,
            step=10.0,
            key="sts_ipm",
        )
        automation_coverage_pct = st.number_input(
            "Automation coverage (%)",
            min_value=0.0,
            max_value=100.0,
            value=80.0,
            step=5.0,
            key="sts_cov",
        )
        hourly_rate = st.number_input(
            "Engineer fully-loaded cost (USD/hour)",
            min_value=0.0,
            value=100.0,
            step=5.0,
            key="sts_rate",
        )
        implement_hours = st.number_input(
            "Number of hours to implement (one-time)",
            min_value=0.0,
            value=40.0,
            step=1.0,
            key="sts_impl_hours",
        )
        maintain_hours_per_year = st.number_input(
            "Number of hours to maintain per year",
            min_value=0.0,
            value=2.0,
            step=1.0,
            key="sts_maint_hours",
        )
        # ROI window fixed to one year for this simple calculator

    # Compute totals from session state (initialize sensible defaults on first load)
    defaults_manual = [10, 15, 10, 15, 15, 10, 15, 10]
    defaults_auto = [5, 5, 5, 5, 5, 5, 5, 5]
    m_vals, a_vals = [], []
    for i, dv in enumerate(defaults_manual, start=1):
        key = f"simple_time_m{i}"
        if key not in st.session_state:
            st.session_state[key] = dv
        m_vals.append(st.session_state.get(key, dv))
    for i, dv in enumerate(defaults_auto, start=1):
        key = f"simple_time_a{i}"
        if key not in st.session_state:
            st.session_state[key] = dv
        a_vals.append(st.session_state.get(key, dv))

    manual_total = float(sum(m_vals))
    auto_total = float(sum(a_vals))
    minutes_saved = max(0.0, manual_total - auto_total)
    tasks_per_year = interactions_per_month * 12.0
    effective_changes = tasks_per_year * (automation_coverage_pct / 100.0)
    annual_hours_saved = (minutes_saved / 60.0) * effective_changes
    annual_cost_savings = annual_hours_saved * hourly_rate
    project_cost_year1 = (implement_hours + maintain_hours_per_year) * hourly_rate
    project_cost_over_window = (
        implement_hours + maintain_hours_per_year * 1
    ) * hourly_rate
    benefit_over_window = annual_cost_savings * 1
    quick_roi_pct = None
    if project_cost_over_window > 0:
        quick_roi_pct = (
            (benefit_over_window - project_cost_over_window) / project_cost_over_window
        ) * 100.0

    # Title and short description above minutes values
    utils.thick_hr(color=hr_color_dict["eia_blue"], thickness=5)
    project_title = st.text_input(
        "Project title",
        value="My new network automation project",
        key="simple_project_title",
    )
    project_desc = st.text_area(
        "Short description",
        value="Here is a short description of my my new network automation project",
        key="simple_project_desc",
        height=80,
    )

    # Determine if all values are still defaults (hide results if so)
    default_title = "My new network automation project"
    default_desc = "Here is a short description of my my new network automation project"
    is_default_times = (m_vals == defaults_manual) and (a_vals == defaults_auto)
    is_default_assumptions = (
        interactions_per_month == 100.0
        and automation_coverage_pct == 80.0
        and hourly_rate == 100.0
        and implement_hours == 40.0
        and maintain_hours_per_year == 2.0
    )
    is_default_text = (project_title == default_title) and (
        project_desc == default_desc
    )
    is_default = is_default_times and is_default_assumptions and is_default_text

    # Show totals (reflecting values from the collapsed section via session_state)
    mcol1, mcol2 = st.columns(2)
    with mcol1:
        st.metric(
            label="Total manual minutes per interaction", value=f"{int(manual_total)}"
        )
    with mcol2:
        st.metric(
            label="Total automated minutes per interaction", value=f"{int(auto_total)}"
        )

    # Manual vs Automated section in a collapsed expander directly under the totals
    with st.expander(
        "Manual vs Automated Time per Change (in minutes)", expanded=False
    ):
        utils.render_time_inputs(
            base_key="simple_time", image_file="images/AnatomyOfNetInteraction.png"
        )

    if not is_default:
        utils.thick_hr(color=hr_color_dict["eia_blue"], thickness=5)
        st.markdown("## Results")
        results_rows = [
            {"Metric": "Minutes saved/interaction", "Value": f"{minutes_saved:.1f}"},
            {"Metric": "Interactions/year", "Value": f"{tasks_per_year:,.0f}"},
            {
                "Metric": "Effective automated interactions/year",
                "Value": f"{effective_changes:,.0f}",
            },
            {"Metric": "Annual hours saved", "Value": f"{annual_hours_saved:,.1f}"},
            {"Metric": "Annual cost savings", "Value": f"${annual_cost_savings:,.2f}"},
            {
                "Metric": "Implementation hours (one-time)",
                "Value": f"{implement_hours:,.1f}",
            },
            {
                "Metric": "Maintenance hours/year",
                "Value": f"{maintain_hours_per_year:,.1f}",
            },
            {
                "Metric": "Project cost (one year)",
                "Value": f"${project_cost_over_window:,.2f}",
            },
            {
                "Metric": "Quick ROI (one year)",
                "Value": (
                    f"{quick_roi_pct:.1f}%" if quick_roi_pct is not None else "N/A"
                ),
            },
        ]
        st.dataframe(results_rows, hide_index=True, use_container_width=True)
        st.caption(
            "Quick ROI formula (one year): ROI = (Benefit − Cost) / Cost × 100%. Benefit = annual cost savings. Cost = (implement hours + maintain hours) × hourly rate."
        )

        # Summary Narrative section under Results
        utils.thick_hr(color=hr_color_dict["eia_blue"], thickness=5)
        st.markdown("### Summary Narrative")
        minutes_saved_r = int(round(minutes_saved))
        interactions_year_r = int(round(tasks_per_year))
        automated_year_r = int(round(effective_changes))
        automation_rate_r = int(round(automation_coverage_pct))
        hours_saved_r = int(round(annual_hours_saved))
        cost_savings_r = int(round(annual_cost_savings))
        narrative_text = (
            f"{project_title}\n\n"
            f"{project_desc}\n\n"
            f"This specific automation delivers clear, measurable benefits by saving {minutes_saved_r:,} minutes per interaction across {interactions_year_r:,} annual interactions, with {automated_year_r:,} of these now automated—reflecting the {automation_rate_r}% automation rate provided ({automated_year_r:,} ÷ {interactions_year_r:,}). The result is {hours_saved_r:,} hours saved each year and ${cost_savings_r:,} in annual cost savings. The implementation required a one-time investment of {implement_hours:,.0f} hours, with only {maintain_hours_per_year:,.0f} hours of maintenance needed per year. Over one year, the project cost is ${project_cost_over_window:,.0f}, resulting in a quick ROI of {quick_roi_pct:,.1f}%. Increasing the automation rate by removing technical debt and deliberate exclusions can further amplify these benefits, allowing more tasks to be automated and boosting both efficiency and cost savings over time."
        )
        st.text(narrative_text)

        # Save button: export inputs, calculations, and summary to JSON
        def to_camel_short(title: str) -> str:
            # keep alphanumerics and split on whitespace
            parts = [
                p
                for p in "".join(
                    ch if ch.isalnum() or ch.isspace() else " " for ch in title
                ).split()
                if p
            ]
            if not parts:
                return "project"
            camel = parts[0].lower() + "".join(w.capitalize() for w in parts[1:])
            return camel[:20]

        summary_text = narrative_text

        payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "project": {
                "title": project_title,
                "shortTitle": to_camel_short(project_title),
                "description": project_desc,
            },
            "assumptions": {
                "interactionsPerMonth": interactions_per_month,
                "automationCoveragePct": automation_coverage_pct,
                "hourlyRate": hourly_rate,
                "implementHoursOneTime": implement_hours,
                "maintainHoursPerYear": maintain_hours_per_year,
            },
            "timePerInteraction": {
                "manualStepsMinutes": m_vals,
                "automatedStepsMinutes": a_vals,
                "manualTotalMinutes": manual_total,
                "automatedTotalMinutes": auto_total,
            },
            "results": {
                "minutesSavedPerInteraction": minutes_saved,
                "interactionsPerYear": tasks_per_year,
                "automatedInteractionsPerYear": effective_changes,
                "automationRatePct": automation_coverage_pct,
                "annualHoursSaved": annual_hours_saved,
                "annualCostSavings": annual_cost_savings,
                "projectCostFirstYear": project_cost_year1,
                "benefitOneYear": benefit_over_window,
                "projectCostOneYear": project_cost_over_window,
                "quickRoiPctOneYear": quick_roi_pct,
            },
            "summaryNarrative": summary_text,
        }

        json_bytes = json.dumps(payload, indent=2).encode("utf-8")
        short_ts = datetime.utcnow().strftime("%Y%m%d_%H%MZ")
        filename = f"SimpleROI_{payload['project']['shortTitle']}_{short_ts}.json"
        clicked = st.download_button(
            label="Save results as JSON",
            data=json_bytes,
            file_name=filename,
            mime="application/json",
            use_container_width=True,
            key="simple_save_json_btn",
        )
        if clicked:
            st.session_state["simple_save_last_filename"] = filename
        if st.session_state.get("simple_save_last_filename"):
            saved_name = st.session_state["simple_save_last_filename"]
            st.success(
                f"Saved '{saved_name}' to your browser's default download location."
            )
            st.caption(
                "Note: If your browser is configured to ask for a download location, it was saved wherever you chose."
            )


    else:
        st.info(
            "Update the title, description, time inputs, and assumptions to see results and a summary narrative."
        )

    utils.thick_hr(color="grey", thickness=5)
    st.caption(
        "Tip: Use the Business Case Calculator for full NPV/IRR/payback modeling."
    )
    try:
        st.page_link(
            "pages/20_Business_Case_Calculator.py",
            label="Open Business Case Calculator",
            icon="🧮",
        )
    except Exception:
        pass


if __name__ == "__main__":
    main()
