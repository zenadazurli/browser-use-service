import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_QDGSLMytkPV-0hOZwq7Fdegns3ouiXVGMqP3yulTQXI")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con gestione profili...")
    
    run("browser-use close --all")
    time.sleep(2)
    
    # Pulisci profili esistenti
    print("🧹 Pulizia profili esistenti...")
    run("browser-use cloud profiles delete --all")
    time.sleep(2)
    
    run(f"browser-use config set api_key {API_KEY}")
    
    # Connetti senza profile persistente
    print("🔌 Connessione al cloud...")
    run("browser-use cloud connect")
    time.sleep(3)
    
    run("browser-use open https://www.easyhits4u.com/logon/")
    
    print("⏳ Attesa React e Turnstile (30 secondi)...")
    time.sleep(30)
    
    print("📝 Compilazione con TAB...")
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
    
    print("⏳ Attesa risoluzione Turnstile (30 secondi)...")
    time.sleep(30)
    
    # Verifica se Turnstile è risolto (cookie cf_clearance)
    cookies_check = run("browser-use cookies get", capture=True)
    if "cf_clearance" not in cookies_check.stdout:
        print("⚠️ Turnstile non ancora risolto, aspetto altri 20 secondi...")
        time.sleep(20)
    
    # Verifica URL
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip()
    print(f"📍 URL: {current_url}")
    
    # Gestione warning page
    if "warning" in current_url:
        print("⚠️ Warning page rilevata, ricarico...")
        run("browser-use open https://www.easyhits4u.com/account/")
        time.sleep(15)
        result = run("browser-use eval 'window.location.href'", capture=True)
        current_url = result.stdout.strip()
        print(f"📍 URL dopo ricarica: {current_url}")
    
    if "/account/" in current_url or "/surf/" in current_url:
        print("✅ Dashboard raggiunta!")
        
        print("⏳ Attesa cookie di sessione (20 secondi)...")
        time.sleep(20)
        
        # Tentativi multipli
        for attempt in range(5):
            print(f"🍪 Tentativo {attempt + 1}/5...")
            cookies = run("browser-use cookies get", capture=True)
            
            sesids_match = re.search(r"'sesids': '([^']+)'", cookies.stdout)
            user_id_match = re.search(r"'user_id': '([^']+)'", cookies.stdout)
            
            if sesids_match and user_id_match:
                print(f"🎉 SUCCESSO! sesids={sesids_match.group(1)}, user_id={user_id_match.group(1)}")
                return sesids_match.group(1), user_id_match.group(1)
            
            time.sleep(5)
    
    print("❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    sesids, user_id = login_and_get_cookies()
    print(f"\n📊 RISULTATO FINALE: sesids={sesids}, user_id={user_id}")
