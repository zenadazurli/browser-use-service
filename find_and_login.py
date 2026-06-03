import subprocess
import time
import re
import os
import json

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_3ZzyZ-QpKHCyfcRUka3QKqMfthARb_baNFIR3gnxwlk")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login e estrazione cookie con API v2...")
    
    # Pulizia e connessione
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Login
    print("📝 Login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    run('browser-use keys "Enter"')
    
    # Attendi redirect a /surf/
    print("⏳ Attesa redirect a /surf/...")
    for attempt in range(30):
        time.sleep(1)
        result = run("browser-use eval 'window.location.href'", capture=True)
        url = result.stdout.strip() if result else ""
        if "/surf/" in url:
            print(f"✅ Redirect riuscito! URL: {url}")
            break
    
    # Attesa extra per sicurezza
    time.sleep(10)
    
    # Usa l'API v2 per ottenere TUTTI i cookie (inclusi HTTP-only)
    print("\n🍪 Estrazione cookie via API v2...")
    
    # Ottieni il browser attuale
    browsers_result = run("browser-use cloud v2 GET /browsers", capture=True)
    print(f"Browser response: {browsers_result.stdout[:200] if browsers_result else ''}")
    
    # Prova a leggere i cookie con il metodo CDP
    cookies_result = run("browser-use cloud v2 GET /cookies", capture=True)
    print(f"Cookies response: {cookies_result.stdout[:500] if cookies_result else ''}")
    
    # Cerca sesids e user_id nel JSON
    try:
        cookies_data = json.loads(cookies_result.stdout) if cookies_result else {}
        for cookie in cookies_data.get('cookies', []):
            if cookie.get('name') == 'sesids':
                print(f"🎉 sesids trovato via API: {cookie.get('value')}")
            if cookie.get('name') == 'user_id':
                print(f"🎉 user_id trovato via API: {cookie.get('value')}")
    except:
        pass
    
    # Metodo alternativo: browser-use cookies get (dovrebbe prendere anche HTTP-only)
    print("\n🍪 browser-use cookies get...")
    cookies = run("browser-use cookies get", capture=True)
    print(f"Output completo:\n{cookies.stdout if cookies else ''}")
    
    # Cerca con regex più flessibili
    sesids_match = re.search(r"'sesids':\s*'([^']+)'", cookies.stdout if cookies else "")
    user_id_match = re.search(r"'user_id':\s*'([^']+)'", cookies.stdout if cookies else "")
    
    if sesids_match and user_id_match:
        print(f"\n🎉 SUCCESSO! sesids={sesids_match.group(1)}, user_id={user_id_match.group(1)}")
        return sesids_match.group(1), user_id_match.group(1)
    
    # Ultimo tentativo: cerca nel JSON
    json_match = re.search(r'\{.*"sesids":\s*"([^"]+)".*\}', cookies.stdout if cookies else "")
    if json_match:
        print(f"🎉 Trovato in JSON: {json_match.group(1)}")
    
    print("\n❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    sesids, user_id = login_and_get_cookies()
    print("=" * 60)
    if sesids and user_id:
        print(f"🎉 SUCCESSO! sesids={sesids}, user_id={user_id}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    run("browser-use close --all")
