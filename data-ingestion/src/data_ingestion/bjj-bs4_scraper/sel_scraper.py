from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import json

#Chrome Launcher
# options = Options()
# options.add_argument("--headless=new")            # modern headless mode
# options.add_argument("--window-size=1920,1080")   # real desktop viewport
# options.add_argument("--no-sandbox")              # needed in many containers
# options.add_argument("--disable-dev-shm-usage")   # avoid /dev/shm crashes in Docker

# driver = webdriver.Chrome(options=options)

# driver.get("https://books.toscrape.com/")

# # Hand the rendered HTML to BeautifulSoup
# soup = BeautifulSoup(driver.page_source, "html.parser")

# # Now parse with BeautifulSoup's API instead of Selenium's
# title = soup.find("h1").get_text(strip=True)

# driver.quit()  # Close the browser after scraping
# RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# books = []
# for book in soup.select(".product_pod"):
#     title = book.h3.a["title"]
#     price = book.select_one(".price_color").get_text(strip=True)
#     rating_class = book.select_one(".star-rating")["class"][1]
#     rating = RATING_MAP.get(rating_class, 0)  # Default to 0 if not found

#     books.append({
#         "title": title,
#         "price": price,
#         "rating": rating
#     })
# print("Total books found:", len(books))
# print(books[0])

# # books = the list of dicts from the previous section

# with open("books.csv", "w", newline="", encoding="utf-8") as f:
#     writer = csv.DictWriter(f, fieldnames=["title", "price", "in_stock", "rating"])
#     writer.writeheader()
#     writer.writerows(books)

# with open("books.json", "w", encoding="utf-8") as f:
#     json.dump(books, f, ensure_ascii=False, indent=4)

# options = Options()
# options.add_argument("--headless=new")
# options.add_argument("--window-size=1920,1080")
# driver = webdriver.Chrome(options=options)

# all_rows = []
# for page in range(1, 4):   # pages 1, 2, 3
#     driver.get(f"https://www.scrapethissite.com/pages/forms/?page_num={page}")
#     soup = BeautifulSoup(driver.page_source, "html.parser")

#     for tr in soup.select("tr.team"):
#         cells = tr.find_all("td")
#         all_rows.append({
#             "team": cells[0].get_text(strip=True),
#             "year": cells[1].get_text(strip=True),
#             "wins": cells[2].get_text(strip=True),
#             "losses": cells[3].get_text(strip=True),
#         })

# driver.quit()
# print(f"scraped {len(all_rows)} rows across 3 pages")
# print(all_rows[0])

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

all_rows = []
for page in range(1, 4):   # pages 1, 2, 3
    driver.get(f"https://digitsu.com/people?page={page}")
    soup = BeautifulSoup(driver.page_source, "html.parser")

    print(soup.select("ul.list-none.rounded-xl"))
    

driver.quit()
print(f"scraped {len(all_rows)} rows across 3 pages")
print(all_rows[0])