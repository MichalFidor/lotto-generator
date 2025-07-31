# Generator Liczb Lotto - CLI + GitHub Actions

Aplikacja generuje 6 liczb z zakresu 1-49 na podstawie różnych źródeł entropii systemowej.

🤖 **Automatyczne powiadomienia**: Workflow GitHub Actions wysyła liczby przez Pushover w każdy wtorek, czwartek i sobotę o 18:00 UTC.

## Źródła "losowości"

1. **Czas systemowy** - precyzyjny timestamp z mikrosekundami
2. **Procesy systemowe** - liczba aktywnych procesów lub PID
3. **Stan pamięci** - entropia z informacji o pamięci systemowej
4. **Pliki tymczasowe** - stan katalogu /tmp
5. **Opóźnienia I/O** - mikropomiary operacji dyskowych
6. **Hash kombinowany** - SHA256 z wszystkich powyższych źródeł

## Jak uruchomić

### Lokalnie (CLI)
```bash
python3 lotto_generator.py
```

### Automatycznie (GitHub Actions)
1. Skonfiguruj secrets w GitHub (patrz `SETUP.md`)
2. Workflow uruchamia się automatycznie w harmonogramie
3. Otrzymasz powiadomienie Pushover z liczbami

### Test powiadomień Pushover
```bash
export PUSHOVER_TOKEN='ap3ncgfapo8qwz5gim81x9f46mbwiz'
export PUSHOVER_USER='twoj_user_key'
python3 test_pushover.py
```

## Przykład działania

```
🎰 GENERATOR LICZB LOTTO
Oparty na entropii systemowej

Zbieranie entropii z systemu...
🕐 Czas systemowy: 1722418234.567891
⚙️  Liczba procesów: 342
💾 Entropia pamięci: 15438
📁 Entropia plików temp: 1247
⚡ Opóźnienie I/O: 234 μs
🔐 Hash entropii: 3f7a9b2c4d8e1f6a...

🎲 Generowanie liczb...
  Liczba 1: 7
  Liczba 2: 15
  Liczba 3: 23
  Liczba 4: 31
  Liczba 5: 42
  Liczba 6: 49

==================================================
🎯 TWOJE SZCZĘŚLIWE LICZBY LOTTO:
==================================================
    7 | 15 | 23 | 31 | 42 | 49
==================================================
📅 Wygenerowano: 2024-07-31 14:30:34
🍀 Powodzenia!
==================================================
```

## Wymagania

- Python 3.6+
- System Unix/Linux/macOS (dla niektórych funkcji entropii)
- Konto Pushover (dla powiadomień)
- curl (dla wysyłania powiadomień)

## Pliki

- `lotto_generator.py` - Główna aplikacja CLI
- `test_pushover.py` - Test powiadomień Pushover
- `.github/workflows/lotto_generator.yml` - Workflow GitHub Actions
- `SETUP.md` - Instrukcje konfiguracji
