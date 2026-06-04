import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Hm4Ml3w-doEMXmHGdlmm2YIjPGXsZpWWoBkVuEAGb_o")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def kill_everything():
    """Uccide ASSOLUTAMENTE TUTTO prima di iniziare"""
    print("🔪 Uccisione TOTALE di tutte le sessioni...")
    
    # Lista completa di comandi per uccidere qualsiasi cosa
    commands = [
        "browser-use close --all",
        "browser-use cloud logout",
        "browser-use cloud v2 DELETE /browsers",
        "browser-use close --all",
    ]
    
    for cmd in commands:
        run(cmd)
        time.sleep(2)
    
    print("⏳ Attesa 15 secondi per liberare completamente...")
    time.sleep(15)
    
    # Verifica finale
    run("browser-use close --all")
    time.sleep(3)

def login_and_get_cookies():
    print("🚀 Login con uccisione TOTALE sessioni...")
    
    # 1. UCCIDI TUTTO (il passo più importante!)
    kill_everything()
    
    # 2. Configura API key
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # 3. Connetti UNA VOLTA SOLA
    print("🔌 Connessione singola al Cloud...")
    result = run("browser-use cloud connect", capture=True)
    print(f"   {result.stdout[:200] if result else ''}")
    time.sleep(5)
    
    # 4. Verifica che la connessione sia attiva
    check = run("browser-use eval '1+1'", capture=True)
    if "2" not in check.stdout:
        print("❌ Connessione fallita, riprovo...")
        run("browser-use cloud connect")
        time.sleep(5)
    
    # 5. Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(25)
    
    # 6. Compila form
    print("📝 Compilazione form...")
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # 7. Invio login
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # 8. Attesa login
    print("⏳ Attesa login (30 secondi)...")
    time.sleep(30)
    
    # 9. Prendi cookie
    print("\n🍪 Estrazione cookie...")
    cookies = run("browser-use cookies get", capture=True)
    cookies_text = cookies.stdout if cookies else ""
    print(f"Output: {cookies_text[:500]}")
    
    # Cerca sesids e user_id
    sesids = re.search(r'sesids=([^;]+)', cookies_text) or re.search(r"'sesids':\s*'([^']+)'", cookies_text)
    user_id = re.search(r'user_id=([^;]+)', cookies_text) or re.search(r"'user_id':\s*'([^']+)'", cookies_text)
    
    if sesids and user_id:
        print(f"\n🎉 SUCCESSO! sesids={sesids.group(1)}, user_id={user_id.group(1)}")
        return sesids.group(1), user_id.group(1)
    
    print("❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - Uccisione Totale Sessioni")
    print("=" * 60)
    
    sesids, user_id = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids and user_id:
        print(f"🎉 RISULTATO: sesids={sesids}, user_id={user_id}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    
    # Cleanup finale
    run("browser-use close --all")
