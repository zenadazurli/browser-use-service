import subprocess
import time
import re
import os
import sys

API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_IIv4wqnq3-x2Go3d4DM-rOrtIZLkTeC3t8ap45com6E")

def run(cmd, capture=False):
    if capture:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True)
    else:
        subprocess.run(cmd, shell=True)

def login_and_get_data():
    print("🚀 Login - esecuzione singola...")
    
    # === FORZA CHIUSURA DI TUTTO ===
    print("🔪 Kill di tutte le sessioni esistenti...")
    run("browser-use close --all")
    time.sleep(5)
    run("browser-use cloud logout")
    time.sleep(3)
    run("browser-use cloud v2 DELETE /browsers")
    time.sleep(5)
    run("browser-use close --all")
    time.sleep(3)
    
    # Config
    run(f"browser-use config set api_key {API_KEY}")
    time.sleep(2)
    
    # Connessione UNA SOLA
    print("🔌 Connessione al Cloud...")
    result = run("browser-use cloud connect", capture=True)
    print(f"   {result.stdout[:200] if result else ''}")
    time.sleep(5)
    
    # Verifica connessione
    check = run("browser-use eval '1+1'", capture=True)
    if "2" not in check.stdout:
        print("❌ Connessione fallita")
        return None, None
    
    # Login
    print("🌐 Apertura login...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    time.sleep(20)
    
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
    
    print("⏳ Attesa dashboard (30 secondi)...")
    time.sleep(30)
    
    # Estrai user_id
    user_id_result = run("browser-use eval 'window.props.USER.id'", capture=True)
    user_id_match = re.search(r'(\d+)', user_id_result.stdout)
    user_id = user_id_match.group(1) if user_id_match else None
    
    # Estrai sesids
    cookies = run("browser-use cookies get", capture=True)
    sesids_match = re.search(r'sesids=([^;]+)', cookies.stdout)
    sesids = sesids_match.group(1) if sesids_match else None
    
    print(f"\n📊 RISULTATI:")
    print(f"   user_id = {user_id}")
    print(f"   sesids = {sesids}")
    
    return sesids, user_id

if __name__ == "__main__":
    print("=" * 60)
    print(f"PID: {os.getpid()}")
    print("=" * 60)
    
    sesids, user_id = login_and_get_data()
    
    if user_id:
        print(f"\n🎉 SUCCESSO! user_id={user_id}, sesids={sesids}")
    else:
        print("\n❌ FALLITO")
    
    # Cleanup
    run("browser-use close --all")
