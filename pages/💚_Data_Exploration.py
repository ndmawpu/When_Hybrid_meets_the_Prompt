import streamlit as st
import pandas as pd
from Model.ultils import *
import plotly.express as px

st.set_page_config(page_title="Plotting Demo", page_icon="📈")
st.markdown("# Explore our courses dataset")
st.sidebar.header("Data Collection")
st.sidebar.markdown(
    '''This research collect online courses data from :red[**Udemy**] with a simple request. Then store it in local cache for easy analysis. Voila! From there all set to dive deep into our research. ⋆ ˚ ꩜ ｡ ⋆୨୧˚''')
st.sidebar.write('Stay tuned for more insights 👀')
st.sidebar.write('©️ University of Economic and Law, VNU-HCM')
st.markdown(
    """Take a look at what inside the datasetsヾ(•ω•`)o . Enjoy!"""
)
df_show_info = pd.read_csv('Data/courses_list.csv',nrows=50, index_col=0)
df_show_courses = pd.read_csv('Data/courses.csv',nrows=50, index_col=0)
df_show_ratings = pd.read_csv("Data/ratings.csv",nrows=50)

tab_ratings, tab_courses, tab_info, tab_dist = st.tabs(["ratings","courses list", "courses info", "Visualization"])
with tab_ratings:
    st.write('ratings datasets: 8,375 rows')
    st.caption('For better user experiences, this table only show 1000 rows')
    st.dataframe(df_show_ratings,use_container_width=True)
with tab_courses:
    st.caption('courses datasets: 8,375')
    st.caption('For better user experiences, this table only show 1000 rows')
    st.dataframe(df_show_courses,use_container_width=True)
with tab_info:
    st.caption('courses inf0 datasets: 4,275,186')
    st.caption('For better user experiences, this table only show 1000 rows')
    st.dataframe(df_show_info,use_container_width=True)
with tab_dist:
    fig_1 = px.histogram(df_courses, x='item_avg_rating', title='Distribution of Average Ratings', width=1000)
    st.plotly_chart(fig_1, use_container_width=True)
    fig_2 = px.histogram(df_courses, x='item_members', title='Distribution of Number of Member', width=1000)
    st.plotly_chart(fig_2, use_container_width=True)
# with st.form("recommend"):
#     # Let the user select the user to investigate
#     user = st.selectbox(
#         "Select a customer to get his recommendations",
#         df_ratings.user_id.unique(),
#     )

#     items_to_recommend = st.slider("How many items to recommend?", 1, 10, 5)
#     print(items_to_recommend)

#     submitted = st.form_submit_button("Recommend!")

st.write(
    """Which courses are on trending"""
)
col1, col2 = st.columns(2, gap='large')
with col1:
    st.caption('Most popular')
    print_list(top_k=5,df=df_courses.sort_values("item_members",ascending=False))
with col2:
    st.caption("Most rated")
    print_list(top_k=5,df=df_courses.sort_values("item_avg_rating", ascending=False))
