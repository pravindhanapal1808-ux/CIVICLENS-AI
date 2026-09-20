import streamlit as st
from PIL import Image
from streamlit_geolocation import streamlit_geolocation
import urllib.request
import urllib.parse
import json

from ai_engine import analyze_image
from database import create_database, add_report, get_reports


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

create_database()


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CIVICLENS AI",
    page_icon="🏙️",
    layout="wide"
)


# ============================================================
# SMART PRIORITY ENGINE
# ============================================================

def calculate_priority(severity, impact_score):

    if severity == "HIGH" and impact_score >= 8:
        return "CRITICAL", 95

    elif severity == "HIGH":
        return "HIGH", 80

    elif severity == "MEDIUM" and impact_score >= 6:
        return "HIGH", 70

    elif severity == "MEDIUM":
        return "MEDIUM", 55

    else:
        return "LOW", 30


# ============================================================
# AUTHORITY ACTION CENTER
# ============================================================

def get_authority_action(issue, priority):

    issue_lower = issue.lower()

    if "pothole" in issue_lower or "road" in issue_lower:

        department = "🏗️ Roads & Infrastructure"

        action = (
            "Inspect and repair the damaged road section. "
            "Check surrounding road conditions and ensure public safety."
        )

    elif "garbage" in issue_lower:

        department = "🧹 Sanitation Department"

        action = (
            "Arrange waste collection and inspect the area. "
            "Check whether additional waste-management measures are required."
        )

    elif "streetlight" in issue_lower or "light" in issue_lower:

        department = "💡 Electrical / Street Lighting Department"

        action = (
            "Inspect the streetlight, identify the electrical fault, "
            "and restore lighting service."
        )

    elif "fallen tree" in issue_lower or "tree" in issue_lower:

        department = "🌳 Parks / Disaster Response Department"

        action = (
            "Remove the fallen tree and secure the affected area. "
            "Check for hazards to pedestrians and vehicles."
        )

    else:

        department = "🏛️ Municipal Civic Services"

        action = (
            "Conduct a field inspection and assign the appropriate "
            "municipal service team."
        )

    if priority == "CRITICAL":

        urgency = "🚨 IMMEDIATE"
        response_time = "Within 24 hours"

    elif priority == "HIGH":

        urgency = "🔴 URGENT"
        response_time = "Within 48 hours"

    elif priority == "MEDIUM":

        urgency = "🟡 SCHEDULED"
        response_time = "Within 7 days"

    else:

        urgency = "🟢 MONITOR"
        response_time = "During routine maintenance"

    return department, action, urgency, response_time


# ============================================================
# REVERSE GEOCODING
# ============================================================

def get_address(latitude, longitude):

    try:

        url = (
            "https://nominatim.openstreetmap.org/reverse?"
            + urllib.parse.urlencode({
                "lat": latitude,
                "lon": longitude,
                "format": "jsonv2",
                "addressdetails": 1
            })
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "CivicLens-AI-Hackathon/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=10
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        address_data = data.get(
            "address",
            {}
        )

        parts = []

        for key in [
            "road",
            "suburb",
            "city",
            "town",
            "village",
            "state",
            "postcode"
        ]:

            value = address_data.get(key)

            if value and value not in parts:
                parts.append(value)

        if parts:

            return ", ".join(parts)

        return data.get(
            "display_name",
            "Address not available"
        )

    except Exception:

        return "Address not available"


# ============================================================
# GENERATE INCIDENT REPORT
# ============================================================

def generate_incident_report(
    report_id,
    issue,
    description,
    severity,
    impact_score,
    priority,
    priority_score,
    location,
    latitude,
    longitude,
    department,
    authority_action,
    urgency,
    response_time
):

    gps_text = "Not available"

    if (
        latitude is not None
        and longitude is not None
    ):

        gps_text = (
            f"{latitude:.6f}, "
            f"{longitude:.6f}"
        )

    report = f"""
============================================================
                    CIVICLENS AI
                CIVIC INCIDENT REPORT
============================================================

Report ID:
#{report_id}

------------------------------------------------------------
ISSUE INFORMATION
------------------------------------------------------------

Issue:
{issue}

AI Description:
{description}

Severity:
{severity}

Impact Score:
{impact_score}/10

------------------------------------------------------------
SMART PRIORITY
------------------------------------------------------------

Priority:
{priority}

Priority Score:
{priority_score}/100

------------------------------------------------------------
LOCATION
------------------------------------------------------------

Address:
{location}

GPS Coordinates:
{gps_text}

------------------------------------------------------------
AUTHORITY ACTION
------------------------------------------------------------

Responsible Department:
{department}

Recommended Action:
{authority_action}

Urgency:
{urgency}

Expected Response:
{response_time}

------------------------------------------------------------
SYSTEM RECOMMENDATION
------------------------------------------------------------

This report was analyzed and prioritized by CIVICLENS AI.

The priority score is an AI-assisted recommendation
intended to help organize civic issue response.

============================================================
              CIVICLENS AI
        "See a problem. Understand it. Solve it."
============================================================
"""

    return report


# ============================================================
# HEADER
# ============================================================

st.title("🏙️ CIVICLENS AI")

st.subheader(
    "See a problem. Understand it. Solve it."
)

st.write(
    "AI-powered civic issue detection and intelligent "
    "municipal prioritization system."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("CIVICLENS AI")

st.sidebar.write(
    "Smart Civic Problem Management"
)

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Report Issue",
        "📊 Dashboard",
        "🗺️ Civic Map",
        "🏛️ Authority Center",
        "📄 Incident Reports"
    ]
)


