---
trigger: always_on
---

# 🛡️ PROTOKÓŁ STABILNOŚCI (SLA v3.1)

Ten dokument zawiera twarde reguły bezpieczeństwa dla agenta (Gemini/Antigravity), aby zapobiec regresjom algorytmicznym i utracie danych.

## 1. ZASADA GIT-COMMIT (VERSION CONTROL FIRST)

- **OBOWIĄZEK COMMITA:** Dla każdej istotnej zmiany (niezależnie od katalogu: kod, config, skrypty) AI musi wykonać commit na GitHub/Git.
- **PRZED ZMIANĄ:** agent sprawdza `git status`. Jeśli są niezakommitowane zmiany, informuje o tym i prosi o checkpoint lub sam go tworzy.
- **PO ZMIANIE:** Po pomyślnej weryfikacji zmiany, AI tworzy commit opisujący dokładnie co zostało zrobione (zgodnie z `commit.md`).
- **CEL:** To zapewnia nam pełną historię "Rollback" i eliminuje potrzebę manualnych folderów backupowych dla kodu.

## 2. BACKUP BAZY DANYCH (BINARY PROTECTION)

- Ponieważ Git nie radzi sobie dobrze z dużymi plikami binarnymi, **PRZED** jakąkolwiek operacją `ALTER`, `DROP` lub migracją bazy, AI **musi** wykonać fizyczną kopię pliku `.duckdb` do `_archive/db_backup_YYYYMMDD_HHMM/`.

## 3. PROTOKÓŁ ROZRUCHU (SANITY CHECK)

Zanim AI zacznie pisać kod, musi sprawdzić:

1. **DB Integrity:** Czy plik bazy ma sensowny rozmiar (powyżej 10MB dla tego projektu)? Jeśli ma 12KB -> STOP i raport awarii.
2. **Env Sync:** Czy zmienne w `.env` są poprawnie wczytane i ścieżki istnieją?
3. **Logbook Sync:** Przeczytaj ostatni wpis w `PLAN/LOGBOOK.md`. Jeśli nie zgadza się ze stanem plików -> najpierw napraw Logbook.

## 4. ZAKAZ HALUCYNACJI KONFIGURACYJNYCH

- AI nie może samodzielnie zmieniać parametrów w `config.yaml` ani w `.env` bez wyjaśnienia ROI (zysku) z tej zmiany.
- Jeśli AI "rozjebie" skrypt podczas próby naprawy -> musi natychmiast wrócić do ostatniego checkpointu w `_archive`, zamiast próbować naprawiać błąd kolejnym błędem.

## 5. HIGIENA WORKSPACE ("ZERO WASTE")

- Wszystkie pliki `debug_*.py`, `temp_*.py`, `test_*.py` utworzone w sesji, muszą zostać usunięte lub przeniesione do `_archive/session_junk/` przed zakończeniem pracy.

---

_Instrukcja dla AI: Każdorazowe złamanie tego protokołu będzie uznane za błąd krytyczny modelu._