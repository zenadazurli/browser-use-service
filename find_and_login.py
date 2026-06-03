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

def kill_all_sessions():
    """Chiude TUTTE le sessioni attive"""
    print("🔪 Chiusura forzata di tutte le sessioni...")
    run("browser-use close --all")
    run("browser-use cloud logout")
    time.sleep(5)
    
    # Prova a chiudere con v2 API se necessario
    run("browser-use cloud v2 DELETE /browsers")
    time.sleep(2)

def login_and_get_cookies():
    print("🚀 Login con chiusura preventiva sessioni...")
    
    # CHIUDI TUTTO prima di iniziare
    kill_all_sessions()
    
    # Configura API key
    run(f"browser-use config set api_key {API_KEY}")
    
    # Connetti al cloud
    print("🔌 Connessione al Browser Use Cloud...")
    result = run("browser-use cloud connect", capture=True)
    print(result.stdout if result else "Connessione avviata")
    time.sleep(5)
    
    # Apri pagina login
    print("🌐 Apertura pagina login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(5)
    
    # Attesa React iniziale
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
    
    # Attesa dashboard
    print("⏳ Attesa caricamento dashboard (max 60 secondi)...")
    time.sleep(60)
    
    # TENTATIVI PER PRENDERE I COOKIE
    print("\n🍪 Ricerca cookie di sessione...")
    
    for attempt in range(10):
        print(f"   Tentativo {attempt + 1}/10...")
        
        # Leggi document.cookie
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
        
        time.sleep(5)
    
    print("\n❌ Cookie non trovati dopo 10 tentativi")
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
    
    # Chiudi sessione alla fine
    print("\n🔚 Chiusura sessione...")
    run("browser-use close --all")
