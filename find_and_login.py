import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu__j__S3W9tN3zjAX1nShO7WaELi3oH0MDMHCD9TvPFiA")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_data():
    print("🚀 Login semplice senza kill...")
    
    # Solo close, niente logout o delete
    run("browser-use close --all")
    time.sleep(2)
    
    # Configura API key
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connetti al cloud (senza forzare)
    print("🔌 Connessione al Cloud...")
    result = run("browser-use cloud connect", capture=True)
    print(f"   {result.stdout[:200] if result else ''}")
    time.sleep(5)
    
    # Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(25)
    
    # Compila form
    print("📝 Compilazione form...")
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    
    # Invio login
    print("🔑 Invio login...")
    run('browser-use keys "Enter"')
    
    # Attesa lunga
    print("⏳ Attesa redirect e caricamento (45 secondi)...")
    time.sleep(45)
    
    # Verifica se siamo loggati
    print("\n🔍 Verifica stato login...")
    
    # Controlla URL
    url_result = run("browser-use eval 'window.location.href'", capture=True)
    current_url = url_result.stdout.strip() if url_result else ""
    print(f"📍 URL: {current_url}")
    
    if "account" in current_url or "surf" in current_url:
        print("✅ Sembra che siamo loggati!")
        
        # Prendi l'HTML
        html_result = run("browser-use get html", capture=True)
        html = html_result.stdout if html_result else ""
        
        # Cerca user_id
        user_match = re.search(r'"id":\s*(\d+)', html)
        if user_match:
            user_id = user_match.group(1)
            print(f"🎉 user_id = {user_id}")
        else:
            user_id = None
        
        # Cerca sesids
        sesids_match = re.search(r'sesids=([^;]+)', html)
        if not sesids_match:
            sesids_match = re.search(r'"sesids":\s*"([^"]+)"', html)
        sesids = sesids_match.group(1) if sesids_match else None
        
        if sesids:
            print(f"🎉 sesids = {sesids}")
        
        return sesids, user_id
    else:
        print("❌ Non siamo loggati (URL ancora su login)")
        return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - Login Semplice")
    print("=" * 60)
    
    sesids, user_id = login_and_get_data()
    
    print("\n" + "=" * 60)
    if user_id:
        print(f"🎉 SUCCESSO! user_id={user_id}, sesids={sesids}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    
    # Non chiudere!
    # run("browser-use close --all")
