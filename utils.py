#!/usr/bin/python3 -tt
# Project: automation_business_case_calculator
# Filename: utils.py
# claudiadeluna
# PyCharm

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "11/25/25"
__copyright__ = "Copyright (c) 2025 Claudia"
__license__ = "Python"


# from __future__ import annotations

from typing import List, Optional
import streamlit as st
import plotly.graph_objects as go


# ---------- Financial helper functions ----------


def compute_npv(discount_rate: float, cash_flows: List[float]) -> float:
    """
    Compute Net Present Value (NPV) for a series of cash flows.

    Parameters
    - discount_rate: Annual discount or hurdle rate as a decimal (e.g., 0.10 for 10%).
    - cash_flows: Sequence of cash flows where index 0 is Year 0 (today), index 1 is Year 1, etc.

    Returns
    - The NPV as a float. Values > 0 indicate value creation at the given discount rate.

    Notes
    - This uses simple annual compounding: cf_t / (1 + r)^t.
    - Sign convention is flexible; commonly investments are negative at t=0 and benefits positive thereafter.
    """
    npv = 0.0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** t)
    return npv


def thick_hr(color: str = "red", thickness: int = 3, margin: str = "1rem 0"):
    """
    Render a visually thicker horizontal line in Streamlit using raw HTML.

    Parameters
    - color: CSS color for the rule (named color or hex).
    - thickness: Pixel height of the line.
    - margin: CSS margin to apply (e.g., "1rem 0").

    Behavior
    - Uses st.markdown with unsafe_allow_html to inject an <hr> replacement.
    """
    st.markdown(
        f"""
        <hr style="
            border: none;
            height: {thickness}px;
            background-color: {color};
            margin: {margin};
        ">
        """,
        unsafe_allow_html=True,
    )


def hr_colors():
    """
    Returns a dictionary of colors for horizontal lines.

    utils.thick_hr(color="#6785a0", thickness=3)
    """
    hr_color_dict = {
        "naf_yellow": "#fffe03",
        "eia_blue": "#92c0e4",
        "eia_dkblue": "#122e43",
    }
    return hr_color_dict


# ---------- Visualization helpers (Plotly) ----------


def render_time_inputs(
    base_key: str, image_file: str = "images/AnatomyOfNetChange.png"
):
    """
    Render the Manual vs Automated Time per Change (in minutes) inputs and return per-step values and totals.

    Parameters
    - base_key: Prefix for widget keys (ensures state isolation per caller/page).
    - image_file: Path to an image to display above the inputs (default AnatomyOfNetChange).

    Returns
    - dict with keys:
      - manual_steps: list[int] (8 items)
      - auto_steps: list[int] (8 items)
      - manual_total: int
      - auto_total: int
    """
    thick_hr(color="grey", thickness=5)
    st.subheader("Manual vs Automated Time per Change (in minutes)")
    st.markdown(
        "***An interaction can be a change, submission, calculation, analysis, or other task that requires execution**"
    )
    cols_img = st.columns([1, 3, 1])
    with cols_img[1]:
        try:
            st.image(image_file, use_container_width=True)
        except Exception:
            pass

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Manual today**")
        m1 = st.number_input(
            "1. Obtain change/task details – manual (minutes/interaction)",
            min_value=0,
            value=10,
            step=1,
            help="Change intent and devices impacted.",
            key=f"{base_key}_m1",
        )
        m2 = st.number_input(
            "2. Develop command payload – manual (minutes/interaction)",
            min_value=0,
            value=15,
            step=1,
            key=f"{base_key}_m2",
        )
        m3 = st.number_input(
            "3. Quantify impact – manual (minutes/interaction)",
            min_value=0,
            value=10,
            step=1,
            key=f"{base_key}_m3",
        )
        m4 = st.number_input(
            "4. Change management, scheduling, notification – manual (minutes/interaction)",
            min_value=0,
            value=15,
            step=1,
            key=f"{base_key}_m4",
        )
        m5 = st.number_input(
            "5. Current state analysis & verification – manual (minutes/interaction)",
            min_value=0,
            value=15,
            step=1,
            key=f"{base_key}_m5",
        )
        m6 = st.number_input(
            "6. Execute Interaction Commands – manual (minutes/interaction)",
            min_value=0,
            value=10,
            step=1,
            key=f"{base_key}_m6",
        )
        m7 = st.number_input(
            "7. Test & verification QA – manual (minutes/interaction)",
            min_value=0,
            value=15,
            step=1,
            key=f"{base_key}_m7",
        )
        m8 = st.number_input(
            "8. Documentation, notification, close out – manual (minutes/interaction)",
            min_value=0,
            value=10,
            step=1,
            key=f"{base_key}_m8",
        )

    with col2:
        st.markdown("**After automation**")
        a1 = st.number_input(
            "1. Obtain change details – automated (minutes/interaction)",
            min_value=0,
            value=5,
            step=1,
            help="Time to capture intent / inputs into automation.",
            key=f"{base_key}_a1",
        )
        a2 = st.number_input(
            "2. Develop command payload – automated (minutes/interaction)",
            min_value=0,
            value=5,
            step=1,
            key=f"{base_key}_a2",
        )
        a3 = st.number_input(
            "3. Quantify impact – automated (minutes/interaction)",
            min_value=0,
            value=5,
            step=1,
            key=f"{base_key}_a3",
        )
        a4 = st.number_input(
            "4. Change management, scheduling, notification – automated (minutes/interaction)",
            min_value=0,
            value=5,
            step=1,
            key=f"{base_key}_a4",
        )
        a5 = st.number_input(
            "5. Current state analysis & verification – automated (minutes/interaction)",
            min_value=0,
            value=5,
            step=1,
            key=f"{base_key}_a5",
        )
        a6 = st.number_input(
            "6. Execute Interaction Commands – automated (minutes/interaction)",
            min_value=0,
            value=5,
            step=1,
            key=f"{base_key}_a6",
        )
        a7 = st.number_input(
            "7. Test & verification QA – automated (minutes/interaction)",
            min_value=0,
            value=5,
            step=1,
            key=f"{base_key}_a7",
        )
        a8 = st.number_input(
            "8. Documentation, notification, close out – automated (minutes/interaction)",
            min_value=0,
            value=5,
            step=1,
            key=f"{base_key}_a8",
        )

    manual_steps = [m1, m2, m3, m4, m5, m6, m7, m8]
    auto_steps = [a1, a2, a3, a4, a5, a6, a7, a8]
    manual_total = sum(manual_steps)
    auto_total = sum(auto_steps)

    tcol1, tcol2 = st.columns(2)
    with tcol1:
        st.metric(label="Total manual minutes per change", value=f"{manual_total}")
    with tcol2:
        st.metric(label="Total automated minutes per change", value=f"{auto_total}")

    return {
        "manual_steps": manual_steps,
        "auto_steps": auto_steps,
        "manual_total": manual_total,
        "auto_total": auto_total,
    }


