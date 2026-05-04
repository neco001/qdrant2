---
description: Rozbudowane procedury administracyjne i zarządzania zasobami (modele, rachunki, monitorowanie tokenów środowiska).
---

# ⚙️ Workflow: Administracja Qwen Engine (Admin & Intelligence)

Zasada: **Obowiązkowe weryfikowanie zwrotu z inwestycji (ROI) oraz stanu portfela to klucz sukcesu i ochrony konta przed nieoczekiwanymi kosztami.**

1. **Kontrola Quoty Finansowej:**
   - Co najmniej raz w ciągu dnia raportuj zużycie DuckDB. Wywołaj systemowe narzędzie `qwen_usage_report`, które zagreguje tokeny po datach i projektach. Przekaż użytkownikowi rzut okiem na ten raport.
2. **Konfiguracja Środowiska Inteligencji (Modele):**
   - Jeśli wymagana jest pewność przypisania właściwego modelu - sprawdź dostępne LLM-y za pomocą `qwen_list_available_models`.
   - Jeśli zidentyfikowałeś nowy lub pożądany model, wskaż go za pomocą `qwen_set_model(role, model_id)`. Role dzielą się na: `strategist` (dla `architect` i `audit`), `coder` (dla pisania `qwen_coder_25`) oraz `scout` (dla mapowania drzew plików, szukania kontekstu).
3. **Odświeżanie Biblioteki Modeli:**
   - Chcąc przymusić pasywne odświeżenie do poszukania modeli SOTA z API, zastosuj: `qwen_refresh_models`. 