# ============================================================
# PAGE 1 — REPORT ISSUE
# ============================================================

if page == "🏠 Report Issue":

    st.header("📸 Report a Civic Issue")

    st.write(
        "Upload an image of a civic problem. "
        "CIVICLENS AI will analyze it and generate "
        "a smart priority recommendation."
    )

    uploaded_file = st.file_uploader(
        "Upload civic issue image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Civic Issue",
            width=500
        )

        st.divider()

        # ----------------------------------------------------
        # GPS
        # ----------------------------------------------------

        st.subheader(
            "📍 Detect Location"
        )

        location_data = streamlit_geolocation()

        latitude = None
        longitude = None
        accuracy = None

        if location_data:

            latitude = location_data.get(
                "latitude"
            )

            longitude = location_data.get(
                "longitude"
            )

            accuracy = location_data.get(
                "accuracy"
            )

        if (
            latitude is not None
            and longitude is not None
        ):

            st.success(
                "📍 GPS location detected"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Latitude",
                    f"{latitude:.6f}"
                )

            with col2:

                st.metric(
                    "Longitude",
                    f"{longitude:.6f}"
                )

            with col3:

                if accuracy:

                    st.metric(
                        "Accuracy",
                        f"{accuracy:.1f} m"
                    )

                else:

                    st.metric(
                        "Accuracy",
                        "N/A"
                    )

            with st.spinner(
                "Finding approximate address..."
            ):

                address = get_address(
                    latitude,
                    longitude
                )

            st.info(
                f"📍 **Detected Address:** {address}"
            )

        else:

            st.warning(
                "📍 Location not detected. "
                "Please allow browser location permission."
            )

            address = "Location not available"

        st.divider()

        # ----------------------------------------------------
        # ANALYZE BUTTON
        # ----------------------------------------------------

        if st.button(
            "🤖 Analyze & Submit Report",
            use_container_width=True
        ):

            with st.spinner(
                "CIVICLENS AI is analyzing the image..."
            ):

                issue, description = analyze_image(
                    image
                )

            # ------------------------------------------------
            # SEVERITY + IMPACT
            # ------------------------------------------------

            issue_lower = issue.lower()

            if (
                "pothole" in issue_lower
                or "fallen tree" in issue_lower
            ):

                severity = "HIGH"
                impact_score = 9.0

            elif (
                "streetlight" in issue_lower
                or "road" in issue_lower
            ):

                severity = "MEDIUM"
                impact_score = 7.0

            elif "garbage" in issue_lower:

                severity = "MEDIUM"
                impact_score = 6.5

            else:

                severity = "LOW"
                impact_score = 4.0

            # ------------------------------------------------
            # PRIORITY
            # ------------------------------------------------

            priority, priority_score = calculate_priority(
                severity,
                impact_score
            )

            # ------------------------------------------------
            # RECOMMENDATION
            # ------------------------------------------------

            if priority == "CRITICAL":

                recommendation = (
                    "Immediate attention required. "
                    "The issue may create significant public risk."
                )

            elif priority == "HIGH":

                recommendation = (
                    "Inspect and resolve the issue as soon as possible."
                )

            elif priority == "MEDIUM":

                recommendation = (
                    "Schedule an inspection and corrective action."
                )

            else:

                recommendation = (
                    "Monitor the issue and address during "
                    "routine maintenance."
                )

            # ------------------------------------------------
            # AUTHORITY ACTION
            # ------------------------------------------------

            (
                department,
                authority_action,
                urgency,
                response_time
            ) = get_authority_action(
                issue,
                priority
            )

            # ------------------------------------------------
            # SAVE REPORT
            # ------------------------------------------------

            add_report(
                issue,
                description,
                severity,
                impact_score,
                recommendation,
                address,
                latitude,
                longitude
            )

            # ------------------------------------------------
            # GET NEW REPORT ID
            # ------------------------------------------------

            reports_after_save = get_reports()

            if reports_after_save:

                report_id = reports_after_save[0][0]

            else:

                report_id = "N/A"

            # ------------------------------------------------
            # DISPLAY RESULTS
            # ------------------------------------------------

            st.success(
                "✅ Civic issue analyzed and saved successfully!"
            )

            st.divider()

            st.subheader(
                "🤖 AI Analysis"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                    f"### {issue}"
                )

                st.write(
                    f"**Description:** {description}"
                )

            with col2:

                st.metric(
                    "Severity",
                    severity
                )

                st.metric(
                    "Impact Score",
                    f"{impact_score}/10"
                )

            st.divider()

            # ------------------------------------------------
            # PRIORITY
            # ------------------------------------------------

            st.subheader(
                "🧠 Smart Priority Engine"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Priority",
                    priority
                )

            with col2:

                st.metric(
                    "Priority Score",
                    f"{priority_score}/100"
                )

            with col3:

                st.metric(
                    "Severity",
                    severity
                )

            st.progress(
                int(priority_score) / 100
            )

            st.info(
                f"💡 **Recommendation:** "
                f"{recommendation}"
            )

            st.divider()

            # ------------------------------------------------
            # AUTHORITY
            # ------------------------------------------------

            st.subheader(
                "🏛️ Authority Action Center"
            )

            st.success(
                f"**Responsible Department:** "
                f"{department}"
            )

            st.write(
                "### 🔧 Recommended Action"
            )

            st.write(
                authority_action
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Urgency",
                    urgency
                )

            with col2:

                st.metric(
                    "Expected Response",
                    response_time
                )

            st.divider()

            # ------------------------------------------------
            # LOCATION
            # ------------------------------------------------

            st.subheader(
                "📍 Location Information"
            )

            st.write(
                f"**Address:** {address}"
            )

            if (
                latitude is not None
                and longitude is not None
            ):

                st.write(
                    f"**GPS:** "
                    f"{latitude:.6f}, "
                    f"{longitude:.6f}"
                )

            # ------------------------------------------------
            # DOWNLOAD REPORT
            # ------------------------------------------------

            st.divider()

            st.subheader(
                "📄 Civic Incident Report"
            )

            incident_report = generate_incident_report(
                report_id,
                issue,
                description,
                severity,
                impact_score,
                priority,
                priority_score,
                address,
                latitude,
                longitude,
                department,
                authority_action,
                urgency,
                response_time
            )

            st.download_button(
                label="📄 Download Civic Incident Report",
                data=incident_report,
                file_name=f"civic_incident_report_{report_id}.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.success(
                f"📄 Incident Report #{report_id} generated successfully!"
            )