def fig_annual_benefits_vs_costs(
    years: int,
    annual_total_benefit: float,
    annual_run_cost_effective: float,
    project_cost: float,
):
    """
    Build a grouped bar chart comparing annual benefits vs. costs.

    Parameters
    - years: Number of modeled years (not counting Year 0).
    - annual_total_benefit: Annual benefit amount (positive) applied to Y1..Y{years}.
    - annual_run_cost_effective: Effective annual run cost (may include debt adjustments), applied to Y1..Y{years} as negative bars.
    - project_cost: One-time Year 0 cost (displayed as negative bar at Y0).

    Returns
    - Plotly Figure configured for display in Streamlit.
    """
    labels = [f"Y{t}" for t in range(0, years + 1)]
    benefits = [0.0] + [float(annual_total_benefit)] * years
    costs = [float(-project_cost)] + [float(-annual_run_cost_effective)] * years

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Benefits", x=labels, y=benefits, marker_color="#16a34a"))
    fig.add_trace(go.Bar(name="Costs", x=labels, y=costs, marker_color="#ef4444"))
    fig.update_layout(
        title="Annual Benefits vs Costs",
        barmode="relative",
        xaxis_title="Year",
        yaxis_title="USD",
        legend_orientation="h",
        legend_yanchor="bottom",
        legend_y=1.02,
        legend_x=0.0,
    )
    return fig


def fig_cumulative_cash_flow(cash_flows: List[float], payback: Optional[float] = None):
    """
    Build a line chart of cumulative cash flow over time.

    Parameters
    - cash_flows: Sequence of cash flows starting with Year 0.
    - payback: Optional payback period (years). If provided and within range, a vertical line is drawn.

    Returns
    - Plotly Figure for cumulative cash flows including a horizontal zero baseline.
    """
    cum = []
    total = 0.0
    for cf in cash_flows:
        total += float(cf)
        cum.append(total)

    labels = [f"Y{t}" for t in range(0, len(cash_flows))]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(len(cash_flows))),
            y=cum,
            mode="lines+markers",
            name="Cumulative",
        )
    )
    fig.add_hline(y=0, line_color="#94a3b8")

    if payback is not None and 0 <= float(payback) <= len(cash_flows) - 1 + 0.01:
        fig.add_vline(x=float(payback), line_color="#f59e0b", line_dash="dash")

    fig.update_layout(
        title="Cumulative Cash Flow",
        xaxis_title="Year",
        yaxis_title="USD",
    )
    return fig


def fig_net_cash_flow(cash_flows: List[float]):
    """
    Build a line chart of net cash flow by year.

    Parameters
    - cash_flows: Sequence of cash flows (Y0..Yn).

    Returns
    - Plotly Figure with a zero baseline to highlight sign changes.
    """
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(len(cash_flows))),
            y=[float(v) for v in cash_flows],
            mode="lines+markers",
            name="Net",
        )
    )
    fig.add_hline(y=0, line_color="#94a3b8")
    fig.update_layout(
        title="Net Cash Flow per Year", xaxis_title="Year", yaxis_title="USD"
    )
    return fig


def fig_waterfall(cash_flows: List[float]):
    """
    Build a waterfall chart for cash flows from Y0 through Yn.

    Parameters
    - cash_flows: Sequence of cash flows (Y0..Yn).

    Returns
    - Plotly Waterfall Figure showing the cumulative progression of cash flows.
    """
    labels = [f"Y{t}" for t in range(0, len(cash_flows))]
    measures = ["relative"] * len(cash_flows)
    fig = go.Figure(
        go.Waterfall(
            name="Cash Flow",
            orientation="v",
            measure=measures,
            x=labels,
            y=[float(v) for v in cash_flows],
            connector={"line": {"color": "rgb(63,63,63)"}},
        )
    )
    fig.update_layout(title=f"Cash Flow Waterfall (Y0..Y{len(cash_flows)-1})")
    return fig


def main():
    """
    Module self-check entry point (optional).

    Purpose
    - Provides a basic callable for ad-hoc verification or future CLI hooks.

    Current behavior
    - No-op (pass). Keep in place to allow running this module directly without errors.
    """
    pass


# Standard call to the main() function.
if __name__ == "__main__":
    main()
