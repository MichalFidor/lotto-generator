#!/usr/bin/env python3
"""
Test script dla powiadomień Pushover
Uruchom to lokalnie aby przetestować czy powiadomienia działają
"""

import os
import subprocess
import sys

def test_pushover():
    """Testuje wysłanie powiadomienia przez Pushover"""
    
    # Sprawdź czy zmienne środowiskowe są ustawione
    token = os.getenv('PUSHOVER_TOKEN')
    user = os.getenv('PUSHOVER_USER')
    
    if not token:
        print("❌ Brak PUSHOVER_TOKEN w zmiennych środowiskowych")
        print("Ustaw: export PUSHOVER_TOKEN='ap3ncgfapo8qwz5gim81x9f46mbwiz'")
        return False
        
    if not user:
        print("❌ Brak PUSHOVER_USER w zmiennych środowiskowych")
        print("Ustaw: export PUSHOVER_USER='twoj_user_key'")
        return False
    
    print("✅ Zmienne środowiskowe OK")
    print(f"📱 Token: {token[:10]}...")
    print(f"👤 User: {user[:10]}...")
    
    # Przygotuj testową wiadomość
    message = """🎰 TEST LOTTO GENERATOR

🎯 Przykładowe liczby: 7 | 15 | 23 | 31 | 42 | 49

📅 Test: $(date '+%Y-%m-%d %H:%M')
🧪 To jest test połączenia z Pushover

🤖 Test z lokalnego skryptu"""

    # Wyślij przez curl
    try:
        cmd = [
            'curl', '-s',
            '--form-string', f'token={token}',
            '--form-string', f'user={user}',
            '--form-string', 'title=🧪 Test Lotto Generator',
            '--form-string', f'message={message}',
            '--form-string', 'priority=0',
            '--form-string', 'sound=cashregister',
            'https://api.pushover.net/1/messages.json'
        ]
        
        print("\n🚀 Wysyłam testowe powiadomienie...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Powiadomienie wysłane pomyślnie!")
            print(f"📋 Odpowiedź: {result.stdout}")
            return True
        else:
            print(f"❌ Błąd wysyłania: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ Brak curl w systemie. Zainstaluj curl.")
        return False
    except Exception as e:
        print(f"❌ Nieoczekiwany błąd: {e}")
        return False

def main():
    """Główna funkcja testowa"""
    print("🧪 TEST POWIADOMIEŃ PUSHOVER")
    print("=" * 40)
    
    if test_pushover():
        print("\n🎉 Test zakończony sukcesem!")
        print("Sprawdź telefon - powinieneś otrzymać powiadomienie.")
    else:
        print("\n💥 Test nieudany!")
        print("Sprawdź konfigurację i spróbuj ponownie.")

if __name__ == "__main__":
    main()