# ============================================================
# PAGE 2 — DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    st.header(
        "📊 Civic Intelligence Dashboard"
    )

    reports = get_reports()

    if not reports:

        st.info(
            "No civic reports available yet."
        )

    else:

        total_reports = len(reports)

        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0

        for report in reports:

            severity = report[3]
            impact_score = report[4]

            priority, score = calculate_priority(
                severity,
                impact_score
            )

            if priority == "CRITICAL":
                critical_count += 1

            elif priority == "HIGH":
                high_count += 1

            elif priority == "MEDIUM":
                medium_count += 1

            else:
                low_count += 1

        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:

            st.metric(
                "Total Reports",
                total_reports
            )

        with col2:

            st.metric(
                "🚨 Critical",
                critical_count
            )

        with col3:

            st.metric(
                "🔴 High",
                high_count
            )

        with col4:

            st.metric(
                "🟡 Medium",
                medium_count
            )

        with col5:

            st.metric(
                "🟢 Low",
                low_count
            )

        st.divider()

        # ----------------------------------------------------
        # PRIORITY QUEUE
        # ----------------------------------------------------

        st.subheader(
            "🧠 Smart Priority Queue"
        )

        priority_reports = []

        for report in reports:

            severity = report[3]
            impact_score = report[4]

            priority, priority_score = calculate_priority(
                severity,
                impact_score
            )

            priority_reports.append(
                (
                    priority_score,
                    report
                )
            )

        priority_reports.sort(
            key=lambda x: x[0],
            reverse=True
        )

        for priority_score, report in priority_reports:

            (
                report_id,
                issue,
                description,
                severity,
                impact_score,
                recommendation,
                location,
                latitude,
                longitude
            ) = report

            priority, score = calculate_priority(
                severity,
                impact_score
            )

            if priority == "CRITICAL":

                icon = "🚨"

            elif priority == "HIGH":

                icon = "🔴"

            elif priority == "MEDIUM":

                icon = "🟡"

            else:

                icon = "🟢"

            with st.expander(
                f"{icon} Report #{report_id} — "
                f"{issue} — Priority {score}/100"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        f"**Issue:** {issue}"
                    )

                    st.write(
                        f"**Severity:** {severity}"
                    )

                    st.write(
                        f"**Impact:** {impact_score}/10"
                    )

                    st.write(
                        f"**Priority:** {priority}"
                    )

                with col2:

                    st.write(
                        f"**Location:** {location}"
                    )

                    st.write(
                        f"**Recommendation:** "
                        f"{recommendation}"
                    )

                    if (
                        latitude is not None
                        and longitude is not None
                    ):

                        st.write(
                            f"**GPS:** "
                            f"{latitude:.6f}, "
                            f"{longitude:.6f}"
                        )

                st.progress(
                    int(score) / 100
                )

        st.divider()

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        st.subheader(
            "📋 Report History"
        )

        for report in reports:

            (
                report_id,
                issue,
                description,
                severity,
                impact_score,
                recommendation,
                location,
                latitude,
                longitude
            ) = report

            st.markdown(
                f"### Report #{report_id}"
            )

            st.write(
                f"**Issue:** {issue}"
            )

            st.write(
                f"**AI Description:** {description}"
            )

            st.write(
                f"**Severity:** {severity}"
            )

            st.write(
                f"**Impact Score:** {impact_score}/10"
            )

            st.write(
                f"**Location:** {location}"
            )

            st.write(
                f"**Recommendation:** {recommendation}"
            )

            st.divider()


