import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_wv8fkZC5bVGk4QJiIeMDI3Ce7tAexKiNi3sfPbTTeSU")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con nuova API key...")
    
    # 1. Pulizia sessioni
    print("🧹 Pulizia sessioni...")
    run("browser-use close --all")
    time.sleep(3)
    
    # 2. Configura API key
    print(f"🔑 Configura API key...")
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # 3. Connetti al cloud
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # 4. Apri login
    print("🌐 Apertura pagina login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(25)
    
    # 5. Compila form con TAB
    print("📝 Compilazione form...")
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # 6. Invio login
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # 7. Attesa redirect
    print("⏳ Attesa redirect (35 secondi)...")
    time.sleep(35)
    
    # 8. Verifica URL
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip() if result else ""
    print(f"📍 URL dopo login: {current_url}")
    
    # 9. Naviga a /surf/
    print("🎯 Navigazione a /surf/?surftype=2&q=start...")
    run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
    time.sleep(20)
    
    # 10. Prendi cookie con --url
    print("\n🍪 Estrazione cookie con browser-use cookies get --url...")
    
    target_url = "https://www.easyhits4u.com/surf/?surftype=2&q=start"
    
    for attempt in range(15):
        print(f"   Tentativo {attempt+1}/15...")
        
        cmd = f'browser-use cookies get --url "{target_url}"'
        cookies = run(cmd, capture=True)
        cookies_text = cookies.stdout if cookies else ""
        
        if attempt == 0:
            print(f"   Output: {cookies_text[:500]}")
        
        # Cerca sesids e user_id in vari formati
        sesids = re.search(r'"sesids"\s*:\s*"([^"]+)"', cookies_text)
        if not sesids:
            sesids = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        if not sesids:
            sesids = re.search(r'sesids=([^;]+)', cookies_text)
        
        user_id = re.search(r'"user_id"\s*:\s*"([^"]+)"', cookies_text)
        if not user_id:
            user_id = re.search(r"'user_id':\s*'([^']+)'", cookies_text)
        if not user_id:
            user_id = re.search(r'user_id=([^;]+)', cookies_text)
        
        if sesids and user_id:
            print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
            print(f"   sesids = {sesids.group(1)}")
            print(f"   user_id = {user_id.group(1)}")
            return sesids.group(1), user_id.group(1)
        
        time.sleep(3)
    
    print("\n❌ Cookie non trovati dopo 15 tentativi")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - EasyHits4U")
    print(f"API Key: {API_KEY[:30]}...")
    print("=" * 60)
    
    sesids, user_id = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids and user_id:
        print("🎉🎉🎉 RISULTATO FINALE: SUCCESSO! 🎉🎉🎉")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
    else:
        print("❌ RISULTATO FINALE: FALLITO")
        print("\n💡 Diagnostica:")
        print("   Se 'URL dopo login' NON contiene /account/ o /surf/ → login fallito")
        print("   Se 'Output' è cookies: [] → nessun cookie, login non autenticato")
        print("   Se HTTP 402 → limite piano free, upgrade necessario")
    print("=" * 60)
    
    run("browser-use close --all")
