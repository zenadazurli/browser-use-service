import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_BLr7W_ET1WX6LjUMII9eEvGetSy0syz5ZYIr9PURyU0")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con attesa prolungata...")
    
    # Pulizia
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    print("📝 Compilazione form...")
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # === ATTESA MOLTO PIÙ LUNGA ===
    print("⏳ Attesa che la dashboard carichi TUTTO (60 secondi)...")
    time.sleep(60)
    
    # Verifica URL
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip() if result else ""
    print(f"📍 URL dopo login: {current_url}")
    
    if "/account/" in current_url or "/surf/" in current_url:
        print("✅ Dashboard raggiunta!")
        
        # === ATTESA EXTRA PER I COOKIE ===
        print("⏳ Attesa che i cookie di sessione vengano impostati (30 secondi)...")
        time.sleep(30)
        
        # === ORA PRENDI I COOKIE ===
        print("\n🍪 Estrazione cookie con funzione nativa...")
        cookies = run("browser-use cookies get", capture=True)
        cookies_text = cookies.stdout if cookies else ""
        print(f"Output:\n{cookies_text[:800]}")
        
        # Cerca sesids
        sesids = re.search(r'sesids=([^;]+)', cookies_text)
        if not sesids:
            sesids = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        if not sesids:
            sesids = re.search(r'"sesids":\s*"([^"]+)"', cookies_text)
        
        if sesids:
            print(f"\n🎉 SUCCESSO! sesids = {sesids.group(1)}")
            return sesids.group(1), "found"
        else:
            print("\n❌ sesids non trovato. Cookie presenti:")
            # Mostra solo i nomi dei cookie
            names = re.findall(r"'name':\s*'([^']+)'", cookies_text)
            print(f"   Nomi cookie: {names}")
    
    print("❌ Login fallito o cookie non trovati")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - Attesa Prolungata")
    print("=" * 60)
    
    sesids, _ = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids:
        print(f"🎉 RISULTATO: sesids = {sesids}")
    else:
        print("❌ FALLITO - Cookie non trovato nemmeno dopo attesa prolungata")
    print("=" * 60)
    
    run("browser-use close --all")
