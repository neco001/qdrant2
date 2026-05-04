---
description: Uruchamia model audytora dla głębokiego reasoningu w poszukiwaniu bugów na środowisku uruchomieniowym.
---

# 🐛 Workflow: Audyt Błędów i SRE (Qwen Audit)

Zasada: **Gdy kod nie działa w nieoczywisty sposób lub architektura sypie niewytłumaczalnymi wyjątkami przed próbą chybionej strzałowej poprawki – zleć zadanie Audytorowi `@mcp:qwen-coding:qwen_audit` .**

1. **Paczka dowodowa (Logi i Kontekst):**
   - Skopiuj do wewnątrz zmiennej `content` zrzut z konsoli informujący o napotkanym błędzie oraz dokładnie wyodrębniony problematyczny stack-trace (szczególnie błędy runtime'owe).
   - Opisz oczekiwane działanie bloku na poziomie logiki aplikacji w zmiennej `context`, dodaj tam też treść sprawdzanego kodu (funkcji).
2. **Zlecenie Audytu:**
   - Wywołaj narzędzie `@mcp:qwen-coding:qwen_audit`. Z uwagi na głęboki nakład procesu analitycznego (chain-of-thought), model dogłębnie sprawdzi wady.
3. **Wnioski i Naprawa:**
   - zachowaj wynik pracy jako potencjalny wkład dla `@mcp:qwen-coding:qwen_architect`
   - zaprezentuj wynik audytu userowi
