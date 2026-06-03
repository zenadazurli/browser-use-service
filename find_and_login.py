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
    
    print("⏳ Attesa redirect alla dashboard (15 secondi)...")
    time.sleep(15)
    
    # Verifica URL
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip()
    print(f"📍 URL dopo redirect: {current_url}")
    
    if "/account/" in current_url or "/surf/" in current_url:
        print("✅ Dashboard raggiunta!")
        
        # --- METODO 1: Attesa semplice (30 secondi) ---
        print("⏳ Attesa che la dashboard esegua tutto il JS (30 secondi)...")
        time.sleep(30)
        
        # Prova a prendere i cookie
        cookies = run("browser-use cookies get", capture=True)
        sesids_match = re.search(r"'sesids': '([^']+)'", cookies.stdout)
        user_id_match = re.search(r"'user_id': '([^']+)'", cookies.stdout)
        
        if sesids_match and user_id_match:
            print(f"🎉 Cookie trovati! sesids={sesids_match.group(1)}, user_id={user_id_match.group(1)}")
            return sesids_match.group(1), user_id_match.group(1)
        
        # --- METODO 2: Forza un refresh della dashboard ---
        print("🔄 Cookie non ancora pronti, faccio refresh della dashboard...")
        run("browser-use open https://www.easyhits4u.com/account/")
        time.sleep(10)
        
        cookies = run("browser-use cookies get", capture=True)
        sesids_match = re.search(r"'sesids': '([^']+)'", cookies.stdout)
        user_id_match = re.search(r"'user_id': '([^']+)'", cookies.stdout)
        
        if sesids_match and user_id_match:
            print(f"🎉 Cookie trovati DOPO REFRESH! sesids={sesids_match.group(1)}")
            return sesids_match.group(1), user_id_match.group(1)
        
        # --- METODO 3: Naviga in un'altra pagina autenticata ---
        print("🔄 Navigo in /surf/ per forzare i cookie...")
        run("browser-use open https://www.easyhits4u.com/surf/")
        time.sleep(10)
        
        cookies = run("browser-use cookies get", capture=True)
        sesids_match = re.search(r"'sesids': '([^']+)'", cookies.stdout)
        user_id_match = re.search(r"'user_id': '([^']+)'", cookies.stdout)
        
        if sesids_match and user_id_match:
            print(f"🎉 Cookie trovati su /surf/! sesids={sesids_match.group(1)}")
            return sesids_match.group(1), user_id_match.group(1)
    
    print("❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    sesids, user_id = login_and_get_cookies()
    print(f"\n📊 RISULTATO FINALE: sesids={sesids}, user_id={user_id}")
