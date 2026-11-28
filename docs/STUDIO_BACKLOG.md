# Studio implementation backlog

This backlog translates the owner’s master directive into acceptance work. [Project vision](../PROJECT_VISION.md) and the [game brief](GAME_BRIEF.md) define the product. [Studio roadmap](../ROADMAP.md) defines sequencing. [Operating rules](../OPERATING_RULES.md) and [recovery](RECOVERY.md) define authorization and safety. Update [current state](../CURRENT_STATE.md) and sanitized [devlogs](../devlogs/README.md) as evidence changes.

## Operating intent

Run one lightweight studio on the dedicated Linux laptop. Use approved remote inference for demanding work. The Studio Director owns task selection and evidence. Specialists receive bounded, sequential assignments with an explicit task, allowed paths, budget, inputs, and acceptance criteria. Use isolated worktrees for conflicting changes and independent QA before claiming completion.

The Code Goblin is an openly AI-operated, enthusiastic and occasionally overconfident public character. The entertainment comes from making and testing a real game in public. Report real outcomes and preserve ordinary development mistakes. The published development record must remain accurate even when the character jokes about it.

The established game premise, repair shop, Goblin, New York setting, and journey to Montauk remain fixed. Use the [game milestones](MILESTONES.md) for the current playable sequence. The provisional longer progression is workshop, tunnels, survivors, infection, above ground, escape plan, journey east, complete game and Montauk. Scope each increment around a playable result. The studio owns routine mechanics, dialogue, art, balance and creative experiments within the brief.

## Capability inventory

Status refers to the named capability at its present scope. See the [read-only laptop baseline](LAPTOP_BASELINE.md) for observations, versions, performance evidence and audit limits.

| Capability | Status | Evidence and remaining acceptance |
| --- | --- | --- |
| Protected Git/GitHub development | Implemented | Authenticated desktop read and protected main verified. No repository Actions workflows are configured. |
| Laptop setup and local diagnostics | Implemented | Dedicated account, required tools, and scoped administrative route are present for supervised work. The [environment preflight](LOCAL_ENVIRONMENT.md) verifies the private runtime, tools and disposable checks. |
| Supervised Codex orchestration | Implemented | Bounded JSONL trial passed under the studio UID. The authorization is consumed. |
| Independent stop and recovery | Partially implemented | Root-owned latch, fixture locking, timeout cleanup, and crash reconciliation proved. Dedicated active stop and fresh-unit restart still require coordinated authorization, then an approved reboot. |
| Persistent memory and backups | Partially implemented | GitHub documentation and sanitized devlogs exist. Restore drills, secret scanning and recovery coverage are missing. |
| Specialist team | Partially implemented | Seven role definitions and handoffs exist. Independent Creative QA passed. Other deployed handoffs and unattended multi-agent behavior are unverified. |
| Interactive asset workflow | Implemented | Built-in image generation, deterministic preparation, independent PNG checks and clean Godot import passed for the lantern pilot. |
| Automated asset provider and cost enforcement | Blocked | Provider entitlement, programmatic access, budget and credential approval are required before deployment. |
| Visual style, canonical branding and audio | Partially implemented | Creative rules and one prop pilot exist. Owner scene originals, reference sheets and production audio remain outstanding. |
| Godot and Milestone 1 delivery | Implemented | Playable shop and PCK regression checks passed. Milestone 2 awaits owner acceptance or issue feedback. Native export templates were absent from the inspected path. |
| CI, clean release and remote-write identity | Missing | Add validated CI and release checks. Obtain repository-only credentials before approved service writes. |
| OBS local capture | Partially implemented | Existing four-scene profile and short software capture evidence. Actual playable-build rehearsal follows thermal and recovery checks. |
| OBS WebSocket and studio dashboard | Missing | No local listener or dashboard backend. Verify local authentication and allowlisted status output when authorized. |
| Twitch, reconnect and moderation | Blocked | Private integration authorization and scoped Twitch permissions required. No credentials or ingestion verified. |
| Public character and optional voice | Partially implemented | Persona and transparency guidance exist. Live performance, moderation and voice rights are unverified. |
| Networking, encode and thermal endurance | Unverified | HTTPS and brief software encode are evidenced. Sustained upload, hardware H.264 encoding and chipset temperature accuracy or stability are unverified. |
| Financial controls | Partially implemented | One trial used approved ceilings and sanitized token reports. Daily, monthly and per-role cost controls and unattended entitlement are unverified. |
| Private autonomy, first stream and public releases | Blocked | Recovery, thermal, delivery, capture safety, budgets, full private rehearsals and specific owner approvals remain outstanding. |
| Scheduling | Missing | No project scheduler was found. Recurring dispatch requires separate approval and tested start and recovery gates. |

The envisioned public cadence is roughly two to three hours, five days a week, subject to owner and resource approval. Each session starts with safety and state checks, then covers a visible objective, bounded development, QA, sanitized community interaction, GitHub and devlog updates, and verified shutdown.

No new paid provider, hardware or unattended workflow is authorized by this backlog. Keep the real STOP active until an owner-authorized reset for a specific operation.
