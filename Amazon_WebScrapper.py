import csv
from bs4 import BeautifulSoup

### Startup the webdriver
from selenium import webdriver #webdriver is the one driving the action;links up w/ the browser, and performs actions
from selenium.webdriver.common.keys import Keys #lets you to type something in the searchbar and enter and see all the search results

PATH = r"C:\Program Files (x86)\chromedriver.exe"

#The web browser we want to use is chrome, and the web driver web driver for this browser is located at this PATH
driver = webdriver.Chrome(PATH)