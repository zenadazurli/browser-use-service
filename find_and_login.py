import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Wwr8NyQJYHl0Qnm9MBXQbAgSFEFOvwAx8X4_HucmwOg")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con navigazione a /surf/...")
    
    # Pulizia iniziale
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connetti al cloud
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # 1. Apri pagina login
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
    
    # 4. Attesa redirect a /account/
    print("⏳ Attesa redirect a /account/...")
    time.sleep(20)
    
    # 5. NAVIGA DIRETTAMENTE A /surf/ (LA CHIAVE!)
    print("🎯 Navigazione a /surf/?surftype=2&q=start...")
    run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
    
    # 6. Attesa che la pagina surf carichi completamente
    print("⏳ Attesa caricamento pagina surf (20 secondi)...")
    time.sleep(20)
    
    # 7. Clicca sul pulsante Start Surfing (opzionale, ma lo facciamo per sicurezza)
    print("🖱️ Cerco pulsante Start Surfing...")
    run('browser-use click "Start Surfing"')
    time.sleep(10)
    
    # 8. ORA prendi i cookie (DOVREBBERO ESSERCI!)
    print("\n🍪 Estrazione cookie...")
    
    for attempt in range(10):
        # document.cookie
        doc = run("browser-use eval 'document.cookie'", capture=True)
        doc_text = doc.stdout if doc else ""
        
        sesids_match = re.search(r'sesids=([^;]+)', doc_text)
        user_id_match = re.search(r'user_id=([^;]+)', doc_text)
        
        if sesids_match and user_id_match:
            sesids = sesids_match.group(1)
            user_id = user_id_match.group(1)
            print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
            print(f"   sesids = {sesids}")
            print(f"   user_id = {user_id}")
            return sesids, user_id
        
        print(f"   Tentativo {attempt+1}/10: cookie non ancora pronti...")
        time.sleep(3)
    
    # Backup: prova browser-use cookies get
    print("\n🔍 Tentativo con browser-use cookies get...")
    cookies = run("browser-use cookies get", capture=True)
    print(f"Output: {cookies.stdout[:500] if cookies else ''}")
    
    sesids_match = re.search(r"'sesids': '([^']+)'", cookies.stdout if cookies else "")
    user_id_match = re.search(r"'user_id': '([^']+)'", cookies.stdout if cookies else "")
    
    if sesids_match and user_id_match:
        print(f"\n🎉 Cookie trovati! sesids={sesids_match.group(1)}")
        return sesids_match.group(1), user_id_match.group(1)
    
    print("\n❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    sesids, user_id = login_and_get_cookies()
    print("=" * 60)
    if sesids and user_id:
        print(f"🎉 SESIDS: {sesids}")
        print(f"🎉 USER_ID: {user_id}")
    else:
        print("❌ FALLITO - Controlla i log")
    print("=" * 60)
    
    # Cleanup
    run("browser-use close --all")
