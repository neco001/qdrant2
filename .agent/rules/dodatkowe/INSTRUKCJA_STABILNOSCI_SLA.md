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

<!--
## 2. BACKUP BAZY DANYCH (BINARY PROTECTION)

- Ponieważ Git nie radzi sobie dobrze z dużymi plikami binarnymi, **PRZED** jakąkolwiek operacją `ALTER`, `DROP` lub migracją bazy, AI **musi** wykonać fizyczną kopię pliku `.duckdb` do `_archive/db_backup_YYYYMMDD_HHMM/`.
-->

## 4. ZAKAZ HALUCYNACJI KONFIGURACYJNYCH

- AI nie może samodzielnie zmieniać parametrów w `config.yaml`, `pyproject.toml` ani w `.env` bez wyjaśnienia ROI (zysku) z tej zmiany.

---

_Instrukcja dla AI: Każdorazowe złamanie tego protokołu będzie uznane za błąd krytyczny modelu._
