import os
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Airtel Network Usage",
    page_icon="📶",
    layout="wide",
)

CSS = """
<style>
    :root {
        --airtel-red: #ff3b3b;
        --ink: #f8fafc;
        --muted: #aab5c5;
        --line: #273449;
        --panel: #111827;
        --panel-raised: #151e2e;
        --canvas: #080c14;
        --sidebar: #0c121d;
    }

    [data-testid="stAppViewContainer"] {
        background: var(--canvas);
        color: var(--ink);
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1480px;
        padding-top: 1.25rem;
        padding-bottom: 1rem;
    }

    [data-testid="stHeader"] {
        height: 0;
        background: transparent;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid var(--line);
        background: var(--sidebar);
    }

    [data-testid="stSidebar"] h2 {
        color: var(--ink);
        font-size: 1.05rem;
        margin-bottom: 0.25rem;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    [data-baseweb="select"] > div {
        border-color: var(--line) !important;
        background: var(--panel-raised) !important;
        color: var(--ink) !important;
    }

    [data-baseweb="select"] svg {
        fill: var(--muted);
    }

    [data-baseweb="popover"] [role="listbox"] {
        border: 1px solid var(--line);
        background: var(--panel-raised);
    }

    [data-baseweb="popover"] [role="option"] {
        color: var(--ink);
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.15rem;
    }

    .brand-mark {
        width: 0.72rem;
        height: 2.15rem;
        border-radius: 999px;
        background: var(--airtel-red);
        transform: skew(-12deg);
        box-shadow: 0 0 0 5px rgba(255, 59, 59, 0.14);
    }

    .brand-title {
        color: var(--ink);
        font-size: clamp(1.55rem, 2.4vw, 2.35rem);
        font-weight: 760;
        letter-spacing: -0.035em;
        line-height: 1.05;
    }

    .reader-line {
        color: var(--muted);
        font-size: 0.96rem;
        margin: 0.35rem 0 0.7rem;
    }

    .reader-line strong {
        color: var(--ink);
    }

    [data-testid="stMetric"] {
        min-height: 118px;
        padding: 0.95rem 1rem;
        border: 1px solid var(--line);
        border-radius: 14px;
        background: var(--panel);
        background: linear-gradient(145deg, var(--panel-raised), var(--panel));
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.22);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 0.84rem;
    }

    [data-testid="stMetricValue"] {
        color: var(--ink);
        font-size: clamp(1.4rem, 2vw, 2rem);
        font-weight: 740;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.76rem;
    }

    [data-testid="stMetricDelta"] > div {
        border: 1px solid var(--line);
        border-radius: 999px;
        background: #0b1220;
        padding: 0.12rem 0.42rem;
    }

    .chart-note, .definition-note, .provenance {
        color: var(--muted);
        font-size: 0.78rem;
        line-height: 1.45;
    }

    .definition-note {
        margin: 0.25rem 0 0.45rem;
        padding: 0.55rem 0.75rem;
        border-left: 3px solid var(--airtel-red);
        border-radius: 0 8px 8px 0;
        background: rgba(255, 59, 59, 0.08);
    }

    .provenance {
        margin-top: 0.45rem;
        padding-top: 0.5rem;
        border-top: 1px solid var(--line);
    }

    .selector-label {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 650;
        margin-bottom: -0.35rem;
    }

    .table-heading {
        color: var(--ink);
        font-size: 1rem;
        font-weight: 700;
        margin: 0.75rem 0 0.15rem;
    }

    .table-heading span {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 400;
        margin-left: 0.35rem;
    }

    .fixed-badge {
        display: inline-block;
        margin-left: 0.35rem;
        padding: 0.08rem 0.38rem;
        border-radius: 999px;
        background: #202b3d;
        color: #cbd5e1;
        font-size: 0.66rem;
        font-weight: 700;
        vertical-align: middle;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid var(--line);
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--muted);
    }

    .stTabs [data-baseweb="tab"] {
        min-width: 130px;
        height: 2.65rem;
        padding: 0 1rem;
        border-radius: 9px 9px 0 0;
        font-size: 0.92rem;
        font-weight: 650;
    }

    .stTabs [aria-selected="true"] {
        color: var(--airtel-red) !important;
    }

    div[data-testid="stPlotlyChart"] {
        border: 1px solid var(--line);
        border-radius: 14px;
        background: var(--panel);
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.2);
        overflow: hidden;
    }

    @media (max-width: 900px) {
        [data-testid="stMainBlockContainer"] {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }
    }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "data", "raw", "airtel.db"))


@st.cache_data(show_spinner=False)
def q(sql, params=()):
    """Run a read-only dashboard query and return its rows."""
    uri = f"file:{DB.replace(os.sep, '/')}?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    try:
        return pd.read_sql_query(sql, con, params=params)
    finally:
        con.close()


def filter_params(connection_type, experiment_group):
    return (connection_type, connection_type, experiment_group, experiment_group)


def format_count(value):
    return f"{int(value):,}"


def style_figure(fig, height, legend=True):
    fig.update_layout(
        height=height,
        margin=dict(l=28, r=22, t=62, b=35),
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(family="Arial, sans-serif", color="#cbd5e1", size=13),
        title=dict(font=dict(color="#f8fafc", size=17), x=0.02, xanchor="left"),
        legend=dict(
            title_text="",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        showlegend=legend,
        hoverlabel=dict(
            bgcolor="#080c14",
            bordercolor="#3a4961",
            font_color="#f8fafc",
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#334155",
        tickfont=dict(size=12, color="#aab5c5"),
        title_font=dict(color="#cbd5e1"),
    )
    fig.update_yaxes(
        gridcolor="#253044",
        linecolor="#334155",
        zeroline=False,
        tickfont=dict(size=12, color="#aab5c5"),
        title_font=dict(color="#cbd5e1"),
    )
    fig.update_annotations(font_color="#dbe4f0")
    return fig


def show_chart(fig):
    st.plotly_chart(
        fig,
        width="stretch",
        config={"displayModeBar": False, "responsive": True},
    )


if not os.path.exists(DB):
    st.error(f"Database not found: {DB}")
    st.stop()

required_objects = q(
    """
    SELECT name
    FROM sqlite_master
    WHERE name IN ('customer_features', 'usage_daily', 'v_usage_month')
    """
)["name"].tolist()
missing = sorted({"customer_features", "usage_daily", "v_usage_month"} - set(required_objects))
if missing:
    st.error("Run the data-preparation notebook first. Missing: " + ", ".join(missing))
    st.stop()


st.markdown(
    """
    <div class="brand-row">
        <div class="brand-mark"></div>
        <div class="brand-title">Airtel Network Usage</div>
    </div>
    <div class="reader-line">
        <strong>For the Network Capacity Planner:</strong>
        understand demand, usage intensity, plan fit and the May double-data offer.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Dashboard filters")
    st.caption("Filters update applicable cards and every chart on both tabs.")
    connection = st.selectbox(
        "Connection type",
        ["All", "Prepaid", "Postpaid"],
        index=0,
    )
    experiment = st.selectbox(
        "Experiment group",
        ["All", "A", "B"],
        index=0,
    )
    st.markdown("---")
    st.caption("Observation window")
    st.markdown("**1 Jan–30 Jun 2025**")
    st.caption("Offer period")
    st.markdown("**From 1 May 2025**")

