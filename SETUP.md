# Konfiguracja GitHub Actions + Pushover

## 1. Ustawienie Secrets w GitHub

Przejdź do swojego repozytorium na GitHub i ustaw następujące secrets:

**Settings → Secrets and variables → Actions → New repository secret**

### Wymagane secrets:

1. **`PUSHOVER_TOKEN`**
   - Wartość: `xxx`
   - To jest token aplikacji Pushover

2. **`PUSHOVER_USER`**
   - Wartość: Twój User Key z Pushover (znajdziesz go na https://pushover.net/)
   - Format: 30-znakowy string, np. `xxx`

## 2. Harmonogram uruchamiania

Workflow uruchamia się automatycznie:
- **Wtorek** o 18:00 UTC
- **Czwartek** o 18:00 UTC  
- **Sobota** o 18:00 UTC

> **Uwaga**: GitHub Actions używa czasu UTC. W Polsce to będzie:
> - Zimą (UTC+1): 19:00
> - Latem (UTC+2): 20:00

## 3. Ręczne uruchomienie

Możesz również uruchomić workflow ręcznie:
1. Idź do zakładki **Actions** w swoim repo
2. Wybierz **Lotto Generator**
3. Kliknij **Run workflow**

## 4. Otrzymywane powiadomienia

Na telefon otrzymasz powiadomienie Pushover z:
- 🎯 Wygenerowanymi liczbami lotto
- 📅 Datą i czasem generowania
- 🎰 Informacją o automatycznym generowaniu

## 5. Monitoring

W zakładce **Actions** możesz:
- Zobaczyć historię wszystkich uruchomień
- Sprawdzić logi z generowania liczb
- Pobrać artefakty z pełnym outputem

## 6. Dostosowanie

### Zmiana harmonogramu
Edytuj linię `cron` w `.github/workflows/lotto_generator.yml`:
```yaml
- cron: '0 18 * * 2,4,6'  # min hour day month day_of_week
```

### Zmiana dźwięku powiadomienia
Zmień `sound` w sekcji curl:
- `cashregister` (domyślny)
- `classical`
- `cosmic`
- `falling`
- `gamelan`
- `incoming`
- `intermission`
- `magic`
- `mechanical`
- `pianobar`
- `siren`
- `spacealarm`
- `tugboat`
- `alien`
- `climb`
- `persistent`
- `echo`
- `updown`
- `none`
