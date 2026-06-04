import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_GK40fU_usliPi1of1qtW314GVH4VixyDqx4AhN6Hulc")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con attesa elemento dashboard...")
    
    # Pulizia
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    # Compila form
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
    
    # === ATTESA INTELLIGENTE: aspetta che un elemento della dashboard sia visibile ===
    print("\n⏳ Attesa che la dashboard carichi (aspetto elemento '.userinfo .text')...")
    
    max_wait = 60  # 60 secondi massimo
    dashboard_loaded = False
    
    for attempt in range(max_wait):
        time.sleep(1)
        
        # Cerca l'elemento che appare SOLO quando sei loggato
        # In questo caso, il nome utente nel menu
        check = run("browser-use eval 'document.querySelector(\".userinfo .text\") !== null'", capture=True)
        
        if "true" in check.stdout:
            print(f"✅ Dashboard caricata! (tentativo {attempt + 1} secondi)")
            dashboard_loaded = True
            break
        
        if attempt % 10 == 0:
            print(f"   Attesa... {attempt}/{max_wait} secondi")
    
    # Verifica anche l'URL come fallback
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip() if result else ""
    print(f"📍 URL attuale: {current_url}")
    
    if not dashboard_loaded and ("/account/" in current_url or "/surf/" in current_url):
        print("✅ Dashboard rilevata da URL!")
        dashboard_loaded = True
    
    if dashboard_loaded:
        print("\n✅ LOGIN CONFERMATO!")
        
        # Attesa extra per i cookie
        print("⏳ Attesa cookie di sessione (10 secondi)...")
        time.sleep(10)
        
        # Prendi i cookie
        print("\n🍪 Estrazione cookie...")
        
        for attempt in range(10):
            print(f"   Tentativo {attempt+1}/10...")
            
            cookies = run("browser-use cookies get", capture=True)
            cookies_text = cookies.stdout if cookies else ""
            
            sesids = re.search(r'sesids=([^;]+)', cookies_text)
            if not sesids:
                sesids = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
            
            user_id = re.search(r'user_id=([^;]+)', cookies_text)
            if not user_id:
                user_id = re.search(r"'user_id':\s*'([^']+)'", cookies_text)
            
            if sesids and user_id:
                print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
                print(f"   sesids = {sesids.group(1)}")
                print(f"   user_id = {user_id.group(1)}")
                return sesids.group(1), user_id.group(1)
            
            time.sleep(2)
        
        print("⚠️ Cookie target non trovati, ma login OK")
        return "login_ok", "login_ok"
    
    print("❌ Login fallito - dashboard non raggiunta")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - Attesa Elemento Dashboard")
    print("=" * 60)
    
    sesids, user_id = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids and user_id:
        if sesids == "login_ok":
            print("✅ Login OK, ma cookie HTTP-only non accessibili")
        else:
            print(f"🎉 SUCCESSO! sesids={sesids}, user_id={user_id}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    
    run("browser-use close --all")
