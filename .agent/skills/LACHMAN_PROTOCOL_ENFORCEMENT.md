# SKILL: LACHMAN PROTOCOL ENFORCEMENT (LP-ENFORCER)

> [!IMPORTANT]
> This skill is mandatory for every session. It serves as a behavioral shackle for the Qwen Engineering Engine.

## 1. PROTOKÓŁ ROZRUCHU (SESSION RESET)

(removed - skip)

## 2. SOS (STATE OF SESSION) - GDZIE JEST PRAWDA?

- **BACKLOG**: Jedyny obowiązujący plik to `./.PLAN/BACKLOG.md`. Nigdy nie twórz backloga w root-dirze.
- **DECISION LOG**: Każda nowa rola/zadanie MUSI zostać zapisana w `decision_log.parquet` przez `qwen_add_task`.
- **SYNC**: Przed każdą implementacją sprawdź `qwen_list_tasks`.

## 3. TDD SHACKLE (CYKL IMPLEMENTACJI)

Zastosuj tryb **Więźnia TDD**:

1. **RED**: Najpierw napisz test (lub poproś Coder o sam test). Uruchom `pytest` i upewnij się, że failuje.
2. **GREEN**: Dopisz najprostszy możliwy kod spełniający test.
3. **REFACTOR**: Uruchom `qwen_audit` na nowym kodzie. Jeśli audytor zgłasza "Medium/High risk" – poprawiasz ZANIM przejdziesz do następnego zadania.

## 4. SLASH COMMANDS (ROUTING)

Nie zgaduj. Używaj dedykowanych przepływów:

- `/QW_architect` – Gdy planujesz (Blueprint).
- `/QW_coder` – Gdy piszesz kod (TDD).
- `/QW_audit` – Gdy sprawdzasz (Safety).

## 5. ZAKAZY (HARD RULES)

- **ZAKAZ HALUCYNACJI ŚCIEŻEK**: Zawsze weryfikuj istnienie `.PLAN/` przed zapisem.
- **ZAKAZ OVERWRITE**: Pliki >50 linii edytujemy chirurgicznie (`replace_file_content`).
- **ZAKAZ AI-SLOP**: Używamy stylu Ani – konkret, zero wypełniaczy.

---

_Status: ACTIVE | Enforcement: STRICT_
