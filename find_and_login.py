import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_7FOVF6I0bF0mjR9lnR3dQUsuJBI46LpQrtqSZQdE4jA")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con metodo TAB...")
    
    # Pulizia base
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione al cloud
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    # Compilazione con TAB
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
    
    # Attesa redirect
    print("⏳ Attesa redirect (30 secondi)...")
    time.sleep(30)
    
    # Verifica URL
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip() if result else ""
    print(f"📍 URL: {current_url}")
    
    # Se siamo su /account/ o /surf/, prendi cookie
    if "/account/" in current_url or "/surf/" in current_url:
        print("✅ Login riuscito!")
        
        # Naviga a /surf/ se non ci sei già
        if "/surf/" not in current_url:
            print("🎯 Navigazione a /surf/...")
            run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
            time.sleep(20)
        
        # Prendi cookie
        print("🍪 Estrazione cookie...")
        cookies = run("browser-use cookies get", capture=True)
        cookies_text = cookies.stdout if cookies else ""
        
        sesids = re.search(r'sesids=([^;]+)', cookies_text) or re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        user_id = re.search(r'user_id=([^;]+)', cookies_text) or re.search(r"'user_id':\s*'([^']+)'", cookies_text)
        
        if sesids and user_id:
            print(f"🎉 SUCCESSO! sesids={sesids.group(1)}, user_id={user_id.group(1)}")
            return sesids.group(1), user_id.group(1)
        else:
            print("⚠️ Cookie non trovati, ma login riuscito")
            return "login_ok", "login_ok"
    else:
        print("❌ Login fallito")
        return None, None

if __name__ == "__main__":
    print("=" * 60)
    sesids, user_id = login_and_get_cookies()
    print("=" * 60)
    if sesids and user_id:
        print(f"🎉 RISULTATO: sesids={sesids}, user_id={user_id}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    run("browser-use close --all")
