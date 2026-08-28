import streamlit as st
import plotly.express as px

from services.sensor_service import (
    load_sensor_data,
    sensor_summary
)

from services.image_service import (
    prepare_image,
    analyze_field_image
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="FarmProfit AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# THEME
# =========================================================

st.markdown(
    """
<style>

:root {
    --background: #191D17;
    --surface: #242B21;
    --surface-light: #2D3629;
    --surface-soft: #354031;

    --green: #7F9668;
    --green-light: #A8BA8E;

    --beige: #E9DEC6;
    --beige-soft: #D3C7AE;
    --beige-muted: #A99E88;

    --text: #F2E9D8;
    --muted: #B5AB98;

    --border: #485340;

    --danger: #C97E70;
    --warning: #D2AE69;
    --success: #91B078;
}

html,
body,
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at top right,
            #293423 0%,
            #1B2118 40%,
            #151914 100%
        );

    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}


/* HERO */

.hero {
    background:
        linear-gradient(
            135deg,
            #2D3827,
            #242C20 55%,
            #342F27
        );

    border: 1px solid var(--border);
    border-radius: 20px;

    padding: 1.55rem 1.7rem;
    margin-bottom: 1.2rem;

    box-shadow:
        0 14px 32px rgba(0,0,0,0.20);
}

.hero-title {
    color: var(--beige);

    font-size: 2.15rem;
    font-weight: 760;

    letter-spacing: -0.03em;
}

.hero-subtitle {
    color: var(--beige-muted);

    margin-top: 0.35rem;

    font-size: 0.94rem;
}

.hero-tag {
    display: inline-block;

    margin-top: 0.9rem;

    padding: 0.38rem 0.75rem;

    border-radius: 999px;

    background: var(--green-light);
    color: #172012;

    font-size: 0.76rem;
    font-weight: 750;
}


/* SECTION */

.section-label {
    color: var(--beige-muted);

    font-size: 0.72rem;
    font-weight: 800;

    text-transform: uppercase;
    letter-spacing: 0.09em;

    margin-top: 0.5rem;
    margin-bottom: 0.55rem;
}


/* FARM STRIP */

.farm-strip {
    background: rgba(36,43,33,0.95);

    border: 1px solid var(--border);
    border-radius: 14px;

    padding: 0.9rem 1rem;

    margin-bottom: 1rem;

    color: var(--muted);
}

.farm-strip strong {
    color: var(--beige);
}


/* CUSTOM METRIC */

.metric-card {
    background:
        linear-gradient(
            145deg,
            #293224,
            #232A20
        );

    border: 1px solid var(--border);
    border-radius: 16px;

    padding: 1.05rem;

    min-height: 112px;

    margin-bottom: 0.55rem;
}

.metric-label {
    color: var(--beige-muted);

    font-size: 0.78rem;

    margin-bottom: 0.55rem;
}

.metric-value {
    color: var(--beige);

    font-size: 1.65rem;
    font-weight: 750;

    line-height: 1;
}

.metric-foot {
    color: var(--muted);

    font-size: 0.73rem;

    margin-top: 0.6rem;
}

.metric-positive {
    color: var(--green-light);
}


/* PANELS */

.panel {
    background: var(--surface);

    border: 1px solid var(--border);
    border-radius: 14px;

    padding: 1rem;

    color: var(--beige-soft);

    margin-bottom: 0.8rem;
}


/* ISSUE CARDS */

.issue-card {
    background:
        linear-gradient(
            145deg,
            #2A3025,
            #242A20
        );

    border: 1px solid var(--border);
    border-left: 4px solid var(--danger);

    border-radius: 14px;

    padding: 1rem;

    margin-bottom: 0.8rem;
}

.issue-card.medium {
    border-left-color: var(--warning);
}

.issue-card.low {
    border-left-color: var(--success);
}

.issue-title {
    color: var(--beige);

    font-weight: 700;
}

.issue-meta {
    color: var(--beige-muted);

    font-size: 0.74rem;

    margin-top: 0.2rem;
    margin-bottom: 0.65rem;
}

.issue-reason {
    color: var(--beige-soft);

    font-size: 0.87rem;

    line-height: 1.45;
}

.recommendation-box {
    margin-top: 0.75rem;

    background: #313A2D;

    border: 1px solid #45513D;
    border-radius: 10px;

    padding: 0.75rem;

    color: var(--beige-soft);

    font-size: 0.86rem;
}

.recommendation-box b {
    color: var(--green-light);
}


/* STREAMLIT METRICS */

[data-testid="stMetric"] {
    background: var(--surface);

    border: 1px solid var(--border);
    border-radius: 14px;

    padding: 0.85rem 1rem;
}


/* INPUTS */

input,
textarea {
    background-color: var(--surface-light) !important;
    color: var(--beige) !important;
}

div[data-baseweb="select"] > div {
    background-color: var(--surface-light);
    color: var(--beige);
}


/* BUTTON */

.stButton > button {
    background:
        linear-gradient(
            135deg,
            #A1B78A,
            #7D9567
        );

    color: #172012;

    border: none;
    border-radius: 10px;

    font-weight: 750;
}

.stButton > button:hover {
    background:
        linear-gradient(
            135deg,
            #B2C899,
            #8BA575
        );

    color: #11170E;
}


/* TABS */

button[data-baseweb="tab"] {
    color: var(--beige-muted);

    font-weight: 650;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--green-light);
}


/* MOBILE */

@media (max-width: 768px) {

    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .hero {
        padding: 1.15rem;
    }

    .hero-title {
        font-size: 1.7rem;
    }

    .metric-value {
        font-size: 1.4rem;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "sensor_df" not in st.session_state:
    st.session_state.sensor_df = None

if "image_result" not in st.session_state:
    st.session_state.image_result = None

if "farm_name" not in st.session_state:
    st.session_state.farm_name = "Demo Farm"

if "location" not in st.session_state:
    st.session_state.location = "Tiruvannamalai, Tamil Nadu"

if "crop" not in st.session_state:
    st.session_state.crop = "Tomato"

if "growth_stage" not in st.session_state:
    st.session_state.growth_stage = "Flowering"


# =========================================================
# HEADER
# =========================================================

hero_html = (
    '<div class="hero">'
    '<div class="hero-title">FarmProfit AI</div>'
    '<div class="hero-subtitle">'
    'AI-driven farm intelligence focused on reducing resource waste '
    'and maximizing expected profit.'
    '</div>'
    '<div class="hero-tag">Profit Optimization Engine</div>'
    '</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True
)


# =========================================================
# NAVIGATION
# =========================================================

overview_tab, input_tab, field_tab, insights_tab = st.tabs(
    [
        "Overview",
        "Farm Data",
        "Field Assessment",
        "AI Insights"
    ]
)


# =========================================================
# FARM INPUT
# =========================================================

with input_tab:

    # -----------------------------------------------------
    # FARM
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-label">Farm Information</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        c1, c2 = st.columns(2)

        with c1:

            farm_name = st.text_input(
                "Farm Name",
                st.session_state.farm_name
            )

            location = st.text_input(
                "Location",
                st.session_state.location
            )

            land_area = st.number_input(
                "Land Area (acres)",
                min_value=0.1,
                value=5.0,
                step=0.5
            )

        with c2:

            crop = st.selectbox(
                "Current Crop",
                [
                    "Tomato",
                    "Rice",
                    "Groundnut",
                    "Maize",
                    "Millet",
                    "Cotton"
                ]
            )

            growth_stage = st.selectbox(
                "Growth Stage",
                [
                    "Pre-sowing",
                    "Germination",
                    "Vegetative",
                    "Flowering",
                    "Fruiting",
                    "Maturity"
                ],
                index=3
            )

            available_budget = st.number_input(
                "Available Budget",
                min_value=0,
                value=120000,
                step=5000
            )


    st.session_state.farm_name = farm_name
    st.session_state.location = location
    st.session_state.crop = crop
    st.session_state.growth_stage = growth_stage


    # -----------------------------------------------------
    # PRODUCTION / REVENUE
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-label">Expected Production</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        c1, c2 = st.columns(2)

        with c1:

            expected_yield = st.number_input(
                "Expected Yield (kg)",
                min_value=0.0,
                value=6000.0,
                step=100.0
            )

        with c2:

            expected_price = st.number_input(
                "Expected Selling Price (per kg)",
                min_value=0.0,
                value=30.0,
                step=1.0
            )


    # -----------------------------------------------------
    # COST
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-label">Production Costs</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        c1, c2 = st.columns(2)

        with c1:

            seed_cost = st.number_input(
                "Seeds",
                min_value=0,
                value=8000,
                step=500
            )

            fertilizer_cost = st.number_input(
                "Fertilizer",
                min_value=0,
                value=12000,
                step=500
            )

            pesticide_cost = st.number_input(
                "Pesticides / Crop Protection",
                min_value=0,
                value=6000,
                step=500
            )

            irrigation_cost = st.number_input(
                "Irrigation",
                min_value=0,
                value=10000,
                step=500
            )

        with c2:

            labour_cost = st.number_input(
                "Labour",
                min_value=0,
                value=25000,
                step=500
            )

            machinery_cost = st.number_input(
                "Machinery / Equipment",
                min_value=0,
                value=12000,
                step=500
            )

            transport_cost = st.number_input(
                "Transport",
                min_value=0,
                value=7000,
                step=500
            )

            other_cost = st.number_input(
                "Other Costs",
                min_value=0,
                value=5000,
                step=500
            )


    # -----------------------------------------------------
    # RESOURCE USAGE
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-label">Resource Usage</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        c1, c2 = st.columns(2)

        with c1:

            water_today = st.number_input(
                "Water Used Today (litres)",
                min_value=0.0,
                value=12000.0,
                step=500.0
            )

            irrigation_duration = st.number_input(
                "Irrigation Duration (minutes)",
                min_value=0.0,
                value=90.0,
                step=5.0
            )

        with c2:

            fertilizer_amount = st.number_input(
                "Fertilizer Applied Recently (kg)",
                min_value=0.0,
                value=25.0,
                step=1.0
            )

            days_since_fertilizer = st.number_input(
                "Days Since Fertilizer Application",
                min_value=0,
                value=3
            )


    # -----------------------------------------------------
    # SENSOR UPLOAD
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-label">Sensor Data</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.caption(
            "Upload time-series farm sensor readings. "
            "CSV can include soil moisture, temperature, humidity, "
            "water flow and irrigation usage."
        )

        uploaded_csv = st.file_uploader(
            "Upload Sensor CSV",
            type=["csv"]
        )

        if uploaded_csv is not None:

            try:

                sensor_df_loaded = load_sensor_data(
                    uploaded_csv
                )

                st.session_state.sensor_df = (
                    sensor_df_loaded
                )

                st.success(
                    f"{len(sensor_df_loaded)} sensor readings loaded."
                )

                st.dataframe(
                    sensor_df_loaded.tail(15),
                    use_container_width=True,
                    hide_index=True
                )

            except Exception as exc:

                st.error(
                    f"Unable to process sensor data: {exc}"
                )


# =========================================================
# FIELD ASSESSMENT
# =========================================================

with field_tab:

    st.markdown(
        '<div class="section-label">Crop Health Assessment</div>',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        source = st.radio(
            "Image Source",
            [
                "Upload Image",
                "Camera"
            ],
            horizontal=True
        )

        image_file = None

        if source == "Upload Image":

            image_file = st.file_uploader(
                "Upload crop or field image",
                type=[
                    "jpg",
                    "jpeg",
                    "png"
                ],
                key="crop_image"
            )

        else:

            image_file = st.camera_input(
                "Capture Crop Image"
            )


        if image_file is not None:

            try:

                image, image_array = prepare_image(
                    image_file
                )

                st.image(
                    image,
                    caption="Crop Image",
                    use_container_width=True
                )


                if st.button(
                    "Analyze Crop Health",
                    use_container_width=True
                ):

                    result = analyze_field_image(
                        image_array
                    )

                    st.session_state.image_result = result


            except Exception as exc:

                st.error(
                    f"Unable to analyze image: {exc}"
                )


    if st.session_state.image_result is not None:

        result = st.session_state.image_result

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Condition",
                result["condition"]
            )

        with c2:

            if "confidence" in result:

                st.metric(
                    "Model Confidence",
                    f"{result['confidence'] * 100:.1f}%"
                )


        c3, c4 = st.columns(2)

        with c3:

            st.metric(
                "Health Score",
                f"{result['health_score']}/100"
            )

        with c4:

            st.metric(
                "Disease Probability",
                f"{result['disease_probability'] * 100:.0f}%"
            )


        notes_html = (
            '<div class="panel">'
            '<strong>Model Assessment</strong><br><br>'
            f'{result["notes"]}'
            '</div>'
        )

        st.markdown(
            notes_html,
            unsafe_allow_html=True
        )


# =========================================================
# SENSOR SUMMARY
# =========================================================

sensor_df = st.session_state.sensor_df


if sensor_df is not None:

    try:

        summary = sensor_summary(
            sensor_df
        )

        soil_moisture = float(
            summary["latest_soil_moisture"]
        )

        avg_temperature = float(
            summary["avg_temperature"]
        )

        avg_humidity = float(
            summary["avg_humidity"]
        )

        sensor_water_used = float(
            summary["total_water_used"]
        )

    except Exception:

        soil_moisture = 45.0
        avg_temperature = 29.0
        avg_humidity = 75.0

        sensor_water_used = (
            water_today
            if "water_today" in locals()
            else 0
        )

else:

    soil_moisture = 45.0
    avg_temperature = 29.0
    avg_humidity = 75.0

    sensor_water_used = (
        water_today
        if "water_today" in locals()
        else 0
    )


# =========================================================
# FINANCIAL CALCULATIONS
# =========================================================

expected_yield = (
    expected_yield
    if "expected_yield" in locals()
    else 6000
)

expected_price = (
    expected_price
    if "expected_price" in locals()
    else 30
)


expected_revenue = (
    expected_yield
    * expected_price
)


cost_values = [
    seed_cost if "seed_cost" in locals() else 8000,
    fertilizer_cost if "fertilizer_cost" in locals() else 12000,
    pesticide_cost if "pesticide_cost" in locals() else 6000,
    irrigation_cost if "irrigation_cost" in locals() else 10000,
    labour_cost if "labour_cost" in locals() else 25000,
    machinery_cost if "machinery_cost" in locals() else 12000,
    transport_cost if "transport_cost" in locals() else 7000,
    other_cost if "other_cost" in locals() else 5000
]


total_cost = sum(
    cost_values
)


expected_profit = (
    expected_revenue
    - total_cost
)


profit_margin = (
    expected_profit
    / expected_revenue
    * 100
    if expected_revenue > 0
    else 0
)


# =========================================================
# PROBLEM DETECTION + SAVINGS
# =========================================================

issues = []

irrigation_saving = 0
fertilizer_saving = 0
protected_revenue = 0


# ---------------------------------------------------------
# WATER
# ---------------------------------------------------------

if (
    soil_moisture > 70
    and sensor_water_used > 10000
):

    irrigation_saving = (
        irrigation_cost * 0.20
        if "irrigation_cost" in locals()
        else 2000
    )

    issues.append(
        {
            "title": "Potential Irrigation Overuse",
            "severity": "High",
            "class_name": "",
            "reason": (
                "Soil moisture remains high while irrigation "
                "usage is still significant."
            ),
            "action": (
                "Reduce the next irrigation cycle and reassess "
                "soil moisture before applying additional water."
            ),
            "impact": (
                f"Estimated cost saving: ₹{irrigation_saving:,.0f}"
            )
        }
    )


# ---------------------------------------------------------
# FERTILIZER
# ---------------------------------------------------------

if (
    "fertilizer_amount" in locals()
    and fertilizer_amount > 20
    and days_since_fertilizer < 5
):

    fertilizer_saving = (
        fertilizer_cost * 0.15
        if "fertilizer_cost" in locals()
        else 1500
    )

    issues.append(
        {
            "title": "Potential Fertilizer Overuse",
            "severity": "Medium",
            "class_name": "medium",
            "reason": (
                "A relatively high fertilizer quantity was "
                "applied recently."
            ),
            "action": (
                "Delay the next fertilizer application until "
                "new soil or crop-response data is available."
            ),
            "impact": (
                f"Estimated cost saving: ₹{fertilizer_saving:,.0f}"
            )
        }
    )


# ---------------------------------------------------------
# HUMIDITY / DISEASE
# ---------------------------------------------------------

if avg_humidity > 80:

    protected_revenue = (
        expected_revenue * 0.03
    )

    issues.append(
        {
            "title": "Elevated Crop Disease Risk",
            "severity": "Medium",
            "class_name": "medium",
            "reason": (
                "Persistent high humidity may increase "
                "the likelihood of fungal stress."
            ),
            "action": (
                "Inspect crop health and monitor affected areas "
                "before visible damage increases."
            ),
            "impact": (
                f"Potential revenue protected: ₹{protected_revenue:,.0f}"
            )
        }
    )


# ---------------------------------------------------------
# IMAGE MODEL
# ---------------------------------------------------------

if st.session_state.image_result is not None:

    image_result = st.session_state.image_result

    if image_result["disease_probability"] > 0.70:

        protected_revenue = max(
            protected_revenue,
            expected_revenue * 0.05
        )

        issues.append(
            {
                "title": "Crop Health Issue Detected",
                "severity": "High",
                "class_name": "",
                "reason": (
                    f"The vision model identified "
                    f"{image_result['condition']}."
                ),
                "action": (
                    "Inspect affected plants and determine the "
                    "appropriate crop-management response."
                ),
                "impact": (
                    f"Potential revenue at risk: "
                    f"₹{protected_revenue:,.0f}"
                )
            }
        )


# =========================================================
# OPTIMIZED PROFIT
# =========================================================

direct_cost_savings = (
    irrigation_saving
    + fertilizer_saving
)


potential_financial_improvement = (
    direct_cost_savings
    + protected_revenue
)


optimized_profit = (
    expected_profit
    + potential_financial_improvement
)


# =========================================================
# OVERVIEW
# =========================================================

with overview_tab:

    farm_strip_html = (
        '<div class="farm-strip">'
        f'<strong>{st.session_state.farm_name}</strong>'
        f'&nbsp;&nbsp;|&nbsp;&nbsp;'
        f'{st.session_state.crop}'
        f'&nbsp;&nbsp;|&nbsp;&nbsp;'
        f'{st.session_state.growth_stage}'
        f'&nbsp;&nbsp;|&nbsp;&nbsp;'
        f'{st.session_state.location}'
        '</div>'
    )

    st.markdown(
        farm_strip_html,
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # FINANCIAL SUMMARY
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-label">Profit Outlook</div>',
        unsafe_allow_html=True
    )


    c1, c2 = st.columns(2)

    with c1:

        html = (
            '<div class="metric-card">'
            '<div class="metric-label">Expected Revenue</div>'
            f'<div class="metric-value">₹{expected_revenue:,.0f}</div>'
            '<div class="metric-foot">'
            'Yield × expected selling price'
            '</div>'
            '</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    with c2:

        html = (
            '<div class="metric-card">'
            '<div class="metric-label">Production Cost</div>'
            f'<div class="metric-value">₹{total_cost:,.0f}</div>'
            '<div class="metric-foot">'
            'Estimated total operating cost'
            '</div>'
            '</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    c3, c4 = st.columns(2)

    with c3:

        html = (
            '<div class="metric-card">'
            '<div class="metric-label">Current Expected Profit</div>'
            f'<div class="metric-value">₹{expected_profit:,.0f}</div>'
            f'<div class="metric-foot">'
            f'Estimated margin: {profit_margin:.1f}%'
            '</div>'
            '</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    with c4:

        html = (
            '<div class="metric-card">'
            '<div class="metric-label">AI Optimized Profit</div>'
            f'<div class="metric-value">₹{optimized_profit:,.0f}</div>'
            '<div class="metric-foot metric-positive">'
            f'Potential improvement: '
            f'₹{potential_financial_improvement:,.0f}'
            '</div>'
            '</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # RESOURCE STATUS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-label">Farm Signals</div>',
        unsafe_allow_html=True
    )

    r1, r2 = st.columns(2)

    with r1:

        st.metric(
            "Soil Moisture",
            f"{soil_moisture:.1f}%"
        )

        st.metric(
            "Average Humidity",
            f"{avg_humidity:.1f}%"
        )

    with r2:

        st.metric(
            "Water Usage",
            f"{sensor_water_used:,.0f} L"
        )

        st.metric(
            "Temperature",
            f"{avg_temperature:.1f} C"
        )


    # -----------------------------------------------------
    # MAIN CONTENT
    # -----------------------------------------------------

    chart_column, issue_column = st.columns(
        [1.65, 1]
    )


    with chart_column:

        st.markdown(
            '<div class="section-label">Sensor Intelligence</div>',
            unsafe_allow_html=True
        )

        if sensor_df is not None:

            if (
                "timestamp" in sensor_df.columns
                and "soil_moisture" in sensor_df.columns
            ):

                fig = px.line(
                    sensor_df,
                    x="timestamp",
                    y="soil_moisture",
                    labels={
                        "timestamp": "Time",
                        "soil_moisture": "Soil Moisture (%)"
                    }
                )

                fig.update_traces(
                    line=dict(
                        width=3,
                        color="#A8BA8E"
                    )
                )

                fig.update_layout(
                    title="Soil Moisture",
                    height=300,
                    paper_bgcolor="#242B21",
                    plot_bgcolor="#242B21",
                    font=dict(
                        color="#D3C7AE"
                    ),
                    xaxis=dict(
                        gridcolor="#485340"
                    ),
                    yaxis=dict(
                        gridcolor="#485340"
                    ),
                    showlegend=False
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )


            if (
                "timestamp" in sensor_df.columns
                and "water_used" in sensor_df.columns
            ):

                fig = px.bar(
                    sensor_df,
                    x="timestamp",
                    y="water_used",
                    labels={
                        "timestamp": "Time",
                        "water_used": "Water Used (L)"
                    }
                )

                fig.update_traces(
                    marker_color="#7F9668"
                )

                fig.update_layout(
                    title="Irrigation Usage",
                    height=280,
                    paper_bgcolor="#242B21",
                    plot_bgcolor="#242B21",
                    font=dict(
                        color="#D3C7AE"
                    ),
                    xaxis=dict(
                        gridcolor="#485340"
                    ),
                    yaxis=dict(
                        gridcolor="#485340"
                    ),
                    showlegend=False
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            st.markdown(
                '<div class="panel">'
                '<strong>No sensor data loaded.</strong><br><br>'
                'Upload a sensor CSV file to enable '
                'time-series resource analysis.'
                '</div>',
                unsafe_allow_html=True
            )


    with issue_column:

        st.markdown(
            '<div class="section-label">Profit Opportunities</div>',
            unsafe_allow_html=True
        )


        if not issues:

            stable_html = (
                '<div class="issue-card low">'
                '<div class="issue-title">'
                'No Major Inefficiencies Detected'
                '</div>'
                '<div class="issue-meta">'
                'Current status: Stable'
                '</div>'
                '<div class="issue-reason">'
                'Current farm data does not show '
                'a major resource optimization opportunity.'
                '</div>'
                '<div class="recommendation-box">'
                '<b>Next best action</b><br>'
                'Continue collecting sensor and crop-health data.'
                '</div>'
                '</div>'
            )

            st.markdown(
                stable_html,
                unsafe_allow_html=True
            )


        for issue in issues:

            issue_html = (
                f'<div class="issue-card {issue["class_name"]}">'
                f'<div class="issue-title">'
                f'{issue["title"]}'
                f'</div>'
                f'<div class="issue-meta">'
                f'Priority: {issue["severity"]}'
                f'</div>'
                f'<div class="issue-reason">'
                f'{issue["reason"]}'
                f'</div>'
                f'<div class="recommendation-box">'
                f'<b>Next best action</b><br>'
                f'{issue["action"]}'
                f'<br><br>'
                f'<b>Financial impact</b><br>'
                f'{issue["impact"]}'
                f'</div>'
                f'</div>'
            )

            st.markdown(
                issue_html,
                unsafe_allow_html=True
            )


# =========================================================
# AI INSIGHTS
# =========================================================

with insights_tab:

    st.markdown(
        '<div class="section-label">Financial Optimization</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Expected Profit",
            f"₹{expected_profit:,.0f}"
        )

    with c2:

        st.metric(
            "Potential Improvement",
            f"₹{potential_financial_improvement:,.0f}"
        )

    with c3:

        st.metric(
            "Optimized Profit",
            f"₹{optimized_profit:,.0f}"
        )


    st.markdown(
        '<div class="section-label">Cost Breakdown</div>',
        unsafe_allow_html=True
    )


    cost_data = {
        "Category": [
            "Seeds",
            "Fertilizer",
            "Crop Protection",
            "Irrigation",
            "Labour",
            "Machinery",
            "Transport",
            "Other"
        ],
        "Cost": cost_values
    }

    import pandas as pd

    cost_df = pd.DataFrame(
        cost_data
    )


    cost_fig = px.bar(
        cost_df,
        x="Category",
        y="Cost"
    )

    cost_fig.update_traces(
        marker_color="#7F9668"
    )

    cost_fig.update_layout(
        height=320,
        paper_bgcolor="#242B21",
        plot_bgcolor="#242B21",
        font=dict(
            color="#D3C7AE"
        ),
        xaxis=dict(
            gridcolor="#485340"
        ),
        yaxis=dict(
            title="Cost",
            gridcolor="#485340"
        )
    )

    st.plotly_chart(
        cost_fig,
        use_container_width=True
    )


    st.markdown(
        '<div class="section-label">Detected Opportunities</div>',
        unsafe_allow_html=True
    )


    for issue in issues:

        issue_html = (
            f'<div class="issue-card {issue["class_name"]}">'
            f'<div class="issue-title">{issue["title"]}</div>'
            f'<div class="issue-reason">{issue["reason"]}</div>'
            f'<div class="recommendation-box">'
            f'<b>Recommended action</b><br>'
            f'{issue["action"]}'
            f'<br><br>'
            f'<b>Financial impact</b><br>'
            f'{issue["impact"]}'
            f'</div>'
            f'</div>'
        )

        st.markdown(
            issue_html,
            unsafe_allow_html=True
        )


    if sensor_df is not None:

        st.markdown(
            '<div class="section-label">Raw Sensor Data</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            sensor_df,
            use_container_width=True,
            hide_index=True
        )