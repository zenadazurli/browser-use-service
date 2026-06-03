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
    
    print("⏳ Attesa redirect (15 secondi)...")
    time.sleep(15)
    
    # Verifica URL (accetta sia /account/ che /surf/)
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip()
    print(f"📍 URL: {current_url}")
    
    # CONTROLLO CORRETTO
    if "/account/" in current_url or "/surf/" in current_url:
        print("✅ LOGIN SUCCESS!")
        
        # Prendi i cookie
        cookies = run("browser-use cookies get", capture=True)
        print(f"🍪 Cookie raw: {cookies.stdout[:500]}")
        
        sesids_match = re.search(r"'sesids': '([^']+)'", cookies.stdout)
        user_id_match = re.search(r"'user_id': '([^']+)'", cookies.stdout)
        
        sesids = sesids_match.group(1) if sesids_match else None
        user_id = user_id_match.group(1) if user_id_match else None
        
        print(f"🎉 sesids={sesids}")
        print(f"🎉 user_id={user_id}")
        
        return sesids, user_id
    else:
        print(f"❌ Login fallito. URL: {current_url}")
        return None, None

if __name__ == "__main__":
    sesids, user_id = login_and_get_cookies()
    print(f"\n📊 RISULTATO FINALE: sesids={sesids}, user_id={user_id}")
