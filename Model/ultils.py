import pandas as pd
import streamlit as st
from constants import *
def get_categories():
    categories = []
    categories = df_courses["item_category"].value_counts().index.to_list()
    categories.insert(0,"All")
    return categories 

def print_rec(top_k,df):
    id_to_link = df_info.set_index('item_id')['item_urls'].to_dict()
    id_to_img = df_info.set_index('item_id')['item_imgs'].to_dict()

    for i in range(top_k):
        rec_id = df.iloc[i]['item_id']
        rec_link = id_to_link.get(rec_id, 'Link not found')
        rec_img = id_to_img.get(rec_id, "Image not found")

        rec_title = df.iloc[i]["item_name"]
        rec_avg_rating = df.iloc[i]["item_avg_rating"]
        rec_category = df.iloc[i]["item_category"]

        # divide the page into 2 columns
        col1, col2 = st.columns(2)

        # print the attributes on the page
        with col1:
            st.image(rec_img)
        with col2:
            st.markdown(f'<p style = "font-size: 20px; font-weight:bold;">{rec_title}</p>', unsafe_allow_html=True)
            st.write(rec_avg_rating)
            st.write(rec_category)
            st.markdown(f'<a href="{rec_link}" style="display: inline-block; padding: 10px 10px; background-color: red; color: white; text-align: center; text-decoration: none; font-size: 10px; font-weight: bold; border-radius: 4px;"> more information</a>',
                        unsafe_allow_html=True)
        st.divider()

def print_list(top_k,df):
    id_to_link = df_info.set_index('item_id')['item_urls'].to_dict()
    id_to_img = df_info.set_index('item_id')['item_imgs'].to_dict()

    for i in range(top_k):
        rec_id = df.iloc[i]['item_id']
        rec_link = id_to_link.get(rec_id, 'Link not found')
        rec_img = id_to_img.get(rec_id, "Image not found")

        rec_title = df.iloc[i]["item_name"]
        rec_avg_rating = df.iloc[i]["item_avg_rating"]
        rec_category = df.iloc[i]["item_category"]

        # divide the page into 2 columns
        col1, col2 = st.columns(2)

        # print the attributes on the page
        with col1:
            st.markdown(f'<p style = "font-size: 16px; font-weight:bold;">{rec_title}</p>', unsafe_allow_html=True)
            st.image(rec_img)
        with col2:
            st.write(rec_avg_rating)
            st.write(rec_category)
            st.markdown(f'<a href="{rec_link}" style="display: inline-block; padding: 10px 10px; background-color: red; color: white; text-align: center; text-decoration: none; font-size: 10px; font-weight: bold; border-radius: 4px;"> more information</a>',
                        unsafe_allow_html=True)
        st.divider()

def print_hybrid(df):
    id_to_link = df_info.set_index('item_id')['item_urls'].to_dict()
    id_to_img = df_info.set_index('item_id')['item_imgs'].to_dict()

    if len(df) == 0:
        st.write(" ")
        st.write(" ")
        cols = st.columns(3)
        cols[1].write('Can not find anything')

    else:

        columns = st.columns(
            [1,1,1]
        )  ## no. of columns to split posters into
        for i in range(len(df)):
            
            rec_id = df.iloc[i]['item_id']
            rec_link = id_to_link.get(rec_id, 'Link not found')
            rec_img = id_to_img.get(rec_id, "Image not found")

            rec_title = df.iloc[i]["item_name"]
            rec_avg_rating = df.iloc[i]["item_avg_rating"]
            rec_category = df.iloc[i]["item_category"]
            with st.container():
            
                col = columns[i % len(columns)]
                col.text(str(rec_title))
                # col.markdown(f'<p style = "font-size: 13px; font-weight:bold;">{rec_title}</p>', unsafe_allow_html=True)
                col.image(rec_img)
            # try:
            #     img_src = (
            #         "Posters/" + str(df.index[movie]) + ".jpg"
            #     )  ## get movie poster by movie ID
            # except:
            #     img_src = "Posters/unavailable.png"  ## get default image if movie poster not in folder

            # img_html = self.get_img_with_href(
            #     img_src,
            #     rec_title,
            #     movie_link,
            # )
            # col.markdown(img_html, unsafe_allow_html=True)

            ## ADD/REMOVE OPTIONS FOR WATCHLIST #####################################
            if (rec_title) not in st.session_state["watchlist"].rec_list:
                add_movie = col.button(
                    "Add to watchlist",
                    on_click=st.session_state["watchlist"].add,
                    args=[(rec_title)],
                    key=i,
                )
            else:
                remove_movie = col.button(
                    "Remove",
                    on_click=st.session_state["watchlist"].remove,
                    args=[(rec_title)],
                    key=i,
                )

class Wishlist:
    def __init__(self) -> None:
        self.rec_list = list()
        
    def add(self, rec_title):
        self.rec_list.append(rec_title)

    def remove(self, rec_title):
        self.rec_list.remove(rec_title)