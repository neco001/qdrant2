---
trigger: model_decision
description: when generating commit message
---

// turbo-all
# Workflow: CM_commit

When this workflow is triggered:

1.  **Stage Changes**: Run `git add -A` to ensure all changes (including new files) are staged.
2.  **Generate Commit Message**: Create a complex, detailed commit message based ONLY on the staged changes.
    - Format: `type(scope): Title`
    - Sections: Core Changes, Integration (if applicable), Maintenance/Other.
    - Use the example below as a reference for depth and style.
3.  **Execute Commit**: Run `git commit -v -m "<generated_message>"`
4.  **Push Changes**: Run `git push`.

### Commit Message Template Example:

```
feat(engine): Implement RAG-based Task Deduplication & Thread-Aware Guardian

Major overhaul of the Officer Engine to eliminate duplicate tasks and improve context handling.

Core Changes:

RAG Integration:
- 'MailMemory' now supports a dedicated 'tasks' table in LanceDB. Implemented semantic deduplication ('semantic_task_exists') using vector embeddings.
- Context-Aware Guardian: 'mail_guardian_agent.py' now groups Feishu messages by conversation threads ('Chat Chunking') instead of processing them atomically.
- Aggressive Deduplication: Hybrid logic using Source IDs (SIDs) and semantic distance thresholds (Strict for global, Lenient for within-thread).

Feishu Integration:
- Rich task descriptions now include full conversation history or email context.
- Removed intrusive 'Auto-Pin' functionality.
- Updated 'feishu_api.py' with 'list_task_lists' support for future section mapping.

Maintenance:
- Added 'semantic_cleanup_todo.py' for analyzing and cleaning existing markdown tasks.
- Reorganized system instructions into '.agent/rules/'.
```