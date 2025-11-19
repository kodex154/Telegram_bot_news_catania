import feedparser
import requests
from bs4 import BeautifulSoup
import re

RSS_URL = "https://www.cataniatoday.it/rss"

def estrai_localita(url_notizia):

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_notizia,headers=headers, timeout=5)

        if response.status_code!=200:
            return "Provincia generica"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        link_localita = soup.find('a', href=re.compile(r'/notizie/[a-z-]+/$'))
        if link_localita:
            testo = link_localita.get_text().replace("/", "").strip()
            return testo.title() 

    except Exception as e:
        print(f"⚠️ Errore nello scraping della pagina: {e}")

    return "Provincia (Generico)"

def ricerca_notizia():
    feed = feedparser.parse(RSS_URL)
    news_list=[]

    for entry in feed.entries[:5]:
        localita = estrai_localita(entry.link)

        articolo = {
            "titolo": entry.title,
            "link": entry.link,
           # "topic": entry.topic,
           # "immagine": estrai_immagine(entry),
            "luogo": localita
            }
        news_list.append(articolo)

    return news_list

if __name__ == "__main__":
    notizie = ricerca_notizia()
    print("\n" + "="*50)
    for n in notizie:
        print(f"📍 LUOGO:   {n['luogo']}")
        print(f"📰 TITOLO:  {n['titolo']}")
        print("-" * 20)

