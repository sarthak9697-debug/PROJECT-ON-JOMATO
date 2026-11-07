from pathlib import Path
from datetime import datetime
import math

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# JOMATO RESTAURANT ANALYTICS DASHBOARD
# Based on JOMATO ASSIGNMENT(1).sql and Jomato.csv
# ============================================================

st.set_page_config(
    page_title="Jomato Restaurant Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------
# 1. DATASET COLUMNS
# ------------------------------------------------------------

REQUIRED_COLUMNS = [
    "OrderId",
    "RestaurantName",
    "RestaurantType",
    "Rating",
    "No.of.Rating",
    "AverageCost",
    "OnlineOrder",
    "TableBooking",
    "CuisinesType",
    "Area",
    "LocalAddress",
    "Delivery time"
]


# ------------------------------------------------------------
# 2. BUILT-IN SAMPLE DATA
# Used only if Jomato.csv is not available.
# ------------------------------------------------------------

DEMO_ROWS = [
    [1, "L-81 Cafe", "Quick Bites", 3.9, 48, 400, "Yes", "No",
     "Fast Food, Beverages", "HSR", "Byresandra,Tavarekere,Madiwala", 59],

    [2, "Refuel", "Cafe", 3.7, 37, 400, "Yes", "No",
     "Cafe, Beverages", "Bannerghatta Road", "Bannerghatta Road", 56],

    [3, "Biryani Central", "Casual Dining", 2.7, 135, 550, "Yes", "No",
     "Biryani, Mughlai, Chinese", "Marathahalli", "Marathahalli", 50],

    [4, "The BBQ", "Casual Dining", 4.2, 220, 800, "No", "Yes",
     "North Indian, BBQ", "Koramangala", "Koramangala", 45],

    [5, "Green Bowl", "Quick Bites", 4.1, 92, 350, "Yes", "No",
     "Healthy Food", "HSR", "HSR Layout", 38],

    [6, "Spice Route", "Fine Dining", 4.5, 310, 1200, "No", "Yes",
     "North Indian", "Indiranagar", "100 Feet Road", 48],

    [7, "Noodle House", "Cafe", 3.4, 65, 500, "Yes", "No",
     "Chinese, Asian", "Whitefield", "Whitefield Main Road", 42],

    [8, "Pizza Corner", "Quick Bites", 3.2, 110, 450, "Yes", "No",
     "Pizza, Fast Food", "Jayanagar", "Jayanagar 4th Block", 35],

    [9, "South Meals", "Casual Dining", 4.0, 175, 300, "No", "Yes",
     "South Indian", "Malleshwaram", "Sampige Road", 40],

    [10, "Dessert Lab", "Desserts", 4.3, 88, 250, "Yes", "No",
     "Desserts, Bakery", "Indiranagar", "CMH Road", 32]
]

DEMO_DF = pd.DataFrame(
    DEMO_ROWS,
    columns=REQUIRED_COLUMNS
)


# ------------------------------------------------------------
# 3. LOAD DATA
# ------------------------------------------------------------

def load_data(uploaded_file):

    if uploaded_file is not None:
        return pd.read_csv(uploaded_file), "Uploaded CSV"

    local_csv = Path(__file__).with_name("Jomato.csv")

    if local_csv.exists():
        return pd.read_csv(local_csv), "Project Jomato.csv"

    return DEMO_DF.copy(), "Built-in sample data"


# ------------------------------------------------------------
# 4. DATA CLEANING AND SQL CALCULATIONS
# ------------------------------------------------------------

def clean_data(raw):

    df = raw.copy()

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "The CSV is missing required Jomato columns: "
            + ", ".join(missing)
        )

    df = df[REQUIRED_COLUMNS].copy()

    # Convert numeric columns
    numeric_columns = [
        "OrderId",
        "Rating",
        "No.of.Rating",
        "AverageCost",
        "Delivery time"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Handle missing text values
    text_columns = [
        "RestaurantName",
        "RestaurantType",
        "OnlineOrder",
        "TableBooking",
        "CuisinesType",
        "Area",
        "LocalAddress"
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

        df[column] = df[column].replace(
            "",
            "Unknown"
        )

    # Validate numeric values
    df["Rating"] = df["Rating"].where(
        df["Rating"].between(0, 5)
    )

    df["No.of.Rating"] = df["No.of.Rating"].clip(
        lower=0
    )

    df["AverageCost"] = df["AverageCost"].where(
        df["AverageCost"] >= 0
    )

    df["Delivery time"] = df["Delivery time"].where(
        df["Delivery time"] >= 0
    )

    # --------------------------------------------------------
    # SQL CASE STATEMENT
    # --------------------------------------------------------

    df["RatingStatus"] = "Bad"

    df.loc[
        df["Rating"] > 3,
        "RatingStatus"
    ] = "Average"

    df.loc[
        df["Rating"] > 3.5,
        "RatingStatus"
    ] = "Good"

    df.loc[
        df["Rating"] > 4,
        "RatingStatus"
    ] = "Excellent"

    # --------------------------------------------------------
    # SQL USER-DEFINED FUNCTION USING STUFF()
    #
    # STUFF(@input, 7, 0, 'Chicken ')
    #
    # Inserts Chicken after the first six characters.
    # --------------------------------------------------------

    def stuff_chicken(value):

        value = str(value)

        return (
            value[:6]
            + "Chicken "
            + value[6:]
        )

    df["StuffedType"] = (
        df["RestaurantType"]
        .apply(stuff_chicken)
    )

    # --------------------------------------------------------
    # SQL CEILING(), FLOOR(), ABS()
    # --------------------------------------------------------

    df["CeilRating"] = df["Rating"].apply(
        lambda x: math.ceil(x)
        if pd.notna(x)
        else pd.NA
    )

    df["FloorRating"] = df["Rating"].apply(
        lambda x: math.floor(x)
        if pd.notna(x)
        else pd.NA
    )

    df["AbsoluteRating"] = df["Rating"].abs()

    return df


# ------------------------------------------------------------
# 5. DASHBOARD STYLING
# ------------------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }

    [data-testid="stMetric"] {
        background: #f6f8fb;
        border: 1px solid #e6eaf0;
        padding: 14px;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# 6. DASHBOARD TITLE
# ------------------------------------------------------------

st.title(
    "🍽️ Jomato Restaurant Analytics Dashboard"
)

st.caption(
    "Restaurant ratings, restaurant types, average cost, "
    "cuisines, ordering options and delivery time."
)


# ------------------------------------------------------------
# 7. SIDEBAR FILTERS
# ------------------------------------------------------------

with st.sidebar:

    st.header("Data & Filters")

    uploaded = st.file_uploader(
        "Upload Jomato CSV (optional)",
        type=["csv"]
    )

    try:

        raw_df, source_label = load_data(uploaded)

        data = clean_data(raw_df)

    except Exception as exc:

        st.error(str(exc))

        st.stop()

    st.caption(
        f"Data source: **{source_label}**"
    )

    st.caption(
        f"Rows loaded: **{len(data):,}**"
    )

    restaurant_types = sorted(
        data["RestaurantType"].dropna().unique().tolist()
    )

    areas = sorted(
        data["Area"].dropna().unique().tolist()
    )

    statuses = [
        "Excellent",
        "Good",
        "Average",
        "Bad"
    ]

    selected_types = st.multiselect(
        "Restaurant Type",
        restaurant_types,
        default=restaurant_types
    )

    selected_areas = st.multiselect(
        "Area",
        areas,
        default=areas
    )

    selected_status = st.multiselect(
        "Rating Status",
        statuses,
        default=statuses
    )

    online_options = sorted(
        data["OnlineOrder"].dropna().unique().tolist()
    )

    selected_online = st.multiselect(
        "Online Order",
        online_options,
        default=online_options
    )


# ------------------------------------------------------------
# 8. APPLY FILTERS
# ------------------------------------------------------------

filtered = data[
    data["RestaurantType"].isin(selected_types)
    &
    data["Area"].isin(selected_areas)
    &
    data["RatingStatus"].isin(selected_status)
    &
    data["OnlineOrder"].isin(selected_online)
].copy()


if filtered.empty:

    st.warning(
        "No records match the selected filters. "
        "Change or clear one or more filters."
    )

    st.stop()


# ------------------------------------------------------------
# 9. KPI CARDS
# ------------------------------------------------------------

st.subheader("Dataset Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Restaurant Records",
    f"{len(filtered):,}"
)

c2.metric(
    "Average Rating",
    f"{filtered['Rating'].mean():.2f}"
    if filtered["Rating"].notna().any()
    else "N/A"
)

c3.metric(
    "Average Cost",
    f"{filtered['AverageCost'].mean():,.0f}"
    if filtered["AverageCost"].notna().any()
    else "N/A"
)

c4.metric(
    "Average Delivery Time",
    f"{filtered['Delivery time'].mean():.1f} min"
    if filtered["Delivery time"].notna().any()
    else "N/A"
)

c5.metric(
    "Total Number of Ratings",
    f"{filtered['No.of.Rating'].sum():,.0f}"
)


# ------------------------------------------------------------
# 10. DASHBOARD TABS
# ------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Overview & Trends",
        "SQL Assignment Outputs",
        "Restaurant Insights",
        "Explore Dataset"
    ]
)


# ============================================================
# TAB 1: OVERVIEW AND TRENDS
# ============================================================

with tab1:

    left, right = st.columns(2)

    # Restaurant records by type
    with left:

        type_counts = (
            filtered["RestaurantType"]
            .value_counts()
            .rename_axis("Restaurant Type")
            .reset_index(name="Records")
        )

        fig = px.bar(
            type_counts,
            x="Restaurant Type",
            y="Records",
            color="Restaurant Type",
            title="Restaurant Records by Type",
            text_auto=True
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Number of records"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Rating status distribution
    with right:

        status_counts = (
            filtered["RatingStatus"]
            .value_counts()
            .reindex(statuses, fill_value=0)
            .rename_axis("Rating Status")
            .reset_index(name="Records")
        )

        fig = px.pie(
            status_counts,
            names="Rating Status",
            values="Records",
            title="Rating Status Distribution",
            hole=0.42
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    left, right = st.columns(2)

    # Average rating by area
    with left:

        area_rating = (
            filtered.groupby(
                "Area",
                as_index=False
            )["Rating"]
            .mean()
            .dropna()
            .sort_values(
                "Rating",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            area_rating,
            x="Area",
            y="Rating",
            title="Average Rating by Area (Top 15)",
            text_auto=".2f"
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Average rating"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Online order availability
    with right:

        online_counts = (
            filtered["OnlineOrder"]
            .value_counts()
            .rename_axis("Online Order")
            .reset_index(name="Records")
        )

        fig = px.pie(
            online_counts,
            names="Online Order",
            values="Records",
            title="Online Order Availability",
            hole=0.42
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# TAB 2: SQL ASSIGNMENT OUTPUTS
# ============================================================

with tab2:

    # --------------------------------------------------------
    # CASE STATEMENT
    # --------------------------------------------------------

    st.markdown(
        "### 1. Rating Status — SQL CASE"
    )

    st.code(
        """
CASE
    WHEN Rating > 4 THEN 'Excellent'
    WHEN Rating > 3.5 THEN 'Good'
    WHEN Rating > 3 THEN 'Average'
    ELSE 'Bad'
END AS RatingStatus
        """,
        language="sql"
    )

    st.dataframe(
        filtered[
            [
                "RestaurantName",
                "Rating",
                "RatingStatus"
            ]
        ].sort_values(
            "Rating",
            ascending=False,
            na_position="last"
        ),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # USER-DEFINED FUNCTION AND STUFF()
    # --------------------------------------------------------

    st.markdown(
        "### 2. Stuffed Restaurant Type — "
        "User-Defined Function and STUFF()"
    )

    st.code(
        """
CREATE FUNCTION dbo.fn_StuffChicken
(@input VARCHAR(100))
RETURNS VARCHAR(100)
AS
BEGIN
    RETURN STUFF(@input, 7, 0, 'Chicken ')
END;
        """,
        language="sql"
    )

    st.caption(
        "The dashboard reproduces the SQL insertion logic "
        "in Python: insert 'Chicken ' at position 7, "
        "after the first six characters."
    )

    st.dataframe(
        filtered[
            [
                "RestaurantName",
                "RestaurantType",
                "StuffedType"
            ]
        ].drop_duplicates().head(100),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # CEILING, FLOOR AND ABS
    # --------------------------------------------------------

    st.markdown(
        "### 3. Rating Calculations — "
        "CEILING(), FLOOR() and ABS()"
    )

    st.code(
        """
SELECT
    Rating,
    CEILING(Rating),
    FLOOR(Rating),
    ABS(Rating)
FROM Jomato$;
        """,
        language="sql"
    )

    st.dataframe(
        filtered[
            [
                "RestaurantName",
                "Rating",
                "CeilRating",
                "FloorRating",
                "AbsoluteRating"
            ]
        ].head(200),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------------
    # ROLLUP AND SUM
    # --------------------------------------------------------

    st.markdown(
        "### 4. Restaurant Type Cost Summary — "
        "SUM() with ROLLUP"
    )

    st.code(
        """
SELECT
    RestaurantType,
    SUM(AverageCost) AS TotalAvgCost
FROM Jomato$
GROUP BY ROLLUP(RestaurantType);
        """,
        language="sql"
    )

    rollup = (
        filtered.groupby(
            "RestaurantType",
            dropna=False
        )["AverageCost"]
        .sum(min_count=1)
        .reset_index(name="TotalAvgCost")
    )

    total = pd.DataFrame(
        [
            {
                "RestaurantType": "Grand Total",
                "TotalAvgCost": filtered["AverageCost"].sum(
                    min_count=1
                )
            }
        ]
    )

    rollup = pd.concat(
        [rollup, total],
        ignore_index=True
    )

    st.dataframe(
        rollup,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Grand Total represents the ROLLUP summary row. "
        "Values are the sum of AverageCost, exactly as in "
        "the SQL query; they are not revenue."
    )

    st.divider()

    # --------------------------------------------------------
    # TOP 1 RESTAURANT
    # --------------------------------------------------------

    st.markdown(
        "### 5. Top Restaurant by Number of Ratings — TOP 1"
    )

    st.code(
        """
SELECT TOP 1
    RestaurantName,
    CuisinesType,
    [no#of#rating]
FROM Jomato$
ORDER BY [no#of#rating] DESC;
        """,
        language="sql"
    )

    top_one = (
        filtered.sort_values(
            "No.of.Rating",
            ascending=False
        ).head(1)
    )

    if not top_one.empty:

        st.dataframe(
            top_one[
                [
                    "RestaurantName",
                    "CuisinesType",
                    "No.of.Rating"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No top restaurant is available for the current filters."
        )

    st.divider()

    # --------------------------------------------------------
    # DATE FUNCTIONS
    # --------------------------------------------------------

    st.markdown(
        "### 6. SQL Date Functions — "
        "GETDATE(), YEAR(), DATENAME() and DAY()"
    )

    now = datetime.now()

    d1, d2, d3, d4 = st.columns(4)

    d1.metric(
        "Current Date",
        now.strftime("%Y-%m-%d")
    )

    d2.metric(
        "Year",
        str(now.year)
    )

    d3.metric(
        "Month Name",
        now.strftime("%B")
    )

    d4.metric(
        "Day",
        str(now.day)
    )

    st.caption(
        "These values are generated at dashboard runtime, "
        "corresponding to the SQL Server date functions "
        "in the assignment."
    )


# ============================================================
# TAB 3: RESTAURANT INSIGHTS
# ============================================================

with tab3:

    st.markdown(
        "### Restaurant and Customer-Facing Insights"
    )

    left, right = st.columns(2)

    # Average cost by restaurant type
    with left:

        cost_type = (
            filtered.groupby(
                "RestaurantType",
                as_index=False
            )["AverageCost"]
            .mean()
            .dropna()
            .sort_values(
                "AverageCost",
                ascending=False
            )
        )

        fig = px.bar(
            cost_type,
            x="RestaurantType",
            y="AverageCost",
            title="Mean Average Cost by Restaurant Type",
            text_auto=".0f"
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Average cost"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Average delivery time by area
    with right:

        delivery_area = (
            filtered.groupby(
                "Area",
                as_index=False
            )["Delivery time"]
            .mean()
            .dropna()
            .sort_values(
                "Delivery time",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            delivery_area,
            x="Area",
            y="Delivery time",
            title="Average Delivery Time by Area (Top 15)",
            text_auto=".1f"
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="Delivery time (minutes)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    left, right = st.columns(2)

    # Rating versus average cost
    with left:

        scatter_data = filtered.dropna(
            subset=[
                "Rating",
                "AverageCost"
            ]
        )

        fig = px.scatter(
            scatter_data,
            x="AverageCost",
            y="Rating",
            color="RestaurantType",
            hover_name="RestaurantName",
            hover_data=[
                "Area",
                "No.of.Rating"
            ],
            title="Rating vs Average Cost"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Table booking availability
    with right:

        booking = (
            filtered["TableBooking"]
            .value_counts()
            .rename_axis("Table Booking")
            .reset_index(name="Records")
        )

        fig = px.bar(
            booking,
            x="Table Booking",
            y="Records",
            color="Table Booking",
            title="Table Booking Availability",
            text_auto=True
        )

        fig.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Most common cuisines
    cuisine_counts = (
        filtered.assign(
            Cuisine=filtered["CuisinesType"].str.split(", ")
        )
        .explode("Cuisine")
        .groupby("Cuisine")
        .size()
        .sort_values(ascending=False)
        .head(15)
        .reset_index(name="Records")
    )

    fig = px.bar(
        cuisine_counts,
        x="Cuisine",
        y="Records",
        title="Most Common Cuisine Labels (Top 15)",
        text_auto=True
    )

    fig.update_layout(
        xaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TAB 4: EXPLORE DATASET
# ============================================================

with tab4:

    st.markdown(
        "### Filtered Jomato Records"
    )

    st.caption(
        "The table contains the original CSV columns "
        "plus calculated fields reproduced from the SQL assignment."
    )

    search = st.text_input(
        "Search restaurant, cuisine, area or restaurant type"
    )

    display_df = filtered.copy()

    if search.strip():

        mask = (
            display_df[
                [
                    "RestaurantName",
                    "CuisinesType",
                    "Area",
                    "RestaurantType"
                ]
            ]
            .astype(str)
            .apply(
                lambda col: col.str.contains(
                    search.strip(),
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        )

        display_df = display_df[mask]

    st.write(
        f"Showing **{len(display_df):,}** records"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=480
    )

    # Download filtered records
    csv_bytes = display_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "Download filtered data as CSV",
        data=csv_bytes,
        file_name="jomato_filtered_data.csv",
        mime="text/csv"
    )


# ------------------------------------------------------------
# 11. FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "Project scope follows the supplied Jomato SQL assignment "
    "and CSV columns. It does not contain employee engagement, "
    "department, profit, or revenue analysis."
)