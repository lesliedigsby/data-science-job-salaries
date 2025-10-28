import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Science Job Salaries Analysis", layout="wide")

st.title('Data Science Job Salaries Dashboard')
st.write("""
This dashboard presents an analysis of data science job salaries based on various factors such as experience level, job title, company size, and location.
Using the 2023 Data Science Job Salaries dataset from Kaggle.
""")

st.markdown("""
            **Author:** Leslie Digsby  
            **Dataset Source:** [Kaggle - Data Science Job Salaries 2023](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries)
            **Description: Interactive dashboard analyzing salary trends in data science across roles, experience levels, and remote work ratios.
            """)

@st.cache_data
def load_data():
    df = pd.read_csv('ds_salaries.csv')
    df['experience_level'] = df['experience_level'].replace({
        'EN': 'Entry-Level',
        'MI': 'Mid-Level',
        'SE': 'Senior-Level',
        'EX': 'Executive-Level'
    })
    return df
df = load_data()

st.sidebar.header('Filters Options')
roles = st.sidebar.multiselect('Select Job Roles', options=df['job_title'].unique(), default=['Data Scientist', 'Data Analyst'])
experience_levels = st.sidebar.multiselect('Select Experience Levels', options=df['experience_level'].unique(), default=df['experience_level'].unique())
remote = st.sidebar.multiselect('Select Remote Work Options', options=df['remote_ratio'].unique(), default=df['remote_ratio'].unique())

filtered_df = df[
    (df['job_title'].isin(roles)) &
    (df['experience_level'].isin(experience_levels)) &
    (df['remote_ratio'].isin(remote))
]

st.subheader('Key Metrics')
col1, col2, col3 = st.columns(3)
col1.metric('Average Salary (USD)', f"${filtered_df['salary_in_usd'].mean():,.2f}")
col2.metric('Highest Salary (USD)', f"${filtered_df['salary_in_usd'].max():,.2f}")
col3.metric('Number of Roles', len(filtered_df['job_title'].unique()))

st.subheader('Salary Distribution')
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(filtered_df['salary_in_usd'], bins=30, kde=True, ax=ax, color='skyblue')
ax.set_xlabel('Salary in USD')
ax.set_ylabel('Count')
st.pyplot(fig)

st.subheader('Average Salary by Experience Level')
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(data=filtered_df, x='experience_level', y='salary_in_usd', ax=ax2, palette='viridis')
ax2.set_xlabel('Experience Level')
ax2.set_ylabel('Salary in USD')
st.pyplot(fig2)

st.subheader('Average Salary by Job Title')
avg_salary = (
    filtered_df.groupby('job_title')['salary_in_usd']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
st.bar_chart(avg_salary)

st.subheader('Salary Comparison: Data Analyst vs Data Scientist')
roles_of_interest = ['Data Analyst', 'Data Scientist']
role_df = df[df['job_title'].isin(roles_of_interest)]

selected_experience_levels = st.selectbox(
    'Select Experience Level:',
    role_df['experience_level'].unique(),
    index=0
)

exp_df = role_df[role_df['experience_level'] == selected_experience_levels]

comparison = (
    exp_df.groupby('job_title')['salary_in_usd']
    .mean()
    .reset_index()
)

if len(comparison) == 2:
    diff = comparison['salary_in_usd'].diff().iloc[-1]
    pct_gap = (diff / comparison['salary_in_usd'].iloc[0]) * 100
else:
    diff = pct_gap = 0

fig3, ax3 = plt.subplots(figsize=(6, 3))
sns.barplot(data=comparison, x='job_title', y='salary_in_usd', ax=ax3, palette='Set2')
ax3.set_title(f'Average Salary by Role ({selected_experience_levels})')
ax3.set_xlabel('Job Title')
ax3.set_ylabel('Average Salary in USD')
st.pyplot(fig3)

st.write(f'At the {selected_experience_levels} level, Data Scientists earn on average ${diff:,.2f} more than Data Analysts, which is approximately {pct_gap:.2f}% higher.')

st.markdown("""
Data Scientists consistently earn more than Data Analysts at almost every experience level, 
with the gap widening as experience increases.  
This trend highlights the premium placed on advanced technical skills 
and modeling expertise in the Data Science career path.
""")