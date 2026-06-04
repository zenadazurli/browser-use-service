import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_IIv4wqnq3-x2Go3d4DM-rOrtIZLkTeC3t8ap45com6E")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_data():
    print("🚀 Login con estrazione dati dall'HTML...")
    
    # Pulizia
    run("browser-use close --all")
    time.sleep(3)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    print("📝 Compilazione form...")
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
    time.sleep(25)
    
    # Naviga a /surf/
    print("🎯 Navigazione a /surf/...")
    run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
    time.sleep(15)
    
    # === ESTRARRE I DATI DALL'HTML ===
    print("\n📊 Estrazione dati dalla pagina...")
    
    # Prendi l'HTML della pagina
    html_result = run("browser-use get html", capture=True)
    html_content = html_result.stdout if html_result else ""
    
    # Estrai user_id da window.props
    user_id_match = re.search(r'"id":\s*(\d+)', html_content)
    if user_id_match:
        user_id = user_id_match.group(1)
        print(f"✅ user_id = {user_id}")
    else:
        user_id = None
    
    # Estrai login name
    login_match = re.search(r'"login":\s*"([^"]+)"', html_content)
    if login_match:
        login = login_match.group(1)
        print(f"✅ login = {login}")
    
    # Estrai auth status
    auth_match = re.search(r'"auth":\s*(true|false)', html_content)
    if auth_match:
        auth = auth_match.group(1)
        print(f"✅ auth = {auth}")
    
    # Estrai sesids dalla stringa window.props (se presente)
    sesids_match = re.search(r'"sesids":\s*"([^"]+)"', html_content)
    if sesids_match:
        sesids = sesids_match.group(1)
        print(f"✅ sesids = {sesids}")
    else:
        sesids = None
    
    # Prova anche a cercare nei cookie (tentativo)
    cookies = run("browser-use cookies get", capture=True)
    cookies_text = cookies.stdout if cookies else ""
    if not sesids:
        sesids_match2 = re.search(r'sesids=([^;]+)', cookies_text)
        if sesids_match2:
            sesids = sesids_match2.group(1)
            print(f"✅ sesids (da cookie) = {sesids}")
    
    print("\n" + "=" * 60)
    if user_id:
        print(f"🎉 SUCCESSO! user_id = {user_id}")
        if sesids:
            print(f"🎉 sesids = {sesids}")
        return sesids, user_id
    else:
        print("❌ user_id non trovato - login fallito")
        return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - Estrazione dati dall'HTML")
    print("=" * 60)
    
    sesids, user_id = login_and_get_data()
    
    print("\n" + "=" * 60)
    if user_id:
        print(f"🎉 RISULTATO: user_id={user_id}, sesids={sesids}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    
    run("browser-use close --all")
