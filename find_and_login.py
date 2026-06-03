import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_81hV55sAhAWBUmxoE0vrDX1g9yAL3zTSSNZO73IxwEc")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con attesa prolungata...")
    
    # Pulisci sessioni
    run("browser-use close --all")
    time.sleep(2)
    
    # Configura API key
    run(f"browser-use config set api_key {API_KEY}")
    
    # Connetti al cloud
    print("🔌 Connessione al Browser Use Cloud...")
    run("browser-use cloud connect")
    time.sleep(3)
    
    # Apri pagina login
    print("🌐 Apertura pagina login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    
    # Attesa React iniziale (generosa)
    print("⏳ Attesa React (25 secondi)...")
    time.sleep(25)
    
    # Compilazione form
    print("📝 Compilazione form...")
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # Invio login
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # === ATTESA CHE LA DASHBOARD CARICHI COMPLETAMENTE ===
    print("⏳ Attesa caricamento dashboard (max 90 secondi)...")
    
    dashboard_loaded = False
    for attempt in range(90):
        time.sleep(1)
        
        # Verifica se siamo sulla dashboard
        url_check = run("browser-use eval 'window.location.href'", capture=True)
        current_url = url_check.stdout.strip()
        
        if "/account/" in current_url or "/surf/" in current_url:
            if not dashboard_loaded:
                print(f"✅ Dashboard raggiunta al tentativo {attempt + 1} secondi!")
                dashboard_loaded = True
                
                # Attesa extra per React e cookie
                print("⏳ Attesa cookie di sessione (20 secondi extra)...")
                time.sleep(20)
                break
        
        if attempt % 15 == 0 and attempt > 0:
            print(f"   URL corrente: {current_url[:80]}...")
    
    # === TENTATIVI MULTIPLI PER PRENDERE I COOKIE ===
    print("\n🍪 Ricerca cookie di sessione...")
    
    # Prova sia document.cookie che browser-use cookies get
    for attempt in range(15):
        print(f"   Tentativo {attempt + 1}/15...")
        
        # METODO 1: document.cookie (più diretto)
        doc_cookies = run("browser-use eval 'document.cookie'", capture=True)
        doc_text = doc_cookies.stdout
        
        sesids_match = re.search(r'sesids=([^;]+)', doc_text)
        user_id_match = re.search(r'user_id=([^;]+)', doc_text)
        
        if sesids_match and user_id_match:
            sesids = sesids_match.group(1)
            user_id = user_id_match.group(1)
            print(f"\n🎉 SUCCESSO AL TENTATIVO {attempt + 1}!")
            print(f"   sesids = {sesids}")
            print(f"   user_id = {user_id}")
            return sesids, user_id
        
        # METODO 2: browser-use cookies get (backup)
        bu_cookies = run("browser-use cookies get", capture=True)
        bu_text = bu_cookies.stdout
        
        sesids_match2 = re.search(r"'sesids': '([^']+)'", bu_text)
        user_id_match2 = re.search(r"'user_id': '([^']+)'", bu_text)
        
        if sesids_match2 and user_id_match2:
            sesids = sesids_match2.group(1)
            user_id = user_id_match2.group(1)
            print(f"\n🎉 SUCCESSO (metodo 2) al tentativo {attempt + 1}!")
            print(f"   sesids = {sesids}")
            print(f"   user_id = {user_id}")
            return sesids, user_id
        
        # Mostra progresso
        if doc_text:
            cookies_found = re.findall(r'([a-z_]+)=[^;]+', doc_text)
            if cookies_found:
                print(f"      Cookie presenti: {cookies_found[:5]}")
        
        time.sleep(3)
    
    print("\n❌ Cookie non trovati dopo 15 tentativi")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - EasyHits4U Login")
    print(f"API Key: {API_KEY[:20]}...")
    print("=" * 60)
    
    sesids, user_id = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids and user_id:
        print("🎉 RISULTATO FINALE: SUCCESSO!")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
    else:
        print("❌ RISULTATO FINALE: FALLITO")
    print("=" * 60)
