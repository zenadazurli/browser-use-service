import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_IIv4wqnq3-x2Go3d4DM-rOrtIZLkTeC3t8ap45com6E")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_data():
    print("🚀 Login e estrazione dati da window.props...")
    
    # Pulizia
    run("browser-use close --all")
    time.sleep(2)
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
    
    # Attesa dashboard
    print("⏳ Attesa dashboard (30 secondi)...")
    time.sleep(30)
    
    # === ESTRARRE user_id da window.props ===
    print("\n📊 Estrazione dati da window.props...")
    
    # Prendi user_id
    user_id_result = run("browser-use eval 'window.props.USER.id'", capture=True)
    print(f"user_id result: {user_id_result.stdout}")
    
    user_id_match = re.search(r'(\d+)', user_id_result.stdout)
    if user_id_match:
        user_id = user_id_match.group(1)
        print(f"✅ user_id = {user_id}")
    else:
        user_id = None
    
    # Prendi login name
    login_result = run("browser-use eval 'window.props.USER.login'", capture=True)
    print(f"login: {login_result.stdout}")
    
    # Prendi auth status
    auth_result = run("browser-use eval 'window.props.USER.auth'", capture=True)
    print(f"auth: {auth_result.stdout}")
    
    # === SESIDS: tentativo con cookies get ===
    print("\n🍪 Tentativo cookies get...")
    cookies = run("browser-use cookies get", capture=True)
    cookies_text = cookies.stdout if cookies else ""
    print(f"Cookies: {cookies_text[:500]}")
    
    sesids_match = re.search(r'sesids=([^;]+)', cookies_text)
    if not sesids_match:
        sesids_match = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
    
    if sesids_match:
        sesids = sesids_match.group(1)
        print(f"✅ sesids = {sesids}")
    else:
        sesids = None
        print("⚠️ sesids non trovato (probabilmente HTTP-only)")
    
    print("\n" + "=" * 60)
    if user_id:
        print(f"🎉 SUCCESSO! user_id = {user_id}")
        if sesids:
            print(f"🎉 sesids = {sesids}")
        else:
            print("💡 Nota: sesids è HTTP-only, ma la sessione è autenticata!")
            print("   Puoi usare il browser autenticato per fare richieste.")
        return sesids, user_id
    else:
        print("❌ Login fallito - window.props.USER non trovato")
        return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - Estrazione dati da window.props")
    print(f"API Key: {API_KEY[:30]}...")
    print("=" * 60)
    
    sesids, user_id = login_and_get_data()
    
    print("\n" + "=" * 60)
    if user_id:
        print(f"🎉 RISULTATO: user_id={user_id}")
        if sesids:
            print(f"🎉 sesids={sesids}")
        else:
            print("⚠️ sesids non accessibile (HTTP-only)")
    else:
        print("❌ FALLITO - Login non riuscito")
    print("=" * 60)
    
    # Mantieni la sessione aperta per usarla
    print("\n💡 La sessione autenticata è ancora attiva.")
    print("   Puoi usare 'browser-use open' per fare richieste autenticate.")
    
    # Non chiudere! (commentato)
    # run("browser-use close --all")
