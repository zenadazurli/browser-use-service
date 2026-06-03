import subprocess
import time
import re
import os

# NUOVA API KEY
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_Wwr8NyQJYHl0Qnm9MBXQbAgSFEFOvwAx8X4_HucmwOg")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def aggressive_clean():
    """Pulizia aggressiva delle sessioni"""
    print("🧹 Pulizia aggressiva sessioni...")
    
    # Lista di tutti i comandi possibili per chiudere
    commands = [
        "browser-use close --all",
        "browser-use cloud logout",
        "browser-use cloud v2 DELETE /browsers",
        "browser-use cloud v2 DELETE /sessions",
    ]
    
    for cmd in commands:
        run(cmd)
        time.sleep(1)
    
    print("⏳ Attesa 15 secondi per liberare risorse...")
    time.sleep(15)

def login_and_get_cookies():
    print("🚀 Avvio con nuova API key...")
    
    # Pulisci tutto
    aggressive_clean()
    
    # Configura API key
    print(f"🔑 Configurazione API key...")
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Verifica che non ci siano sessioni
    run("browser-use close --all")
    time.sleep(2)
    
    # Connetti al cloud
    print("🔌 Connessione al Cloud...")
    result = run("browser-use cloud connect", capture=True)
    print(f"   {result.stdout[:300] if result else 'Connessione avviata'}")
    time.sleep(5)
    
    # Apri login
    print("🌐 Apertura pagina login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(5)
    
    print("⏳ Attesa React (30 secondi)...")
    time.sleep(30)
    
    # Compilazione form
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
    
    # Monitoraggio URL
    print("⏳ Monitoraggio URL per 120 secondi...")
    dashboard_reached = False
    
    for attempt in range(120):
        time.sleep(1)
        result = run("browser-use eval 'window.location.href'", capture=True)
        current_url = result.stdout.strip() if result else ""
        current_url = current_url.replace("result: ", "").strip()
        
        if attempt % 15 == 0:
            print(f"   [{attempt}s] URL: {current_url[:80] if current_url else 'empty'}")
        
        if "/account/" in current_url or "/surf/" in current_url:
            print(f"\n✅ Dashboard raggiunta dopo {attempt} secondi!")
            print(f"   URL completo: {current_url}")
            dashboard_reached = True
            break
        
        if "warning" in current_url:
            print(f"   ⚠️ Warning page a {attempt}s, continuo ad attendere...")
    
    if not dashboard_reached:
        # Controllo finale
        final = run("browser-use eval 'window.location.href'", capture=True)
        final_url = final.stdout.strip() if final else ""
        print(f"\n📍 URL finale: {final_url}")
        
        # Se siamo su warning, prova a ricaricare
        if "warning" in final_url:
            print("🔄 Tentativo di refresh...")
            run("browser-use open https://www.easyhits4u.com/account/")
            time.sleep(15)
            dashboard_reached = True
    
    if not dashboard_reached:
        print("❌ Dashboard non raggiunta")
        return None, None
    
    # Attesa extra per i cookie
    print("\n⏳ Attesa cookie di sessione (40 secondi)...")
    time.sleep(40)
    
    # Tentativi cookie multipli
    print("🍪 Ricerca cookie...")
    for attempt in range(20):
        print(f"   Tentativo {attempt+1}/20...")
        
        # Metodo 1: document.cookie
        doc = run("browser-use eval 'document.cookie'", capture=True)
        doc_text = doc.stdout if doc else ""
        
        sesids_match = re.search(r'sesids=([^;]+)', doc_text)
        user_id_match = re.search(r'user_id=([^;]+)', doc_text)
        
        if sesids_match and user_id_match:
            sesids = sesids_match.group(1)
            user_id = user_id_match.group(1)
            print(f"\n🎉 SUCCESSO! sesids={sesids}, user_id={user_id}")
            return sesids, user_id
        
        # Metodo 2: browser-use cookies get
        bu_cookies = run("browser-use cookies get", capture=True)
        bu_text = bu_cookies.stdout if bu_cookies else ""
        
        sesids_match2 = re.search(r"'sesids': '([^']+)'", bu_text)
        user_id_match2 = re.search(r"'user_id': '([^']+)'", bu_text)
        
        if sesids_match2 and user_id_match2:
            print(f"\n🎉 SUCCESSO (metodo 2)! sesids={sesids_match2.group(1)}")
            return sesids_match2.group(1), user_id_match2.group(1)
        
        # Mostra progresso
        if attempt % 5 == 0 and doc_text:
            cookies_found = re.findall(r'([a-z_]+)=', doc_text)
            print(f"      Cookie trovati: {cookies_found[:10] if cookies_found else 'nessuno'}")
        
        time.sleep(5)
    
    print("❌ Cookie non trovati dopo 20 tentativi")
    return None, None

if __name__ == "__main__":
    print("=" * 60)
    print("Browser Use Cloud - EasyHits4U")
    print(f"API Key: {API_KEY[:30]}...")
    print("=" * 60)
    
    sesids, user_id = login_and_get_cookies()
    
    print("\n" + "=" * 60)
    if sesids and user_id:
        print("🎉🎉🎉 SUCCESSO FINALE! 🎉🎉🎉")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
    else:
        print("❌ FALLITO")
        print("\nPossibili soluzioni:")
        print("1. Aumenta i tempi di attesa")
        print("2. Usa un piano a pagamento di Browser Use")
        print("3. Controlla manualmente se il login funziona")
    print("=" * 60)
    
    # Cleanup finale
    print("\n🔚 Cleanup...")
    run("browser-use close --all")
