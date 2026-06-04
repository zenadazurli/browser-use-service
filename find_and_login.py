import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Hm4Ml3w-doEMXmHGdlmm2YIjPGXsZpWWoBkVuEAGb_o")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login e cattura cookie...")
    
    # Pulizia iniziale
    run("browser-use close --all")
    time.sleep(3)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione al cloud
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # 1. Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(25)
    
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
    
    # 4. Attesa che il login venga elaborato
    print("⏳ Attesa login (30 secondi)...")
    time.sleep(30)
    
    # 5. Verifica URL (controllo se il redirect è avvenuto)
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip() if result else ""
    print(f"📍 URL dopo login: {current_url}")
    
    # 6. Prendi cookie immediatamente
    print("\n🍪 Estrazione cookie...")
    
    for attempt in range(10):
        print(f"   Tentativo {attempt+1}/10...")
        
        # Prendi cookie con URL esplicito
        cookies = run("browser-use cookies get --url https://www.easyhits4u.com", capture=True)
        cookies_text = cookies.stdout if cookies else ""
        
        if attempt == 0:
            print(f"   Output: {cookies_text[:500]}")
        
        # Cerca sesids e user_id in tutti i formati possibili
        sesids = re.search(r'sesids=([^;]+)', cookies_text) or re.search(r"'sesids':\s*'([^']+)'", cookies_text) or re.search(r'"sesids":\s*"([^"]+)"', cookies_text)
        user_id = re.search(r'user_id=([^;]+)', cookies_text) or re.search(r"'user_id':\s*'([^']+)'", cookies_text) or re.search(r'"user_id":\s*"([^"]+)"', cookies_text)
        
        if sesids and user_id:
            print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
            print(f"   sesids = {sesids.group(1)}")
            print(f"   user_id = {user_id.group(1)}")
            return sesids.group(1), user_id.group(1)
        
        time.sleep(3)
    
    print("\n❌ Cookie non trovati dopo 10 tentativi")
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
        print("\n💡 Possibili cause:")
        print("   - Turnstile non risolto")
        print("   - Credenziali errate")
        print("   - Limite sessioni Browser Use (HTTP 429)")
        print("   - Piano Railway free (limiti egress)")
    print("=" * 60)
    
    # Cleanup finale
    run("browser-use close --all")
