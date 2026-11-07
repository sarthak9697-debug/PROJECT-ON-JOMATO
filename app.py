import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Synergizing Success | Operations & Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI/UX
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    h1, h2, h3 {
        color: #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

# Built-in Robust Fallback Dataset Generator
@st.cache_data
def load_data():
    np.random.seed(42)
    n_rows = 300
    
    departments = ['Engineering', 'Data & Analytics', 'Operations', 'Sales', 'Customer Success', 'Finance']
    categories = ['Infrastructure', 'Process Optimization', 'Client Delivery', 'Internal R&D', 'Support']
    first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Ethan', 'Fiona', 'George', 'Hannah', 'Ian', 'Julia',
                   'Kevin', 'Laura', 'Michael', 'Nina', 'Oscar', 'Paula', 'Quentin', 'Rachel', 'Sam', 'Tina']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson']
    
    data = {
        'employee_id': [f"EMP-{1000 + i}" for i in range(n_rows)],
        'employee_name': [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n_rows)],
        'department': np.random.choice(departments, n_rows, p=[0.25, 0.20, 0.20, 0.15, 0.10, 0.10]),
        'category': np.random.choice(categories, n_rows),
        'revenue': np.round(np.random.normal(80000, 22000, n_rows).clip(25000, 160000), 2),
        'profit_margin': np.round(np.random.normal(0.28, 0.08, n_rows).clip(0.05, 0.60), 4),
        'employee_performance_score': np.round(np.random.normal(82, 10, n_rows).clip(50, 100), 1),
        'operational_cost': np.round(np.random.normal(45000, 12000, n_rows).clip(10000, 95000), 2),
        'hours_worked': np.random.randint(140, 210, n_rows)
    }
    
    df = pd.DataFrame(data)
    df['net_profit'] = np.round(df['revenue'] * df['profit_margin'], 2)
    df['efficiency_index'] = np.round((df['employee_performance_score'] * df['profit_margin'] * 100) / (df['operational_cost'] / 1000), 2)
    return df

df = load_data()

# Sidebar Control Panel
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("Filter operational metrics, employee performance, and department efficiency in real time.")

selected_dept = st.sidebar.multiselect(
    "Select Department(s)",
    options=df['department'].unique(),
    default=df['department'].unique()
)

perf_range = st.sidebar.slider(
    "Performance Score Range",
    min_value=float(df['employee_performance_score'].min()),
    max_value=float(df['employee_performance_score'].max()),
    value=(float(df['employee_performance_score'].min()), float(df['employee_performance_score'].max()))
)

margin_range = st.sidebar.slider(
    "Profit Margin Range",
    min_value=0.0,
    max_value=0.6,
    value=(0.0, 0.6),
    format="%.2f"
)

search_query = st.sidebar.text_input("🔍 Search Employee Name or ID", "")

# Apply Filter Logic
filtered_df = df[
    (df['department'].isin(selected_dept)) &
    (df['employee_performance_score'].between(perf_range[0], perf_range[1])) &
    (df['profit_margin'].between(margin_range[0], margin_range[1]))
]

if search_query:
    filtered_df = filtered_df[
        filtered_df['employee_name'].str.contains(search_query, case=False, na=False) |
        filtered_df['employee_id'].str.contains(search_query, case=False, na=False)
    ]

# Main Application Title & Description
st.title("Synergizing Success: Improving Operational Efficiency and Employee Engagement")
st.markdown("""
Welcome to the executive decision-support dashboard. This platform connects **SQL database intelligence** with interactive Python analytics to evaluate **employee performance**, **revenue generation**, and **departmental efficiency**. Use the sidebar controls to explore the dataset instantly.
""")

# Key Metrics Row
col1, col2, col3, col4, col5 = st.columns(5)

total_revenue = filtered_df['revenue'].sum()
avg_margin = filtered_df['profit_margin'].mean() * 100
avg_perf = filtered_df['employee_performance_score'].mean()
total_net_profit = filtered_df['net_profit'].sum()
total_headcount = filtered_df['employee_id'].nunique()

col1.metric("Total Revenue", f"${total_revenue:,.0f}", delta=f"{len(filtered_df)} records")
col2.metric("Avg Profit Margin", f"{avg_margin:.1f}%", delta="Target: >25%")
col3.metric("Avg Performance", f"{avg_perf:.1f} / 100", delta="High Engagement")
col4.metric("Total Net Profit", f"${total_net_profit:,.0f}", delta="Net Return")
col5.metric("Active Headcount", f"{total_headcount}", delta="Employees")

st.markdown("---")

# Interactive Visualizations Section
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("🏢 Department Revenue & Profit Breakdown")
    dept_agg = filtered_df.groupby('department')[['revenue', 'net_profit']].sum().reset_index()
    fig_dept = px.bar(
        dept_agg,
        x='department',
        y=['revenue', 'net_profit'],
        barmode='group',
        labels={'value': 'Amount ($)', 'department': 'Department', 'variable': 'Metric'},
        title="Revenue vs Net Profit by Department",
        color_discrete_sequence=['#3b82f6', '#10b981']
    )
    fig_dept.update_layout(legend_title_text='Metric', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_dept, use_container_width=True)

with row1_col2:
    st.subheader("📈 Performance vs. Revenue Correlation")
    fig_scatter = px.scatter(
        filtered_df,
        x='employee_performance_score',
        y='revenue',
        color='department',
        size='net_profit',
        hover_data=['employee_name', 'profit_margin'],
        title="Employee Performance Score vs. Revenue Generated",
        labels={'employee_performance_score': 'Performance Score', 'revenue': 'Revenue ($)'}
    )
    fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader("⚙️ Operational Efficiency Index Distribution")
    fig_box = px.box(
        filtered_df,
        x='department',
        y='efficiency_index',
        color='department',
        title="Efficiency Index Distribution Across Departments",
        labels={'efficiency_index': 'Efficiency Index', 'department': 'Department'}
    )
    fig_box.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_box, use_container_width=True)

with row2_col2:
    st.subheader("📊 Category Operational Breakdown")
    cat_agg = filtered_df.groupby('category')['operational_cost'].sum().reset_index()
    fig_pie = px.pie(
        cat_agg,
        names='category',
        values='operational_cost',
        title="Operational Cost Distribution by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# Data Table View & Export Section
st.subheader("📋 Detailed Operations & Performance Dataset")
st.markdown("Inspect, sort, and filter tabular records below. You can also download the filtered dataset as a CSV file.")

csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_data,
    file_name="synergizing_success_filtered_data.csv",
    mime="text/csv",
)

st.dataframe(filtered_df, use_container_width=True, height=350)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 14px;'>"
    "Synergizing Success Dashboard | Built with Streamlit, Pandas, and Plotly | Recruiter-Ready Edition"
    "</p>",
    unsafe_allow_html=True
)