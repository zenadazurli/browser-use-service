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

def login_with_tab():
    print("🚀 Login con metodo TAB...")
    
    # Pulisci e connetti
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    run("browser-use cloud connect")
    time.sleep(3)
    
    # Apri la pagina
    run("browser-use open https://www.easyhits4u.com/logon/")
    
    # ATTESA REACT (20 secondi)
    print("⏳ Attesa React (20 secondi)...")
    time.sleep(20)
    
    # METODO TAB (quello che funzionava in locale!)
    print("📝 Compilazione con TAB...")
    
    # Tab al primo campo
    run('browser-use keys "Tab"')
    time.sleep(1)
    
    # Digita username/email
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    
    # Tab al campo password
    run('browser-use keys "Tab"')
    time.sleep(1)
    
    # Digita password
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # Enter per inviare
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # Attendi redirect
    print("⏳ Attesa redirect (15 secondi)...")
    time.sleep(15)
    
    # Verifica URL
    result = run("browser-use eval 'window.location.href'", capture=True)
    print(f"📍 URL: {result.stdout}")
    
    if "/surf/" in result.stdout:
        print("✅ LOGIN SUCCESS!")
        
        # Prendi cookie
        cookies = run("browser-use cookies get", capture=True)
        sesids_match = re.search(r"'sesids': '([^']+)'", cookies.stdout)
        user_id_match = re.search(r"'user_id': '([^']+)'", cookies.stdout)
        
        print(f"🎉 sesids={sesids_match.group(1) if sesids_match else None}")
        print(f"🎉 user_id={user_id_match.group(1) if user_id_match else None}")
    else:
        print("❌ Login fallito")

if __name__ == "__main__":
    login_with_tab()
