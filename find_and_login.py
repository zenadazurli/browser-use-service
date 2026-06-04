import subprocess
import time
import re
import os
import threading

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_GK40fU_usliPi1of1qtW314GVH4VixyDqx4AhN6Hulc")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

# Variabile globale per i cookie
found_cookies = {"sesids": None, "user_id": None}
stop_polling = False

def poll_cookies():
    """Thread che fa polling continuo dei cookie"""
    global found_cookies, stop_polling
    
    print("🔄 [POLLING] Avviato monitoraggio cookie...")
    attempt = 0
    
    while not stop_polling:
        attempt += 1
        print(f"🔄 [POLLING] Tentativo {attempt}...")
        
        # Prendi i cookie
        cookies = run("browser-use cookies get", capture=True)
        cookies_text = cookies.stdout if cookies else ""
        
        # Cerca sesids
        sesids = re.search(r'sesids=([^;]+)', cookies_text)
        if not sesids:
            sesids = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        
        # Cerca user_id
        user_id = re.search(r'user_id=([^;]+)', cookies_text)
        if not user_id:
            user_id = re.search(r"'user_id':\s*'([^']+)'", cookies_text)
        
        if sesids and not found_cookies["sesids"]:
            found_cookies["sesids"] = sesids.group(1)
            print(f"🎯 [POLLING] TROVATO sesids = {found_cookies['sesids']}")
        
        if user_id and not found_cookies["user_id"]:
            found_cookies["user_id"] = user_id.group(1)
            print(f"🎯 [POLLING] TROVATO user_id = {found_cookies['user_id']}")
        
        # Se abbiamo entrambi, ferma il polling
        if found_cookies["sesids"] and found_cookies["user_id"]:
            print("✅ [POLLING] Entrambi i cookie trovati! Arresto polling...")
            break
        
        # Aspetta 2 secondi prima del prossimo tentativo
        time.sleep(2)
    
    print("🔄 [POLLING] Monitoraggio terminato")

def login_and_get_cookies():
    global stop_polling
    
    print("🚀 Login con polling cookie...")
    
    # Pulizia iniziale
    run("browser-use close --all")
    time.sleep(3)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione al cloud
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Avvia thread di polling
    poll_thread = threading.Thread(target=poll_cookies)
    poll_thread.start()
    
    # Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    # Compila form
    print("📝 Compilazione form...")
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # Invio login
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # Attendi che il polling trovi i cookie (max 120 secondi)
    max_wait = 120
    for i in range(max_wait):
        if found_cookies["sesids"] and found_cookies["user_id"]:
            break
        time.sleep(1)
        if i % 10 == 0:
            print(f"⏳ Attesa cookie... {i}/{max_wait} secondi")
    
    # Ferma il polling
    stop_polling = True
    poll_thread.join(timeout=5)
    
    # Verifica URL finale
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip() if result else ""
    print(f"📍 URL finale: {current_url}")
    
    if found_cookies["sesids"] and found_cookies["user_id"]:
        print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
        print(f"   sesids = {found_cookies['sesids']}")
        print(f"   user_id = {found_cookies['user_id']}")
        return found_cookies["sesids"], found_cookies["user_id"]
    
    print("\n❌ Cookie non trovati dopo 120 secondi")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - Polling Cookie")
    print(f"API Key: {API_KEY[:30]}...")
    print("Monitoraggio continuo fino a quando i cookie non arrivano")
    print("=" * 60)
    
    sesids, user_id = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids and user_id:
        print(f"🎉 RISULTATO FINALE: sesids={sesids}, user_id={user_id}")
    else:
        print("❌ RISULTATO FINALE: FALLITO")
        print("\n💡 Possibili cause:")
        print("   - HTTP 429: troppe sessioni, aspetta 10 minuti")
        print("   - Cookie HTTP-only: non accessibili via CLI")
        print("   - Turnstile non risolto")
    print("=" * 60)
    
    # Cleanup
    run("browser-use close --all")
