import sqlite3
import os
from datetime import datetime

# Gestione del percorso assoluto per non perdere il DB tra le cartelle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')

def execute_query(query, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()

def init_db():
    # Tabella Utenti
    execute_query('''
        CREATE TABLE IF NOT EXISTS utenti (
            id_telegram INTEGER PRIMARY KEY,
            username TEXT,
            topics TEXT,
            comuni TEXT
        )''')
    # Tabella News (aggiunto time_stamp nell'INSERT)
    execute_query('''
        CREATE TABLE IF NOT EXISTS news_inviate (
            id_news TEXT PRIMARY KEY,
            time_stamp TEXT
        )''')
    print("Inizializzazione DB completata")

def salva_preferenze(user_id, username, topics, comuni):
    """Aggiorna o inserisce le preferenze dell'utente"""
    query = "INSERT OR REPLACE INTO utenti (id_telegram, username, topics, comuni) VALUES (?, ?, ?, ?)"
    execute_query(query, (user_id, username, topics, comuni))
    print(f"Preferenze aggiornate per {username}")

def check_news(id_news):
    """Controlla se la news è già stata inviata, se no la aggiunge con l'ora attuale"""
    query = "SELECT 1 FROM news_inviate WHERE id_news = ?"
    # NOTA: (id_news,) con la virgola è fondamentale!
    if execute_query(query, (id_news,)):
        return True
    
    # Se non c'è, la aggiungiamo includendo il timestamp attuale
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_query("INSERT INTO news_inviate (id_news, time_stamp) VALUES (?, ?)", (id_news, now))
    return False

def clean_db():
    """Elimina notizie più vecchie di 7 giorni"""
    query = "DELETE FROM news_inviate WHERE time_stamp < datetime('now', '-7 days')"
    execute_query(query)
    print("Pulizia database effettuata")

if __name__ == "__main__":
    init_db()
