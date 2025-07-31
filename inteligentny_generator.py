#!/usr/bin/env python3
"""
Generator liczb lotto oparty na analizie statystycznej
"""

import random
import numpy as np
from collections import Counter
from datetime import datetime

class InteligentnyGeneratorLotto:
    
    def __init__(self):
        # Dane z analizy - liczby gorące i zimne
        self.liczby_gorace = [17, 21, 34, 38, 24, 27, 4, 6, 25, 13]
        self.liczby_zimne = [48, 43, 47, 12, 44, 33, 35, 23, 16, 39]
        self.liczby_neutralne = [i for i in range(1, 50) if i not in self.liczby_gorace and i not in self.liczby_zimne]
        
        # Statystyki z analizy
        self.suma_min = 120
        self.suma_max = 180
        self.suma_srednia = 149
        
        # Przedziały dziesiątek (41-49 rzadziej)
        self.przedzial_1_10 = list(range(1, 11))
        self.przedzial_11_20 = list(range(11, 21))
        self.przedzial_21_30 = list(range(21, 31))
        self.przedzial_31_40 = list(range(31, 41))
        self.przedzial_41_49 = list(range(41, 50))
    
    def generuj_strategia_gorace(self):
        """Strategia oparta na liczbach gorących"""
        print("🔥 STRATEGIA: Liczby gorące")
        
        liczby = []
        
        # 4 liczby z gorących
        liczby.extend(random.sample(self.liczby_gorace, 4))
        
        # 2 liczby z neutralnych/zimnych
        pozostale = [i for i in range(1, 50) if i not in liczby]
        liczby.extend(random.sample(pozostale, 2))
        
        return self._dostosuj_do_kryteriow(liczby)
    
    def generuj_strategia_zimne(self):
        """Strategia oparta na liczbach zimnych (teoria wyrównania)"""
        print("❄️ STRATEGIA: Liczby zimne (wyrównanie)")
        
        liczby = []
        
        # 3 liczby z zimnych
        liczby.extend(random.sample(self.liczby_zimne, 3))
        
        # 3 liczby z pozostałych
        pozostale = [i for i in range(1, 50) if i not in liczby]
        liczby.extend(random.sample(pozostale, 3))
        
        return self._dostosuj_do_kryteriow(liczby)
    
    def generuj_strategia_mieszana(self):
        """Strategia mieszana (50/50 gorące/zimne)"""
        print("🎯 STRATEGIA: Mieszana (gorące + zimne)")
        
        liczby = []
        
        # 2 gorące
        liczby.extend(random.sample(self.liczby_gorace, 2))
        
        # 2 zimne
        liczby.extend(random.sample(self.liczby_zimne, 2))
        
        # 2 neutralne
        liczby.extend(random.sample(self.liczby_neutralne, 2))
        
        return self._dostosuj_do_kryteriow(liczby)
    
    def generuj_strategia_pozycyjna(self):
        """Strategia oparta na analizie pozycyjnej"""
        print("📊 STRATEGIA: Pozycyjna")
        
        liczby = []
        
        # Pozycja 1: małe liczby (1-15)
        liczby.append(random.choice(range(1, 16)))
        
        # Pozycja 2: średnie-małe (10-25)
        liczby.append(random.choice([x for x in range(10, 26) if x not in liczby]))
        
        # Pozycja 3: średnie (15-35)
        liczby.append(random.choice([x for x in range(15, 36) if x not in liczby]))
        
        # Pozycja 4: średnie-duże (20-40)
        liczby.append(random.choice([x for x in range(20, 41) if x not in liczby]))
        
        # Pozycja 5: duże (30-45)
        liczby.append(random.choice([x for x in range(30, 46) if x not in liczby]))
        
        # Pozycja 6: bardzo duże (35-49)
        liczby.append(random.choice([x for x in range(35, 50) if x not in liczby]))
        
        return sorted(liczby)
    
    def generuj_strategia_sekwencje(self):
        """Strategia z uwzględnieniem sekwencji"""
        print("🔗 STRATEGIA: Z sekwencjami")
        
        liczby = []
        
        # Dodaj jedną parę kolejnych liczb (49.9% losowań ma sekwencje)
        start_sekwencji = random.randint(1, 47)
        liczby.extend([start_sekwencji, start_sekwencji + 1])
        
        # Dodaj 4 pozostałe liczby
        pozostale = [i for i in range(1, 50) if i not in liczby]
        liczby.extend(random.sample(pozostale, 4))
        
        return self._dostosuj_do_kryteriow(liczby)
    
    def generuj_strategia_dziesiatki(self):
        """Strategia z równomiernym rozkładem dziesiątek"""
        print("🔢 STRATEGIA: Równomierne dziesiątki")
        
        liczby = []
        
        # Po jednej z każdego przedziału (oprócz 41-49)
        liczby.append(random.choice(self.przedzial_1_10))
        liczby.append(random.choice(self.przedzial_11_20))
        liczby.append(random.choice(self.przedzial_21_30))
        liczby.append(random.choice(self.przedzial_31_40))
        
        # Ostatnie 2 z dowolnych przedziałów
        wszystkie_oproc_41_49 = (self.przedzial_1_10 + self.przedzial_11_20 + 
                                self.przedzial_21_30 + self.przedzial_31_40)
        dostepne = [x for x in wszystkie_oproc_41_49 if x not in liczby]
        liczby.extend(random.sample(dostepne, 2))
        
        return self._dostosuj_do_kryteriow(liczby)
    
    def _dostosuj_do_kryteriow(self, liczby):
        """Dostosowuje liczby do kryteriów statystycznych"""
        liczby = list(set(liczby))  # usuń duplikaty
        
        # Upewnij się, że mamy 6 liczb
        while len(liczby) < 6:
            nowa = random.randint(1, 49)
            if nowa not in liczby:
                liczby.append(nowa)
        
        if len(liczby) > 6:
            liczby = random.sample(liczby, 6)
        
        # Dostosuj do 3 parzystych + 3 nieparzystych
        parzyste = [x for x in liczby if x % 2 == 0]
        nieparzyste = [x for x in liczby if x % 2 == 1]
        
        if len(parzyste) != 3:
            # Skoryguj proporcje
            if len(parzyste) > 3:
                # Za dużo parzystych
                nadmiar = len(parzyste) - 3
                do_usuniecia = random.sample(parzyste, nadmiar)
                for x in do_usuniecia:
                    liczby.remove(x)
                    # Dodaj nieparzystą
                    while True:
                        nowa = random.choice([i for i in range(1, 50, 2) if i not in liczby])
                        liczby.append(nowa)
                        break
            else:
                # Za mało parzystych
                brakuje = 3 - len(parzyste)
                do_usuniecia = random.sample(nieparzyste, brakuje)
                for x in do_usuniecia:
                    liczby.remove(x)
                    # Dodaj parzystą
                    while True:
                        nowa = random.choice([i for i in range(2, 50, 2) if i not in liczby])
                        liczby.append(nowa)
                        break
        
        return sorted(liczby)
    
    def generuj_losowanie_kompletne(self):
        """Generuje kompletne losowanie ze wszystkimi strategiami"""
        print("=" * 60)
        print("🎲 INTELIGENTNY GENERATOR LOTTO")
        print(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print("=" * 60)
        
        strategie = [
            ("Gorące liczby", self.generuj_strategia_gorace),
            ("Zimne liczby", self.generuj_strategia_zimne),
            ("Mieszana", self.generuj_strategia_mieszana),
            ("Pozycyjna", self.generuj_strategia_pozycyjna),
            ("Z sekwencjami", self.generuj_strategia_sekwencje),
            ("Równomierne dziesiątki", self.generuj_strategia_dziesiatki)
        ]
        
        wyniki = {}
        
        for nazwa, funkcja in strategie:
            liczby = funkcja()
            suma = sum(liczby)
            parzyste = sum(1 for x in liczby if x % 2 == 0)
            
            print(f"\n{nazwa}:")
            print(f"  Liczby: {', '.join(map(str, liczby))}")
            print(f"  Suma: {suma}")
            print(f"  Parzyste: {parzyste}/6")
            
            # Sprawdź sekwencje
            sekwencje = self._znajdz_sekwencje(liczby)
            if sekwencje:
                print(f"  Sekwencje: {sekwencje}")
            
            wyniki[nazwa] = {
                'liczby': liczby,
                'suma': suma,
                'parzyste': parzyste
            }
        
        # Rekomendacja
        print("\n" + "="*60)
        print("🏆 REKOMENDACJA EKSPERTA:")
        print("="*60)
        
        # Znajdź strategię z sumą najbliższą średniej
        najlepsza = min(wyniki.items(), 
                       key=lambda x: abs(x[1]['suma'] - self.suma_srednia))
        
        print(f"Najlepsza strategia: {najlepsza[0]}")
        print(f"Liczby: {', '.join(map(str, najlepsza[1]['liczby']))}")
        print(f"Uzasadnienie: Suma {najlepsza[1]['suma']} najbliższa średniej {self.suma_srednia}")
        
        return wyniki
    
    def _znajdz_sekwencje(self, liczby):
        """Znajduje sekwencje w liczbach"""
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

def main():
    generator = InteligentnyGeneratorLotto()
    wyniki = generator.generuj_losowanie_kompletne()
    
    print("\n" + "="*60)
    print("📈 STATYSTYKI WYGENEROWANYCH ZESTAWÓW:")
    print("="*60)
    
    wszystkie_liczby = []
    wszystkie_sumy = []
    
    for nazwa, dane in wyniki.items():
        wszystkie_liczby.extend(dane['liczby'])
        wszystkie_sumy.append(dane['suma'])
    
    czestotliwosc = Counter(wszystkie_liczby)
    
    print(f"Najczęstsze liczby w tym losowaniu:")
    for liczba, freq in czestotliwosc.most_common(10):
        print(f"  {liczba}: {freq} razy")
    
    print(f"\nŚrednia suma wygenerowanych zestawów: {np.mean(wszystkie_sumy):.1f}")
    print(f"Zakres sum: {min(wszystkie_sumy)} - {max(wszystkie_sumy)}")

if __name__ == "__main__":
    main()
