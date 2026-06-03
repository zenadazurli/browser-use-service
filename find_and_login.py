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
    print("🚀 Login con attesa MOLTO lunga per cookie...")
    
    # Pulizia
    run("browser-use close --all")
    time.sleep(3)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(25)
    
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
    
    print("⏳ Attesa redirect a /surf/ (45 secondi)...")
    time.sleep(45)
    
    print("🎯 Navigazione a /surf/?surftype=2&q=start...")
    run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
    
    # --- ATTESA MOLTO LUNGA PER I COOKIE ---
    print("⏳ ATTESA MOLTO LUNGA per caricamento cookie (90 secondi)...")
    print("   I cookie sesids e user_id arrivano dopo molto tempo!")
    time.sleep(90)
    
    # Tentativi con attesa crescente
    print("\n🍪 Estrazione cookie con tentativi prolungati...")
    
    for attempt in range(20):
        print(f"   Tentativo {attempt+1}/20 (attesa {3 + attempt}s prima del tentativo)...")
        
        # Attesa crescente tra i tentativi
        time.sleep(3 + attempt // 2)
        
        # Prova con export
        run("browser-use cookies export /tmp/cookies.json")
        time.sleep(1)
        
        try:
            with open("/tmp/cookies.json", "r") as f:
                cookies_data = f.read()
            
            sesids = re.search(r'"sesids"\s*:\s*"([^"]+)"', cookies_data)
            user_id = re.search(r'"user_id"\s*:\s*"([^"]+)"', cookies_data)
            
            if sesids and user_id:
                print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
                print(f"   sesids = {sesids.group(1)}")
                print(f"   user_id = {user_id.group(1)}")
                return sesids.group(1), user_id.group(1)
        except:
            pass
        
        # Prova con document.cookie
        doc = run("browser-use eval 'document.cookie'", capture=True)
        doc_text = doc.stdout if doc else ""
        
        sesids_match = re.search(r'sesids=([^;]+)', doc_text)
        user_id_match = re.search(r'user_id=([^;]+)', doc_text)
        
        if sesids_match and user_id_match:
            print(f"\n🎉 SUCCESSO via document.cookie!")
            print(f"   sesids = {sesids_match.group(1)}")
            print(f"   user_id = {user_id_match.group(1)}")
            return sesids_match.group(1), user_id_match.group(1)
        
        # Mostra progresso ogni 5 tentativi
        if attempt % 5 == 0:
            cookies_found = re.findall(r'([a-z_]+)=', doc_text)
            print(f"      Cookie attuali: {cookies_found[:10]}")
    
    print("\n❌ Cookie non trovati dopo 20 tentativi e attesa totale di ~5 minuti")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - EasyHits4U")
    print("ATTESA MOLTO LUNGA per cookie (fino a 5 minuti)")
    print("=" * 60)
    
    start_time = time.time()
    sesids, user_id = login_and_get_cookies()
    elapsed = int(time.time() - start_time)
    
    print("\n" + "=" * 60)
    print(f"Tempo totale: {elapsed} secondi")
    if sesids and user_id:
        print("🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    
    run("browser-use close --all")
