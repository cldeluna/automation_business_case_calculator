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


def _join(items):
    items = [i for i in items if i]
    if not items:
        return "TBD"
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + f" and {items[-1]}"


def main():
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
            ### Intent or the abstracted version of what you are trying to do
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
                "Other observability tool(s)", key="obs_tool_other"
            )

        # Narrative synthesis

        selected_methods = [k for k, v in state_methods_checks.items() if v]
        selected_tools = [k for k, v in obs_tools_checks.items() if v]
        if obs_tools_other_enabled and obs_tools_other.strip():
            selected_tools.append(obs_tools_other.strip())

        methods_sentence = (
            f"Network state will be determined via {_join(selected_methods)}."
        )
        go_no_go_sentence = f"Go/No-Go logic: {go_no_go_text.strip() or 'TBD'}."
        if add_logic_choice == "Yes":
            additional_logic_sentence = f"Additional gating logic will be applied: {add_logic_text.strip() or 'TBD'}."
        else:
            additional_logic_sentence = (
                "No additional gating logic beyond the defined go/no-go criteria."
            )
        tools_sentence_obs = (
            f"Observability will be supported by {_join(selected_tools)}."
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
                    "tools": selected_tools,
                },
            },
        }
        st.session_state["solution_wizard"] = merged_obs

        # Orchestration section

    # Orchestration section
    with st.expander("Orchestration", expanded=False):
        st.subheader("Will the solution utilize orchestration?")
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

        orch_choice = st.radio(
            "Select an option",
            ["No", "Yes – internal via custom scripts", "Yes – provide details"],
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

        methods_sentence = f"Collection will use {_join(selected_methods)}."
        auth_sentence = f"Authentication will leverage {_join(selected_auth)}."
        handling_sentence = f"Traffic handling will include {_join(selected_handling)}."
        norm_sentence = f"Collected data will be normalized via {_join(selected_norm)}."
        scale_sentence = f"Expected scale: ~{devices or 'TBD'} devices, ~{metrics or 'TBD'} metrics/sec, cadence {cadence or 'TBD'}."

        utils.thick_hr(color="#6785a0", thickness=3)
        st.markdown("**Preview Solution Highlights**")
        st.write(methods_sentence)
        st.write(auth_sentence)
        st.write(handling_sentence)
        st.write(norm_sentence)
        st.write(scale_sentence)

        existing = st.session_state.get("solution_wizard", {})
        merged_col = {
            **existing,
            "collector": {
                "methods": methods_sentence,
                "auth": auth_sentence,
                "handling": handling_sentence,
                "normalization": norm_sentence,
                "scale": scale_sentence,
                "selections": {
                    "methods": selected_methods,
                    "auth": selected_auth,
                    "handling": selected_handling,
                    "normalization": selected_norm,
                    "devices": devices,
                    "metrics_per_sec": metrics,
                    "cadence": cadence,
                },
            },
        }
        st.session_state["solution_wizard"] = merged_col

    # Executor section (moved after Collector)
    with st.expander("Executor", expanded=False):
        st.markdown(
            """
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

    # Live narrative preview
    utils.thick_hr(color="grey", thickness=5)
    st.subheader("Solution Highlights")
    payload = st.session_state.get("solution_wizard", {})

    def _md_line(text: str) -> str:
        return f"- {text}" if text else ""

    def _is_meaningful(text: str) -> bool:
        if not text:
            return False
        t = text.strip().lower()
        if "tbd" in t:
            return False
        default_placeholders = {
            "no additional gating logic beyond the defined go/no-go criteria.",
            "this solution will not employ a distinct orchestration layer.",
        }
        return t not in default_placeholders

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

    # Dependencies block in highlights
    deps = payload.get("dependencies", [])
    if deps:
        dep_lines = []
        for d in deps:
            name = (d or {}).get("name")
            details = (d or {}).get("details")
            if name:
                if details:
                    dep_lines.append(_md_line(f"{name}: {details}"))
                else:
                    dep_lines.append(_md_line(f"{name}"))
        if dep_lines:
            any_content = True
            st.markdown("**Dependencies & External Interfaces**")
            st.markdown("\n".join(dep_lines))

    if not any_content:
        st.info(
            "Work through the Automation Framework functions/layers to see highlights here."
        )

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
