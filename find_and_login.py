import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_7FOVF6I0bF0mjR9lnR3dQUsuJBI46LpQrtqSZQdE4jA")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Avvio...")
    
    # Cleanup
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # 1. Login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    print("📝 Compilazione form...")
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    run('browser-use keys "Enter"')
    
    # 2. Attendi redirect a /surf/
    print("⏳ Attesa redirect a /surf/...")
    for attempt in range(40):
        time.sleep(1)
        result = run("browser-use eval 'window.location.href'", capture=True)
        url = result.stdout.strip() if result else ""
        if "/surf/" in url:
            print(f"✅ Redirect riuscito dopo {attempt+1} secondi!")
            break
    else:
        print("⚠️ Redirect non rilevato, continuo...")
    
    # 3. Attesa extra per caricamento completo
    print("⏳ Attesa caricamento completo (20 secondi)...")
    time.sleep(20)
    
    # 4. Estrai cookie con metodo diretto
    print("\n🍪 Estrazione cookie...")
    
    # Prova con document.cookie
    doc = run("browser-use eval 'document.cookie'", capture=True)
    doc_text = doc.stdout if doc else ""
    print(f"document.cookie: {doc_text[:200]}")
    
    # Prova con browser-use cookies get
    cookies = run("browser-use cookies get", capture=True)
    cookies_text = cookies.stdout if cookies else ""
    print(f"browser-use cookies get: {cookies_text[:500]}")
    
    # Regex per cercare sesids e user_id
    sesids = None
    user_id = None
    
    # Cerca in document.cookie
    match = re.search(r'sesids=([^;]+)', doc_text)
    if match:
        sesids = match.group(1)
        print(f"✅ sesids trovato in document.cookie: {sesids}")
    
    match = re.search(r'user_id=([^;]+)', doc_text)
    if match:
        user_id = match.group(1)
        print(f"✅ user_id trovato in document.cookie: {user_id}")
    
    # Se non trovati, cerca nel formato JSON
    if not sesids:
        match = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        if match:
            sesids = match.group(1)
            print(f"✅ sesids trovato in cookies get: {sesids}")
    
    if not user_id:
        match = re.search(r"'user_id':\s*'([^']+)'", cookies_text)
        if match:
            user_id = match.group(1)
            print(f"✅ user_id trovato in cookies get: {user_id}")
    
    # Se ancora non trovati, cerca nel JSON
    if not sesids:
        match = re.search(r'"sesids":\s*"([^"]+)"', cookies_text)
        if match:
            sesids = match.group(1)
            print(f"✅ sesids trovato in JSON: {sesids}")
    
    if not user_id:
        match = re.search(r'"user_id":\s*"([^"]+)"', cookies_text)
        if match:
            user_id = match.group(1)
            print(f"✅ user_id trovato in JSON: {user_id}")
    
    if sesids and user_id:
        print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
        return sesids, user_id
    
    print("\n❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - EasyHits4U")
    print(f"API Key: {API_KEY[:30]}...")
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
    
    # Cleanup
    run("browser-use close --all")
