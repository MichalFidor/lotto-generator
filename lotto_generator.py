#!/usr/bin/env python3
"""
Generator liczb loterii oparty na różnych czynnikach losowości
Generuje 6 liczb z zakresu 1-49
"""

import random
import time
import hashlib
import os
import sys
from datetime import datetime
import subprocess

class LottoGenerator:
    def __init__(self):
        self.numbers = set()
        self.entropy_sources = []
        
    def collect_entropy(self):
        """Zbiera różne źródła entropii do generowania liczb"""
        entropy_data = []
        
        # 1. Czas systemowy z mikrosekundami
        current_time = time.time()
        entropy_data.append(str(current_time))
        print(f"🕐 Czas systemowy: {current_time}")
        
        # 2. Procesy systemowe
        try:
            # Liczba uruchomionych procesów
            process_count = len(os.listdir('/proc')) if os.path.exists('/proc') else len(str(os.getpid()))
            entropy_data.append(str(process_count))
            print(f"⚙️  Liczba procesów: {process_count}")
        except:
            entropy_data.append(str(os.getpid()))
            print(f"⚙️  PID procesu: {os.getpid()}")
        
        # 3. Użycie pamięci/CPU
        try:
            # Na macOS używamy vm_stat
            vm_output = subprocess.check_output(['vm_stat'], text=True)
            memory_entropy = sum(ord(c) for c in vm_output[:100])
            entropy_data.append(str(memory_entropy))
            print(f"💾 Entropia pamięci: {memory_entropy}")
        except:
            # Fallback - użycie random urandom
            memory_entropy = int.from_bytes(os.urandom(4), 'big')
            entropy_data.append(str(memory_entropy))
            print(f"💾 Entropia systemowa: {memory_entropy}")
        
        # 4. Stan plików tymczasowych
        try:
            temp_files = os.listdir('/tmp')
            temp_entropy = len(temp_files) + sum(len(f) for f in temp_files[:10])
            entropy_data.append(str(temp_entropy))
            print(f"📁 Entropia plików temp: {temp_entropy}")
        except:
            temp_entropy = hash(str(datetime.now()))
            entropy_data.append(str(temp_entropy))
            print(f"📁 Entropia czasu: {temp_entropy}")
        
        # 5. Opóźnienia I/O
        start_io = time.perf_counter()
        try:
            with open('/dev/null', 'w') as f:
                f.write('test')
        except:
            pass
        io_delay = int((time.perf_counter() - start_io) * 1000000)
        entropy_data.append(str(io_delay))
        print(f"⚡ Opóźnienie I/O: {io_delay} μs")
        
        # 6. Hash z kombinacji wszystkich źródeł
        combined = ''.join(entropy_data)
        hash_entropy = hashlib.sha256(combined.encode()).hexdigest()
        print(f"🔐 Hash entropii: {hash_entropy[:16]}...")
        
        return hash_entropy
    
    def generate_from_entropy(self, entropy_hash):
        """Generuje liczby na podstawie zebranej entropii"""
        print("\n🎲 Generowanie liczb...")
        
        # Dzielimy hash na segmenty i generujemy liczby
        for i in range(6):
            # Bierzemy różne części hash'a dla każdej liczby
            segment = entropy_hash[i*8:(i+1)*8]
            
            # Konwertujemy hex na int i mapujemy na zakres 1-49
            hex_value = int(segment, 16)
            number = (hex_value % 49) + 1
            
            # Upewniamy się, że liczba jest unikalna
            while number in self.numbers:
                hex_value += 1
                number = (hex_value % 49) + 1
            
            self.numbers.add(number)
            
            # Dodajemy małe opóźnienie dla efektu wizualnego
            time.sleep(0.2)
            print(f"  Liczba {i+1}: {number}")
        
        return sorted(list(self.numbers))
    
    def display_results(self, numbers):
        """Wyświetla wyniki w ładnym formacie"""
        print("\n" + "="*50)
        print("🎯 TWOJE SZCZĘŚLIWE LICZBY LOTTO:")
        print("="*50)
        
        # Wyświetlamy liczby w ładnym formacie
        number_str = " | ".join(f"{num:2d}" for num in numbers)
        print(f"   {number_str}")
        
        print("="*50)
        print(f"📅 Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🍀 Powodzenia!")
        print("="*50)
    
    def run(self):
        """Główna funkcja aplikacji"""
        print("🎰 GENERATOR LICZB LOTTO")
        print("Oparty na entropii systemowej\n")
        
        print("Zbieranie entropii z systemu...")
        entropy = self.collect_entropy()
        
        numbers = self.generate_from_entropy(entropy)
        self.display_results(numbers)

def main():
    """Punkt wejścia aplikacji"""
    try:
        generator = LottoGenerator()
        generator.run()
    except KeyboardInterrupt:
        print("\n\n👋 Do widzenia!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
