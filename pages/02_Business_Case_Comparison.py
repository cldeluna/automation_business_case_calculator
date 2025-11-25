#!/usr/bin/env python3

import streamlit as st
import json
from typing import Dict, Any

st.set_page_config(page_title="Business Case Comparison", page_icon="images/EIA_Favicon.png", layout="wide")

st.title("Business Case Comparison")

with st.sidebar:
    st.image("images/EIA Logo FINAL small_Round.png", width=64)

st.markdown(
    """
Upload two saved scenario JSON files (e.g., Buy vs Build) to compare key metrics side-by-side.
Use clear slugs to label each scenario for readability.
"""
)

col_names = st.columns(2)
with col_names[0]:
    slug_a = st.text_input("Scenario A name (slug)", value="buy")
with col_names[1]:
    slug_b = st.text_input("Scenario B name (slug)", value="build")

col_uploads = st.columns(2)
with col_uploads[0]:
    file_a = st.file_uploader("Upload Scenario A JSON", type=["json"], key="cmpA")
with col_uploads[1]:
    file_b = st.file_uploader("Upload Scenario B JSON", type=["json"], key="cmpB")

if file_a is not None and file_b is not None:
    try:
        dataA: Dict[str, Any] = json.loads(file_a.read().decode("utf-8"))
        dataB: Dict[str, Any] = json.loads(file_b.read().decode("utf-8"))

        def val(d: Dict[str, Any], k: str, default=0.0):
            v = d.get(k, default)
            try:
                return float(v)
            except Exception:
                return default

        rows = []

        def add_row(name: str, key: str, fmt="${:,.2f}"):
            a = val(dataA, key, 0.0)
            b = val(dataB, key, 0.0)
            delta = b - a
            rows.append({
                "Metric": name,
                slug_a: fmt.format(a) if isinstance(a, float) else a,
                slug_b: fmt.format(b) if isinstance(b, float) else b,
                "Delta (B−A)": fmt.format(delta) if isinstance(delta, float) else delta,
            })

        rows.append({
            "Metric": "Acquisition strategy",
            slug_a: dataA.get("acquisition_strategy", ""),
            slug_b: dataB.get("acquisition_strategy", ""),
            "Delta (B−A)": "",
        })
        add_row("Project cost (Y0)", "project_cost")
        add_row("Annual run cost (effective)", "annual_run_cost_effective")
        add_row("Annual total benefit", "annual_total_benefit")
        add_row("Annual net benefit", "annual_net_benefit")
        add_row("NPV", "npv")
        # IRR expected as decimal; show as percent
        a_irr = val(dataA, "irr", 0.0)
        b_irr = val(dataB, "irr", 0.0)
        rows.append({
            "Metric": "IRR (%)",
            slug_a: f"{a_irr*100:,.2f}%",
            slug_b: f"{b_irr*100:,.2f}%",
            "Delta (B−A)": f"{(b_irr - a_irr)*100:,.2f}%",
        })
        # Payback (years)
        a_pb = dataA.get("payback", None)
        b_pb = dataB.get("payback", None)
        rows.append({
            "Metric": "Payback (years)",
            slug_a: (f"{a_pb:,.2f}" if isinstance(a_pb, (int, float)) else str(a_pb)),
            slug_b: (f"{b_pb:,.2f}" if isinstance(b_pb, (int, float)) else str(b_pb)),
            "Delta (B−A)": (f"{(b_pb - a_pb):,.2f}" if isinstance(a_pb, (int, float)) and isinstance(b_pb, (int, float)) else ""),
        })

        st.markdown("### Comparison Table")
        st.table(rows)

    except Exception as e:
        st.error(f"Failed to compare scenarios: {e}")
else:
    st.info("Upload two scenario JSON files to see the comparison.")
