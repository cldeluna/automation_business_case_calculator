<p align="right">
  <img src="images/EIA Logo FINAL small_Dark Background.png" alt="EIA Logo" width="180">
</p>

# Automation Business Case App

Build a defensible, CXO-ready business case for Network Automation. This Streamlit app turns simple engineering inputs (how often a change happens, minutes saved by automation, costs to buy/build, and optional risk “debts”) into finance-friendly outputs: NPV, IRR, payback, cash flows, and a polished Markdown report you can download and share. You can also save scenarios to JSON and compare them side-by-side.

Created by **Claudia de Luna** and **Enterprise Infrastructure Acceleration (EIA)**  
Contact: <claudia@eianow.com> • https://eianow.com

## Key Features
- **Business Case Calculator**
  - Enter volumes and time per step (manual vs automated) for a specific change type.
  - Model Buy vs Build with itemized one-time and annual run costs.
  - Optionally include “Debts & Risk” as costs scaled by non-automated scope:
    - Technical Debt (annual + optional one-time remediation and residual %).
    - CSAT Debt (annual + optional one-time remediation and residual %).
  - Add optional business benefits (Revenue Acceleration, Deployment Speed, Compliance, Security, etc.), each with value, methodology, and assumptions.
  - Computes NPV, IRR, Payback, annual net benefit, and cumulative cash checkpoints (1/3/5 yrs).
  - Generates a CXO-ready Markdown report and NABCD(E) summary.
  - Download ZIP containing the Markdown report and a timestamped scenario JSON.

- **Business Case Comparison**
  - Upload two saved scenario JSON files (e.g., Buy vs Build) and compare key outcomes side-by-side.
  - Shows deltas for project cost, run cost, total/net benefits, NPV, IRR, and payback.

## App Pages
- 🧮 `Business Case Calculator` (`pages/01_Business_Case_Calculator.py`)
  - Interactive inputs and instant calculations.
  - Report builder and scenario save/load utilities.

- 📊 `Business Case Comparison` (`pages/02_Business_Case_Comparison.py`)
  - Side-by-side comparison table built from two uploaded scenario JSON files.

## Requirements
- Python 3.11+ (per pyproject)
- Streamlit (declared in pyproject)

Install dependencies with pip (reads pyproject):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

If you manage dependencies with a virtual environment, activate it first.

### Using uv (preferred in this repo)
If you use uv for dependency and environment management:

1) Install uv (macOS):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# After install, ensure ~/.local/bin (or the printed path) is on your PATH
```

2) (Optional) Ensure Python 3.11 is available and set for the project:

```bash
# Install a specific Python if needed
uv python install 3.11
```

3) Create a virtual environment (optional) and install dependencies from pyproject:

```bash
# Create a venv in .venv (optional)
uv venv .venv
source .venv/bin/activate

