import requests
import bs4
import json

#Variables
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
paginated_url = "https://digitsu.com/people?page={page}"
fighters = []
MAX_PAGES = 189

#Scraping loop
for page in range(1, MAX_PAGES + 1):   # pages 1, 2, 3
    response = requests.get(paginated_url.format(page=page), headers=headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    for li in soup.select("ul.list-none.rounded-xl li"):
        name = li.select_one("p").get_text(strip=True)

        full_name = name.split('“')[0] 
        try:
            nickname = name.split('“')[1]  # Remove any unwanted characters and whitespace
        except IndexError:
            nickname = None  # Handle the case where there is no nickname
            pass
        fighters.append({
            'name': full_name,
            'nickname': nickname[:-1] if nickname else None  # Remove the closing quote if nickname exists
        })

print(len(fighters))

#Save to JSON
with open("fighters.json", "w", encoding="utf-8") as f:
    json.dump(fighters, f, ensure_ascii=False, indent=4)

