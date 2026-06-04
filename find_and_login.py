import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_BLr7W_ET1WX6LjUMII9eEvGetSy0syz5ZYIr9PURyU0")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con metodo collaudato...")
    
    # Pulizia base
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione al cloud
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # 1. Apri login
    print("🌐 Apertura pagina login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    # 2. Compila form con TAB (metodo che funzionava)
    print("📝 Compilazione form...")
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # 3. Invio login
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # 4. Attesa redirect
    print("⏳ Attesa redirect (30 secondi)...")
    time.sleep(30)
    
    # 5. Verifica URL
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip() if result else ""
    print(f"📍 URL dopo login: {current_url}")
    
    # 6. Se siamo su /account/ o /surf/, prendi i cookie
    if "/account/" in current_url or "/surf/" in current_url:
        print("✅ Login riuscito!")
        
        # Attesa extra per cookie
        print("⏳ Attesa cookie (10 secondi)...")
        time.sleep(10)
        
        # Prendi cookie
        print("\n🍪 Estrazione cookie...")
        cookies = run("browser-use cookies get", capture=True)
        cookies_text = cookies.stdout if cookies else ""
        print(f"Cookie ricevuti:\n{cookies_text[:800]}")
        
        # Cerca sesids e user_id
        sesids = re.search(r'sesids=([^;]+)', cookies_text) or re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        user_id = re.search(r'user_id=([^;]+)', cookies_text) or re.search(r"'user_id':\s*'([^']+)'", cookies_text)
        
        if sesids and user_id:
            print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
            print(f"   sesids = {sesids.group(1)}")
            print(f"   user_id = {user_id.group(1)}")
            return sesids.group(1), user_id.group(1)
        else:
            print("⚠️ Cookie target non trovati, ma login OK")
            return "login_ok", "login_ok"
    else:
        print("❌ Login fallito - redirect non avvenuto")
        return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - EasyHits4U")
    print("Versione stabile con nuova API key")
    print("=" * 60)
    
    sesids, user_id = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids and user_id:
        if sesids == "login_ok":
            print("✅ Login riuscito! Cookie target non presenti (forse HTTP-only)")
        else:
            print(f"🎉 SUCCESSO COMPLETO!")
            print(f"   sesids = {sesids}")
            print(f"   user_id = {user_id}")
    else:
        print("❌ Login fallito")
    print("=" * 60)
    
    # Cleanup
    run("browser-use close --all")