# ============================================================
# PAGE 3 — CIVIC MAP
# ============================================================

elif page == "🗺️ Civic Map":

    st.header(
        "🗺️ Civic Issue Map"
    )

    reports = get_reports()

    if not reports:

        st.info(
            "No location-based reports available."
        )

    else:

        map_data = []

        for report in reports:

            latitude = report[7]
            longitude = report[8]

            if (
                latitude is not None
                and longitude is not None
            ):

                map_data.append(
                    {
                        "latitude": latitude,
                        "longitude": longitude
                    }
                )

        if map_data:

            st.map(
                map_data,
                latitude="latitude",
                longitude="longitude",
                zoom=11
            )

            st.success(
                f"📍 {len(map_data)} civic issue location(s) mapped."
            )

            st.divider()

            st.subheader(
                "📍 Mapped Civic Issues"
            )

            for report in reports:

                (
                    report_id,
                    issue,
                    description,
                    severity,
                    impact_score,
                    recommendation,
                    location,
                    latitude,
                    longitude
                ) = report

                if (
                    latitude is not None
                    and longitude is not None
                ):

                    priority, score = calculate_priority(
                        severity,
                        impact_score
                    )

                    st.write(
                        f"**Report #{report_id} — {issue}**"
                    )

                    st.write(
                        f"📍 {location}"
                    )

                    st.write(
                        f"Priority: **{priority} "
                        f"({score}/100)**"
                    )

                    st.write(
                        f"GPS: "
                        f"{latitude:.6f}, "
                        f"{longitude:.6f}"
                    )

                    st.divider()

        else:

            st.warning(
                "Reports exist, but GPS coordinates "
                "are unavailable."
            )


# ============================================================
# PAGE 4 — AUTHORITY ACTION CENTER
# ============================================================

