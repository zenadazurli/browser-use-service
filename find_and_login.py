import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_eYG0cuuk1jkNcpIWUbvTiKCE11OKR4gGniXqeqzmMPY")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con browser-use cookies get --url...")
    
    # Pulizia base
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # 1. Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    # 2. Compila form
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
    time.sleep(30)
    
    # 4. Naviga a /surf/
    print("🎯 Navigazione a /surf/...")
    run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
    time.sleep(20)
    
    # 5. Prendi cookie con --url
    print("\n🍪 Estrazione cookie con browser-use cookies get --url...")
    
    target_url = "https://www.easyhits4u.com/surf/?surftype=2&q=start"
    
    for attempt in range(15):
        print(f"   Tentativo {attempt+1}/15...")
        
        # USO LA FUNZIONE NATIVA CON --url
        cmd = f'browser-use cookies get --url "{target_url}"'
        cookies = run(cmd, capture=True)
        cookies_text = cookies.stdout if cookies else ""
        
        if attempt == 0:
            print(f"   Output completo:\n{cookies_text[:500]}")
        
        # Cerca sesids e user_id nel formato JSON
        sesids = re.search(r'"sesids"\s*:\s*"([^"]+)"', cookies_text)
        user_id = re.search(r'"user_id"\s*:\s*"([^"]+)"', cookies_text)
        
        # Cerca anche formato 'name': 'value'
        if not sesids:
            sesids = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        if not user_id:
            user_id = re.search(r"'user_id':\s*'([^']+)'", cookies_text)
        
        # Cerca formato name=value
        if not sesids:
            sesids = re.search(r'sesids=([^;]+)', cookies_text)
        if not user_id:
            user_id = re.search(r'user_id=([^;]+)', cookies_text)
        
        if sesids and user_id:
            print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
            print(f"   sesids = {sesids.group(1)}")
            print(f"   user_id = {user_id.group(1)}")
            return sesids.group(1), user_id.group(1)
        
        time.sleep(3)
    
    print("\n❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - EasyHits4U")
    print("Uso di browser-use cookies get --url")
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
    
    run("browser-use close --all")
