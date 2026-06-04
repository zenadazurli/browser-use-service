import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu__j__S3W9tN3zjAX1nShO7WaELi3oH0MDMHCD9TvPFiA")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con navigazione a /surf/...")
    
    # Pulizia iniziale
    print("🧹 Pulizia sessioni...")
    run("browser-use close --all")
    time.sleep(3)
    
    # Configura API key
    print(f"🔑 Configura API key...")
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
    
    # 2. Compila form con TAB
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
    print("⏳ Attesa redirect a /account/ (20 secondi)...")
    time.sleep(20)
    
    # 5. NAVIGA DIRETTAMENTE A /surf/ (LA CHIAVE!)
    print("🎯 Navigazione a /surf/?surftype=2&q=start...")
    run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
    
    # 6. Attesa che la pagina surf carichi
    print("⏳ Attesa caricamento pagina surf (15 secondi)...")
    time.sleep(15)
    
    # 7. Prova a cliccare Start Surfing
    print("🖱️ Click su Start Surfing...")
    run('browser-use click "Start Surfing"')
    time.sleep(10)
    
    # 8. ORA prendi i cookie
    print("\n🍪 Estrazione cookie...")
    
    for attempt in range(15):
        print(f"   Tentativo {attempt+1}/15...")
        
        # Metodo 1: document.cookie
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
        
        # Metodo 2: browser-use cookies get
        cookies = run("browser-use cookies get", capture=True)
        cookies_text = cookies.stdout if cookies else ""
        
        sesids_match2 = re.search(r"'sesids': '([^']+)'", cookies_text)
        user_id_match2 = re.search(r"'user_id': '([^']+)'", cookies_text)
        
        if sesids_match2 and user_id_match2:
            print(f"\n🎉 SUCCESSO (metodo 2)!")
            print(f"   sesids = {sesids_match2.group(1)}")
            print(f"   user_id = {user_id_match2.group(1)}")
            return sesids_match2.group(1), user_id_match2.group(1)
        
        # Mostra progresso
        if doc_text and attempt % 5 == 0:
            cookies_found = re.findall(r'([a-z_]+)=', doc_text)
            print(f"      Cookie presenti: {cookies_found[:8] if cookies_found else 'nessuno'}")
        
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
        print("\nPossibili cause:")
        print("1. Limite sessioni concorrenti (HTTP 429)")
        print("2. Tempi di attesa insufficienti")
        print("3. Problemi con Turnstile")
    print("=" * 60)
    
    # Cleanup
    print("\n🔚 Chiusura sessione...")
    run("browser-use close --all")
