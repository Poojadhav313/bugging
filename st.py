import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(page_title = 'test 1')

selected = option_menu(
  menu_title = None,
  options = ['Home', 'About', 'Feedback'],
  orientation = 'horizontal',
  styles={
    "container" : {"padding" : "0", "background-color" :"grey"} ,

  }
)
def convert(obj):
  l=[]
  for i in ast.literal_eval(obj):
    l.append(i['name'])
  return l

def convertt(obj):
  l=[]
  count = 0
  for i in ast.literal_eval(obj):
    if count == 3:
      l.append(i['name'])
      count = count + 1
    else:
      break
  return l

movies=pd.read_csv("movies.csv")
credit = pd.read_csv("credits.csv")
movies.dropna(inplace = True)
movies = movies.merge(credit, on="title")
movies = movies[['movie_id','title','overview','genres','cast','crew','keywords']]

movies.iloc[0].keywords
movies['keywords'] = movies['keywords'].apply(convert)


  


movies['cast'] = movies['cast'].apply(convert)
movies["overview"]=movies["overview"].apply(lambda x:x.split())
movies["genres"]=movies["genres"].apply(lambda x:[i.replace(" ","")for i in x])
movies["keywords"]=movies["keywords"].apply(lambda x:[i.replace(" ","")for i in x])
movies["cast"]=movies["cast"].apply(lambda x:[i.replace(" ","")for i in x])

movies['tags'] = movies['overview']+ movies['genres'] + movies['keywords'] + movies['cast']
df = movies[['movie_id','title','tags']]
df['tags'] = df['tags'].apply(lambda x:' '.join(x))
df['tags'] = df['tags'].apply(lambda x:x.lower())
df['title'] = df['title'].apply(lambda x:x.lower())

cv = CountVectorizer(max_features = 5000, stop_words='english')
data = cv.fit_transform(df['tags']).toarray()
similarity = cosine_similarity(data)



def movie_recommend(m):
  m= m.lower()
  
  #similarity = cosine_similarity(data)
  index = []
  try:
    index = df[df['title'] == m].index[0]
  except:
    pass
  distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
  for i in distances[1:8]:
    print("{}".format(df.iloc[i[0]].title.capitalize()))



def home_page():
  st.title = "Movie recommendation system"

  Mname = st.text_input("enter movies name ")
  
  
  
  
  
 

  

  


  a = [movie_recommend(Mname)]

  st.write(a)






if selected == 'Home':
  home_page()
if selected == 'About':
  st.subheader("about")
if selected == 'Feedback':
  st.subheader("feedback")
