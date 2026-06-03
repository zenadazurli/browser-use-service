import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_erc0JdqWNeyDyHgpqBRbZc38O3thjYdStPz_tw3FofU")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con debug URL...")
    
    # Chiudi sessioni precedenti
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    
    # Connetti
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(3)
    
    # Apri login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(5)
    
    print("⏳ Attesa React (30 secondi)...")
    time.sleep(30)
    
    print("📝 Compilazione...")
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
    
    # === MONITORAGGIO URL ===
    print("⏳ Monitoraggio URL per 90 secondi...")
    final_url = None
    
    for attempt in range(90):
        time.sleep(1)
        result = run("browser-use eval 'window.location.href'", capture=True)
        current_url = result.stdout.strip() if result else ""
        
        # Pulisci il testo (rimuovi "result: " se presente)
        current_url = current_url.replace("result: ", "").strip()
        
        if attempt % 10 == 0:
            print(f"   [{attempt}s] URL: {current_url[:80]}")
        
        if "/account/" in current_url or "/surf/" in current_url:
            print(f"\n✅ Dashboard raggiunta dopo {attempt} secondi!")
            print(f"   URL: {current_url}")
            final_url = current_url
            break
        
        if "warning" in current_url:
            print(f"⚠️ Warning page rilevata a {attempt} secondi!")
    
    if not final_url:
        # Controllo finale
        final_result = run("browser-use eval 'window.location.href'", capture=True)
        final_url = final_result.stdout.strip() if final_result else ""
        print(f"\n📍 URL finale dopo timeout: {final_url}")
    
    # Attesa extra dopo dashboard
    print("\n⏳ Attesa cookie (30 secondi extra)...")
    time.sleep(30)
    
    # Tentativi cookie
    print("🍪 Ricerca cookie...")
    for attempt in range(15):
        print(f"   Tentativo {attempt+1}/15...")
        
        # document.cookie
        doc = run("browser-use eval 'document.cookie'", capture=True)
        doc_text = doc.stdout if doc else ""
        
        sesids = re.search(r'sesids=([^;]+)', doc_text)
        user_id = re.search(r'user_id=([^;]+)', doc_text)
        
        if sesids and user_id:
            print(f"\n🎉 SUCCESSO! sesids={sesids.group(1)}, user_id={user_id.group(1)}")
            return sesids.group(1), user_id.group(1)
        
        if attempt % 5 == 0 and doc_text:
            print(f"      Cookie attuali: {re.findall(r'([a-z_]+)=', doc_text)[:5]}")
        
        time.sleep(4)
    
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
