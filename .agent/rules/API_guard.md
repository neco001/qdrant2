---
trigger: model_decision
description: always when agent wants to run API request to any LLM or other service
---

**YOU ARE NOT ALLOWED TO USE API REQUESTS TO ANY SERVICE**
until:
- you obtain explicit permission from the user
- script which requests API must shows current usage (during series of requests) of tokens
- for LLM you have to monitor cost of usage. asking user for permission you have to provide estimated cost and tokens usage expected for entire run of script