elif page == "🏛️ Authority Center":

    st.header(
        "🏛️ Authority Action Center"
    )

    st.write(
        "AI-generated operational guidance for "
        "municipal authorities."
    )

    reports = get_reports()

    if not reports:

        st.info(
            "No reports available."
        )

    else:

        authority_reports = []

        for report in reports:

            severity = report[3]
            impact_score = report[4]

            priority, priority_score = calculate_priority(
                severity,
                impact_score
            )

            authority_reports.append(
                (
                    priority_score,
                    report
                )
            )

        authority_reports.sort(
            key=lambda x: x[0],
            reverse=True
        )

        for priority_score, report in authority_reports:

            (
                report_id,
                issue,
                description,
                severity,
                impact_score,
                recommendation,
                location,
                latitude,
                longitude
            ) = report

            priority, score = calculate_priority(
                severity,
                impact_score
            )

            (
                department,
                authority_action,
                urgency,
                response_time
            ) = get_authority_action(
                issue,
                priority
            )

            if priority == "CRITICAL":

                icon = "🚨"

            elif priority == "HIGH":

                icon = "🔴"

            elif priority == "MEDIUM":

                icon = "🟡"

            else:

                icon = "🟢"

            with st.expander(
                f"{icon} Report #{report_id} — "
                f"{issue} — Priority {score}/100",
                expanded=(priority == "CRITICAL")
            ):

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Priority",
                        priority
                    )

                with col2:

                    st.metric(
                        "Priority Score",
                        f"{score}/100"
                    )

                with col3:

                    st.metric(
                        "Impact",
                        f"{impact_score}/10"
                    )

                st.divider()

                st.subheader(
                    issue
                )

                st.write(
                    f"**AI Description:** {description}"
                )

                st.write(
                    f"**Severity:** {severity}"
                )

                st.write(
                    f"**Location:** {location}"
                )

                if (
                    latitude is not None
                    and longitude is not None
                ):

                    st.write(
                        f"**GPS:** "
                        f"{latitude:.6f}, "
                        f"{longitude:.6f}"
                    )

                st.divider()

                st.subheader(
                    "🏛️ Responsible Department"
                )

                st.success(
                    department
                )

                st.subheader(
                    "🔧 Recommended Authority Action"
                )

                st.write(
                    authority_action
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.warning(
                        f"**Urgency:** {urgency}"
                    )

                with col2:

                    st.info(
                        f"**Response:** {response_time}"
                    )

                st.divider()

                # ------------------------------------------------
                # DOWNLOAD REPORT FROM AUTHORITY CENTER
                # ------------------------------------------------

                incident_report = generate_incident_report(
                    report_id,
                    issue,
                    description,
                    severity,
                    impact_score,
                    priority,
                    score,
                    location,
                    latitude,
                    longitude,
                    department,
                    authority_action,
                    urgency,
                    response_time
                )

                st.download_button(
                    label="📄 Download Incident Report",
                    data=incident_report,
                    file_name=f"civic_incident_report_{report_id}.txt",
                    mime="text/plain",
                    key=f"authority_download_{report_id}"
                )


# ============================================================
# PAGE 5 — INCIDENT REPORTS
# ============================================================

elif page == "📄 Incident Reports":

    st.header(
        "📄 Civic Incident Reports"
    )

    st.write(
        "Generate and download structured reports "
        "for submitted civic issues."
    )

    reports = get_reports()

    if not reports:

        st.info(
            "No incident reports available yet."
        )

    else:

        for report in reports:

            (
                report_id,
                issue,
                description,
                severity,
                impact_score,
                recommendation,
                location,
                latitude,
                longitude
            ) = report

            priority, priority_score = calculate_priority(
                severity,
                impact_score
            )

            (
                department,
                authority_action,
                urgency,
                response_time
            ) = get_authority_action(
                issue,
                priority
            )

            with st.expander(
                f"📄 Report #{report_id} — {issue}"
            ):

                st.write(
                    f"**Priority:** {priority}"
                )

                st.write(
                    f"**Priority Score:** "
                    f"{priority_score}/100"
                )

                st.write(
                    f"**Location:** {location}"
                )

                st.write(
                    f"**Department:** {department}"
                )

                st.write(
                    f"**Urgency:** {urgency}"
                )

                incident_report = generate_incident_report(
                    report_id,
                    issue,
                    description,
                    severity,
                    impact_score,
                    priority,
                    priority_score,
                    location,
                    latitude,
                    longitude,
                    department,
                    authority_action,
                    urgency,
                    response_time
                )

                st.download_button(
                    label="📥 Download Report",
                    data=incident_report,
                    file_name=f"civic_incident_report_{report_id}.txt",
                    mime="text/plain",
                    key=f"report_download_{report_id}"
                )


# ============================================================
# FOOTER
# ============================================================

st.sidebar.divider()

st.sidebar.caption(
    "CIVICLENS AI — Tech for Better Tomorrow"
)

st.sidebar.caption(
    "Open-source AI Hackathon Prototype"
)