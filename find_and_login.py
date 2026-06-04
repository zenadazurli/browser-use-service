import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_lfGFTGeTCkD6-0riqR0zD_DMU3TtKPM78iNOpFW82c8")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies_from_headers():
    print("🚀 Login e cattura cookie dagli headers...")
    
    # Config
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # === ATTIVA NETWORK LOGGING ===
    print("📡 Attivazione network logging...")
    run("browser-use eval 'window.performance.getEntries()'")
    
    # Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    # Compila
    print("📝 Compilazione form...")
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # === CATTURA LA RICHIESTA DI LOGIN ===
    print("🔑 Invio login e cattura headers...")
    
    # Esegui login e prendi i response headers
    run('browser-use keys "Enter"')
    
    # Attesa che la richiesta completi
    time.sleep(30)
    
    # === PRENDI I COOKIE DALLA RESPONSE ===
    print("\n🍪 Estrazione cookie dalla response...")
    
    # Metodo: prendi tutte le richieste di rete
    network = run("browser-use eval 'JSON.stringify(performance.getEntriesByType(\"resource\"))'", capture=True)
    
    # Cerca nella response della POST al login
    response_cookies = run("browser-use eval 'document.cookie'", capture=True)
    print(f"document.cookie: {response_cookies.stdout}")
    
    # Prova a prendere i cookie via CDP
    cdp_cookies = run("browser-use cloud v2 GET /cookies", capture=True)
    print(f"CDP cookies: {cdp_cookies.stdout[:500] if cdp_cookies else ''}")
    
    # Estrai sesids e user_id
    sesids = re.search(r'sesids=([^;]+)', response_cookies.stdout if response_cookies else "")
    user_id = re.search(r'user_id=([^;]+)', response_cookies.stdout if response_cookies else "")
    
    if sesids:
        print(f"\n🎉 sesids = {sesids.group(1)}")
    if user_id:
        print(f"🎉 user_id = {user_id.group(1)}")
    
    if sesids and user_id:
        return sesids.group(1), user_id.group(1)
    
    print("\n❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    sesids, user_id = login_and_get_cookies_from_headers()
    print(f"\n📊 RISULTATO: sesids={sesids}, user_id={user_id}")
    run("browser-use close --all")
