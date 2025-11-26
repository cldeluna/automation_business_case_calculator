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


# ---------- Financial helper functions ----------


def compute_npv(discount_rate: float, cash_flows: List[float]) -> float:
    """Net Present Value.
    cash_flows[0] is year 0 (today), cash_flows[1] is year 1, etc.
    """
    npv = 0.0
    for t, cf in enumerate(cash_flows):
        npv += cf / ((1 + discount_rate) ** t)
    return npv


def compute_payback_period(cash_flows: List[float]) -> Optional[float]:
    """Simple (undiscounted) payback period in years.
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
    cash_flows: List[float],
    guess_low: float = -0.9,
    guess_high: float = 10.0,
    tol: float = 1e-6,
    max_iter: int = 100,
) -> Optional[float]:
    """Very simple IRR using binary search.
    Returns r such that NPV(r) ~= 0, or None if no solution exists.
    """

    def npv_at(rate: float) -> float:
        return compute_npv(rate, cash_flows)

    npv_low = npv_at(guess_low)
    npv_high = npv_at(guess_high)

    # Need sign change to have a root in [low, high]
    if npv_low * npv_high > 0:
        return None

    for _ in range(max_iter):
        mid = (guess_low + guess_high) / 2
        npv_mid = npv_at(mid)
        if abs(npv_mid) < tol:
            return mid
        if npv_low * npv_mid < 0:
            guess_high = mid
            npv_high = npv_mid
        else:
            guess_low = mid
            npv_low = npv_mid

    return (guess_low + guess_high) / 2


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
