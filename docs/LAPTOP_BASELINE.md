# Code Goblin laptop baseline — November 24, 2026

## Scope

Read-only observations from the existing Codex desktop session, scoped host inventory and read-only GitHub calls. Previously tested operations are identified as historical evidence. This audit did not start a model, game, OBS, project service, encoder, stress test, package installation or reboot. No credentials, raw environment, network addresses or private window titles are recorded. Only this report and the backlog reconciliation were edited.

## Repository and local work

The authoritative remote is `https://github.com/bryce496913/code-goblin.git`. GitHub reported live `main` at `5c195064c920ff1243e77eac04c2543fdb97dc30`. The local `origin/main` reference was still `40f8285` at audit start. The clean review checkout at `c2eae65` has the same tree as live main, `24311e617e678c8d202be5e940927bc592315e46`. The audit did not fetch, rebase, reset or switch branches.

| Checkout | Branch and HEAD | Audit observation |
| --- | --- | --- |
| Studio operations | `codex/phase-01-laptop-baseline`, `f8f0ea2` | Existing modified state file and untracked devlogs, trial scripts and recovery fixture. Preserved. |
| Current review | `codex/creative-pilot-qa`, `c2eae65` | Clean at audit start. Same content as live main. Contains the audit documentation edits. |
| Original checkout | `main`, original skeleton | Working tree clean and one commit ahead of its local tracking ref. Preserved. |
| Other linked worktrees | Milestone 1, Phase 02 operations and master backlog branches | In place. No worktree was removed or reused. |

Architecture PR #2, Milestone 1 PR #3, Phase 02 PR #4, master backlog PR #5, asset pilot PR #6 and independent asset QA PR #7 were verified merged. Main requires PRs for administrators and disallows force pushes and deletion. Required approving-review count is zero. GitHub Actions reported zero workflows. The desktop CLI's authenticated account has repository admin and push permission metadata. No write was attempted.

Reviewed `AGENTS.md`, operating rules, architectural and recovery documents, milestones, current state and backlog. Seven role files and the handoff procedure are present. Merged runtime-related code covers shell entry points, bounded offline fixtures, the one-shot Codex launcher and image preparation. An additional Phase 03 recovery fixture is local to the operations checkout. The repository does not contain a deployed scheduler, dashboard backend, Twitch client, formal CI workflow or commissioned unattended supervisor.

Godot main opens the repair shop. The source and exported pack previously passed normal movement and repair-loop checks. The currently stored PCK matched the established SHA-256 `a45bba09820fe3ce46d9f850879b31f0271d5a00daa673ca4f5db783d0889ad3`. No new gameplay run was made. Both owner branding originals were absent from the checked tracked assets, OBS source inventory and filename search across the project, Pictures and Downloads. The lantern pilot and its independent file QA are present.

## Host and performance

| Item | Observed |
| --- | --- |
| OS | Linux Mint 22.3 Zena, Ubuntu Noble base, kernel 6.17.0-23-generic, x86-64, systemd 255. |
| CPU and GPU | Intel Core i3-5005U 2.00 GHz, two physical cores and four logical CPUs. Intel HD Graphics 5500. |
| Memory | 3.7 GiB RAM, 1.3 GiB available at snapshot. 1.4 GiB of 3.7 GiB swap in use. The single snapshot was close to the previous 1.25 GiB launch floor. |
| Storage | 238.5 GiB non-rotational SATA device. Workspace ext4 filesystem 110 GiB, 89 GiB used, 16 GiB available, 86% used. Disk health telemetry was unavailable through the inspected tools. |
| Network | Intel Wireless 7260, link up, sampled signal −54 dBm. Read-only GitHub and ChatGPT HTTPS requests returned 200. TLS connection time was about 0.21 s and 0.14 s respectively. Sustained upload, jitter and reconnect behavior were unverified. |
| Video | VA-API Intel iHD driver 24.1.0 exposed H.264 decode profiles and no encode entry point. GStreamer exposes software x264 and H.264 decode. The previous OBS rehearsal produced a verified 960 × 540 software H.264 recording at about 24 fps. Hardware encoding remains unverified. |
| Thermal | Repeated passive readings showed CPU package 70–73°C, chipset sensor 112.5–114.5°C, fan about 3,304 RPM, and zero reported core or package throttle counts for the inspected CPU. The chipset exposes a 115°C trip point. The high reading repeated, and the sensor's accuracy and sustained-load behavior remain unverified. |

The chipset reading is the highest-priority hardware risk. Verify it before a sustained Godot and OBS rehearsal. The observed swap use, near-floor available RAM, disk occupancy and small CPU also support sequential specialist work and conservative software encode settings. Prior brief capture succeeded, while prolonged recording, upload and thermal stability still need a controlled rehearsal after the temperature check.

## Tools, identity and permissions

