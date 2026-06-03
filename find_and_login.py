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

def aggressive_reset():
    """Reset totale di Browser Use"""
    print("🔄 Reset totale...")
    run("browser-use close --all")
    time.sleep(2)
    run("browser-use cloud logout")
    time.sleep(2)
    run("browser-use cloud v2 DELETE /browsers")
    time.sleep(3)
    run("browser-use close --all")
    time.sleep(2)

def login_and_get_cookies():
    print("🚀 Tentativo con reset totale...")
    
    # Reset aggressivo
    aggressive_reset()
    
    # Login con nuova chiave
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    connect_result = run("browser-use cloud connect", capture=True)
    print(f"   {connect_result.stdout[:200] if connect_result else ''}")
    time.sleep(5)
    
    # Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    
    # Attesa MOLTO lunga
    print("⏳ Attesa 45 secondi...")
    time.sleep(45)
    
    # Verifica se cf_clearance è presente
    print("🔍 Verifica Turnstile...")
    cf = run("browser-use eval 'document.cookie'", capture=True)
    print(f"   Cookie: {cf.stdout[:200] if cf else 'none'}")
    
    # Compila form
    print("📝 Compilazione...")
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # Invio
    print("🔑 Invio...")
    run('browser-use keys "Enter"')
    
    # Monitoraggio URL
    print("⏳ Monitoraggio redirect (60 secondi)...")
    for attempt in range(60):
        time.sleep(1)
        result = run("browser-use eval 'window.location.href'", capture=True)
        url = result.stdout.strip() if result else ""
        url = url.replace("result: ", "").strip()
        
        if attempt % 15 == 0:
            print(f"   [{attempt}s] URL: {url[:60] if url else 'empty'}")
        
        if "/account/" in url or "/surf/" in url:
            print(f"\n✅ Redirect dopo {attempt} secondi!")
            break
    
    # Vai a /surf/
    print("\n🎯 Navigazione a /surf/...")
    run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
    time.sleep(20)
    
    # Prendi cookie
    print("🍪 Cookie...")
    cookies = run("browser-use cookies get", capture=True)
    cookies_text = cookies.stdout if cookies else ""
    
    sesids = re.search(r'sesids=([^;]+)', cookies_text) or re.search(r"'sesids':\s*'([^']+)'", cookies_text)
    user_id = re.search(r'user_id=([^;]+)', cookies_text) or re.search(r"'user_id':\s*'([^']+)'", cookies_text)
    
    if sesids and user_id:
        print(f"\n🎉 SUCCESSO! sesids={sesids.group(1)}, user_id={user_id.group(1)}")
        return sesids.group(1), user_id.group(1)
    
    print("\n❌ Fallito")
    return None, None

if __name__ == "__main__":
    sesids, user_id = login_and_get_cookies()
    print(f"\n📊 RISULTATO: sesids={sesids}, user_id={user_id}")
    run("browser-use close --all")
