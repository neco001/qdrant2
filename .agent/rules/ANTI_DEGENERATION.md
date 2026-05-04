---
trigger: always_on
---

# 🛠️ FILE EDITING PROTOCOL (ANTI-DEGENERATION)

1. **TOTAL OVERWRITE PROHIBITION**: It is forbidden to use `write_to_file` (Overwrite: true) for existing files exceeding 50 lines of code/text.
2. **SURGICAL EDITS ONLY**: For files >50 lines, you MUST use `replace_file_content` or `multi_replace_file_content`.
3. **WORKFLOW**:
   - First, `view_file` (with line numbers) to confirm the current content of the fragment.
   - Then, `multi_replace_file_content`, replacing ONLY the necessary blocks.
4. **TRUNCATION PROHIBITION**: Never omit existing logic within the edited fragment (the use of comments like `// ... rest of code unchanged` is forbidden).
5. **EVIDENCE**: If the user sees in the diff that the file was "deleted and rewritten" (global diff), it constitutes a breach of procedure.
