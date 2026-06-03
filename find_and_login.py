import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_4wzHqQosQu6ev98_YPugxgPl_fMb86Vs4qYgDMSWwDU")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def wait_for_turnstile_complete():
    """Attende che Turnstile sia completato - max 60 secondi"""
    print("🔍 Attesa completamento Turnstile...")
    
    for attempt in range(30):
        # Controlla se l'iframe Turnstile è scomparso
        iframe_check = run("browser-use eval 'document.querySelector(\"iframe[src*=\\\"challenges.cloudflare.com\\\"]\") === null'", capture=True)
        
        # Controlla se cf_clearance è presente
        cookies = run("browser-use cookies get", capture=True)
        has_cf = "cf_clearance" in cookies.stdout
        
        # Controlla se siamo sulla dashboard
        url_check = run("browser-use eval 'window.location.href.includes(\"/account/\") || window.location.href.includes(\"/surf/\")'", capture=True)
        
        if iframe_check.stdout.strip() == "true" and has_cf and url_check.stdout.strip() == "true":
            print(f"✅ Turnstile completato! (tentativo {attempt + 1})")
            return True
        
        print(f"⏳ Attesa... iframe gone={iframe_check.stdout.strip()[:5]}, cf={has_cf}")
        time.sleep(2)
    
    print("⚠️ Timeout: Turnstile non completato entro 60 secondi")
    return False

def login_and_get_cookies():
    print("🚀 Login con metodo TAB...")
    
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    run("browser-use cloud connect")
    time.sleep(3)
    
    run("browser-use open https://www.easyhits4u.com/logon/")
    
    print("⏳ Attesa React (20 secondi)...")
    time.sleep(20)
    
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
    
    # ATTESA INTELLIGENTE: aspetta che Turnstile sia completato
    if not wait_for_turnstile_complete():
        print("❌ Turnstile non completato, abort")
        return None, None
    
    # Ora che Turnstile è completo, prendi i cookie
    print("🍪 Estrazione cookie di sessione...")
    cookies = run("browser-use cookies get", capture=True)
    
    sesids_match = re.search(r"'sesids': '([^']+)'", cookies.stdout)
    user_id_match = re.search(r"'user_id': '([^']+)'", cookies.stdout)
    
    sesids = sesids_match.group(1) if sesids_match else None
    user_id = user_id_match.group(1) if user_id_match else None
    
    if sesids and user_id:
        print(f"🎉 SUCCESSO! sesids={sesids}, user_id={user_id}")
    else:
        print(f"⚠️ Cookie target non trovati. Cookies disponibili: {re.findall(r\"'name': '([^']+)'\", cookies.stdout)}")
    
    return sesids, user_id

if __name__ == "__main__":
    sesids, user_id = login_and_get_cookies()
    print(f"\n📊 RISULTATO FINALE: sesids={sesids}, user_id={user_id}")