| Tool or integration | Verified status |
| --- | --- |
| Git and GitHub CLI | Git 2.43.0 and gh 2.45.0. Authenticated read and branch-protection checks passed. Dedicated repository-scoped remote-write credential remains deferred. |
| Codex desktop and CLI | Interactive desktop session working. System CLI 0.130.0. Project-pinned desktop CLI 0.172.0 reported ChatGPT login. Dedicated CLI installation and login were verified in the prior owner and supervised trial evidence. The dedicated token and login were not read or refreshed during this audit. |
| Godot | 4.6.2 stable, Compatibility renderer in project. PCK workflow verified from prior builds. No native export templates found under the inspected user data path. |
| OBS and Twitch | OBS 30.0.2.1. OBS stopped. Code Goblin Local profile and four scenes present. Game Preview uses XComposite plus a text overlay. Starting Soon, Workbench and Emergency Pause use text sources. No WebSocket config or TCP listener on 4455. No stream service file in the dedicated profile. Twitch authorization or ingestion was not verified. |
| Developer and media dependencies | Python 3.12.3, Pillow 10.2.0, Node 18.19.1, npm 9.2.0, rg, Xorg tooling, GStreamer 1.24.2, vainfo and sensors present. ffmpeg CLI, jq and smartctl absent on PATH. GStreamer enumeration emitted a DMA-format plugin warning, while software x264 and H.264 decode were still listed. |
| Image generation | Interactive built-in generation, offline prep, independent PNG reproducibility and a clean Godot import previously verified. No OpenAI API key was visible in the audited process environment. Provider service credentials, API billing, automation entitlement and quotas remain unverified. |
| Host permissions | Dedicated non-login account UID 997, private home mode 0750, no supplementary groups. The root-owned STOP is active at mode 0644. The root-owned one-run claim remains at mode 0700. System and user managers were inspected with scoped host approval. Earlier privileged transient execution used native desktop authorization, which may time out. |
| Services and scheduling | No named Code Goblin system or user units or timers were found. Cron daemon is active. No matching entries in visible user or system cron configuration. Privileged per-user spool contents were outside the audit. No studio dispatch was observed. |

## Codex execution interfaces

- **Verified in prior supervised evidence:** desktop interaction, a scoped `codex exec` JSONL marker task with the pinned CLI, and explicit session resume on the desktop account. The dedicated UID completed its one authorized marker trial. This audit started no turns.
- **Advertised locally:** interactive CLI, `exec`, non-interactive review, JSONL, resume, sandbox options and ephemeral mode. The pinned CLI also advertises App Server and standalone exec-server as experimental. Neither server was started or wired to studio operations.
- **SDK:** OpenAI documents TypeScript and Python SDK interfaces. The TypeScript package did not resolve from the audit worktree and the Python SDK was not importable from the inspected environment. No packages were installed and no SDK session was exercised.
- **Subagents:** Independent QA was previously delegated in the interactive desktop environment and recorded in merged PR #7. The pinned CLI reports mixed legacy and current feature flags, including `multi_agent_v2` disabled. Dedicated or unattended subagent execution is unverified. Actual studio dispatch remains gated.

Official interface references: [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode), [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk), [App Server](https://learn.chatgpt.com/docs/app-server), and [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Owner actions and acceptance order

1. Coordinate a window to approve the native Linux dialogs for dedicated active-stop and fresh-unit restart. Approve a reboot separately after those pass. The observed dedicated crash fixture is prior evidence. Production STOP stays in place.
2. Arrange a thermal verification before sustained concurrent application work. Confirm the original Starting Soon and Emergency Pause files or provide the originals. Confirm Milestone 1 acceptance or report a playtest issue before Milestone 2.
3. After Phase 03 and the thermal check, authorize the private OBS rehearsal. Twitch authorization will need only the scopes required for the chosen integration.
4. Authorize future execution and generation budgets, entitlement, remote-write credentials, private autonomy, public broadcast, releases and scheduling at their respective gates. The consumed supervised claim grants no further run.

See the [reconciled capability inventory](STUDIO_BACKLOG.md).

## November 27 follow-up

Private runtime setup completed under the supervised desktop account. The root and all six subdirectories verified at mode 0700. The final preflight passed required tool execution, pinned Codex exec option discovery, GitHub main connectivity, a brief headless GDScript, and transparent PNG preparation. Negative fixtures confirmed missing dependency reporting, missing directory reporting, unsafe-mode detection and repair, and symlink refusal. All required tools were already installed. See [local environment setup and repair](LOCAL_ENVIRONMENT.md).

The follow-up snapshot showed about 1.7 GiB available RAM, 1.3 GiB swap in use, and 16 GiB free workspace disk. The chipset and CPU package sensors read 83°C and 41°C respectively. The earlier near-trip chipset readings remain relevant to sustained-load verification. No stress test was run. The production STOP remained active.

The unchanged Milestone 1 source and export both passed all six repair-loop assertions in a clean scratch validation. The new pack matched the previous playtest build checksum byte for byte.
