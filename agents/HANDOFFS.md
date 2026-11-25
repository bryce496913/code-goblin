# Specialist handoffs

The Studio Director assigns one active task at a time. A specialist uses the corresponding [role instructions](README.md) in an isolated worktree or scratch directory as appropriate. The Director retains control of dispatch, owner approvals and integration.

Each assignment records the task ID, role, goal, allowed paths, approved tools, budget and deadline, source inputs, acceptance checks and decisions reserved for the owner. The specialist returns output paths and checksums, test results, provenance, usage and unresolved issues. A handoff contains no authentication material or raw public messages.

| Role | Receives | Hands back |
| --- | --- | --- |
| Studio Director | Roadmap, evidence and approvals | Bounded assignments, priorities and integration decisions |
| Game Developer | Approved milestone and write scope | Playable changes, asset requests and reproducible checks |
| Creative Agent | Asset request and approved references | Source and prepared asset, provenance and visual inspection |
| Narrative Agent | Game brief and affected story scope | Dialogue or story changes with lore consistency checks |
| QA Agent | Candidate, acceptance criteria and locked inputs | Independent reproduction and evidence, including uncovered cases |
| Community Agent | Allowlisted public status and moderated feedback | Sanitized suggestions and approved commentary |
| Infrastructure Agent | Scoped operational task | Runbook, fixture results, resource evidence and unresolved gates |

QA receives the candidate after implementation and runs the checks independently before the Director promotes it. If a separate reviewer is unavailable, record that distinction in the handoff. The Director pauses approval when a required test fails or a permission boundary changes. Runtime task leases and raw logs belong outside Git.
