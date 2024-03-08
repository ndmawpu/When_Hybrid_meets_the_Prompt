import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import joblib
# from sentence_transformers import SentenceTransformer 

from Model.Hybrid.Rec_WeightedHybrid import *
from Model.Filtering.Rec_Filtering import RecommenderFiltering
from Model.ultils import *
from Model.LLMs.SBERT import RecommenderPrompt

from constants import *

def run():
    #--------------------------------------------------------
    # Homepage
    st.set_page_config(
        page_title="When Hybrid meets the Prompt",
        layout="wide",
        page_icon="💚",
    )

    @st.cache_data(show_spinner='Loading dataset...')  
    def load_data():
        rating_info_subset = pd.read_csv(r"Data/rating_info_subset.csv", nrows=10000)
        return rating_info_subset

    @st.cache_data(show_spinner='Loading models...')
    def load_lasso():
        lasso_model = joblib.load(r'Assets/lasso_model.pkl')
        # predictions_lasso = joblib.load(r'Assets/lasso.pkl')
        return lasso_model

    # @st.cache_data(show_spinner='Loading KNNBaselines...')
    # def load_knn():
    #     predictions_knn = joblib.load(r'Assets/knn.pkl')
    #     return predictions_knn
    
    if "watchlist" not in st.session_state:
        st.session_state["watchlist"] = Wishlist()

    
    with st.sidebar:
        st.caption("How would you like to get recommendations?")
        rec_option = option_menu(
            menu_title=None,
            options=["Filter","Hybrid Model","Prompt"],
            orientation="vertical",
            icons=["filter", "cpu" , "chat-heart"]
        )
        
        about_tab, appreciation_tab = st.tabs(["About", "Appreciation"])
        with about_tab: st.markdown(script_about)
        with appreciation_tab: st.markdown(script_appreciation)


    match rec_option:
        case "Filter":
            category_tab, title_tab = st.tabs(["Filter by Category","Filter by Title"])
            with category_tab:
                slbCategory = st.selectbox("Category", get_categories())

                col1, col2 = st.columns(2)
                with col1:
                    slbSortOrder = st.radio("Sort Order", ["Descending","Ascending"])
                with col2:
                    slbSortByMem = st.radio("Sort By", ["Rating", "Popular"])
                btnType = st.button("Recommend by Category")
                
                sort_order = False if slbSortOrder == "Descending" else True
                sort_by = False if slbSortByMem == "Average ratings" else True

                if btnType:
                    st.balloons()
                    filterer = RecommenderFiltering(df=df_courses,
                                                    top_k=top_k, 
                                                    sort_order=sort_order, 
                                                    sort_by_mem=sort_by)
                    if slbCategory == "All":
                        rec_filter = filterer._sort_values(df_courses)
                    else:
                        filterer.keyword_search(item_categories=slbCategory)
                        rec_filter = filterer.rec_rs
                    try:
                        print_rec(top_k=top_k,df=rec_filter)
                    except: st.write("Can't find any recommendations for you")
                    
            with title_tab:   
                inputTitle = st.text_input("Enter title")
                btnTitle = st.button("Recommend by Title")

                if btnTitle:
                    st.balloons()
                    filterer = RecommenderFiltering(df=df_courses,
                                                    top_k=top_k, 
                                                    sort_order=sort_order, 
                                                    sort_by_mem=sort_by)
                    filterer.keyword_search(item_title=inputTitle)
                    try:
                        rec_filter = filterer.rec_rs
                        print_rec(top_k=len(rec_filter),df=rec_filter)
                    except AttributeError:
                        st.write("Can't find any recommendations for you")                        

        case "Hybrid Model":
            rating_info_subset = load_data()
            # predictions_knn = load_knn()
            lasso_model = load_lasso()
            col1, col2 = st.columns(2,gap='medium')
            with col1:
                st.subheader("Select courses that you maybe interested in")
                print_hybrid(df=df_courses[:60])

            with col2:  
                st.caption("Your list")
                st.table(pd.Series(st.session_state["watchlist"].rec_list, name="Course Name"))

                movie_to_remove = st.selectbox(
                    "Select a movie to drop", st.session_state["watchlist"].rec_list
                    )
                remove_movie = st.button(
                    "Drop",
                    on_click=st.session_state["watchlist"].remove,
                    args=[(movie_to_remove)], )
                st.subheader("Here is you recommendation")
                try:
                    with st.spinner('Wait for it...'):
                        recommended_courses = cbf_recommend(st.session_state["watchlist"].rec_list,
                                                        rating_info_subset=rating_info_subset,
                                                        lasso_model=lasso_model,
                                                        num_recommendations=top_k)
                        print_rec(top_k=top_k, df=recommended_courses)
                except:
                    st.info(r'(；′⌒`) Sorry cannot find any recommendations for this course, please re-select others')
                # recommended_courses = weighted_hybrid_recommend([st.session_state["watchlist"].rec_list], 
                #                                             predictions_knn=predictions_knn, 
                #                                             predictions_lasso=predictions_lasso,
                #                                             rating_info_subset=rating_info_subset,
                #                                             num_recommendations=top_k, cf_weight=0.15, cbf_weight=0.85)
                # st.write(recommended_courses)


        case "Prompt":
            with st.chat_message("assistant", avatar="😎"):
                st.write("How can i help you generate recommender tasks?")
            input_prompt = st.text_input("Describe your desired recommendations",value="",key=1)
            
            btnPrompt = st.button("Prompt Recommend")
            if btnPrompt:
                st.balloons()
                if input_prompt == "":
                    st.warning("Please describe your desired recommendations")
                else:
                    vectors = joblib.load('Assets/courses_embeddings.pkl')
                    prompt = RecommenderPrompt(df=df_courses,
                                            top_k=top_k,
                                            vectors=vectors, 
                                            input_prompt=input_prompt)
                    with st.chat_message("assistant"):
                        st.write("Here is my recommendations for you")
                        prompt.recCourses()

if __name__ == "__main__":
    run()