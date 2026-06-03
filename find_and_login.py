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
    print("🚀 Login con navigazione a /surf/...")
    
    # Pulizia iniziale
    print("🧹 Pulizia sessioni...")
    run("browser-use close --all")
    time.sleep(3)
    
    print(f"🔑 Configura API key...")
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
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
    
    print("⏳ Attesa redirect a /account/ (20 secondi)...")
    time.sleep(20)
    
    print("🎯 Navigazione a /surf/?surftype=2&q=start...")
    run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
    
    print("⏳ Attesa caricamento pagina surf (15 secondi)...")
    time.sleep(15)
    
    # Prova a cliccare Start Surfing con indice invece che testo
    print("🖱️ Cerco indice di Start Surfing...")
    state = run("browser-use state", capture=True)
    if state and state.stdout:
        lines = state.stdout.split('\n')
        for line in lines:
            if 'Start Surfing' in line and 'button' in line.lower():
                match = re.search(r'\[(\d+)\]', line)
                if match:
                    idx = match.group(1)
                    print(f"   Trovato Start Surfing all'indice {idx}")
                    run(f'browser-use click "{idx}"')
                    break
    
    time.sleep(10)
    
    # METODO PIÙ DIRETTO: usa browser-use cookies export
    print("\n🍪 Esportazione cookie con 'cookies export'...")
    run("browser-use cookies export /tmp/cookies.json")
    time.sleep(2)
    
    # Leggi il file esportato
    try:
        with open("/tmp/cookies.json", "r") as f:
            cookies_data = f.read()
        print(f"   Cookie export: {cookies_data[:500]}")
        
        sesids = re.search(r'"sesids"\s*:\s*"([^"]+)"', cookies_data)
        user_id = re.search(r'"user_id"\s*:\s*"([^"]+)"', cookies_data)
        
        if sesids and user_id:
            print(f"\n🎉 SUCCESSO da export! sesids={sesids.group(1)}, user_id={user_id.group(1)}")
            return sesids.group(1), user_id.group(1)
    except Exception as e:
        print(f"   Errore lettura export: {e}")
    
    # Backup: prova browser-use cookies get con formato JSON
    print("\n🍪 browser-use cookies get...")
    cookies = run("browser-use cookies get", capture=True)
    cookies_text = cookies.stdout if cookies else ""
    print(f"   Output: {cookies_text[:800]}")
    
    sesids_match = re.search(r'sesids=([^;]+)', cookies_text) or re.search(r"'sesids':\s*'([^']+)'", cookies_text)
    user_id_match = re.search(r'user_id=([^;]+)', cookies_text) or re.search(r"'user_id':\s*'([^']+)'", cookies_text)
    
    if sesids_match and user_id_match:
        print(f"\n🎉 SUCCESSO! sesids={sesids_match.group(1)}, user_id={user_id_match.group(1)}")
        return sesids_match.group(1), user_id_match.group(1)
    
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
        print("🎉🎉🎉 RISULTATO FINALE: SUCCESSO! 🎉🎉🎉")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
    else:
        print("❌ RISULTATO FINALE: FALLITO")
        print("\n💡 I cookie potrebbero essere HTTP-only e non accessibili")
        print("   Dovremmo usare l'API v2 di Browser Use")
    print("=" * 60)
    
    run("browser-use close --all")
