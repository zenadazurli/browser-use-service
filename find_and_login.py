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
    print("🚀 Login e navigazione a /surf/...")
    
    # Cleanup
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # 1. Vai al login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(25)
    
    # 2. Compila
    print("📝 Compilazione form...")
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # 3. Invia
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    time.sleep(15)
    
    # 4. NAVIGA DIRETTAMENTE ALL'URL CHE SETTA I COOKIE
    target_url = "https://www.easyhits4u.com/surf/?surftype=2&q=start"
    print(f"🎯 Navigazione a: {target_url}")
    run(f"browser-use open {target_url}")
    
    # 5. ATTESA LUNGA per il caricamento e l'impostazione dei cookie
    print("⏳ Attesa che i cookie vengano impostati (40 secondi)...")
    time.sleep(40)
    
    # 6. Prendi i cookie da quell'URL
    print("\n🍪 Estrazione cookie...")
    
    for attempt in range(15):
        print(f"   Tentativo {attempt+1}/15...")
        
        # Prendi cookie
        cookies = run("browser-use cookies get", capture=True)
        cookies_text = cookies.stdout if cookies else ""
        
        # Cerca sesids e user_id
        sesids = re.search(r'sesids=([^;]+)', cookies_text)
        user_id = re.search(r'user_id=([^;]+)', cookies_text)
        
        # Prova anche formato JSON
        if not sesids:
            sesids = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        if not user_id:
            user_id = re.search(r"'user_id':\s*'([^']+)'", cookies_text)
        
        if sesids and user_id:
            sesids_val = sesids.group(1) if hasattr(sesids, 'group') else sesids
            user_id_val = user_id.group(1) if hasattr(user_id, 'group') else user_id
            print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
            print(f"   sesids = {sesids_val}")
            print(f"   user_id = {user_id_val}")
            return sesids_val, user_id_val
        
        if attempt % 5 == 0:
            # Mostra i cookie trovati
            found = re.findall(r'([a-z_]+)=', cookies_text)
            print(f"      Cookie trovati: {found[:10] if found else 'nessuno'}")
        
        time.sleep(3)
    
    print("\n❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - EasyHits4U")
    print(f"Target: /surf/?surftype=2&q=start")
    print("=" * 60)
    
    sesids, user_id = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids and user_id:
        print("🎉🎉🎉 RISULTATO FINALE: SUCCESSO! 🎉🎉🎉")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
    else:
        print("❌ RISULTATO FINALE: FALLITO")
        print("\n💡 Possibili cause:")
        print("   1. Turnstile non risolto")
        print("   2. Credenziali errate")
        print("   3. Tempi di attesa insufficienti")
    print("=" * 60)
    
    run("browser-use close --all")
