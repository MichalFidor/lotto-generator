#!/usr/bin/env python3
"""
Analiza wyników lotto - szukanie prawidłowości i statystyk
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from collections import Counter, defaultdict
import re

def wczytaj_dane_lotto(plik_csv):
    """Wczytuje dane z pliku CSV i przetwarza je"""
    dane = []
    
    with open(plik_csv, 'r', encoding='utf-8') as f:
        for linia in f:
            linia = linia.strip()
            if not linia:
                continue
                
            # Parsowanie linii: "1. 27.01.1957 8,12,31,39,43,45"
            parts = linia.split(' ')
            if len(parts) >= 3:
                numer_losowania = parts[0].rstrip('.')
                data_str = parts[1]
                liczby_str = ' '.join(parts[2:])
                
                # Parsowanie daty
                try:
                    data = datetime.strptime(data_str, '%d.%m.%Y')
                except:
                    continue
                
                # Parsowanie liczb
                try:
                    liczby = [int(x) for x in liczby_str.split(',')]
                    if len(liczby) == 6:  # Sprawdzamy czy to standardowe lotto (6 liczb)
                        dane.append({
                            'numer_losowania': int(numer_losowania),
                            'data': data,
                            'liczby': sorted(liczby),
                            'liczba_1': liczby[0] if len(liczby) > 0 else None,
                            'liczba_2': liczby[1] if len(liczby) > 1 else None,
                            'liczba_3': liczby[2] if len(liczby) > 2 else None,
                            'liczba_4': liczby[3] if len(liczby) > 3 else None,
                            'liczba_5': liczby[4] if len(liczby) > 4 else None,
                            'liczba_6': liczby[5] if len(liczby) > 5 else None,
                        })
                except:
                    continue
    
    return pd.DataFrame(dane)

def analiza_czestotliwosci(df):
    """Analiza częstotliwości występowania liczb"""
    print("=== ANALIZA CZĘSTOTLIWOŚCI LICZB ===")
    
    # Zbieranie wszystkich wylosowanych liczb
    wszystkie_liczby = []
    for _, row in df.iterrows():
        wszystkie_liczby.extend(row['liczby'])
    
    # Zliczanie wystąpień
    czestotliwosc = Counter(wszystkie_liczby)
    
    print(f"Łączna liczba losowań: {len(df)}")
    print(f"Najczęściej losowane liczby:")
    for liczba, ilosc in czestotliwosc.most_common(10):
        procent = (ilosc / len(df)) * 100
        print(f"  {liczba}: {ilosc} razy ({procent:.1f}%)")
    
    print(f"\nNajrzadziej losowane liczby:")
    for liczba, ilosc in czestotliwosc.most_common()[-10:]:
        procent = (ilosc / len(df)) * 100
        print(f"  {liczba}: {ilosc} razy ({procent:.1f}%)")
    
    return czestotliwosc

def analiza_sum_i_srednych(df):
    """Analiza sum wylosowanych liczb"""
    print("\n=== ANALIZA SUM I ŚREDNICH ===")
    
    sumy = [sum(row['liczby']) for _, row in df.iterrows()]
    srednie = [np.mean(row['liczby']) for _, row in df.iterrows()]
    
    print(f"Średnia suma wylosowanych liczb: {np.mean(sumy):.1f}")
    print(f"Mediana sumy: {np.median(sumy):.1f}")
    print(f"Odchylenie standardowe sum: {np.std(sumy):.1f}")
    print(f"Minimalna suma: {min(sumy)}")
    print(f"Maksymalna suma: {max(sumy)}")
    
    return sumy, srednie

def analiza_par_i_nieparzystych(df):
    """Analiza liczb parzystych i nieparzystych"""
    print("\n=== ANALIZA LICZB PARZYSTYCH I NIEPARZYSTYCH ===")
    
    statystyki_parzyste = []
    
    for _, row in df.iterrows():
        parzyste = sum(1 for x in row['liczby'] if x % 2 == 0)
        nieparzyste = 6 - parzyste
        statystyki_parzyste.append(parzyste)
    
    rozklad_parzystych = Counter(statystyki_parzyste)
    
    print("Rozkład liczby parzystych w losowaniu:")
    for ilosc_parzystych in sorted(rozklad_parzystych.keys()):
        wystapienia = rozklad_parzystych[ilosc_parzystych]
        procent = (wystapienia / len(df)) * 100
        print(f"  {ilosc_parzystych} parzystych: {wystapienia} razy ({procent:.1f}%)")

def analiza_dziesiątek(df):
    """Analiza rozkładu według dziesiątek"""
    print("\n=== ANALIZA ROZKŁADU WEDŁUG DZIESIĄTEK ===")
    
    dziesiatki = defaultdict(int)
    
    for _, row in df.iterrows():
        for liczba in row['liczby']:
            dziesiatka = (liczba - 1) // 10
            dziesiatki[dziesiatka] += 1
    
    print("Rozkład według dziesiątek:")
    for dziesiatka in sorted(dziesiatki.keys()):
        zakres = f"{dziesiatka*10+1}-{min((dziesiatka+1)*10, 49)}"
        ilosc = dziesiatki[dziesiatka]
        procent = (ilosc / (len(df) * 6)) * 100
        print(f"  {zakres}: {ilosc} razy ({procent:.1f}%)")

def analiza_sekwencji(df):
    """Analiza sekwencji kolejnych liczb"""
    print("\n=== ANALIZA SEKWENCJI KOLEJNYCH LICZB ===")
    
    sekwencje_2 = 0
    sekwencje_3_plus = 0
    max_sekwencja = 0
    
    for _, row in df.iterrows():
        liczby = sorted(row['liczby'])
        aktualna_sekwencja = 1
        najdluzsza_sekwencja = 1
        
        for i in range(1, len(liczby)):
            if liczby[i] == liczby[i-1] + 1:
                aktualna_sekwencja += 1
                najdluzsza_sekwencja = max(najdluzsza_sekwencja, aktualna_sekwencja)
            else:
                aktualna_sekwencja = 1
        
        if najdluzsza_sekwencja >= 2:
            sekwencje_2 += 1
        if najdluzsza_sekwencja >= 3:
            sekwencje_3_plus += 1
        
        max_sekwencja = max(max_sekwencja, najdluzsza_sekwencja)
    
    print(f"Losowania z sekwencją co najmniej 2 kolejnych liczb: {sekwencje_2} ({(sekwencje_2/len(df)*100):.1f}%)")
    print(f"Losowania z sekwencją co najmniej 3 kolejnych liczb: {sekwencje_3_plus} ({(sekwencje_3_plus/len(df)*100):.1f}%)")
    print(f"Najdłuższa znaleziona sekwencja: {max_sekwencja}")

def analiza_powtorzen(df):
    """Analiza powtórzeń liczb w kolejnych losowaniach"""
    print("\n=== ANALIZA POWTÓRZEŃ W KOLEJNYCH LOSOWANIACH ===")
    
    powtorzenia = []
    
    for i in range(1, len(df)):
        poprzednie = set(df.iloc[i-1]['liczby'])
        aktualne = set(df.iloc[i]['liczby'])
        wspolne = len(poprzednie.intersection(aktualne))
        powtorzenia.append(wspolne)
    
    rozklad_powt = Counter(powtorzenia)
    
    print("Rozkład powtórzeń liczb w kolejnym losowaniu:")
    for ilosc_powt in sorted(rozklad_powt.keys()):
        wystapienia = rozklad_powt[ilosc_powt]
        procent = (wystapienia / len(powtorzenia)) * 100
        print(f"  {ilosc_powt} powtórzeń: {wystapienia} razy ({procent:.1f}%)")

def analiza_trendy_czasowe(df):
    """Analiza trendów w czasie"""
    print("\n=== ANALIZA TRENDÓW CZASOWYCH ===")
    
    # Grupowanie po dekadach
    df['dekada'] = (df['data'].dt.year // 10) * 10
    
    print("Średnia suma wylosowanych liczb w dekadach:")
    for dekada in sorted(df['dekada'].unique()):
        dane_dekady = df[df['dekada'] == dekada]
        srednia_suma = np.mean([sum(row['liczby']) for _, row in dane_dekady.iterrows()])
        print(f"  {dekada}s: {srednia_suma:.1f}")

def main():
    """Główna funkcja analizy"""
    print("Wczytywanie danych...")
    df = wczytaj_dane_lotto('wyniki-lotto-all-time.csv')
    
    if df.empty:
        print("Nie udało się wczytać danych!")
        return
    
    print(f"Wczytano {len(df)} losowań z okresu {df['data'].min()} - {df['data'].max()}")
    
    # Przeprowadzanie analiz
    czestotliwosc = analiza_czestotliwosci(df)
    sumy, srednie = analiza_sum_i_srednych(df)
    analiza_par_i_nieparzystych(df)
    analiza_dziesiątek(df)
    analiza_sekwencji(df)
    analiza_powtorzen(df)
    analiza_trendy_czasowe(df)
    
    print("\n=== PODSUMOWANIE NAJWAŻNIEJSZYCH OBSERWACJI ===")
    print("1. Sprawdź czy któreś liczby wyraźnie odstają od średniej częstotliwości")
    print("2. Przeanalizuj rozkład sum - czy jest normalny?") 
    print("3. Zobacz czy proporcje parzystych/nieparzystych są równe")
    print("4. Sprawdź czy wszystkie dziesiątki są równomiernie reprezentowane")
    print("5. Oceń częstotliwość występowania sekwencji")

if __name__ == "__main__":
    main()
