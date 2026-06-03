import subprocess
import time
import re
import os

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_3ZzyZ-QpKHCyfcRUka3QKqMfthARb_baNFIR3gnxwlk")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con navigazione a /surf/...")
    
    # Pulizia e connessione
    run("browser-use close --all")
    time.sleep(2)
    run(f"browser-use config set api_key {API_KEY}")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Login
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    run('browser-use keys "Enter"')
    
    time.sleep(20)
    
    # Naviga a /surf/
    print("🎯 Navigazione a /surf/...")
    run("browser-use open https://www.easyhits4u.com/surf/?surftype=2&q=start")
    time.sleep(15)
    
    # Click sul pulsante Start Surfing (usa selettore CSS)
    print("🖱️ Click su Start Surfing...")
    # Metodo 1: click per indice (prendiamo dallo state)
    state = run("browser-use state", capture=True)
    print(f"Stato pagina: {state.stdout[:500] if state else ''}")
    
    # Cerca l'indice del bottone Start Surfing
    lines = state.stdout.split('\n') if state else []
    button_index = None
    for line in lines:
        if 'Start Surfing' in line and 'button' in line.lower():
            match = re.search(r'\[(\d+)\]', line)
            if match:
                button_index = int(match.group(1))
                print(f"✅ Trovato Start Surfing all'indice {button_index}")
                break
    
    if button_index:
        run(f'browser-use click "{button_index}"')
    else:
        # Fallback: click con eval JavaScript
        print("⚠️ Indice non trovato, uso JavaScript...")
        run("browser-use eval 'document.querySelector(\".start-surfing\").click()'")
    
    time.sleep(15)
    
    # Prendi cookie
    print("\n🍪 Estrazione cookie...")
    for attempt in range(20):
        doc = run("browser-use eval 'document.cookie'", capture=True)
        doc_text = doc.stdout if doc else ""
        
        sesids_match = re.search(r'sesids=([^;]+)', doc_text)
        user_id_match = re.search(r'user_id=([^;]+)', doc_text)
        
        if sesids_match and user_id_match:
            print(f"\n🎉 SUCCESSO! sesids={sesids_match.group(1)}, user_id={user_id_match.group(1)}")
            return sesids_match.group(1), user_id_match.group(1)
        
        if attempt % 5 == 0:
            cookies_found = re.findall(r'([a-z_]+)=', doc_text)
            print(f"   Tentativo {attempt+1}/20 - Cookie: {cookies_found}")
        
        time.sleep(3)
    
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
