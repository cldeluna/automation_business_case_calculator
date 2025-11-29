#!/usr/bin/python3 -tt
# Project: automation_business_case_calculator
# Filename: 03_Solution_Wizard.py
# claudiadeluna
# PyCharm

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "11/25/25"
__copyright__ = "Copyright (c) 2025 Claudia"
__license__ = "Python"


import streamlit as st
import json
from datetime import datetime
import utils
from wizard_utils import join_human, md_line, is_meaningful
import pandas as pd
import plotly.express as px

# Optional lightweight holiday support
try:
    import holidays as _hol
except Exception:  # pragma: no cover
    _hol = None


def _join(items):
    # Delegate to shared tested helper
    return join_human(items)


def main():
    """
    Solution Wizard (NAF Framework) interactive page

    Includes guided inputs for:
    - Presentation, Intent, Observability, Orchestration, Collector, and Executor
    - Collector now includes a dedicated "Collection tools" selector (e.g., SuzieQ, Catalyst Center, Nexus Dashboard, ACI APIC, Arista CVP, Prometheus)

    Planning section:
    - "Staffing, Timeline, & Milestones" with:
      - Staffing fields (direct staff count and markdown-supported staffing plan)
      - Start date calendar
      - Editable milestone rows (name, duration in business days, notes)
      - Business-day scheduling that skips weekends and optionally public holidays (via python-holidays)
      - Optional Plotly Gantt chart visualization
      - Summary callouts for expected delivery date (st.success) and approximate duration in months/years (st.info)

    Highlights & export:
    - Solution Highlights suppress default/empty content (e.g., default timeline and default dependencies are hidden)
    - Exports consolidated payload to JSON in st.session_state["solution_wizard"], including:
      - presentation/intent/observability/orchestration/collector/executor narratives and selections
      - timeline: start_date, total_business_days, projected_completion, staff_count, staffing_plan_md, holiday_region, and detailed items
    """
    # Page config
    st.set_page_config(
        page_title="Solution Wizard",
        page_icon="images/EIA_Favicon.png",
        layout="wide",
    )

    with st.sidebar:
        st.image("images/EIA Logo FINAL small_Round.png", width=75)

    # Title with NAF icon
    title_cols = st.columns([0.08, 0.92])
    with title_cols[0]:
        st.image("images/naf_icon.png", use_container_width=True)
    with title_cols[1]:
        st.markdown("**Network Automation Forum's Automation Framework**")

    # Intro: purpose of the wizard and how it relates to the calculator
    st.markdown(
        """
        The Solution Wizard helps you think through your automation project using the Network Automation Forum (NAF) Automation Framework.

        - **Purpose:** Guide structured thinking across the NAF components so you identify stakeholders, scope, data flows, and build/buy/support decisions.
        - **Optional:** You don't need to complete this wizard to use the Business Case Calculator. If you already worked this out elsewhere and have the inputs, you can skip the wizard.
        - **Second set of eyes:** Use it as a checklist to ensure you’ve considered all key components; the framework helps make sure nothing critical is missed.
        - **Authoring aid:** Your selections here can help generate narrative text for the "Detailed solution description (Markdown supported)" field in the calculator.

        Remember: to complete the Business Case Calculator effectively, you should have a clear understanding of what the automation will do, who it will serve, and how it will be built (or bought) and supported going forward.
        """
    )

    # Framework diagram
    st.image(
        "images/naf_arch_framework_figure.png",
        use_container_width=True,
    )

    st.caption(
        "Source: https://github.com/Network-Automation-Forum/reference/blob/main/docs/Framework/Framework.md"
    )

    # Collapsible guiding questions
    with st.expander("Guiding Questions by Framework Component", expanded=False):
        st.markdown(
            """
            - **Intent**
              - Defines the logic and the persistence layer for the desired state of the network (config and operational expectations).
              - Represents network aspects in structured form, supports CRUD via standard APIs, uses neutral models, and can include validation, aggregation, service decomposition, and artifact generation.

            - **Observability**
              - Persists the actual network state and provides logic to process it.
              - Offers programmatic access and query for analytics, detects drift vs. intent, and can enrich data with context (e.g., EoL, CVEs, maintenance).

            - **Orchestrator**
              - Coordinates and sequences automation tasks across components in response to events.
              - Can be event‑driven, support dry‑run, scheduling, rollback/compensation, logging/traceability, and correlation.

            - **Executor**
              - Performs the network changes (writes) guided by intent.
              - Works with write interfaces (CLI/SSH, NETCONF, gNMI/gNOI, REST), supports transactional/dry‑run flows, and can operate in imperative or declarative styles with idempotency.

            - **Collector**
              - Retrieves the actual state (reads) from the network via APIs/CLIs and telemetry (e.g., SNMP, syslog, flows, streaming telemetry) and can normalize data across vendors.

            - **Presentation**
              - Provides user interfaces (dashboards/GUI, ITSM, chat, CLI) and access controls for interacting with the system.
              - Can allow both read and write interactions and integrates with other components as needed.
            """
        )

    utils.thick_hr(color="grey", thickness=5)
    st.markdown("***Expand each section of the framework to work though the wizard***")

    # Presentation section
    with st.expander("Presentation", expanded=False):
        st.markdown(
            """
        **Presentation Layer Characteristics**
        - Provides robust, flexible authentication and authorization.
        - Can take many forms: GUIs, ITSM/change systems, chat/messaging, portals, reports.
        - May support read and write: view data, initiate tasks, approve changes.
        - Interfaces with other framework blocks as needed; it is the primary human touchpoint, without requiring a single pane of glass.
            """
        )
        st.subheader("Intended users")
        cols = st.columns(3)
        user_opts = [
            "Network Engineers",
            "IT",
            "Operations",
            "Help Desk",
            "Other IT Organizations",
            "Any User",
            "Authorized Users",
        ]
        user_checks = {}
        for i, opt in enumerate(user_opts):
            with cols[i % 3]:
                user_checks[opt] = st.checkbox(opt, key=f"pres_user_{opt}")
        with cols[0]:
            custom_users_enabled = st.checkbox(
                "Custom (fill in)", key="pres_user_custom_enable"
            )
            custom_users = ""
            if custom_users_enabled:
                custom_users = st.text_input("Custom users", key="pres_user_custom")

        st.subheader("How will your users interact with your solution?")
        cols2 = st.columns(3)
        interact_opts = ["CLI", "Web GUI", "Other GUI", "API"]
        interact_checks = {}
        for i, opt in enumerate(interact_opts):
            with cols2[i % 3]:
                interact_checks[opt] = st.checkbox(opt, key=f"pres_interact_{opt}")
        with cols2[0]:
            custom_interact_enabled = st.checkbox(
                "Custom (fill in)", key="pres_interact_custom_enable"
            )
            custom_interact = ""
            if custom_interact_enabled:
                custom_interact = st.text_input(
                    "Custom interaction", key="pres_interact_custom"
                )

        st.subheader("What tools will the Presentation layer use?")
        cols3 = st.columns(3)
        tool_opts = [
            "Python",
            "Python Web Framework (Streamlit, Flask, etc.)",
            "General Web Framework",
            "Automation Framework",
            "REST API",
            "GraphQL API",
            "Custom API",
        ]
        tool_checks = {}
        for i, opt in enumerate(tool_opts):
            with cols3[i % 3]:
                tool_checks[opt] = st.checkbox(opt, key=f"pres_tool_{opt}")
        with cols3[0]:
            custom_tool_enabled = st.checkbox(
                "Custom (fill in)", key="pres_tool_custom_enable"
            )
            custom_tool = ""
            if custom_tool_enabled:
                custom_tool = st.text_input("Custom tool(s)", key="pres_tool_custom")

        st.subheader("How will your users authenticate?")
        cols4 = st.columns(2)
        auth_opts_pres = [
            "No Authentication (suitable only for demos and very specific use cases)",
            "Repository authorization/sharing",
            "built in Authentication via Username/Password or TOKEN",
            "Custom Authentication to external system (AD, SSH Keys, OAUTH2)",
        ]
        auth_checks_pres = {}
        for i, opt in enumerate(auth_opts_pres):
            with cols4[i % 2]:
                auth_checks_pres[opt] = st.checkbox(opt, key=f"pres_auth_{opt}")
        with cols4[0]:
            auth_other_enabled = st.checkbox(
                "Other (fill in details)", key="pres_auth_other_enable"
            )
            auth_other = ""
            if auth_other_enabled:
                auth_other = st.text_input(
                    "Other authentication details", key="pres_auth_other_text"
                )

        # Narrative synthesis
        selected_users = [k for k, v in user_checks.items() if v]
        if custom_users_enabled and custom_users.strip():
            selected_users.append(custom_users.strip())

        selected_interactions = [k for k, v in interact_checks.items() if v]
        if custom_interact_enabled and custom_interact.strip():
            selected_interactions.append(custom_interact.strip())

        selected_tools = [k for k, v in tool_checks.items() if v]
        if custom_tool_enabled and custom_tool.strip():
            selected_tools.append(custom_tool.strip())

        selected_auth_pres = [k for k, v in auth_checks_pres.items() if v]
        if auth_other_enabled and auth_other.strip():
            selected_auth_pres.append(auth_other.strip())

        users_sentence = f"This solution targets {_join(selected_users)}."
        interaction_sentence = (
            f"Users will interact with the solution via {_join(selected_interactions)}."
        )
        tools_sentence = (
            f"The presentation layer will be built using {_join(selected_tools)}."
        )
        auth_sentence_pres = (
            f"Presentation authentication will use {_join(selected_auth_pres)}."
        )

        utils.thick_hr(color="#6785a0", thickness=3)
        st.markdown("**Preview Solution Highlights**")
        st.write(users_sentence)
        st.write(interaction_sentence)
        st.write(tools_sentence)
        st.write(auth_sentence_pres)

        st.session_state["wizard_pres_narrative"] = {
            "users": users_sentence,
            "interaction": interaction_sentence,
            "tools": tools_sentence,
            "auth": auth_sentence_pres,
        }
        existing_payload = st.session_state.get("solution_wizard", {})
        merged_payload = {
            **existing_payload,
            "presentation": {
                "users": users_sentence,
                "interaction": interaction_sentence,
                "tools": tools_sentence,
                "auth": auth_sentence_pres,
                "selections": {
                    "users": selected_users,
                    "interactions": selected_interactions,
                    "tools": selected_tools,
                    "auth": selected_auth_pres,
                },
            },
        }
        st.session_state["solution_wizard"] = merged_payload

    # Intent section
    with st.expander("Intent", expanded=False):

        st.markdown(
            """
            Intent or the abstracted version of what you are trying to do
            - Represents any network aspect in a structured form (addressing, DC infrastructure, routing, virtual services, secrets, operational limits, templates/mappings, policies, artifacts).
            - Supports full CRUD operations and exposes a standard, well-documented API (e.g., REST, GraphQL).
            - Uses neutral models that derive into vendor-specific configurations.
            - Provides a unified desired-state view across potentially distributed data sources.
            - Includes governance metadata (timestamps, origin, ownership, validity windows).
            - Ideally transactional with custom validation and versioned access.
            - May include intended state logic: validation, aggregation/replication, service decomposition, combine data to generate config artifacts.
            
            ***When first starting out abstraction may be low and so intent could be as simple as a file with vlan numbers and names you want to provision.***
            """
        )
        st.subheader("How will Intent be developed?")
        cols = st.columns(3)
        intent_dev_opts = [
            "Templates",
            "Policies",
            "Service Profiles",
            "Model-driven (data models)",
            "Declarative (YAML/JSON)",
            "Forms/GUI",
            "Domain-specific language (DSL)",
            "GitOps workflow (PRs/Reviews)",
            "API-driven",
            "Import from Source of Truth (CMDB/IPAM/Inventory/Git)",
        ]
        intent_checks = {}
        for i, opt in enumerate(intent_dev_opts):
            with cols[i % 3]:
                intent_checks[opt] = st.checkbox(opt, key=f"intent_dev_{opt}")
        intent_custom_enabled = st.checkbox(
            "Custom (fill in)", key="intent_dev_custom_enable"
        )
        intent_custom = ""
        if intent_custom_enabled:
            intent_custom = st.text_input(
                "Custom intent development approach", key="intent_dev_custom"
            )

        # How will Intent be provided?
        st.subheader("How will Intent be provided?")
        cols_p = st.columns(3)
        intent_prov_opts = [
            "Text file",
            "Serialized format (JSON, YAML)",
            "CSV",
            "Excel",
        ]
        intent_prov_checks = {}
        for i, opt in enumerate(intent_prov_opts):
            with cols_p[i % 3]:
                intent_prov_checks[opt] = st.checkbox(opt, key=f"intent_prov_{opt}")
        with cols_p[0]:
            intent_prov_custom_enabled = st.checkbox(
                "Custom (fill in)", key="intent_prov_custom_enable"
            )
            intent_prov_custom = ""
            if intent_prov_custom_enabled:
                intent_prov_custom = st.text_input(
                    "Custom provider format", key="intent_prov_custom"
                )

        # Narrative synthesis (Intent)
        selected_intent_devs = [k for k, v in intent_checks.items() if v]
        if intent_custom_enabled and intent_custom.strip():
            selected_intent_devs.append(intent_custom.strip())

        selected_intent_prov = [k for k, v in intent_prov_checks.items() if v]
        if intent_prov_custom_enabled and intent_prov_custom.strip():
            selected_intent_prov.append(intent_prov_custom.strip())

        intent_sentence = (
            f"Intent will be developed using {_join(selected_intent_devs)}."
        )
        intent_provided_sentence = (
            f"Intent will be provided via {_join(selected_intent_prov)}."
        )

        utils.thick_hr(color="#6785a0", thickness=3)
        st.markdown("**Preview Solution Highlights**")
        st.write(intent_sentence)
        st.write(intent_provided_sentence)

        # Persist into session
        st.session_state["wizard_intent_narrative"] = {
            "development": intent_sentence,
            "provided": intent_provided_sentence,
        }

        # Merge with existing wizard payload
        existing = st.session_state.get("solution_wizard", {})
        merged = {
            **existing,
            "intent": {
                "development": intent_sentence,
                "provided": intent_provided_sentence,
                "selections": {
                    "development": selected_intent_devs,
                    "provided": selected_intent_prov,
                },
            },
        }
        st.session_state["solution_wizard"] = merged

    # Observability section
    with st.expander("Observability", expanded=False):
        st.markdown(
            """
            - Supports historical data persistence with powerful programmatic access for analytics, reporting, and troubleshooting.
            - Provides a capable query language to extract and explore data.
            - Surfaces current-state insights and emits events when drift is detected between observed and intended state; events may be handled by humans or routed to Orchestration.
            - Data may be enriched with context from intended state and third parties (e.g., EoL, CVEs, maintenance notices) to improve correlation and analysis.
            """
        )
        st.subheader("How will you determine network state?")
        cols_obs = st.columns(3)
        state_methods_opts = [
            "Manual",
            "Purpose-built Python Script",
            "API call",
        ]
        state_methods_checks = {}
        for i, opt in enumerate(state_methods_opts):
            with cols_obs[i % 3]:
                state_methods_checks[opt] = st.checkbox(opt, key=f"obs_state_{opt}")

        st.subheader("Describe the basic go/no go logic")
        go_no_go_text = st.text_area(
            "Go/No-Go criteria",
            key="obs_go_no_go",
            placeholder="e.g., Proceed if all pre-checks pass and no policy violations are detected",
        )

        st.subheader(
            "Will there be additional logic applied to state to determine if the automation can move forward?"
        )
        add_logic_choice = st.radio(
            "Additional gating logic?",
            ["No", "Yes"],
            horizontal=True,
            key="obs_add_logic_choice",
        )
        add_logic_text = ""
        if add_logic_choice == "Yes":
            add_logic_text = st.text_area(
                "Describe additional logic", key="obs_add_logic_text"
            )

        st.subheader("What tools will be used to support the observability layer?")
        cols_tools = st.columns(3)
        obs_tools_opts = [
            "SuzieQ Open Source",
            "SuzieQ Enterprise",
            "Network Vendor Product (Cisco Catalyst Center, Arista CVP, etc.)",
            "Custom Python Scripts",
        ]
        obs_tools_checks = {}
        for i, opt in enumerate(obs_tools_opts):
            with cols_tools[i % 3]:
                obs_tools_checks[opt] = st.checkbox(opt, key=f"obs_tool_{opt}")
        obs_tools_other_enabled = st.checkbox(
            "Other (fill in)", key="obs_tool_other_enable"
        )
        obs_tools_other = ""
        if obs_tools_other_enabled:
            obs_tools_other = st.text_input(
                "Other observability tool(s)", key="obs_tool_other_text"
            )

        # Compile selected observability tools before narrative
        selected_tools_obs = [k for k, v in obs_tools_checks.items() if v]
        if obs_tools_other_enabled and (obs_tools_other or "").strip():
            selected_tools_obs.append(obs_tools_other.strip())

        # Build method and go/no-go narratives
        selected_methods = [k for k, v in state_methods_checks.items() if v]
        methods_sentence = f"Network state will be determined via {_join(selected_methods)}."
        go_no_go_sentence = f"Go/No-Go criteria: {(go_no_go_text or '').strip() or 'TBD'}."

        if add_logic_choice == "Yes":
            additional_logic_sentence = f"Additional gating logic will be applied: {add_logic_text.strip() or 'TBD'}."
        else:
            additional_logic_sentence = (
                "No additional gating logic beyond the defined go/no-go criteria."
            )
        tools_sentence_obs = (
            f"Observability will be supported by {_join(selected_tools_obs)}."
        )

        utils.thick_hr(color="#6785a0", thickness=3)
        st.markdown("**Preview Solution Highlights**")
        st.write(methods_sentence)
        st.write(go_no_go_sentence)
        st.write(additional_logic_sentence)
        st.write(tools_sentence_obs)

        # Persist
        existing = st.session_state.get("solution_wizard", {})
        merged_obs = {
            **existing,
            "observability": {
                "methods": methods_sentence,
                "go_no_go": go_no_go_sentence,
                "additional_logic": additional_logic_sentence,
                "tools": tools_sentence_obs,
                "selections": {
                    "methods": selected_methods,
                    "go_no_go_text": go_no_go_text,
                    "additional_logic_enabled": add_logic_choice == "Yes",
                    "additional_logic_text": add_logic_text,
                    "tools": selected_tools_obs,
                },
            },
        }
        st.session_state["solution_wizard"] = merged_obs

        # Orchestration section

    # Orchestration section
    with st.expander("Orchestration", expanded=False):

        st.markdown(
            """
            Orchestration coordinates processes across framework components to create end-to-end workflows.
            Key capabilities typically include:
            - Event-driven execution (sync, async, scheduled)
            - Safe rollback/compensation on errors
            - Dry-run previews before execution
            - Scheduling (one-time or recurring)
            - Logging, tracing, and audit visibility
            - Optional event correlation and inference
            """
        )

        st.subheader("Will the solution utilize orchestration?")

        orch_choice = st.radio(
            "Select an option",
            ["No", "Yes – internal via custom scripts and logic", "Yes – provide details"],
            key="orch_choice",
            horizontal=False,
        )

        orch_details = ""
        if orch_choice == "Yes – provide details":
            orch_details = st.text_area(
                "Describe the orchestration approach",
                key="orch_details_text",
                placeholder="e.g., Use a workflow engine to trigger validations, approvals, execution, and post-checks; event-driven via webhooks; nightly reconciliations; rollback on failure; full traceability.",
            )

        # Narrative synthesis
        if orch_choice == "No":
            orch_sentence = (
                "This solution will not employ a distinct orchestration layer."
            )
        elif orch_choice == "Yes – internal via custom scripts and logic":
            orch_sentence = "Orchestration will be implemented internally using custom scripts and logic to coordinate end-to-end workflows."
        else:
            orch_sentence = (
                f"Orchestration will be utilized: {orch_details.strip() or 'TBD'}."
            )

        utils.thick_hr(color="#6785a0", thickness=3)
        st.markdown("**Preview Solution Highlights**")
        st.write(orch_sentence)

        # Persist
        existing = st.session_state.get("solution_wizard", {})
        merged_orch = {
            **existing,
            "orchestration": {
                "summary": orch_sentence,
                "selections": {
                    "choice": orch_choice,
                    "details": orch_details,
                },
            },
        }
        st.session_state["solution_wizard"] = merged_orch

    # Collector section
    with st.expander("Collector", expanded=False):
        st.markdown(
            """
            The collection layer focuses on retrieving the actual state of the network over time and ideally presenting it in a normalized format.
            - The collector can be thought of as a "read only" version of the executor.
            - It includes capabilities for retrieving live data from the network using read interfaces.
            - Retrieved data should be normalized across vendors and collection methods in a time series format.
            """
        )
        st.subheader("Collection methods (protocols/APIs)")
        cols_c1 = st.columns(3)
        collect_method_opts = [
            "SNMP",
            "CLI/SSH",
            "NETCONF",
            "gNMI",
            "REST API",
            "Webhooks",
            "Syslog",
            "Streaming Telemetry",
        ]
        collect_checks = {}
        for i, opt in enumerate(collect_method_opts):
            with cols_c1[i % 3]:
                collect_checks[opt] = st.checkbox(opt, key=f"collector_method_{opt}")

        st.subheader("Authentication")
        cols_c2 = st.columns(3)
        auth_opts = ["Username/Password", "SSH Keys", "OAuth2", "API Token", "mTLS"]
        auth_checks = {}
        for i, opt in enumerate(auth_opts):
            with cols_c2[i % 3]:
                auth_checks[opt] = st.checkbox(opt, key=f"collector_auth_{opt}")

        st.subheader("Traffic handling")
        cols_c3 = st.columns(3)
        handling_opts = [
            "Rate limiting",
            "Retries",
            "Exponential backoff",
            "Buffering/Queue",
        ]
        handling_checks = {}
        for i, opt in enumerate(handling_opts):
            with cols_c3[i % 3]:
                handling_checks[opt] = st.checkbox(opt, key=f"collector_handle_{opt}")

        st.subheader("Normalization and schemas")
        cols_c4 = st.columns(3)
        norm_opts = [
            "Timestamping",
            "Tagging/labels",
            "Topology enrichment",
            "Schema mapping",
        ]
        norm_checks = {}
        for i, opt in enumerate(norm_opts):
            with cols_c4[i % 3]:
                norm_checks[opt] = st.checkbox(opt, key=f"collector_norm_{opt}")

        # Collection tools (moved here from separate section)
        st.subheader("Collection tools")
        cols_ct = st.columns(3)
        tool_opts = [
            "SuzieQ",
            "Cisco Catalyst Center",
            "Cisco Nexus Dashboard",
            "Cisco ACI APIC",
            "Arista CVP",
            "Prometheus",
        ]
        tool_checks = {}
        for i, opt in enumerate(tool_opts):
            with cols_ct[i % 3]:
                tool_checks[opt] = st.checkbox(opt, key=f"collection_tool_{opt}")
        tools_other_enable = st.checkbox(
            "Other (fill in)", key="collection_tools_other_enable"
        )
        tools_other_text = ""
        if tools_other_enable:
            tools_other_text = st.text_input(
                "Other collection tool(s)", key="collection_tools_other"
            )

        st.subheader("Expected scale")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            devices = st.text_input(
                "Devices (approx)", key="collector_devices", placeholder="e.g., 500"
            )
        with col_s2:
            metrics = st.text_input(
                "Metrics/sec (approx)", key="collector_metrics", placeholder="e.g., 50k"
            )
        with col_s3:
            cadence = st.text_input(
                "Polling/stream cadence",
                key="collector_cadence",
                placeholder="e.g., 30s polling; streaming realtime",
            )

        selected_methods = [k for k, v in collect_checks.items() if v]
        selected_auth = [k for k, v in auth_checks.items() if v]
        selected_handling = [k for k, v in handling_checks.items() if v]
        selected_norm = [k for k, v in norm_checks.items() if v]
        selected_tools = [k for k, v in tool_checks.items() if v]
        if tools_other_enable and (tools_other_text or "").strip():
            selected_tools.append(tools_other_text.strip())

        methods_sentence = f"Collection will use {_join(selected_methods)}."
        auth_sentence = f"Authentication will leverage {_join(selected_auth)}."
        handling_sentence = f"Traffic handling will include {_join(selected_handling)}."
        norm_sentence = f"Collected data will be normalized via {_join(selected_norm)}."
        scale_sentence = f"Expected scale: ~{devices or 'TBD'} devices, ~{metrics or 'TBD'} metrics/sec, cadence {cadence or 'TBD'}."
        tools_sentence_coll = f"Collection tools will include {_join(selected_tools)}."

        utils.thick_hr(color="#6785a0", thickness=3)
        st.markdown("**Preview Solution Highlights**")
        st.write(methods_sentence)
        st.write(auth_sentence)
        st.write(handling_sentence)
        st.write(norm_sentence)
        st.write(scale_sentence)
        st.write(tools_sentence_coll)

        existing = st.session_state.get("solution_wizard", {})
        merged_col = {
            **existing,
            "collector": {
                "methods": methods_sentence,
                "auth": auth_sentence,
                "handling": handling_sentence,
                "normalization": norm_sentence,
                "scale": scale_sentence,
                "tools": tools_sentence_coll,
                "selections": {
                    "methods": selected_methods,
                    "auth": selected_auth,
                    "handling": selected_handling,
                    "normalization": selected_norm,
                    "devices": devices,
                    "metrics_per_sec": metrics,
                    "cadence": cadence,
                    "tools": selected_tools,
                },
            },
        }
        st.session_state["solution_wizard"] = merged_col

    # Executor section
    with st.expander("Executor", expanded=False):
        st.markdown(
            """
            The executor executes the actual changes to the network.
            - It MUST be capable of interacting with any supported network write interfaces (e.g., SSH/CLI, NETCONF, gNMI/gNOI, REST APIs).
            - It SHOULD support operations that alter network state, from deploying full/partial configs to device actions (reboots, upgrades).
            - Task input SHOULD originate from the intended state or be derived via data from Observability.
            - It SHOULD provide a dry‑run capability and support transactional execution.
            - It MAY support both imperative and declarative approaches, and operations SHOULD be idempotent.
            """
        )
        st.subheader("How will your solution execute change?")
        cols_exec = st.columns(2)
        exec_opts = [
            "Automating CLI interaction with Python automation frameworks (Netmiko, Napalm, Nornir, PyATS)",
            "Automating execution with a tool like Ansible",
            "Custom Python scripts",
            "Via manufacturer management application (Cisco DNA Center, Arista CVP)",
        ]
        exec_checks = {}
        for i, opt in enumerate(exec_opts):
            with cols_exec[i % 2]:
                exec_checks[opt] = st.checkbox(opt, key=f"exec_{i}")
        with cols_exec[0]:
            exec_custom_enable = st.checkbox(
                "Custom (describe in detail)", key="exec_custom_enable"
            )
            exec_custom_text = ""
            if exec_custom_enable:
                exec_custom_text = st.text_area(
                    "Custom execution approach", key="exec_custom_text"
                )

        selected_exec = [k for k, v in exec_checks.items() if v]
        if exec_custom_enable and exec_custom_text.strip():
            selected_exec.append(exec_custom_text.strip())

        exec_sentence = f"Execution will be performed using {_join(selected_exec)}."

        utils.thick_hr(color="#6785a0", thickness=3)
        st.markdown("**Preview Solution Highlights**")
        st.write(exec_sentence)

        existing = st.session_state.get("solution_wizard", {})
        merged_exec = {
            **existing,
            "executor": {
                "methods": exec_sentence,
                "selections": {
                    "methods": selected_exec,
                },
            },
        }
        st.session_state["solution_wizard"] = merged_exec

    # Transition to external interfaces and planning
    utils.thick_hr(color="grey", thickness=5)
    st.markdown(
        "While the framework helps you think about the technical implementation, for a complete project let's now consider external interfaces, staffing, and timelines."
    )

    # Dependencies & External Interfaces (shared across pages)
    with st.expander("Dependencies & External Interfaces", expanded=False):
        st.caption(
            "Select the external systems this automation will interact with and add details where applicable."
        )

        # Initialize or reuse shared dependency definitions
        if "dep_defs" not in st.session_state:
            st.session_state["dep_defs"] = [
                {
                    "key": "network_infra",
                    "label": "Network Infrastructure",
                    "default": True,
                    "details": False,
                    "help": "The automation will act on some or all of the organization's network infrastructure (switches, appliances, routers, etc.).",
                },
                {
                    "key": "network_controllers",
                    "label": "Network Controllers",
                    "default": False,
                    "details": True,
                    "help": "Controller platforms that abstract device APIs (e.g., Cisco APIC/ND). Provide which controller(s) and scope.",
                },
                {
                    "key": "revision_control",
                    "label": "Revision Control system",
                    "default": True,
                    "details": True,
                    "help": "System for versioning configuration/templates and code (e.g., GitHub, GitLab, Bitbucket).",
                    "default_detail": "GitHub",
                },
                {
                    "key": "itsm",
                    "label": "ITSM/Change Management System",
                    "default": False,
                    "details": True,
                    "help": "Ticketing/approval workflow (e.g., ServiceNow, Jira Service Management). Include integration points.",
                },
                {
                    "key": "authn",
                    "label": "Authentication System",
                    "default": False,
                    "details": True,
                    "help": "Identity/RBAC, secrets, SSO (e.g., Okta, Azure AD, LDAP, Vault). Specify how access is controlled.",
                },
                {
                    "key": "ipams",
                    "label": "IPAMS Systems",
                    "default": False,
                    "details": True,
                    "help": "IP address management and DNS (e.g., Infoblox, BlueCat). Describe lookups/updates involved.",
                },
                {
                    "key": "inventory",
                    "label": "Inventory Systems",
                    "default": False,
                    "details": True,
                    "help": "Source of truth/CMDB/inventory (e.g., NetBox, InfraHub, ServiceNow CMDB). What data do you read/write?",
                },
                {
                    "key": "design_intent",
                    "label": "Design Data/Intent Systems",
                    "default": False,
                    "details": True,
                    "help": "Systems holding golden intent or design models (InfraHub, Custom DB).",
                },
                {
                    "key": "observability",
                    "label": "Observability System",
                    "default": False,
                    "details": True,
                    "help": "Telemetry/monitoring/logs/traces (e.g., SuzieQ, Prometheus).",
                },
                {
                    "key": "vendor_mgmt",
                    "label": "Vendor Tool/Management System",
                    "default": False,
                    "details": True,
                    "help": "(e.g., Cisco DNAC, Wireless Controllers, Miraki, Arista CVP, Aruba Central, Juniper Apstra).",
                },
            ]
        dep_defs = st.session_state["dep_defs"]

        deps_selected = []
        for d in dep_defs:
            checked = st.checkbox(
                d["label"],
                key=f"dep_{d['key']}",
                value=bool(
                    st.session_state.get(f"dep_{d['key']}", d.get("default", False))
                ),
                help=d.get("help"),
            )
            detail_text = ""
            if checked and d.get("details"):
                default_detail = d.get("default_detail", "")
                if d["key"] == "revision_control":
                    default_detail = "GitHub"
                detail_text = st.text_input(
                    f"Details for {d['label']}",
                    value=str(
                        st.session_state.get(f"dep_{d['key']}_details", default_detail)
                    ),
                    key=f"dep_{d['key']}_details",
                )
            if checked:
                deps_selected.append(
                    {"name": d["label"], "details": (detail_text or "").strip()}
                )

        # Persist into wizard payload
        existing = st.session_state.get("solution_wizard", {})
        merged_deps = {
            **existing,
            "dependencies": deps_selected,
        }
        st.session_state["solution_wizard"] = merged_deps

    # Staffing, Timeline, & Milestones
    with st.expander("Staffing, Timeline, & Milestones", expanded=False):
        st.caption(
            "Capture a high-level plan with durations in business days. Start date drives scheduled dates."
        )
        st.info(
            "Duration should reflect expected staffing. For example, if a step is 10 business days of work but two people will work in parallel, you may model it as 5–6 days to allow for coordination overhead."
        )

        st.subheader("Staffing plan")
        st.caption("Provide expected direct staffing and a short plan. Markdown is supported.")
        col_sp1, col_sp2 = st.columns([1, 3])
        with col_sp1:
            staff_count = st.number_input(
                "Direct staff on project",
                min_value=0,
                value=int(st.session_state.get("timeline_staff_count", 1)),
                step=1,
                key="_timeline_staff_count",
            )
            st.session_state["timeline_staff_count"] = int(staff_count)
        with col_sp2:
            staffing_plan = st.text_area(
                "Staffing plan (markdown supported)",
                value=str(st.session_state.get("timeline_staffing_plan", "")),
                height=120,
                key="_timeline_staffing_plan",
            )
            st.session_state["timeline_staffing_plan"] = staffing_plan

        # Holiday calendar selector (lightweight)
        region_options = [
            "None",
            "United States",
            "Canada",
            "United Kingdom",
            "Germany",
            "India",
            "Australia",
        ]
        holiday_region = st.selectbox(
            "Holiday calendar",
            options=region_options,
            index=region_options.index(
                st.session_state.get("timeline_holiday_region", "None")
                if st.session_state.get("timeline_holiday_region", "None") in region_options
                else "None"
            ),
            help="Used to skip public holidays when computing business days.",
            key="_timeline_holiday_region",
        )
        st.session_state["timeline_holiday_region"] = holiday_region

        def _build_holiday_set(start_year: int, years_ahead: int = 2):
            if _hol is None or holiday_region == "None":
                return set()
            years = list(range(start_year, start_year + max(1, years_ahead) + 1))
            cal = None
            try:
                if holiday_region == "United States":
                    cal = _hol.UnitedStates(years=years)
                elif holiday_region == "Canada":
                    cal = _hol.Canada(years=years)
                elif holiday_region == "United Kingdom":
                    cal = _hol.UnitedKingdom(years=years)
                elif holiday_region == "Germany":
                    cal = _hol.Germany(years=years)
                elif holiday_region == "India":
                    cal = _hol.India(years=years)
                elif holiday_region == "Australia":
                    cal = _hol.Australia(years=years)
            except Exception:
                cal = None
            return set(cal.keys()) if cal else set()

        # Helper: add business days (Mon–Fri), with optional holidays
        def _add_business_days(d, n, holiday_set=None):
            from datetime import timedelta

            days = int(n or 0)
            cur = d
            while days > 0:
                cur = cur + timedelta(days=1)
                if cur.weekday() < 5 and (holiday_set is None or cur not in holiday_set):  # Mon=0 .. Sun=6
                    days -= 1
            return cur

        # Start date
        default_start = st.session_state.get("timeline_start_date")
        start_date = st.date_input(
            "Project start date",
            value=default_start or datetime.today().date(),
            key="_timeline_start_date_input",
        )
        st.session_state["timeline_start_date"] = start_date

        # Milestones state
        if "timeline_milestones" not in st.session_state:
            st.session_state["timeline_milestones"] = [
                {"name": "Planning", "duration": 5, "notes": ""},
                {"name": "Design", "duration": 10, "notes": ""},
                {"name": "Build", "duration": 10, "notes": ""},
                {"name": "Test", "duration": 5, "notes": ""},
                {"name": "Pilot", "duration": 5, "notes": ""},
                {"name": "Production Rollout", "duration": 10, "notes": ""},
            ]

        # Controls
        c_a, c_b = st.columns([1, 1])
        with c_a:
            if st.button("Add milestone row", key="_timeline_add_row"):
                st.session_state["timeline_milestones"].append(
                    {"name": "", "duration": 0, "notes": ""}
                )
        with c_b:
            st.caption("Use the fields below to edit milestone name, duration (business days), and notes.")

        # Render rows
        to_delete = []
        for idx, row in enumerate(list(st.session_state["timeline_milestones"])):
            rcols = st.columns([3, 2, 5, 1])
            with rcols[0]:
                row_name = st.text_input(
                    "Milestone",
                    value=str(row.get("name", "")),
                    key=f"_tl_name_{idx}",
                )
            with rcols[1]:
                row_duration = st.number_input(
                    "Duration (business days)",
                    min_value=0,
                    value=int(row.get("duration", 0)),
                    step=1,
                    key=f"_tl_duration_{idx}",
                )
            with rcols[2]:
                row_notes = st.text_input(
                    "Notes/comments",
                    value=str(row.get("notes", "")),
                    key=f"_tl_notes_{idx}",
                )
            with rcols[3]:
                del_flag = st.checkbox("Delete", key=f"_tl_del_{idx}")
                if del_flag:
                    to_delete.append(idx)

            # Persist edits back to state
            st.session_state["timeline_milestones"][idx] = {
                "name": row_name,
                "duration": int(row_duration),
                "notes": row_notes,
            }

        # Apply deletions (from end to start)
        for i in sorted(to_delete, reverse=True):
            if 0 <= i < len(st.session_state["timeline_milestones"]):
                st.session_state["timeline_milestones"].pop(i)

        # Build schedule
        schedule = []
        cursor = start_date
        holiday_set = _build_holiday_set(start_date.year, years_ahead=3)
        total_bd = 0
        for row in st.session_state["timeline_milestones"]:
            name = (row.get("name") or "").strip()
            dur = int(row.get("duration") or 0)
            notes = row.get("notes") or ""
            if not name and dur <= 0:
                continue
            start = cursor
            end = _add_business_days(start, dur, holiday_set) if dur > 0 else start
            schedule.append(
                {
                    "name": name or "(Unnamed)",
                    "duration_bd": dur,
                    "start": start,
                    "end": end,
                    "notes": notes,
                }
            )
            cursor = end  # next starts after this completes
            total_bd += max(0, dur)

        # Summary & display
        if schedule:
            st.markdown("**Timeline summary (business days only)**")
            st.write(
                f"Start: {start_date.strftime('%Y-%m-%d')} • Total duration: {total_bd} business days • Projected completion: {schedule[-1]['end'].strftime('%Y-%m-%d')}"
            )
            # Success/info callouts
            st.success(f"Expected delivery date: {schedule[-1]['end'].strftime('%Y-%m-%d')}")
            months_est = total_bd / 21.75 if total_bd else 0.0  # approx working days per month
            years_est = months_est / 12.0 if months_est else 0.0
            st.info(
                f"Approximate duration: {months_est:.1f} months ({years_est:.2f} years) based on business days"
            )

            st.markdown("**Milestones schedule**")
            for item in schedule:
                st.write(
                    f"- {item['name']}: {item['start'].strftime('%Y-%m-%d')} → {item['end'].strftime('%Y-%m-%d')} ({item['duration_bd']} bd)"
                )

            # Optional: Visual timeline
            show_chart = st.checkbox("Show Gantt chart", value=True, key="_timeline_show_chart")
            if show_chart:
                df = pd.DataFrame(
                    [
                        {
                            "Task": it["name"],
                            "Start": it["start"],
                            "Finish": it["end"],
                            "Duration (bd)": it["duration_bd"],
                        }
                        for it in schedule
                    ]
                )
                if not df.empty:
                    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Task")
                    fig.update_yaxes(autorange="reversed")  # earliest at top
                    fig.update_layout(height=380, margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add at least one milestone to build a timeline.")

        # Persist into wizard payload
        existing = st.session_state.get("solution_wizard", {})
        merged_tl = {
            **existing,
            "timeline": {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "total_business_days": total_bd,
                "projected_completion": schedule[-1]["end"].strftime("%Y-%m-%d") if schedule else None,
                "staff_count": int(st.session_state.get("timeline_staff_count", 0)),
                "staffing_plan_md": st.session_state.get("timeline_staffing_plan", ""),
                "holiday_region": holiday_region,
                "items": [
                    {
                        "name": i["name"],
                        "duration_bd": i["duration_bd"],
                        "start": i["start"].strftime("%Y-%m-%d"),
                        "end": i["end"].strftime("%Y-%m-%d"),
                        "notes": i["notes"],
                    }
                    for i in schedule
                ],
            },
        }
        st.session_state["solution_wizard"] = merged_tl

    # Live narrative preview
    utils.thick_hr(color="grey", thickness=5)
    st.subheader("Solution Highlights")
    payload = st.session_state.get("solution_wizard", {})

    def _md_line(text: str) -> str:
        # Delegate to shared tested helper
        return md_line(text)

    def _is_meaningful(text: str) -> bool:
        # Delegate to shared tested helper
        return is_meaningful(text)

    any_content = False

    pres = payload.get("presentation", {})
    if pres:
        sec_lines = []
        if pres.get("users") and _is_meaningful(pres.get("users")):
            sec_lines.append(_md_line(pres.get("users")))
        if pres.get("interaction") and _is_meaningful(pres.get("interaction")):
            sec_lines.append(_md_line(pres.get("interaction")))
        if pres.get("tools") and _is_meaningful(pres.get("tools")):
            sec_lines.append(_md_line(pres.get("tools")))
        if pres.get("auth") and _is_meaningful(pres.get("auth")):
            sec_lines.append(_md_line(pres.get("auth")))
        if sec_lines:
            any_content = True
            st.markdown("**Presentation**")
            st.markdown("\n".join(sec_lines))

    intent = payload.get("intent", {})
    if intent:
        sec_lines = []
        if intent.get("development") and _is_meaningful(intent.get("development")):
            sec_lines.append(_md_line(intent.get("development")))
        if intent.get("provided") and _is_meaningful(intent.get("provided")):
            sec_lines.append(_md_line(intent.get("provided")))
        if sec_lines:
            any_content = True
            st.markdown("**Intent**")
            st.markdown("\n".join(sec_lines))

    obs = payload.get("observability", {})
    if obs:
        sec_lines = []
        if obs.get("methods") and _is_meaningful(obs.get("methods")):
            sec_lines.append(_md_line(obs.get("methods")))
        if obs.get("go_no_go") and _is_meaningful(obs.get("go_no_go")):
            sec_lines.append(_md_line(obs.get("go_no_go")))
        if obs.get("additional_logic") and _is_meaningful(obs.get("additional_logic")):
            sec_lines.append(_md_line(obs.get("additional_logic")))
        if obs.get("tools") and _is_meaningful(obs.get("tools")):
            sec_lines.append(_md_line(obs.get("tools")))
        if sec_lines:
            any_content = True
            st.markdown("**Observability**")
            st.markdown("\n".join(sec_lines))

    orch = payload.get("orchestration", {})
    if orch:
        sec_lines = []
        if orch.get("summary") and _is_meaningful(orch.get("summary")):
            sec_lines.append(_md_line(orch.get("summary")))
        if sec_lines:
            any_content = True
            st.markdown("**Orchestration**")
            st.markdown("\n".join(sec_lines))

    executor = payload.get("executor", {})
    if executor:
        sec_lines = []
        if executor.get("methods") and _is_meaningful(executor.get("methods")):
            sec_lines.append(_md_line(executor.get("methods")))
        if sec_lines:
            any_content = True
            st.markdown("**Executor**")
            st.markdown("\n".join(sec_lines))

    collector = payload.get("collector", {})
    if collector:
        sec_lines = []
        if collector.get("methods") and _is_meaningful(collector.get("methods")):
            sec_lines.append(_md_line(collector.get("methods")))
        if collector.get("auth") and _is_meaningful(collector.get("auth")):
            sec_lines.append(_md_line(collector.get("auth")))
        if collector.get("handling") and _is_meaningful(collector.get("handling")):
            sec_lines.append(_md_line(collector.get("handling")))
        if collector.get("normalization") and _is_meaningful(
            collector.get("normalization")
        ):
            sec_lines.append(_md_line(collector.get("normalization")))
        if collector.get("scale") and _is_meaningful(collector.get("scale")):
            sec_lines.append(_md_line(collector.get("scale")))
        if sec_lines:
            any_content = True
            st.markdown("**Collector**")
            st.markdown("\n".join(sec_lines))

    # Staffing, Timeline block in highlights
    timeline = payload.get("timeline")
    if timeline:
        # Determine if timeline appears to be default/unmodified
        default_items = [
            {"name": "Planning", "duration_bd": 5},
            {"name": "Design", "duration_bd": 10},
            {"name": "Build", "duration_bd": 10},
            {"name": "Test", "duration_bd": 5},
            {"name": "Pilot", "duration_bd": 5},
            {"name": "Production Rollout", "duration_bd": 10},
        ]
        items_slim = [
            {"name": (i or {}).get("name"), "duration_bd": (i or {}).get("duration_bd")}
            for i in (timeline.get("items") or [])
        ]
        looks_default_items = items_slim == default_items
        staff_ct = timeline.get("staff_count")
        plan_md = (timeline.get("staffing_plan_md") or "").strip()
        looks_default_staff = (staff_ct == 1) and (plan_md == "")

        is_default_timeline = looks_default_items and looks_default_staff

        lines = []
        start = timeline.get("start_date")
        total_bd = timeline.get("total_business_days")
        end = timeline.get("projected_completion")
        header = f"Staff {staff_ct if staff_ct is not None else 'TBD'} • Start {start or 'TBD'} • Total {total_bd if total_bd is not None else 'TBD'} bd • Completion {end or 'TBD'}"
        if not is_default_timeline:
            lines.append(_md_line(header))
            if plan_md:
                lines.append(_md_line("Staffing plan:"))
                # indent the plan to render as a sub-bullet
                for pl in plan_md.splitlines()[:8]:  # cap lines for brevity
                    lines.append(f"  - {pl}")
            for i in (timeline.get("items") or [])[:15]:  # cap to 15 for display brevity
                lines.append(
                    _md_line(
                        f"{i.get('name')}: {i.get('start')} → {i.get('end')} ({i.get('duration_bd')} bd)"
                    )
                )
            if lines:
                any_content = True
                st.markdown("**Staffing, Timeline, & Milestones**")
                st.markdown("\n".join(lines))

    # Dependencies block in highlights (suppress if still defaults)
    deps = payload.get("dependencies", [])
    if deps:
        # Build slim list for default detection
        deps_slim = [
            {"name": (d or {}).get("name"), "details": (d or {}).get("details", "").strip()}
            for d in deps
            if (d or {}).get("name")
        ]
        # Default selections present at first render
        default_deps = [
            {"name": "Network Infrastructure", "details": ""},
            {"name": "Revision Control system", "details": "GitHub"},
        ]
        def _sorted(items):
            return sorted(items, key=lambda x: (x.get("name") or "", x.get("details") or ""))
        looks_default_deps = _sorted(deps_slim) == _sorted(default_deps)

        dep_lines = []
        if not looks_default_deps:
            for d in deps_slim:
                nm = d.get("name")
                dt = d.get("details")
                if nm:
                    dep_lines.append(_md_line(f"{nm}: {dt}" if dt else f"{nm}"))

        if dep_lines:
            any_content = True
            st.markdown("**Dependencies & External Interfaces**")
            st.markdown("\n".join(dep_lines))

    if not any_content:
        st.info("Start filling in the sections above to see Solution Highlights here.")

    # Final download (all blocks) — only when there is meaningful content
    if any_content:
        st.markdown("---")
        st.subheader("Export Solution Wizard")
        final_payload = payload
        final_json_bytes = json.dumps(final_payload, indent=2).encode("utf-8")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button(
            label="Download Wizard JSON",
            data=final_json_bytes,
            file_name=f"solution_wizard_{ts}.json",
            mime="application/json",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