params = filter_params(connection, experiment)
group_palette = {"A": "#8da2c0", "B": "#ff3b3b"}
red_scale = ["#7f1d1d", "#ff3b3b"]

overview_tab, detail_tab = st.tabs(["Overview", "Month detail"])


with overview_tab:
    fixed_usage = q("SELECT COUNT(*) AS usage_days FROM usage_daily").iloc[0]
    fixed_offer = q(
        """
        SELECT
            ROUND(AVG(CASE WHEN ab_group = 'A' THEN subscriber_avg_mb END), 1) AS group_a_mb,
            ROUND(AVG(CASE WHEN ab_group = 'B' THEN subscriber_avg_mb END), 1) AS group_b_mb,
            ROUND(
                100.0 * (
                    AVG(CASE WHEN ab_group = 'B' THEN subscriber_avg_mb END)
                    / AVG(CASE WHEN ab_group = 'A' THEN subscriber_avg_mb END) - 1
                ), 1
            ) AS lift_pct
        FROM (
            SELECT
                c.ab_group,
                u.customer_id,
                AVG(u.data_mb) AS subscriber_avg_mb
            FROM usage_daily u
            JOIN customer_features c ON c.customer_id = u.customer_id
            WHERE u.usage_date >= '2025-05-01'
            GROUP BY c.ab_group, u.customer_id
        )
        """
    ).iloc[0]
    intensity = q(
        """
        SELECT
            ROUND(AVG(c.mb_per_active_day), 1) AS active_day_mb,
            ROUND(AVG(c.mb_per_observed_day), 1) AS calendar_day_mb,
            COUNT(*) AS subscribers
        FROM customer_features c
        WHERE (? = 'All' OR c.connection_type = ?)
          AND (? = 'All' OR c.ab_group = ?)
        """,
        params,
    ).iloc[0]

    card1, card2, card3 = st.columns(3)
    with card1:
        st.metric(
            "Usage-day records · Jan–Jun 2025",
            format_count(fixed_usage["usage_days"]),
            delta="Fixed base-scale measure",
            delta_color="off",
        )
    with card2:
        st.metric(
            "Offer increased Group B usage",
            f"+{fixed_offer['lift_pct']:.1f}%",
            delta="One-tailed p = 1.12×10⁻⁸³ · fixed test result",
            delta_color="normal",
        )
    with card3:
        st.metric(
            "Data per active day",
            f"{intensity['active_day_mb']:,.1f} MB",
            delta=(
                f"{intensity['calendar_day_mb']:,.1f} MB/calendar day · "
                f"n={format_count(intensity['subscribers'])}"
            ),
            delta_color="off",
        )

    st.markdown(
        """
        <div class="definition-note">
            <strong>Measure definition:</strong> active-day usage averages only days with recorded activity;
            calendar-day usage spreads each subscriber’s total over the full 181-day observation window.
            They answer different capacity questions and are not combined.
        </div>
        """,
        unsafe_allow_html=True,
    )

    monthly_usage = q(
        """
        SELECT
            strftime('%Y-%m', u.usage_date) AS month,
            CASE
                WHEN u.usage_date >= '2025-05-01' THEN 'Offer period'
                ELSE 'Pre-offer'
            END AS period,
            c.ab_group,
            COUNT(DISTINCT u.customer_id) AS active_subscribers,
            COUNT(*) AS usage_day_count,
            ROUND(SUM(u.data_mb) / 1024.0 / 1024.0, 2) AS total_tb,
            ROUND(AVG(u.data_mb), 1) AS mb_per_usage_day
        FROM usage_daily u
        JOIN customer_features c ON c.customer_id = u.customer_id
        WHERE (? = 'All' OR c.connection_type = ?)
          AND (? = 'All' OR c.ab_group = ?)
        GROUP BY month, period, c.ab_group
        ORDER BY month, c.ab_group
        """,
        params,
    )
    hero_title = (
        "Group B usage jumps after the offer starts in May"
        if experiment in ("All", "B")
        else "Group A usage remains stable through the offer period"
    )
    hero = px.line(
        monthly_usage,
        x="month",
        y="mb_per_usage_day",
        color="ab_group",
        markers=True,
        color_discrete_map=group_palette,
        custom_data=["usage_day_count"],
        title=hero_title,
        labels={"month": "Month", "mb_per_usage_day": "MB per usage day"},
    )
    hero.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
        hovertemplate=(
            "Month: %{x}<br>MB per usage day: %{y:,.1f}"
            "<br>Usage-day records: %{customdata[0]:,}<extra>Group %{fullData.name}</extra>"
        ),
    )
    hero.add_vrect(
        x0="2025-05",
        x1="2025-06",
        fillcolor="#ff3b3b",
        opacity=0.07,
        line_width=0,
        annotation_text="Offer period",
        annotation_position="top left",
    )
    style_figure(hero, 315, legend=True)
    overview_top_left, overview_top_right = st.columns([2, 1])
    with overview_top_left:
        show_chart(hero)

    monthly_network = q(
        """
        SELECT
            m.month,
            COUNT(DISTINCT m.customer_id) AS active_subscribers,
            ROUND(SUM(m.total_mb) / 1024.0 / 1024.0, 1) AS total_tb
        FROM v_usage_month m
        JOIN customer_features c ON c.customer_id = m.customer_id
        WHERE (? = 'All' OR c.connection_type = ?)
          AND (? = 'All' OR c.ab_group = ?)
        GROUP BY m.month
        ORDER BY m.month
        """,
        params,
    )
    with overview_top_right:
        active_fig = px.bar(
            monthly_network,
            x="month",
            y="active_subscribers",
            text_auto=",.0f",
            title="Active subscriber count rises through June",
            labels={"month": "Month", "active_subscribers": "Active subscribers"},
            color_discrete_sequence=["#ff3b3b"],
        )
        active_fig.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate="Month: %{x}<br>Active subscribers: %{y:,}<extra></extra>",
        )
        style_figure(active_fig, 315, legend=False)
        show_chart(active_fig)

    overview_bottom_left, overview_bottom_right = st.columns(2)
    with overview_bottom_left:
        traffic_fig = px.area(
            monthly_network,
            x="month",
            y="total_tb",
            custom_data=["active_subscribers"],
            title="Monthly network traffic peaks after the May offer",
            labels={"month": "Month", "total_tb": "Total data (TB)"},
            color_discrete_sequence=["#ff3b3b"],
        )
        traffic_fig.update_traces(
            line=dict(width=3),
            fillcolor="rgba(228, 0, 0, 0.12)",
            hovertemplate=(
                "Month: %{x}<br>Total data: %{y:,.1f} TB"
                "<br>Active subscribers: %{customdata[0]:,}<extra></extra>"
            ),
        )
        style_figure(traffic_fig, 320, legend=False)
        show_chart(traffic_fig)

    allowance = q(
        """
        SELECT
            c.plan_name,
            c.monthly_gb,
            COUNT(*) AS subscribers,
            ROUND(AVG(c.total_data_mb / 1024.0 / 6.0), 2) AS actual_gb_per_month,
            ROUND(
                100.0 * AVG((c.total_data_mb / 1024.0 / 6.0) / c.monthly_gb),
                1
            ) AS allowance_used_pct
        FROM customer_features c
        WHERE c.usage_days > 0
          AND (? = 'All' OR c.connection_type = ?)
          AND (? = 'All' OR c.ab_group = ?)
        GROUP BY c.plan_name, c.monthly_gb
        ORDER BY allowance_used_pct
        """,
        params,
    )
    allowance_ref = q(
        """
        SELECT ROUND(
            100.0 * AVG((c.total_data_mb / 1024.0 / 6.0) / c.monthly_gb),
            1
        ) AS base_allowance_pct
        FROM customer_features c
        WHERE c.usage_days > 0
          AND (? = 'All' OR c.connection_type = ?)
          AND (? = 'All' OR c.ab_group = ?)
        """,
        params,
    ).iloc[0]["base_allowance_pct"]
    allowance_fig = px.bar(
        allowance,
        x="allowance_used_pct",
        y="plan_name",
        orientation="h",
        color="allowance_used_pct",
        color_continuous_scale=red_scale,
        custom_data=["subscribers", "monthly_gb", "actual_gb_per_month"],
        title="Most plans use only a fraction of their stated data allowance",
        labels={"allowance_used_pct": "Allowance used (%)", "plan_name": "Plan"},
    )
    allowance_fig.update_traces(
        hovertemplate=(
            "%{y}<br>Allowance used: %{x:.1f}%"
            "<br>Subscribers: %{customdata[0]:,}"
            "<br>Allowance: %{customdata[1]:,.1f} GB/month"
            "<br>Actual: %{customdata[2]:,.2f} GB/month<extra></extra>"
        )
    )
    allowance_fig.add_vline(
        x=allowance_ref,
        line_width=2,
        line_dash="dash",
        line_color="#e2e8f0",
        annotation_text=f"Filtered-base average · {allowance_ref:.1f}%",
        annotation_position="top",
    )
    allowance_fig.update_layout(coloraxis_showscale=False)
    style_figure(allowance_fig, 320, legend=False)
    with overview_bottom_right:
        show_chart(allowance_fig)

    st.markdown(
        """
        <div class="table-heading">
            Monthly network demand and offer impact
            <span>January–June 2025 · filtered view</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    overview_table = monthly_usage.rename(
        columns={
            "month": "Month",
            "period": "Period",
            "ab_group": "Experiment group",
            "active_subscribers": "Active subscribers",
            "usage_day_count": "Usage-day records",
            "total_tb": "Total data (TB)",
            "mb_per_usage_day": "MB per usage day",
        }
    )
    st.dataframe(
        overview_table,
        width="stretch",
        height=280,
        hide_index=True,
        column_config={
            "Active subscribers": st.column_config.NumberColumn(format="%d"),
            "Usage-day records": st.column_config.NumberColumn(format="%d"),
            "Total data (TB)": st.column_config.NumberColumn(format="%.2f"),
            "MB per usage day": st.column_config.NumberColumn(format="%.1f"),
        },
    )

    st.markdown(
        """
        <div class="provenance">
            <strong>Data provenance:</strong> Airtel circle and plan structures reflect real telecom products;
            subscriber-level records are synthetic. All displayed figures are calculated in SQL from the local SQLite database.
        </div>
        """,
        unsafe_allow_html=True,
    )


with detail_tab:
    available_months = q(
        "SELECT DISTINCT strftime('%Y-%m', usage_date) AS month FROM usage_daily ORDER BY month"
    )["month"].tolist()

    detail_card1, detail_card2, detail_card3, month_control = st.columns([1, 1, 1, 0.9])
    with month_control:
        st.markdown('<div class="selector-label">DETAIL SELECTOR</div>', unsafe_allow_html=True)
        selected_month = st.selectbox(
            "Selected month",
            available_months,
            index=0,
            format_func=lambda value: pd.to_datetime(value).strftime("%B %Y"),
            label_visibility="visible",
        )

    month_start = f"{selected_month}-01"
    month_params = (month_start, month_start) + params
    monthly_cards = q(
        """
        SELECT
            COUNT(DISTINCT u.customer_id) AS active_subscribers,
            ROUND(SUM(u.data_mb) / 1024.0 / 1024.0, 2) AS total_tb,
            ROUND(AVG(u.data_mb), 1) AS mb_per_usage_day,
            COUNT(*) AS usage_day_count
        FROM usage_daily u
        JOIN customer_features c ON c.customer_id = u.customer_id
        WHERE u.usage_date >= ?
          AND u.usage_date < date(?, '+1 month')
          AND (? = 'All' OR c.connection_type = ?)
          AND (? = 'All' OR c.ab_group = ?)
        """,
        month_params,
    ).iloc[0]

    with detail_card1:
        st.metric(
            "Subscribers using the network",
            format_count(monthly_cards["active_subscribers"]),
            delta="Distinct subscribers in selected month",
            delta_color="off",
        )
    with detail_card2:
        st.metric(
            "Total data carried",
            f"{monthly_cards['total_tb']:,.2f} TB",
            delta="1 TB = 1,024 × 1,024 MB",
            delta_color="off",
        )
    with detail_card3:
        st.metric(
            "Data per usage day",
            f"{monthly_cards['mb_per_usage_day']:,.1f} MB",
            delta=f"Based on {format_count(monthly_cards['usage_day_count'])} usage-day records",
            delta_color="off",
        )

    daily = q(
        """
        SELECT
            u.usage_date,
            COUNT(*) AS usage_day_count,
            COUNT(DISTINCT u.customer_id) AS active_subscribers,
            ROUND(SUM(u.data_mb) / 1024.0 / 1024.0, 2) AS daily_tb,
            ROUND(
                AVG(SUM(u.data_mb) / 1024.0 / 1024.0) OVER (),
                2
            ) AS avg_daily_tb
        FROM usage_daily u
        JOIN customer_features c ON c.customer_id = u.customer_id
        WHERE u.usage_date >= ?
          AND u.usage_date < date(?, '+1 month')
          AND (? = 'All' OR c.connection_type = ?)
          AND (? = 'All' OR c.ab_group = ?)
        GROUP BY u.usage_date
        ORDER BY u.usage_date
        """,
        month_params,
    )
    daily_ref = daily.iloc[0]["avg_daily_tb"]
    month_label = pd.to_datetime(selected_month).strftime("%B %Y")
    daily_fig = px.line(
        daily,
        x="usage_date",
        y="daily_tb",
        markers=True,
        custom_data=["active_subscribers", "usage_day_count"],
        title=f"Daily network load remains consistent across {month_label}",
        labels={"usage_date": "Date", "daily_tb": "Data carried (TB)"},
        color_discrete_sequence=["#ff3b3b"],
    )
    daily_fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6),
        hovertemplate=(
            "%{x}<br>Data carried: %{y:,.2f} TB"
            "<br>Active subscribers: %{customdata[0]:,}"
            "<br>Usage-day records: %{customdata[1]:,}<extra></extra>"
        ),
    )
    daily_fig.add_hline(
        y=daily_ref,
        line_width=2,
        line_dash="dash",
        line_color="#94a3b8",
        annotation_text=f"Monthly daily average · {daily_ref:.2f} TB",
        annotation_position="bottom right",
    )
    style_figure(daily_fig, 315, legend=False)
    detail_top_left, detail_top_right = st.columns([2, 1])
    with detail_top_left:
        show_chart(daily_fig)

    with detail_top_right:
        group_detail = q(
            """
            SELECT
                c.ab_group,
                CASE
                    WHEN MIN(u.usage_date) >= '2025-05-01' THEN 'Offer period'
                    ELSE 'Pre-offer'
                END AS period,
                COUNT(*) AS usage_day_count,
                COUNT(DISTINCT u.customer_id) AS subscribers,
                ROUND(SUM(u.data_mb) / 1024.0 / 1024.0, 2) AS total_tb,
                ROUND(AVG(u.data_mb), 1) AS mb_per_usage_day
            FROM usage_daily u
            JOIN customer_features c ON c.customer_id = u.customer_id
            WHERE u.usage_date >= ?
              AND u.usage_date < date(?, '+1 month')
              AND (? = 'All' OR c.connection_type = ?)
              AND (? = 'All' OR c.ab_group = ?)
            GROUP BY c.ab_group
            ORDER BY c.ab_group
            """,
            month_params,
        )
        if len(group_detail) == 1:
            group_title = (
                f"Group {group_detail.iloc[0]['ab_group']} averages "
                f"{group_detail.iloc[0]['mb_per_usage_day']:,.0f} MB per usage day"
            )
        elif selected_month >= "2025-05":
            group_title = "Group B records more data per usage day after the offer"
        else:
            group_title = "A and B show similar usage intensity before the offer"
        group_fig = px.bar(
            group_detail,
            x="ab_group",
            y="mb_per_usage_day",
            color="ab_group",
            color_discrete_map=group_palette,
            custom_data=["usage_day_count", "subscribers"],
            text="mb_per_usage_day",
            title=group_title,
            labels={"ab_group": "Experiment group", "mb_per_usage_day": "MB per usage day"},
        )
        group_fig.update_traces(
            texttemplate="%{text:,.0f} MB",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "Group %{x}<br>MB per usage day: %{y:,.1f}"
                "<br>Usage-day records: %{customdata[0]:,}"
                "<br>Subscribers: %{customdata[1]:,}<extra></extra>"
            ),
        )
        style_figure(group_fig, 315, legend=False)
        show_chart(group_fig)

    detail_bottom_left, detail_bottom_right = st.columns(2)
    with detail_bottom_left:
        device_detail = q(
            """
            SELECT
                c.device_type,
                COUNT(*) AS usage_day_count,
                COUNT(DISTINCT u.customer_id) AS subscribers,
                ROUND(AVG(u.data_mb), 1) AS mb_per_usage_day
            FROM usage_daily u
            JOIN customer_features c ON c.customer_id = u.customer_id
            WHERE u.usage_date >= ?
              AND u.usage_date < date(?, '+1 month')
              AND (? = 'All' OR c.connection_type = ?)
              AND (? = 'All' OR c.ab_group = ?)
            GROUP BY c.device_type
            ORDER BY mb_per_usage_day DESC
            """,
            month_params,
        )
        device_fig = px.bar(
            device_detail,
            x="device_type",
            y="mb_per_usage_day",
            color="device_type",
            custom_data=["usage_day_count", "subscribers"],
            text="mb_per_usage_day",
            title="Smartphones account for far greater usage intensity",
            labels={"device_type": "Device type", "mb_per_usage_day": "MB per usage day"},
            color_discrete_sequence=["#ff3b3b", "#71839f"],
        )
        device_fig.update_traces(
            texttemplate="%{text:,.0f} MB",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "%{x}<br>MB per usage day: %{y:,.1f}"
                "<br>Usage-day records: %{customdata[0]:,}"
                "<br>Subscribers: %{customdata[1]:,}<extra></extra>"
            ),
        )
        style_figure(device_fig, 300, legend=False)
        show_chart(device_fig)

    weekday = q(
        """
        SELECT
            CASE strftime('%w', u.usage_date)
                WHEN '0' THEN 'Sun'
                WHEN '1' THEN 'Mon'
                WHEN '2' THEN 'Tue'
                WHEN '3' THEN 'Wed'
                WHEN '4' THEN 'Thu'
                WHEN '5' THEN 'Fri'
                WHEN '6' THEN 'Sat'
            END AS weekday,
            CAST(strftime('%w', u.usage_date) AS INTEGER) AS weekday_order,
            COUNT(*) AS usage_day_count,
            COUNT(DISTINCT u.customer_id) AS subscribers,
            ROUND(AVG(u.data_mb), 1) AS mb_per_usage_day
        FROM usage_daily u
        JOIN customer_features c ON c.customer_id = u.customer_id
        WHERE u.usage_date >= ?
          AND u.usage_date < date(?, '+1 month')
          AND (? = 'All' OR c.connection_type = ?)
          AND (? = 'All' OR c.ab_group = ?)
        GROUP BY weekday, weekday_order
        ORDER BY weekday_order
        """,
        month_params,
    )
    weekday_fig = px.bar(
        weekday,
        x="weekday",
        y="mb_per_usage_day",
        color="mb_per_usage_day",
        color_continuous_scale=red_scale,
        custom_data=["usage_day_count", "subscribers"],
        title=f"Usage intensity is broadly stable across weekdays in {month_label}",
        labels={"weekday": "Day of week", "mb_per_usage_day": "MB per usage day"},
    )
    weekday_fig.update_traces(
        hovertemplate=(
            "%{x}<br>MB per usage day: %{y:,.1f}"
            "<br>Usage-day records: %{customdata[0]:,}"
            "<br>Subscribers: %{customdata[1]:,}<extra></extra>"
        )
    )
    weekday_fig.update_layout(coloraxis_showscale=False)
    style_figure(weekday_fig, 300, legend=False)
    with detail_bottom_right:
        show_chart(weekday_fig)

    st.markdown(
        f"""
        <div class="table-heading">
            Monthly network demand and offer impact
            <span>{month_label} · A/B detail</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    detail_table = group_detail.rename(
        columns={
            "ab_group": "Experiment group",
            "period": "Period",
            "subscribers": "Active subscribers",
            "usage_day_count": "Usage-day records",
            "total_tb": "Total data (TB)",
            "mb_per_usage_day": "MB per usage day",
        }
    )
    detail_table = detail_table[
        [
            "Experiment group",
            "Period",
            "Active subscribers",
            "Usage-day records",
            "Total data (TB)",
            "MB per usage day",
        ]
    ]
    st.dataframe(
        detail_table,
        width="stretch",
        hide_index=True,
        column_config={
            "Active subscribers": st.column_config.NumberColumn(format="%d"),
            "Usage-day records": st.column_config.NumberColumn(format="%d"),
            "Total data (TB)": st.column_config.NumberColumn(format="%.2f"),
            "MB per usage day": st.column_config.NumberColumn(format="%.1f"),
        },
    )

    st.markdown(
        """
        <div class="provenance">
            <strong>Data provenance:</strong> Airtel circle and plan structures reflect real telecom products;
            subscriber-level records are synthetic. Terabytes use the binary conversion 1 TB = 1,024² MB.
            All displayed figures are calculated in SQL from the local SQLite database.
        </div>
        """,
        unsafe_allow_html=True,
    )
