import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_7FOVF6I0bF0mjR9lnR3dQUsuJBI46LpQrtqSZQdE4jA")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Avvio con verifica Turnstile...")
    
    # Cleanup
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # 1. Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    
    # 2. Attesa che React e Turnstile carichino
    print("⏳ Attesa React e Turnstile (30 secondi)...")
    time.sleep(30)
    
    # 3. Verifica se il form è presente
    print("🔍 Verifica presenza form...")
    form_check = run("browser-use eval 'document.querySelector(\"input[name=username]\") !== null'", capture=True)
    print(f"   Form presente: {form_check.stdout.strip() if form_check else 'unknown'}")
    
    # 4. Compila form
    print("📝 Compilazione form...")
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # 5. Invio login
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # 6. Attesa con verifica URL ogni secondo
    print("⏳ Monitoraggio URL per 60 secondi...")
    dashboard_reached = False
    
    for attempt in range(60):
        time.sleep(1)
        result = run("browser-use eval 'window.location.href'", capture=True)
        url = result.stdout.strip() if result else ""
        url = url.replace("result: ", "").strip()
        
        if attempt % 10 == 0:
            print(f"   [{attempt}s] URL: {url[:80] if url else 'empty'}")
        
        if "/account/" in url or "/surf/" in url:
            print(f"\n✅ Dashboard raggiunta dopo {attempt} secondi!")
            dashboard_reached = True
            break
        
        if "warning" in url:
            print(f"   ⚠️ Warning page a {attempt}s, aspetto...")
    
    if not dashboard_reached:
        # Controllo finale
        final_url = run("browser-use eval 'window.location.href'", capture=True)
        print(f"\n📍 URL finale: {final_url.stdout if final_url else 'unknown'}")
        
        # Verifica se c'è un errore di login
        error_check = run("browser-use eval 'document.body.innerText.includes(\"Incorrect\")'", capture=True)
        if "true" in (error_check.stdout if error_check else ""):
            print("❌ Errore: Credenziali non corrette")
        else:
            print("❌ Login fallito - possibile blocco Turnstile")
        
        return None, None
    
    # 7. Attesa extra per cookie
    print("\n⏳ Attesa cookie (20 secondi)...")
    time.sleep(20)
    
    # 8. Estrai cookie
    print("🍪 Estrazione cookie...")
    
    doc = run("browser-use eval 'document.cookie'", capture=True)
    doc_text = doc.stdout if doc else ""
    print(f"document.cookie: {doc_text[:300]}")
    
    cookies = run("browser-use cookies get", capture=True)
    cookies_text = cookies.stdout if cookies else ""
    print(f"browser-use cookies get: {cookies_text[:500]}")
    
    # Cerca sesids e user_id
    sesids = None
    user_id = None
    
    match = re.search(r'sesids=([^;]+)', doc_text)
    if match:
        sesids = match.group(1)
    
    match = re.search(r'user_id=([^;]+)', doc_text)
    if match:
        user_id = match.group(1)
    
    if not sesids:
        match = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
        if match:
            sesids = match.group(1)
    
    if not user_id:
        match = re.search(r"'user_id':\s*'([^']+)'", cookies_text)
        if match:
            user_id = match.group(1)
    
    if sesids and user_id:
        print(f"\n🎉 SUCCESSO! sesids={sesids}, user_id={user_id}")
        return sesids, user_id
    
    print("\n❌ Cookie non trovati")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    sesids, user_id = login_and_get_cookies()
    print("=" * 60)
    if sesids and user_id:
        print(f"🎉 RISULTATO: sesids={sesids}, user_id={user_id}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    run("browser-use close --all")
