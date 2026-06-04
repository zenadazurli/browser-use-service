import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_j5cD-CjtrMt_B0ZeLbjY63JzanTQIRjeaROaJYfLs54")

def run_sync(cmd, timeout=60):
    """Esegue un comando e aspetta la risposta prima di continuare"""
    print(f"   > {cmd[:80]}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.stdout:
        print(f"   < {result.stdout[:100].strip()}")
    return result

def wait_for_element(selector, timeout=60):
    """Aspetta che un elemento sia presente nel DOM"""
    print(f"⏳ Attesa elemento: {selector}")
    start = time.time()
    while time.time() - start < timeout:
        result = run_sync(f'browser-use eval "document.querySelector(\'{selector}\') !== null"', timeout=10)
        if "true" in result.stdout:
            print(f"✅ Elemento trovato! ({int(time.time() - start)}s)")
            return True
        time.sleep(2)
    print(f"❌ Elemento non trovato dopo {timeout}s")
    return False

def login_and_get_cookies():
    print("🚀 Login sincronizzato con Browser Use...")
    
    # 1. Pulizia
    print("\n[1] Pulizia sessioni...")
    run_sync("browser-use close --all")
    time.sleep(2)
    run_sync(f"browser-use config set api_key {API_KEY}")
    time.sleep(1)
    
    # 2. Connessione
    print("\n[2] Connessione al Cloud...")
    result = run_sync("browser-use cloud connect")
    if "connected" not in result.stdout:
        print("   Connessione fallita, riprovo...")
        time.sleep(3)
        result = run_sync("browser-use cloud connect")
    print("✅ Connesso!")
    time.sleep(3)
    
    # 3. Apri login
    print("\n[3] Apertura pagina login...")
    run_sync("browser-use open https://www.easyhits4u.com/logon/")
    
    # 4. Aspetta form
    print("\n[4] Attesa caricamento form...")
    wait_for_element('input[name="username"]', timeout=30)
    
    # 5. Compila username
    print("\n[5] Compilazione username...")
    run_sync('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    
    # 6. Tab al password
    print("\n[6] Vai al campo password...")
    run_sync('browser-use keys "Tab"')
    time.sleep(1)
    
    # 7. Compila password
    print("\n[7] Compilazione password...")
    run_sync('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # 8. Invio login
    print("\n[8] Invio login...")
    run_sync('browser-use keys "Enter"')
    
    # 9. Attesa dashboard
    print("\n[9] Attesa dashboard...")
    if wait_for_element('.userinfo .text', timeout=60):
        print("✅ Dashboard raggiunta!")
        
        # 10. Attesa cookie
        print("\n[10] Attesa cookie di sessione (10s)...")
        time.sleep(10)
        
        # 11. Prendi cookie con retry
        print("\n[11] Estrazione cookie...")
        for attempt in range(10):
            print(f"   Tentativo {attempt+1}/10...")
            result = run_sync("browser-use cookies get")
            
            sesids = re.search(r'sesids=([^;]+)', result.stdout)
            if not sesids:
                sesids = re.search(r"'sesids':\s*'([^']+)'", result.stdout)
            
            user_id = re.search(r'user_id=([^;]+)', result.stdout)
            if not user_id:
                user_id = re.search(r"'user_id':\s*'([^']+)'", result.stdout)
            
            if sesids and user_id:
                print(f"\n🎉🎉🎉 SUCCESSO! 🎉🎉🎉")
                print(f"   sesids = {sesids.group(1)}")
                print(f"   user_id = {user_id.group(1)}")
                return sesids.group(1), user_id.group(1)
            
            time.sleep(3)
        
        print("❌ Cookie non trovati dopo 10 tentativi")
    else:
        print("❌ Dashboard non raggiunta")
    
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - Modalità Sincrona")
    print(f"API Key: {API_KEY[:30]}...")
    print("=" * 60)
    
    sesids, user_id = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids and user_id:
        print(f"🎉 RISULTATO: sesids={sesids}, user_id={user_id}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    
    run_sync("browser-use close --all")
