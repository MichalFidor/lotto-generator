#!/usr/bin/env python3
"""
Inteligentny generator liczb lotto oparty na analizie statystycznej i entropii
Generuje 6 liczb z zakresu 1-49 używając różnych strategii eksperckkich
"""

import random
import time
import hashlib
import os
import sys
from datetime import datetime
import subprocess
from collections import Counter

class InteligentnyLottoGenerator:
    def __init__(self):
        self.numbers = set()
        self.entropy_sources = []
        
        # Dane z analizy statystycznej (oparte na 7223 losowaniach)
        self.liczby_gorace = [17, 21, 34, 38, 24, 27, 4, 6, 25, 13]  # Najczęstsze
        self.liczby_zimne = [48, 43, 47, 12, 44, 33, 35, 23, 16, 39]  # Najrzadsze
        self.liczby_neutralne = [i for i in range(1, 50) if i not in self.liczby_gorace and i not in self.liczby_zimne]
        
        # Ostatnie trendy (z ostatnich 100 losowań)
        self.ostatnie_gorace = [20, 49, 17, 30, 11, 28, 36, 38, 22, 37]
        self.ostatnie_zimne = [47, 14, 16, 27, 32, 33, 45, 26, 4, 1]
        
        # Parametry statystyczne
        self.suma_optymalna = 149  # Średnia z analizy
        self.suma_min = 120
        self.suma_max = 180
        
        # Strategie dostępne
        self.strategie = {
            'gorace': 'Liczby historycznie gorące',
            'zimne': 'Liczby zimne (teoria wyrównania)', 
            'mieszana': 'Strategia mieszana (50/50)',
            'pozycyjna': 'Rozkład pozycyjny',
            'sekwencje': 'Z uwzględnieniem sekwencji',
            'dziesiatki': 'Równomierne dziesiątki',
            'ostatnie_trendy': 'Ostatnie trendy (100 losowań)'
        }
    def wybierz_strategie(self, entropy_hash):
        """Wybiera strategię na podstawie entropii (zapewnia różnorodność)"""
        # Używamy hash'a do deterministycznego ale nieprzewidywalnego wyboru
        hash_value = int(entropy_hash[:8], 16)
        strategie_lista = list(self.strategie.keys())
        wybrana = strategie_lista[hash_value % len(strategie_lista)]
        
        print(f"🎯 Wybrana strategia: {self.strategie[wybrana]}")
        return wybrana
    
    def generuj_strategie_gorace(self):
        """Strategia: liczby historycznie najczęstsze"""
        liczby = []
        # 4 liczby z historycznie gorących
        liczby.extend(random.sample(self.liczby_gorace, 4))
        # 2 liczby z neutralnych
        pozostale = [i for i in range(1, 50) if i not in liczby]
        liczby.extend(random.sample(pozostale, 2))
        return self._dostosuj_kryteria(liczby)
    
    def generuj_strategie_zimne(self):
        """Strategia: liczby rzadkie (teoria wyrównania)"""
        liczby = []
        # 3 liczby z zimnych
        liczby.extend(random.sample(self.liczby_zimne, 3))
        # 3 pozostałe
        pozostale = [i for i in range(1, 50) if i not in liczby]
        liczby.extend(random.sample(pozostale, 3))
        return self._dostosuj_kryteria(liczby)
    
    def generuj_strategie_mieszana(self):
        """Strategia: mix gorących i zimnych"""
        liczby = []
        liczby.extend(random.sample(self.liczby_gorace, 2))
        liczby.extend(random.sample(self.liczby_zimne, 2))
        liczby.extend(random.sample(self.liczby_neutralne, 2))
        return self._dostosuj_kryteria(liczby)
    
    def generuj_strategie_pozycyjna(self):
        """Strategia: rozkład pozycyjny (każda pozycja ma swój zakres)"""
        liczby = []
        zakresy = [(1, 15), (10, 25), (15, 35), (20, 40), (30, 45), (35, 49)]
        
        for i, (min_val, max_val) in enumerate(zakresy):
            dostepne = [x for x in range(min_val, max_val + 1) if x not in liczby]
            if dostepne:
                liczby.append(random.choice(dostepne))
        
        # Upewnij się, że mamy 6 liczb
        while len(liczby) < 6:
            nowa = random.randint(1, 49)
            if nowa not in liczby:
                liczby.append(nowa)
                
        return sorted(liczby[:6])
    
    def generuj_strategie_sekwencje(self):
        """Strategia: z sekwencjami (49.9% losowań ma sekwencje 2+)"""
        liczby = []
        # Dodaj parę kolejnych liczb
        start = random.randint(1, 47)
        liczby.extend([start, start + 1])
        # Dodaj 4 pozostałe
        pozostale = [i for i in range(1, 50) if i not in liczby]
        liczby.extend(random.sample(pozostale, 4))
        return self._dostosuj_kryteria(liczby)
    
    def generuj_strategie_dziesiatki(self):
        """Strategia: równomierne dziesiątki (unika 41-49)"""
        liczby = []
        # Po jednej z każdego przedziału oprócz 41-49
        przedzialy = [
            list(range(1, 11)),    # 1-10
            list(range(11, 21)),   # 11-20  
            list(range(21, 31)),   # 21-30
            list(range(31, 41))    # 31-40
        ]
        
        for przedzial in przedzialy:
            liczby.append(random.choice(przedzial))
        
        # 2 dodatkowe z dowolnych przedziałów (oprócz 41-49)
        wszystkie_oproc_41_49 = []
        for przedzial in przedzialy:
            wszystkie_oproc_41_49.extend(przedzial)
        
        dostepne = [x for x in wszystkie_oproc_41_49 if x not in liczby]
        liczby.extend(random.sample(dostepne, 2))
        
        return self._dostosuj_kryteria(liczby)
    
    def generuj_strategie_ostatnie_trendy(self):
        """Strategia: ostatnie trendy z 100 losowań"""
        liczby = []
        # 3 z ostatnio gorących
        liczby.extend(random.sample(self.ostatnie_gorace, 3))
        # 2 z ostatnio zimnych (kontrary)
        liczby.extend(random.sample(self.ostatnie_zimne, 2))
        # 1 neutralna
        pozostale = [i for i in range(1, 50) if i not in liczby]
        liczby.append(random.choice(pozostale))
        return self._dostosuj_kryteria(liczby)
    
    def _dostosuj_kryteria(self, liczby):
        """Dostosowuje liczby do kryteriów statystycznych"""
        liczby = list(set(liczby))  # Usuń duplikaty
        
        # Upewnij się że mamy 6 liczb
        while len(liczby) < 6:
            nowa = random.randint(1, 49)
            if nowa not in liczby:
                liczby.append(nowa)
        
        if len(liczby) > 6:
            liczby = random.sample(liczby, 6)
        
        # Dostosuj do 3 parzystych + 3 nieparzystych (34.1% losowań)
        parzyste = [x for x in liczby if x % 2 == 0]
        nieparzyste = [x for x in liczby if x % 2 == 1]
        
        # Skoryguj proporcje jeśli trzeba
        if len(parzyste) != 3:
            liczby = self._popraw_parzyste_nieparzyste(liczby)
        
        return sorted(liczby)
    
    def _popraw_parzyste_nieparzyste(self, liczby):
        """Poprawia proporcje parzystych/nieparzystych do 3/3"""
        parzyste = [x for x in liczby if x % 2 == 0]
        nieparzyste = [x for x in liczby if x % 2 == 1]
        
        if len(parzyste) > 3:
            # Za dużo parzystych
            nadmiar = parzyste[3:]
            for x in nadmiar:
                liczby.remove(x)
                # Dodaj nieparzystą
                while True:
                    nowa = random.choice(range(1, 50, 2))
                    if nowa not in liczby:
                        liczby.append(nowa)
                        break
        elif len(parzyste) < 3:
            # Za mało parzystych
            brakuje = 3 - len(parzyste)
            nadmiar_nieparzystych = nieparzyste[3:]
            for i in range(min(brakuje, len(nadmiar_nieparzystych))):
                liczby.remove(nadmiar_nieparzystych[i])
                # Dodaj parzystą
                while True:
                    nowa = random.choice(range(2, 50, 2))
                    if nowa not in liczby:
                        liczby.append(nowa)
                        break
        
        return liczby
    
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
        """Generuje liczby używając inteligentnych strategii opartych na entropii"""
        print("\n🎲 Wybór strategii na podstawie entropii...")
        
        # Wybierz strategię na podstawie entropii
        strategia = self.wybierz_strategie(entropy_hash)
        
        # Mapowanie strategii do funkcji
        strategie_funkcje = {
            'gorace': self.generuj_strategie_gorace,
            'zimne': self.generuj_strategie_zimne,
            'mieszana': self.generuj_strategie_mieszana,
            'pozycyjna': self.generuj_strategie_pozycyjna,
            'sekwencje': self.generuj_strategie_sekwencje,
            'dziesiatki': self.generuj_strategie_dziesiatki,
            'ostatnie_trendy': self.generuj_strategie_ostatnie_trendy
        }
        
        # Generuj liczby według wybranej strategii
        print("🧮 Generowanie liczb...")
        time.sleep(0.3)
        
        liczby = strategie_funkcje[strategia]()
        
        # Dodaj efekt wizualny
        for i, liczba in enumerate(liczby):
            time.sleep(0.2)
            print(f"  Liczba {i+1}: {liczba}")
        
        return liczby, strategia
    
    def display_results(self, liczby, strategia):
        """Wyświetla wyniki z rekomendacjami eksperta"""
        suma = sum(liczby)
        parzyste = sum(1 for x in liczby if x % 2 == 0)
        
        # Sprawdź sekwencje
        sekwencje = self._znajdz_sekwencje(liczby)
        
        print("\n" + "="*60)
        print("🎯 TWOJE SZCZĘŚLIWE LICZBY LOTTO:")
        print("="*60)
        
        # Wyświetlamy liczby w ładnym formacie
        number_str = " | ".join(f"{num:2d}" for num in liczby)
        print(f"   {number_str}")
        
        print("="*60)
        print("🧠 REKOMENDACJE EKSPERTA:")
        print(f"   📊 Strategia: {self.strategie[strategia]}")
        print(f"   ➕ Suma: {suma} (optymalna: 120-180)")
        print(f"   ⚪ Parzyste/Nieparzyste: {parzyste}/6 (ideał: 3/3)")
        
        if sekwencje:
            print(f"   🔗 Sekwencje: {', '.join(sekwencje)}")
        else:
            print(f"   🔗 Sekwencje: brak")
            
        # Ocena jakości
        ocena = self._ocen_zestaw(liczby, suma, parzyste, sekwencje)
        print(f"   ⭐ Ocena eksperta: {ocena}")
        
        print("="*60)
        print(f"📅 Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🍀 Powodzenia!")
        print("="*60)
        
        # Zwróć dane dla workflow
        return {
            'liczby': liczby,
            'strategia': strategia,
            'suma': suma,
            'parzyste': parzyste,
            'ocena': ocena
        }
    
    def _znajdz_sekwencje(self, liczby):
        """Znajduje sekwencje kolejnych liczb"""
        liczby = sorted(liczby)
        sekwencje = []
        i = 0
        
        while i < len(liczby) - 1:
            if liczby[i+1] == liczby[i] + 1:
                start = i
                while i < len(liczby) - 1 and liczby[i+1] == liczby[i] + 1:
                    i += 1
                sekwencje.append(f"{liczby[start]}-{liczby[i]}")
            i += 1
        
        return sekwencje
    
    def _ocen_zestaw(self, liczby, suma, parzyste, sekwencje):
        """Ocenia jakość zestawu według kryteriów statystycznych"""
        punkty = 0
        
        # Suma w optymalnym zakresie (120-180)
        if 120 <= suma <= 180:
            punkty += 2
        elif 100 <= suma <= 200:
            punkty += 1
        
        # Idealne parzyste/nieparzyste (3/3)
        if parzyste == 3:
            punkty += 2
        elif parzyste in [2, 4]:
            punkty += 1
        
        # Sekwencje (występują w 49.9% losowań)
        if len(sekwencje) >= 1:
            punkty += 1
        
        # Sprawdź czy unika przedziału 41-49
        liczby_41_49 = sum(1 for x in liczby if 41 <= x <= 49)
        if liczby_41_49 <= 1:
            punkty += 1
        
        # Sprawdź gorące/zimne liczby
        gorace_w_zestawie = sum(1 for x in liczby if x in self.liczby_gorace)
        if gorace_w_zestawie >= 2:
            punkty += 1
        
        if punkty >= 6:
            return "DOSKONAŁY ⭐⭐⭐⭐⭐"
        elif punkty >= 4:
            return "BARDZO DOBRY ⭐⭐⭐⭐"
        elif punkty >= 3:
            return "DOBRY ⭐⭐⭐"
        elif punkty >= 2:
            return "ŚREDNI ⭐⭐"
        else:
            return "SŁABY ⭐"
    
    def run(self):
        """Główna funkcja aplikacji"""
        print("🎰 INTELIGENTNY GENERATOR LOTTO")
        print("Oparty na analizie 7,223 losowań (1957-2025)\n")
        
        print("Zbieranie entropii z systemu...")
        entropy = self.collect_entropy()
        
        liczby, strategia = self.generate_from_entropy(entropy)
        dane = self.display_results(liczby, strategia)
        
        return dane

def main():
    """Punkt wejścia aplikacji"""
    try:
        generator = InteligentnyLottoGenerator()
        dane = generator.run()
        return dane
    except KeyboardInterrupt:
        print("\n\n👋 Do widzenia!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
