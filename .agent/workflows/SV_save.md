---
# Workflow: SV_save
description: Finalizes and saves session context using Qwen-Coding MCP tools.
---

When this workflow is triggered:

1.  **Update Session Supplement**: Call `qwen_update_session_context_tool(session_summary: "...")`. 
    - Construct a concise summary of the decisions, changes, and state of the current session.
    - This updates `_SESSION_SUPPLEMENT.md` in the project root.

2.  **Synchronize State (Backup)**: Run `qwen_sync_state()` if there are pending decisions to ensure the filesystem reflects the latest `decision_log`.

3.  **Project Context Refresh (As Needed)**: 
    - Check if `.context/` directory or `_PROJECT_CONTEXT.md` exists and is up to date.
    - If the project structure or tech stack changed significantly during the session, call `qwen_init_context_tool()`.

4.  **Logbook Anchor**: Add a brief entry to `PLAN/LOGBOOK.md` tagged as `[ANCHOR]` confirming the context save.
