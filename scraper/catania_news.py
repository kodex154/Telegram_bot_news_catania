import feedparser
import requests
from bs4 import BeautifulSoup
import re

RSS_URL = "https://www.cataniatoday.it/rss"

def analizza_html(url_notizia):
    localita_trovata = None
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_notizia, headers=headers, timeout=3)
        if response.status_code != 200: return None

        soup = BeautifulSoup(response.text, 'html.parser')

        link_loc = soup.find('a', href=re.compile(r'^/notizie/[a-z-]+/$'))
        if link_loc:
            localita_trovata = link_loc.get_text().replace("/", "").strip().title()
        if localita_trovata == "Ultime Notizie":
            localita_trovata = "Catania"
            
    except Exception as e:
        print(f"⚠️ Errore: {e}")

    return localita_trovata

def ricerca_notizia():
    feed = feedparser.parse(RSS_URL)
    news_list=[]

    for entry in feed.entries[:5]:
        localita = analizza_html(entry.link)
        
        articolo = {
            "titolo": entry.title,
            "link": entry.link,
            "topic": entry.tags[0].term,
           "immagine": entry.enclosures[0].href,
            "luogo": localita,
            "riassunto": entry.description
            }
        news_list.append(articolo)

    return news_list

if __name__ == "__main__":
    notizie = ricerca_notizia()
    print("\n" + "="*50)
    for n in notizie:
        print(f"📍 LUOGO:   {n['luogo']}")
        print(f"📰 TITOLO:  {n['titolo']}")
        print(f"   Topic: {n['topic']}")
        print(f"   Link: {n['link']}")
        print(f"   Immagine: {n['immagine']}")
        print(f"   Riassunto: {n['riassunto']}")
        print("-" * 20)
