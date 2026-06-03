import subprocess
import time
import re
import os
import sys
import json

# NUOVA API KEY (aggiornata!)
API_KEY = os.environ.get("BROWSER_USE_API_KEY", "bu_4wzHqQosQu6ev98_YPugxgPl_fMb86Vs4qYgDMSWwDU")

def run(cmd, capture=False):
    """Esegue un comando shell"""
    if capture:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result
    else:
        subprocess.run(cmd, shell=True)
        return None

def log(msg, level="INFO"):
    """Log formattato"""
    print(f"[{level}] {msg}", flush=True)

def find_and_login():
    """Trova gli indici dinamicamente e fa il login"""
    log("🚀 Avvio servizio su Railway...")
    
    # 1. Pulisci sessioni precedenti
    log("Pulizia sessioni...")
    run("browser-use close --all")
    time.sleep(2)
    
    # 2. Configura API key
    log(f"Configurazione API key: {API_KEY[:20]}...")
    run(f"browser-use config set api_key {API_KEY}")
    
    # 3. Connetti al cloud
    log("Connessione al Browser Use Cloud...")
    run("browser-use cloud connect")
    time.sleep(3)
    
    # 4. Apri la pagina
    log("Apertura https://www.easyhits4u.com/logon/...")
    run("browser-use open https://www.easyhits4u.com/logon/")
    
    # 5. ATTESA REACT (la parte più critica)
    log("⏳ Attesa che React renderizzi (20 secondi)...", "WAIT")
    for i in range(20):
        time.sleep(1)
        if i % 5 == 0:
            print(f"   Attesa... {20-i} secondi rimasti", flush=True)
    
    # 6. Prendi lo stato e cerca gli indici
    log("🔍 Ricerca indici dinamica...")
    state = run("browser-use state", capture=True)
    
    if not state or not state.stdout:
        log("ERRORE: Impossibile ottenere lo stato della pagina", "ERROR")
        return None, None, None
    
    lines = state.stdout.split('\n')
    
    username_idx = None
    password_idx = None
    button_idx = None
    
    log("Analisi stato pagina...")
    
    for line in lines:
        line_lower = line.lower()
        
        # Cerca campo username/email
        if ('username' in line_lower or 'email' in line_lower or 'e-mail' in line_lower) and 'input' in line_lower:
            match = re.search(r'\[(\d+)\]', line)
            if match:
                username_idx = int(match.group(1))
                log(f"✅ Trovato Username index: {username_idx}")
        
        # Cerca campo password
        if 'password' in line_lower and 'input' in line_lower:
            match = re.search(r'\[(\d+)\]', line)
            if match:
                password_idx = int(match.group(1))
                log(f"✅ Trovato Password index: {password_idx}")
        
        # Cerca bottone (button, btn_green, Sign In, Enter)
        if ('button' in line_lower or 'btn_green' in line_lower) and ('sign' in line_lower or 'enter' in line_lower or 'login' in line_lower):
            match = re.search(r'\[(\d+)\]', line)
            if match:
                button_idx = int(match.group(1))
                log(f"✅ Trovato Button index: {button_idx} - {line.strip()[:100]}")
    
    # Se non trova il bottone, cerca qualsiasi button
    if button_idx is None:
        log("⚠️ Bottone non trovato con criteri specifici, cerco qualsiasi button...")
        for i, line in enumerate(lines):
            if 'button' in line.lower():
                match = re.search(r'\[(\d+)\]', line)
                if match:
                    button_idx = int(match.group(1))
                    log(f"✅ Trovato Button generico index: {button_idx}")
                    break
    
    # 7. Usa gli indici trovati
    if username_idx and password_idx and button_idx:
        log(f"\n📝 INDICI TROVATI: user={username_idx}, pass={password_idx}, btn={button_idx}")
        log("Procedo con il login...")
        
        # Compila username
        log(f"Compilo username con indice {username_idx}...")
        run(f'browser-use type "{username_idx}" "sandrominori50+ulugarecexisa@gmail.com"')
        time.sleep(1)
        
        # Compila password
        log(f"Compilo password con indice {password_idx}...")
        run(f'browser-use type "{password_idx}" "DDnmVV45!!"')
        time.sleep(1)
        
        # Clicca sul bottone
        log(f"Clicco sul bottone con indice {button_idx}...")
        run(f'browser-use click "{button_idx}"')
        
        # Attendi redirect
        log("⏳ Attesa redirect alla dashboard (10 secondi)...", "WAIT")
        time.sleep(10)
        
        # Verifica URL
        result = run("browser-use eval 'window.location.href'", capture=True)
        current_url = result.stdout.strip() if result else "N/A"
        log(f"📍 URL dopo login: {current_url[:100]}")
        
        if "/surf/" in current_url:
            log("✅ LOGIN SUCCESSFUL!", "SUCCESS")
            
            # Prendi i cookie
            cookies_result = run("browser-use cookies get", capture=True)
            if cookies_result and cookies_result.stdout:
                # Estrai sesids
                sesids_match = re.search(r"'sesids': '([^']+)'", cookies_result.stdout)
                user_id_match = re.search(r"'user_id': '([^']+)'", cookies_result.stdout)
                
                sesids = sesids_match.group(1) if sesids_match else None
                user_id = user_id_match.group(1) if user_id_match else None
                
                log(f"🎉 sesids: {sesids}", "SUCCESS")
                log(f"🎉 user_id: {user_id}", "SUCCESS")
                
                # Salva su file per debug
                with open("/tmp/cookies.json", "w") as f:
                    json.dump({"sesids": sesids, "user_id": user_id}, f)
                
                return sesids, user_id, button_idx
            else:
                log("❌ Cookie non ricevuti", "ERROR")
        else:
            log(f"❌ Login fallito. URL: {current_url}", "ERROR")
            
            # Se warning, ricarica
            if "warning" in current_url:
                log("⚠️ Rilevata warning page, aspetto e ricarico...", "WARN")
                time.sleep(5)
                run("browser-use reload")
                time.sleep(5)
    else:
        log(f"❌ Indici non trovati: user={username_idx}, pass={password_idx}, btn={button_idx}", "ERROR")
        
        # Debug: stampa le prime 50 righe dello state
        log("\n🔧 DEBUG: Prime 50 righe dello state:")
        for i, line in enumerate(lines[:50]):
            print(f"  {i}: {line[:150]}")
    
    return None, None, None

if __name__ == "__main__":
    log("=" * 60)
    log("Browser Use Cloud Service per EasyHits4U")
    log(f"API Key: {API_KEY[:20]}...")
    log("=" * 60)
    
    sesids, user_id, button_idx = find_and_login()
    
    log("\n" + "=" * 60)
    if sesids and user_id:
        log("🎉 RISULTATO FINALE: SUCCESSO!")
        log(f"   sesids = {sesids}")
        log(f"   user_id = {user_id}")
        log(f"   button_index_usato = {button_idx}")
    else:
        log("❌ RISULTATO FINALE: FALLITO")
        log("   Controlla i log per maggiori dettagli")
    log("=" * 60)
