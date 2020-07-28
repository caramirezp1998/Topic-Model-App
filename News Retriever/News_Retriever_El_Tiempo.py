#!/usr/bin/env python
# coding: utf-8

# # Web Scraping news retriever

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


print("Libraries are loaded")

# Here we use the beautiful soup library to parse the html code from the link
url = "https://www.eltiempo.com/"
res = rq.get(url)
html = res.text
soup = BeautifulSoup(html)
pretty_html=BeautifulSoup.prettify(soup)


# In[3]:


def content_of(url):
    """This function is in charge parsing the url receive by parameter and extracting all the content
    inside the p tags (text tags) and title, which is the h1 tag. It returns a tuple of the headline and the title """
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
    """This function extracts and return all the hyperlinks that can be accesed through the url given by parameter,
    that belongs the class article and is not a video. This function returns a list with all the links to the articles of the web page"""
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
    """ This function recieves the El Tiempo news website and uses the other two functions in order to created a dictionary, with the title, content, link, and category of the article. The dictionary is return after all the articles accessible through the main page are revised for extraction.  
    """
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
    """ This function saves the dictionary recieved by the last function and saves it in the given directory in a json format with the date of extraction in its name"""
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

print("Functions were declared successfully")

url = "https://www.eltiempo.com"
json_content(url)

print("Content was successfully extracted and saved")
# In[11]:



