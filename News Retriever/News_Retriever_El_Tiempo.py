#!/usr/bin/env python
# coding: utf-8

# # Web Scraping news retriever
# This project will consist of making an app that can download 5 news from a given number of websites for later usage of their information in an abstractive summarization model and extractive summarization model.

# In[2]:


#Imports
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import re
import json as js
import datetime
import os

# ## First Step examine the news website
# In this step we will analyze "El Tiempo" a Colombian news website
# 

# ## This is the algorithm in charge of searching an specific parameter in the name of the link
# 

# In[122]:


print("Se cargaron las librerias")

url = "https://www.eltiempo.com/"
res = rq.get(url)
html = res.text
soup = BeautifulSoup(html)
pretty_html=BeautifulSoup.prettify(soup)


# In[3]:


def content_of(url):
    res = rq.get(url)
    html = res.text
    soup = BeautifulSoup(html)
    headline= soup.find_all("h1")[0].get_text()
    p_tags=soup.find_all("p")
    contenido=[]
    titulo=[]
    for con in p_tags:
        if con.get("class") is not None:
            if con.get("class") == ["contenido"]:
                contenido.append(con.get_text())
    return (headline, contenido)

def news_of(url):
    """This function extracts and return all the hyperlinks with the word of interest chosen of a certain link"""
    res = rq.get(url)
    html = res.text
    soup = BeautifulSoup(html)
    pretty_html=BeautifulSoup.prettify(soup)
  
    #Find all the hyperlinks
    article_tags= soup.find_all("article")
    ref=[]
    for i in range(0,len(article_tags)):
        clase = article_tags[i].get("class")
        if clase is not None:
            is_a_video = re.findall("video", "".join(clase))
            if is_a_video != ["video"]:
                a_tags=article_tags[i].find_all("a")
                for lin in a_tags:
                    if lin.get("class") == ['title', 'page-link']:
                        ref.append(lin.get("href"))
                
    return ref


# In[4]:


def content_of_all_El_Tiempo(url):
    refs= news_of(url)
    news=[]
    for link in refs:
        if link.startswith("/"):
            titulo, contenido = content_of(url+link)
            tot=""
            for text in contenido:
                tot=tot+" "+text
            categoria= re.findall('(?<=/)[a-z-]+(?=/)', link)[0]
            temp_dic = {"titulo": titulo, "contenido": tot, "link": url+link,"categoria":categoria.replace("-", " ")}
            news.append(temp_dic)
        
            
    return news
   


# In[5]:

def json_content(url):
    
    print("\n")
    print("\n")
    print(os.getcwd())
    print("\n")
    print("\n")
    news_El_Tiempo= content_of_all_El_Tiempo(url)
    x=datetime.datetime.now().strftime("%Y-%m-%d")
    with open(f"C:\\Users\\usuario\\Desktop\\Universidad\\Proyectos Personales\\News Retriever\\El_Tiempo\\news_El_Tiempo_{x}.json", "w") as f:
        js.dump(news_El_Tiempo, f)


# In[6]:

print("Se definieron las funciones")

url = "https://www.eltiempo.com"
json_content(url)

print("Exito")
# In[11]:


# x=datetime.datetime.now().strftime("%Y-%m-%d")
# with open(f"El_Tiempo/news_El_Tiempo_{x}.json", 'r') as d:
#     info_dict =js.load(d)
# df=pd.DataFrame(info_dict)
# df.head()
# df.shape


# In[141]:





# In[ ]:





# In[ ]:




