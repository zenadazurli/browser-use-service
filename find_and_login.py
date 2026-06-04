import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_803Me3Zuh40VXqkk6qCxQh6Fs3_Wj30tRMEQpaAYN6Y")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_sesids():
    print("🚀 Login - senza kill, lasciamo fare a Browser Use...")
    
    # SOLO configurazione, niente kill
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione diretta (senza close)
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    # Compila
    print("📝 Compilazione...")
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    run('browser-use keys "Enter"')
    
    # Attesa lunga
    print("⏳ Attesa 60 secondi...")
    time.sleep(60)
    
    # Controlla URL
    result = run("browser-use eval 'window.location.href'", capture=True)
    print(f"📍 URL: {result.stdout}")
    
    # Cerca sesids
    cookies = run("browser-use cookies get", capture=True)
    cookies_text = cookies.stdout if cookies else ""
    print(f"🍪 Cookie: {cookies_text[:500]}")
    
    sesids = re.search(r'sesids=([^;]+)', cookies_text)
    if sesids:
        print(f"\n🎉 SUCCESSO! sesids={sesids.group(1)}")
        return sesids.group(1)
    
    # Se non trovato, aspetta ancora
    print("⏳ Attesa altri 30 secondi...")
    time.sleep(30)
    
    cookies = run("browser-use cookies get", capture=True)
    sesids = re.search(r'sesids=([^;]+)', cookies.stdout if cookies else "")
    if sesids:
        print(f"🎉 Trovato dopo attesa extra! sesids={sesids.group(1)}")
        return sesids.group(1)
    
    print("❌ sesids non trovato")
    return None

if __name__ == "__main__":
    print("=" * 60)
    sesids = login_and_get_sesids()
    print("=" * 60)
    if sesids:
        print(f"🎉 RISULTATO: sesids={sesids}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
