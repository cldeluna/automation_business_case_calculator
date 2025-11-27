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
    """Net Present Value.
    cash_flows[0] is year 0 (today), cash_flows[1] is year 1, etc.
    """
    npv = 0.0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** t)
    return npv

#
# def compute_payback_period(cash_flows: List[float]) -> Optional[float]:
#     """Simple (undiscounted) payback period in years.
#     Returns fractional years, or None if payback never happens.
#     """
#     cumulative = 0.0
#     for t in range(len(cash_flows)):
#         prev_cumulative = cumulative
#         cumulative += cash_flows[t]
#         if cumulative >= 0:
#             if t == 0:
#                 return 0.0
#             cash_this_year = cash_flows[t]
#             if cash_this_year == 0:
#                 return float(t)
#             fraction = (0 - prev_cumulative) / cash_this_year
#             return (t - 1) + fraction
#     return None
#
#
# def compute_irr(
#     cash_flows: List[float],
#     guess_low: float = -0.9,
#     guess_high: float = 10.0,
#     tol: float = 1e-6,
#     max_iter: int = 100,
# ) -> Optional[float]:
#     """Very simple IRR using binary search.
#     Returns r such that NPV(r) ~= 0, or None if no solution exists.
#     """
#
#     def npv_at(rate: float) -> float:
#         return compute_npv(rate, cash_flows)
#
#     npv_low = npv_at(guess_low)
#     npv_high = npv_at(guess_high)
#
#     # Need sign change to have a root in [low, high]
#     if npv_low * npv_high > 0:
#         return None
#
#     for _ in range(max_iter):
#         mid = (guess_low + guess_high) / 2
#         npv_mid = npv_at(mid)
#         if abs(npv_mid) < tol:
#             return mid
#         if npv_low * npv_mid < 0:
#             guess_high = mid
#             npv_high = npv_mid
#         else:
#             guess_low = mid
#             npv_low = npv_mid
#
#     return (guess_low + guess_high) / 2
#

def thick_hr(color: str = "red", thickness: int = 3, margin: str = "1rem 0"):
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


# ---------- Visualization helpers (Plotly) ----------


def fig_annual_benefits_vs_costs(
    years: int,
    annual_total_benefit: float,
    annual_run_cost_effective: float,
    project_cost: float,
):
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
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(range(len(cash_flows))), y=[float(v) for v in cash_flows], mode="lines+markers", name="Net")
    )
    fig.add_hline(y=0, line_color="#94a3b8")
    fig.update_layout(title="Net Cash Flow per Year", xaxis_title="Year", yaxis_title="USD")
    return fig


def fig_waterfall(cash_flows: List[float]):
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
    Utility helpers for the Automation Business Case app.

    Phase 1: financial helpers migrated from the single-file app so that
    pages can import from utils and we can continue refactoring incrementally.
    """
    pass


# Standard call to the main() function.
if __name__ == "__main__":
    main()