# Install all project dependencies from pyproject.toml
uv sync
```

4) Run the app with uv:

```bash
uv run streamlit run Automation_BusinessCase_App.py
```

## How to Run
From this project folder, start the Streamlit app:

```bash
streamlit run Automation_BusinessCase_App.py
```

Or with uv:

```bash
uv run streamlit run Automation_BusinessCase_App.py
```

Streamlit will open a browser tab. Use the sidebar or the home page links to navigate to:
- 🧮 Business Case Calculator
- 📊 Business Case Comparison

## Checklist: Values you’ll need
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
  - CSAT Debt
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
  - [ ] Typical values/assumptions
- **Finance**
  - [ ] Discount rate / hurdle rate (%)

<details>
<summary><strong>How the calculations work</strong></summary>

The calculator turns engineering inputs into business metrics. Here’s exactly how, in plain English:

- <strong>Tasks per year</strong>  
  <code>tasks_per_year = changes_per_month × 12</code>

- <strong>Time saved per change (hours)</strong>  
  <code>hours_saved_per_change = (manual_total_minutes − auto_total_minutes) ÷ 60</code>

- <strong>Effective automated changes/year</strong>  
  <code>effective_changes_per_year = tasks_per_year × (automation_coverage_% ÷ 100)</code>

- <strong>Annual hours saved</strong>  
  <code>annual_hours_saved = hours_saved_per_change × effective_changes_per_year</code>

- <strong>Annual cost savings (time)</strong>  
  <code>annual_cost_savings = annual_hours_saved × engineer_hourly_rate</code>

- <strong>Additional benefits (optional)</strong>  
  Sum of any checked benefit categories.  
  <code>annual_additional_benefits = Σ benefit_annual_value</code>

- <strong>Total annual benefit</strong>  
  <code>annual_total_benefit = annual_cost_savings + annual_additional_benefits</code>

- <strong>Annual run cost (effective)</strong>  
  Includes ongoing run cost plus optional debts (scaled by non‑automated scope).  
  <code>annual_run_cost_effective = annual_run_cost + tech_debt_annual_after + csat_debt_annual_after</code>

- <strong>Annual net benefit</strong>  
  <code>annual_net_benefit = annual_total_benefit − annual_run_cost_effective</code>

- <strong>Project cost (Year 0)</strong>  
  One‑time Buy/Build cost, plus any one‑time remediation.  
  <code>project_cost_effective = project_cost + tech_debt_remediation_one_time + csat_debt_remediation_one_time</code>

- <strong>Cash flows (Year 0..N)</strong>  
  Year 0 is the investment (negative), followed by N years of annual net benefit.  
  <code>cash_flows = [−project_cost_effective] + [annual_net_benefit] × years</code>

- <strong>Net Present Value (NPV)</strong>  
  Uses your discount (hurdle) rate <code>r</code> to reflect time value of money.  
  <code>NPV = Σ ( CF_t ÷ (1 + r)^t ), t = 0..years</code>

- <strong>Payback period (undiscounted)</strong>  
  Years until cumulative cash ≥ 0; if it happens mid‑year, the model interpolates a fraction.

- <strong>Internal Rate of Return (IRR)</strong>  
  The discount rate where NPV = 0. If IRR > your discount rate, the project clears the financial bar.

- <strong>Cumulative checkpoints (1/3/5 yrs)</strong>  
  Simple running totals to show progress recovering the initial investment.

- <strong>Sign convention</strong>  
  Benefits are positive (returns). Costs are investments and appear as negative cash flows.

</details>

## Change Workflow Anatomy (context)
The calculator asks for minutes per step for both manual and automated workflows. This diagram illustrates the 8 steps used in the app:

<p align="center">
  <img src="./images/AnatomyOfNetChange.png" alt="Anatomy of a Network Change" width="70%">
  <br/>
  <em>Eight-step change workflow used for manual vs automated time inputs.</em>
  <br/>
</p>

## Intangible / Soft Benefits (context)
Some outcomes are hard to price precisely but still matter for funding and prioritization. In the app’s sidebar you can select relevant categories (not monetized by default), such as:

- Relationship and Trust
- Demand and Alignment
- Organizational Behavior
- Financial and Political Capital
- Culture and Talent
- Risk and Resilience
- Reputation and Influence

Selected items appear in the web output and are included in the Markdown report and scenario JSON.

## Using the Business Case Calculator
1. **Initiative details**
   - Title and short description/scope.
2. **Volume & cost assumptions (sidebar)**
   - Switches per location, locations, changes per month, automation coverage %, engineer hourly rate.
3. **Acquisition strategy**
   - Choose Buy tool(s) or Build in-house and enter one-time + annual costs.
4. **Debts & Risk (optional)**
   - Toggle Technical Debt and/or CSAT Debt. Enter 100% annual impact, remediation cost (optional), and residual %.
5. **Additional Benefits (optional)**
   - Check any categories that apply and provide annual value, methodology, and typical assumptions.
6. **Manual vs Automated time per change**
   - Enter minutes for the 8 workflow steps on both sides.
7. **Calculate Business Case**
   - The app computes hours saved, annual benefits, net benefit after run costs, cash flows (Year 0–5), NPV, IRR, and payback.
8. **Review Outputs**
   - Business Case Summary, Cost Modeling table, Cash Flows, Metrics, Cumulative checkpoints, Sanity-check panel.
9. **NABCD(E) Summary**
   - Copy-pasteable summary aligned to Need, Approach, Benefits, Competitiveness, Defensibility, Exit/Ask.
10. **Download**
   - Download the full Markdown report, or a ZIP containing the report and scenario JSON.
11. **Save/Load Scenarios**
   - Download a JSON describing your inputs and results.
   - Upload a saved JSON to rebuild the Markdown report later.

## Using the Comparison Page
1. Prepare two scenario JSON files (e.g., one for “Buy”, one for “Build”).
2. Open 📊 Business Case Comparison.
3. Provide short slugs for each scenario (labels).
4. Upload the JSON files. The table shows A vs B with deltas for:
   - Project cost, annual run cost (effective), total benefits, net benefits, NPV, IRR, payback.

## Scenario JSON Structure (high level)
The downloaded JSON includes inputs and computed outputs. Key fields:
- Inputs: `years`, `automation_title`, `automation_description`, device counts, `tasks_per_year`, `automation_coverage_pct`, `hourly_rate`, manual/automated minutes, `acquisition_strategy`, `cost_breakdown`, debts toggles and parameters, `benefits`.
- Outputs: `annual_hours_saved`, `annual_cost_savings`, `annual_total_benefit`, `annual_run_cost_effective`, `annual_net_benefit`, `project_cost`, `discount_rate_pct`, `cash_flows`, `npv`, `payback`, `irr`, `cum_1`, `cum_3`, `cum_5`.

## Notes and Assumptions
- NPV/IRR are computed from Year 0 to Year 5 using your discount rate.
- Payback is undiscounted and shown in fractional years when applicable.
- Technical/CSAT debt costs are applied to the non-automated portion of the scope and can include remediation effects.
- IRR may be “not meaningful” if cash flows do not change sign.

## Troubleshooting
- If the browser does not open, visit the URL shown in your terminal (e.g., http://localhost:8501).
- If you see import errors, ensure Streamlit is installed in the active environment.
- For strange IRR results, verify that net cash flows change sign (negative Year 0, positive subsequent years).

## Tech Stack
- Python, Streamlit

## Project Structure
- `Automation_BusinessCase_App.py` – Home/landing page and navigation links.
- `pages/01_Business_Case_Calculator.py` – Main calculator, report builder, scenario save/load, ZIP download.
- `pages/02_Business_Case_Comparison.py` – Scenario comparison tool.

## Guiding Quote
> According to Darwin's Origin of Species, it is not the most intellectual of the species that survives; it is not the strongest that survives; but the species that survives is the one that is able best to adapt and adjust to the changing environment in which it finds itself.
>
> — Leon C. Megginson, “Lessons from Europe for American Business,” Southwestern Social Science Quarterly (1963) 44(1): 3–13, p. 4. Context: the quote originated as a paraphrase of Darwin.

## License
Licensed under the **Apache License, Version 2.0**. See [`LICENSE`](./LICENSE) for details.

Attribution notices are provided in [`NOTICE`](./NOTICE). When redistributing in source or binary form, preserve the LICENSE and NOTICE files.

