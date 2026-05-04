---
name: mcpservers
description: MCP servers usage
---

# MCP SERVERS & TOOLS (Strategic Guide)

## 1. QWEN-CODING (The Main Engine)

Serwer `mcp:qwen-coding` to Twój główny arsenał. Używaj go według następujących wzorców:

### A. Infrastructure & Telemetry (Auto-Managed)

- **`qwen_usage_report`**: Sprawdzanie zużycia tokenów i kosztów bieżącej sesji.
- **`qwen_list_available_models`**: Sprawdzenie, które modele (Plus, Turbo, Max) są aktualnie przypisane do ról (coder, architect, audit).

### B. Coding & Architecture

- **`qwen_coder`**: Implementacja kodu. Używaj mode: `pro` dla trudnych zadań i `expert` dla głębokich refaktorów. Standardowo obsługuje TDD.
- **`qwen_architect`**: **Protokół Lachmana (LP)**. Uruchamiaj przy planowaniu nowych, złożonych ficzerów. Generuje pełny Blueprint (roadmap, manifest, swarm tasks).
- **`qwen_init_context_tool`**: Inicjalizacja plików kontekstowych projektu (.context/\_PROJECT_CONTEXT.md itp.) przy użyciu analizy Swarm.

### C. Analysis & Strategy

- **`qwen_sparring`**: Do debat strategicznych. `sparring1` (flash), `sparring2` (standard), `sparring3` (deep pro). Używaj, gdy decyzja wymaga zderzenia wielu perspektyw (Red/Blue/White Cell).
- **`qwen_audit` / `qwen_diff_audit`**: Głęboka analiza kodu pod kątem regresji i błędów logicznych. `qwen_diff_audit` używaj przed commitem do sprawdzenia staged changes.
- **`qwen_swarm`**: Równoległa analiza wieloagentowa. Idealna do audytu całych katalogów lub skomplikowanego researchu.

### D. Task & State Management (SOS System)

- **`qwen_add_task`**: Dodawanie zadań do BACKLOG.md i decision_log.
- **`qwen_sync_state`**: Synchronizacja stanu sesji z systemem plików (materializacja decyzji).
- **`qwen_update_task_tool`**: Aktualizacja statusu zadań (pending -> completed).

## 2. COMPLEMENTARY SERVERS

- **`mcp-vault`**: Uniwersalne proxy i admin konsola. Używaj `mcpv_admin` do zarządzania innymi serwerami. Użyj `list_servers` do sprawdzenia aktywnych serwerów, `list_tools` do sprawdzenia narzędzi danego serwera, `toggle_server`/`toggle_tool` do włączania/wyłączania.
- **`py-executor`**: Wykonywanie kodu Python. Używaj do manipulacji danymi, obliczeń lub automatyzacji zadań na plikach (PDF, Excel).
- **`duckdb`**: Dostęp do Data Warehouse. Używaj do zapytań SQL na plikach .parquet i .duckdb (pamiętaj o `read_only=True`).
- **`linkedin-writer`**: Specjalistyczne narzędzie do formatowania i optymalizacji treści pod LinkedIn.

## 3. QDRANT (Vector Database)

Serwer `qdrant2` (lub `qdrant3` w zależności od konfiguracji) to wektorowa baza danych do wyszukiwania semantycznego.

### C. Aktywacja serwera

Serwer Qdrant może być domyślnie wyłączony. Aby go włączyć:

1. Sprawdź dostępne narzędzia: `mcp:mcp-vault:mcpv_admin(action="list_tools", params={"server_name": "qdrant"})`
2. jeżeli nie widzisz narzędzi sprobuj `mcp:mcp-vault:get_initial_context`

### A. Podstawowe operacje

- **`search`**: Wyszukiwanie podobnych tekstów w kolekcji. Parametry: `collection_name`, `query`, `limit` (domyślnie 5). Automatycznie dostosowuje wymiary wektorów.

### B. Zarządzanie kolekcjami

- **`scroll`**: Przeglądanie rekordów w kolekcji (introspekcja). Parametry: `collection_name`, `limit` (domyślnie 10), `offset`.
- **`store`**: Zapisywanie tekstu i metadanych do kolekcji. Parametry: `collection_name`, `text`, `metadata` (obiekt JSON).

### C. Przykłady użycia

```python
# Wyszukiwanie semantyczne
search(collection_name="docs", query="jak zainicjalizować projekt", limit=3)

# Przegląd kolekcji
scroll(collection_name="docs", limit=10)

# Zapis dokumentu
store(collection_name="docs", text="Instrukcja instalacji...", metadata={"type": "guide", "version": "1.0"})
```
