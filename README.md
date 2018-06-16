# wiki_api
An API built for web integration that can return the top most relevant parent categories of a topic ( with context) using web scraping.

## How it works

wiki_api was made using a modular approach for easy maintainance and integration into web applications. It works by first taking input of the 'keyword' to be searched along with its associated context. It then performs a google search to ascertain whether an associated wikipedia page exists. If it does then it scrapes the top 3 parent categories of the keyword-context pair. The top 3 selection is made by finding the 3 categories with the highest number of associated sub categories which was used as a measure of relevancy. Multithreading was used to reduce computational time by parallelising each category search. 

## Dependencies

wiki_api was scripted in Python 3.6 and the following packages were used:

a) googlesearch

b) requests

c) json

d) multiprocessing.dummy
