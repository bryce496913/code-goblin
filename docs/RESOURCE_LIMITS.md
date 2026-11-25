# Budget and resource plan

No additional expenditure is authorized by Pass 001. Use existing authorized tools on one laptop. Confirm Codex account entitlement and usage limits separately from API project billing. Record potential API charges, external service costs, export storage and asset generation costs before enabling those services. Pricing, quotas, paid asset allowances and approved budget caps are unresolved. Keep paid integrations and new spending disabled pending owner approval.

Before private trials, measure idle and concurrent Godot/OBS CPU, available memory, disk use and encoder load. Set explicit CPU and memory guardrails, a free disk floor, retention caps, maximum task and session durations, and per-session and daily usage ceilings. These values are unresolved pending laptop baseline and owner approval. Restrict execution to one specialist worker and limit logging and output sizes.

Propose at most two retries after an initial transient failure, bounded by the session deadline, with backoff and provider retry guidance. Stop on persistent limits, authentication failures or uncertain side effects. Count retries per operation and preserve the count on resume. Use recorded session usage to evaluate limits before autonomous trials. Public session duration and schedule are subject to rehearsals and owner authorization.

Set caps on generated assets, repeated test failures and tool calls where the runner can count them. Stop dispatching when a cap is reached and use the remaining session time for wrap-up.
