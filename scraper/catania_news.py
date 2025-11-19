import feedparser
import requests
from bs4 import BeautifulSoup
import re

RSS_URL = "https://www.cataniatoday.it/rss"

TOPIC_AMMESSI = [
    "Cronaca", "Politica", "Attualità", "Sport", 
    "Economia E Lavoro",
    "Meteo", "Ambiente", 
    "Salute", "Motori", "Dossier", "Guide Catania","Cinema"
]
def analizza_html(url_notizia):
    localita_trovata = None
    topic_trovato = "Attualità"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url_notizia, headers=headers, timeout=3)
        if response.status_code != 200: return None, topic_trovato 

        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. LOCALITÀ
        link_loc = soup.find('a', href=re.compile(r'^/notizie/[a-z-]+/$'))
        if link_loc:
            localita_trovata = link_loc.get_text().replace("/", "").strip().title()

        # 2. TOPIC (Versione Super Pulita)
        candidati = soup.find_all('a',href=re.compile(r'^/[a-z-]+/$'))
       # print(candidati)
        for tag in candidati:
            txt = tag.get_text().strip().title()
            
            # Whitelist check
            if txt in TOPIC_AMMESSI:
                topic_trovato = txt
                break

    except Exception as e:
        print(f"⚠️ Errore: {e}")

    return localita_trovata, topic_trovato

def ricerca_notizia():
    feed = feedparser.parse(RSS_URL)
    news_list=[]

    for entry in feed.entries[:5]:
        localita,topic_def = analizza_html(entry.link)
        if 'tags' in entry and len(entry.tags) > 0:

        # 2. Prendo il primo elemento (indice 0)
        # Ogni tag è un dizionario: {'term': 'Cronaca', 'scheme': null, ...}
            tag_strano = entry.tags[0]

        # 3. Estraggo il valore 'term' (il testo vero e proprio)
            categoria = tag_strano.term

        articolo = {
            "titolo": entry.title,
            "link": entry.link,
            "topic": categoria,
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
        print(f"   Topic: {n['topic']}")
        print(f"   Link: {n['link']}")
        print("-" * 20)

