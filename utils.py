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
    """
    hr_color_dict = {
        "naf_yellow": "#fffe03",
        "eia_blue": "#92c0e4",
        "eia_dkblue": "#122e43",
    }
    return hr_color_dict


# ---------- Visualization helpers (Plotly) ----------


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
    fig.add_trace(
        go.Bar(name="Benefits", x=labels, y=benefits, marker_color="#16a34a")
    )
    fig.add_trace(
        go.Bar(name="Costs", x=labels, y=costs, marker_color="#ef4444")
    )
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
        go.Scatter(x=list(range(len(cash_flows))), y=cum, mode="lines+markers", name="Cumulative")
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
        go.Scatter(x=list(range(len(cash_flows))), y=[float(v) for v in cash_flows], mode="lines+markers", name="Net")
    )
    fig.add_hline(y=0, line_color="#94a3b8")
    fig.update_layout(title="Net Cash Flow per Year", xaxis_title="Year", yaxis_title="USD")
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
