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
    print("🚀 Login e attesa per sesids...")
    
    # 1. Config
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # 2. Chiudi sessioni vecchie
    run("browser-use close --all")
    time.sleep(3)
    
    # 3. Connetti al cloud
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # 4. Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    # 5. Compila form
    print("📝 Compilazione form...")
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # 6. Invio login
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # 7. ATTESA CHE IL LOGIN COMPLETI
    print("⏳ Attesa redirect e caricamento dashboard (40 secondi)...")
    time.sleep(40)
    
    # 8. Verifica URL
    result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = result.stdout.strip() if result else ""
    print(f"📍 URL dopo login: {current_url}")
    
    # 9. Se siamo su account o surf, procedi
    if "/account/" in current_url or "/surf/" in current_url:
        print("✅ Login riuscito! Attesa cookie di sessione...")
        
        # Attesa extra per i cookie
        time.sleep(15)
        
        # 10. Prendi sesids con cookies get
        print("\n🍪 Estrazione sesids...")
        
        for attempt in range(10):
            print(f"   Tentativo {attempt+1}/10...")
            
            # Prova cookies get
            cookies = run("browser-use cookies get", capture=True)
            cookies_text = cookies.stdout if cookies else ""
            
            # Cerca sesids in vari formati
            sesids = re.search(r'sesids=([^;]+)', cookies_text)
            if not sesids:
                sesids = re.search(r"'sesids':\s*'([^']+)'", cookies_text)
            if not sesids:
                sesids = re.search(r'"sesids":\s*"([^"]+)"', cookies_text)
            
            if sesids:
                print(f"\n🎉🎉🎉 SESIDS TROVATO! 🎉🎉🎉")
                print(f"   sesids = {sesids.group(1)}")
                
                # Prendi anche user_id se possibile
                user_id = re.search(r'user_id=([^;]+)', cookies_text)
                if user_id:
                    print(f"   user_id = {user_id.group(1)}")
                
                return sesids.group(1)
            
            time.sleep(3)
        
        # 11. Se non trovato nei cookie, prova dall'HTML
        print("\n📄 Cerco sesids nell'HTML...")
        html = run("browser-use get html", capture=True)
        html_text = html.stdout if html else ""
        
        sesids = re.search(r'"sesids":\s*"([^"]+)"', html_text)
        if sesids:
            print(f"🎉 sesids trovato nell'HTML: {sesids.group(1)}")
            return sesids.group(1)
        
        # 12. Come ultima risorsa, naviga a /surf/ e riprova
        print("\n🔄 Navigazione a /surf/ per forzare i cookie...")
        run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
        time.sleep(20)
        
        cookies = run("browser-use cookies get", capture=True)
        sesids = re.search(r'sesids=([^;]+)', cookies.stdout if cookies else "")
        if sesids:
            print(f"🎉 sesids trovato su /surf/: {sesids.group(1)}")
            return sesids.group(1)
    
    print("\n❌ Login fallito o sesids non trovato")
    return None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - Estrazione sesids")
    print(f"API Key: {API_KEY[:30]}...")
    print("=" * 60)
    
    sesids = login_and_get_sesids()
    
    print("\n" + "=" * 60)
    if sesids:
        print(f"🎉🎉🎉 SUCCESSO! sesids = {sesids} 🎉🎉🎉")
    else:
        print("❌ FALLITO - sesids non trovato")
        print("\n💡 Possibili cause:")
        print("   - Turnstile non risolto")
        print("   - Credenziali errate")
        print("   - Troppe sessioni attive (HTTP 429)")
    print("=" * 60)
    
    run("browser-use close --all")
