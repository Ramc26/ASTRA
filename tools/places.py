# tools/places.py

import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def get_nearby_places(location: str, limit: int = 10) -> List[Dict[str, str]]:
    """
    1) Try MakeMyTrip for top attractions.
    2) If that yields < limit, fall back to Holidify.
    Returns up to `limit` dicts with keys: name, description, time_required.
    """
    places: List[Dict[str, str]] = []

    # --- 1) MakeMyTrip ---
    mm_url = f"https://www.makemytrip.com/tripideas/places-to-visit-in-{location.lower()}"
    try:
        mm_resp = requests.get(mm_url, headers={"User-Agent": "Mozilla/5.0"})
        mm_resp.raise_for_status()
        mm_soup = BeautifulSoup(mm_resp.text, "html.parser")

        cards = mm_soup.find_all(
            "div",
            class_=lambda c: c and c.startswith("MostLovedPlaceCard__Container")
        )
        for card in cards[:limit]:
            name = card.find(
                "h3",
                class_=lambda c: c and "MostLovedPlaceCard__Heading" in c
            ).get_text(strip=True)

            desc_tag = card.find(
                "div",
                class_=lambda c: c and "MostLovedPlaceCard__Desc" in c
            )
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            time_tag = card.find(
                "span",
                class_=lambda c: c and "MostLovedPlaceCard__NewPrice" in c
            )
            time_required = time_tag.get_text(strip=True) if time_tag else ""

            places.append({
                "name": name,
                "description": description,
                "time_required": time_required
            })

    except Exception:
        # swallow and fallback below
        places = []

    # --- 2) Fallback: Holidify ---
    if len(places) < limit:
        try:
            holo_url = f"https://www.holidify.com/places/{location}/sightseeing-and-things-to-do.html"
            holo_resp = requests.get(holo_url, headers={"User-Agent": "Mozilla/5.0"})
            holo_resp.raise_for_status()
            holo_soup = BeautifulSoup(holo_resp.text, "html.parser")

            container = holo_soup.find("div", id="attractionList")
            cards = container.find_all(
                "div",
                class_=lambda c: c and "card content-card" in c
            )

            for card in cards:
                if len(places) >= limit:
                    break

                # name
                name_tag = card.find("h3", class_="card-heading")
                if not name_tag:
                    continue
                name = name_tag.get_text(strip=True)

                # description
                desc_tag = card.find("div", class_="readMoreSmall card-text")
                description = desc_tag.get_text(strip=True) if desc_tag else ""

                # time_required: distance from city center
                dist_tag = card.select_one("p.objective.mb-2 span")
                time_required = dist_tag.get_text(strip=True) if dist_tag else ""

                places.append({
                    "name": name,
                    "description": description,
                    "time_required": time_required
                })

        except Exception:
            # if even fallback fails, just return whatever we have
            pass

    return places[:limit]

print(get_nearby_places("Lonavala"))