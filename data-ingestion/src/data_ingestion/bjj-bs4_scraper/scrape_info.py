import json
import requests
import bs4
import re
import unicodedata
from datetime import datetime

fighters = json.load(open("data-ingestion/src/data_ingestion/bjj-bs4_scraper/data/fighters.json", "r", encoding="utf-8"))
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
URL_TEMPLATE = "https://digitsu.com/people/{url_name}"
URL_NAME_OVERRIDES = {
    "Micael Galvão": "mica-galvao",
}


def make_url_name(name):
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return ascii_name.lower().replace(" ", "-")

fighter_info = []

for fighter in fighters:
    name = fighter['name']
    url_name = URL_NAME_OVERRIDES.get(name, make_url_name(name))

    response = requests.get(URL_TEMPLATE.format(url_name=url_name), headers=HEADERS)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        # Extract the desired information from the soup object
        # For example, let's say we want to extract the fighter's profile info

        record_label = soup.find(
            "span",
            string=lambda text: isinstance(text, str) and text.strip() == "Record:"
        )

        #W/L/D Record
        record_element = (
            record_label.find_next_sibling("span") if record_label else None
        )
        record = record_element.get_text(strip=True) if record_element else None
        record_parts = record.split("-") if record else []
        win = record_parts[0] if len(record_parts) > 0 else None
        loss = record_parts[1] if len(record_parts) > 1 else None
        draw = record_parts[2].replace(' (W', '') if len(record_parts) > 2 else None
        
        #Born Date
        born_label = soup.find(
                    "span",
                    string=lambda text: isinstance(text, str) and text.strip() == "Born:"
                )
        born_element = (
            born_label.find_next_sibling("span") if born_label else None
        )
        born = born_element.get_text(strip=True) if born_element else None
        born_date_match = re.match(r"([A-Za-z]+ \d{1,2}, \d{4})", born or "")
        born_date = (
            datetime.strptime(born_date_match.group(1), "%B %d, %Y").date().isoformat()
            if born_date_match
            else None
        )

        #Black Belt Under
        belt_under_label = soup.find(
            "span",
            string=lambda text: isinstance(text, str) and text.strip() == "Black Belt Under:"
        )
        belt_under_element = (
            belt_under_label.find_next_sibling("span") if belt_under_label else None
        )
        belt_under = belt_under_element.get_text(strip=True) if belt_under_element else None

        #Weight Class
        weight_class_label = soup.find(
            "span",
            string=lambda text: isinstance(text, str) and text.strip() == "Weight Class:"
        )
        weight_class_element = (
            weight_class_label.find_next_sibling("span") if weight_class_label else None
        )
        weight_class = weight_class_element.get_text(strip=True) if weight_class_element else None
        weight_match = re.match(
            r"(?P<name>.*?)\s*\(?\s*(?P<kgs>\d+(?:\.\d+)?)\s*kg\s*/\s*"
            r"(?P<lbs>\d+(?:\.\d+)?)\s*lbs?\s*\)?$",
            weight_class or "",
            re.IGNORECASE,
        )
        weight_class_name = weight_match.group("name").strip() if weight_match else None
        weight_kgs = float(weight_match.group("kgs")) if weight_match else None
        weight_lbs = float(weight_match.group("lbs")) if weight_match else None

        #Favorite Technique
        fav_techniques_label = soup.find(
            "span",
            string=lambda text: isinstance(text, str) and text.strip() == "Favorite Technique:"
        )
        fav_technique_element = (
            fav_techniques_label.find_next_sibling("span") if fav_techniques_label else None
        )
        fav_technique = fav_technique_element.get_text(strip=True) if fav_technique_element else None

        team_label = soup.find(
            "span",
            string=lambda text: isinstance(text, str) and text.strip() == "Team:"
        )
        team_element = (
            team_label.find_next_sibling("span") if team_label else None
        )
        team = team_element.get_text(strip=True) if team_element else None  

        fighter_info.append({
            'name': name,
            'nickname': fighter['nickname'],
            'wins' : win,
            'losses' : loss,
            'draws' : draw,
            'born_date' : born_date,
            'belt_under' : belt_under,
            'weight_class_name' : weight_class_name,
            'weight_kgs' : weight_kgs,
            'weight_lbs' : weight_lbs,
            'fav_technique' : fav_technique,
            'team' : team
        })

with open("fighters_info.json", "w", encoding="utf-8") as f:
    json.dump(fighter_info, f, ensure_ascii=False, indent=4)
