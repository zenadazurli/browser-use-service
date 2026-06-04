import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_oJs1YK25fCYMMRt3VE9gyrwhoy2udmE5AZGYScUv9tk")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def check_login():
    print("🚀 Test login...")
    
    # Config
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione
    print("🔌 Connessione...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(15)
    
    # Compila
    print("📝 Compilazione...")
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # Invia
    print("🔑 Invio...")
    run('browser-use keys "Enter"')
    
    # === VERIFICHE ===
    print("\n🔍 Verifico se il login è riuscito...")
    
    # 1. Controlla URL dopo 30 secondi
    time.sleep(30)
    url_result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = url_result.stdout.strip() if url_result else ""
    print(f"📍 URL: {current_url}")
    
    # 2. Controlla se c'è il nome utente nella pagina
    html_result = run("browser-use get html", capture=True)
    html = html_result.stdout if html_result else ""
    
    if "ujachiko" in html:
        print("✅✅✅ LOGIN RIUSCITO! ✅✅✅")
        print("   Trovato 'ujachiko' nell'HTML")
        return True
    elif "/account/" in current_url or "/surf/" in current_url:
        print("✅✅✅ LOGIN RIUSCITO! ✅✅✅")
        print(f"   URL: {current_url}")
        return True
    elif "warning" in current_url:
        print("⚠️ Bloccato da Cloudflare (warning page)")
        return False
    else:
        print("❌ Login fallito")
        print(f"   URL: {current_url}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    success = check_login()
    print("=" * 60)
    if success:
        print("🎉 IL LOGIN HA FUNZIONATO!")
    else:
        print("❌ IL LOGIN NON HA FUNZIONATO")
    print("=" * 60)
    run("browser-use close --all")
