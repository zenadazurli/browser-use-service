import subprocess
import time
import re
import os
import signal
import sys

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_lfGFTGeTCkD6-0riqR0zD_DMU3TtKPM78iNOpFW82c8")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_cookies():
    print("🚀 Login con container persistente...")
    
    # Config
    run(f"browser-use config set api_key {API_KEY}")
    run("browser-use close --all")
    time.sleep(3)
    
    # Connessione
    print("🔌 Connessione al Cloud...")
    run("browser-use cloud connect")
    time.sleep(5)
    
    # Login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
    print("📝 Compilazione...")
    run('browser-use type "sandrominori50+ulugarecexisa@gmail.com"')
    time.sleep(1)
    run('browser-use keys "Tab"')
    time.sleep(1)
    run('browser-use type "DDnmVV45!!"')
    time.sleep(1)
    run('browser-use keys "Enter"')
    
    # === ATTESA LUNGA (3 MINUTI) ===
    print("⏳ Attesa 3 minuti per login e cookie...")
    for i in range(180):
        time.sleep(1)
        if i % 30 == 0:
            print(f"   Attesa... {i}/180 secondi")
    
    # Prendi cookie
    print("\n🍪 Estrazione cookie...")
    cookies = run("browser-use cookies get", capture=True)
    print(cookies.stdout[:1000] if cookies else "Nessun cookie")
    
    # Cerca sesids
    sesids = re.search(r'sesids=([^;]+)', cookies.stdout if cookies else "")
    if sesids:
        print(f"\n🎉 SUCCESSO! sesids={sesids.group(1)}")
        return sesids.group(1)
    
    print("❌ Cookie non trovati")
    return None

def handle_timeout(signum, frame):
    print("⏰ Timeout, ma continuo...")

if __name__ == "__main__":
    # Ignora timeout
    signal.signal(signal.SIGALRM, handle_timeout)
    
    print("=" * 60)
    sesids = login_and_get_cookies()
    print("=" * 60)
    if sesids:
        print(f"🎉 RISULTATO: sesids={sesids}")
    else:
        print("❌ FALLITO")
    print("=" * 60)
    
    # Non chiudere subito
    print("\n⏳ Mantengo container aperto 30 secondi...")
    time.sleep(30)
