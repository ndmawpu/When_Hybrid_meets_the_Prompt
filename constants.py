import pandas as pd
top_k = 10
df_info = pd.read_csv('Data/courses_list.csv')
df_courses = pd.read_csv('Data/courses_processed.csv', index_col=0)
df_ratings = pd.read_csv("Data/ratings_processed.csv", index_col=0)


script_about = '''
This web app is a demo of the Recommender system Scientific research project

***when Hybrid meets the Prompt*** (๑•̀ㅂ•́)و✧

©️ University of Economic and Law, VNU-HCM
'''
script_appreciation = '''
Words fail to express how grateful and appreciative I am for the bombass opportunity to work with my amazing and admirable co-researcher mates: 

- :red[**Nguyen Dinh Minh Anh**]
- :green[**Phan Cao Bao Tram**]
- :violet[**Huynh Thi Kim Ngan**]
- :orange[**Phan Thuy Anh**]
- :blue[**Phan Ngoc Huong Giang**]

the greatest, coolest, and most honourable homies.☆･ﾟ*.✩°｡ ⋆⸜ ✮.

©️ University of Economic and Law, VNU-HCM
'''