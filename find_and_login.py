import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_bR7YYHPaJDUiGw12ieDu4FLfHZU0YGR4lVLcbBeHcI4")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con nuova API key...")
    
    # 1. Chiudi TUTTO prima di iniziare
    print("🔪 Chiusura sessioni precedenti...")
    run("browser-use close --all")
    time.sleep(5)
    
    # 2. Configura API key
    print("🔑 Configura API key...")
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # 3. Connetti UNA SOLA VOLTA
    print("🔌 Connessione al Cloud...")
    result = run("browser-use cloud connect", capture=True)
    print(f"   {result.stdout[:200] if result else 'Connessione avviata'}")
    time.sleep(8)
    
    # 4. Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(25)
    
    # 5. Compila form
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
    
    # 7. Attesa login
    print("⏳ Attesa login (35 secondi)...")
    time.sleep(35)
    
    # 8. Prendi cookie
    print("\n🍪 Estrazione cookie...")
    
    for attempt in range(10):
        print(f"   Tentativo {attempt+1}/10...")
        
        # Prova con cookies get
        cookies = run("browser-use cookies get", capture=True)
        cookies_text = cookies.stdout if cookies else ""
        
        if attempt == 0:
            print(f"   Output: {cookies_text[:500]}")
        
        # Cerca sesids e user_id
        sesids = re.search(r'sesids=([^;]+)', cookies_text)
        if not sesids:
            sesids = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        if not sesids:
            sesids = re.search(r'"sesids":\s*"([^"]+)"', cookies_text)
        
        user_id = re.search(r'user_id=([^;]+)', cookies_text)
        if not user_id:
            user_id = re.search(r"'user_id':\s*'([^']+)'", cookies_text)
        if not user_id:
            user_id = re.search(r'"user_id":\s*"([^"]+)"', cookies_text)
        
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
        print("   - Se vedi 'HTTP 429' → Troppe sessioni, aspetta 10 minuti")
        print("   - Se vedi 'Error creating cloud profile' → Problema Railway")
        print("   - Se output cookie vuoto → Login fallito")
    print("=" * 60)
    
    # Cleanup finale
    print("\n🔚 Chiusura sessione...")
    run("browser-use close --all")
