import csv
from bs4 import BeautifulSoup

### Startup the webdriver
from selenium import webdriver #webdriver is the one driving the action;links up w/ the browser, and performs actions
from selenium.webdriver.common.keys import Keys #lets you to type something in the searchbar and enter and see all the search results

PATH = r"C:\Program Files (x86)\chromedriver.exe"

#The web browser we want to use is chrome, and the web driver web driver for this browser is located at this PATH
driver = webdriver.Chrome(PATH)

#Getting the information needed.
def extract_record(item):
    
    #description and url
    atag = item.h2.a # that is where the info in HTML is stored for that item. ie:name and link to the product
    
    description = atag.text.strip() #gets the name of the product
    url = "https://www.amazon.ca/" + atag.get("href") #gets the url of the product
    
    try:
        #price
        price_parent = item.find("span", "a-price")
        price = price_parent.find("span", "a-offscreen").text
    except AttributeError:
        return
    try:
        #rating and review count
        rating = item.i.text
        review_count = item.find("span",{"class" :"a-size-base", "class":"s-underline-text"}).text
    except AttributeError:
        rating = ""
        review_count = ""

    result = (description, price, rating, review_count, url)
    
    return result
    