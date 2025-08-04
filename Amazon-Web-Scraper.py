import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\\Program Files (x86)\\chromedriver.exe"
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
service = Service(PATH)
driver = webdriver.Chrome(service=service, options=options)

def get_url(search_term):
    search_term = search_term.replace(' ', '+')
    return f"https://www.amazon.ca/s?k={search_term}&page={{}}"

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.ca" + atag.get("href")

    try:
        price = item.find("span", class_="a-price").find("span", class_="a-offscreen").text
    except AttributeError:
        return None

    try:
        rating = item.i.text
        review_count = item.select_one("span.a-size-base.s-underline-text").text
    except AttributeError:
        rating = ""
        review_count = ""

    return (description, price, rating, review_count, url)

def main(search_term):
    records = []
    url = get_url(search_term)

    for page in range(1, 4):
        try:
            driver.get(url.format(page))
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
            )
        except Exception as e:
            print(f"Failed to load page {page}: {e}")
            continue

        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.quit()
    filename = f"Amazon_Scraping_Results_{search_term.replace(' ', '_')}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Description", "Price", "Rating", "ReviewCount", "Url"])
        writer.writerows(records)

if __name__ == "__main__":
    main("Protein shaker bottle")