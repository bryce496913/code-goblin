# Studio roadmap

Advance after recording acceptance evidence in [current state](CURRENT_STATE.md). The [game milestones](docs/MILESTONES.md) retain the established playable progression.

| Phase | Status | Acceptance evidence | Blockers |
| --- | --- | --- | --- |
| 00 Repository restructuring and environment audit | In review | Audit, roles, policies, roadmap and design validated and integrated through PR | PR integration |
| 01 Linux environment setup | Complete for supervised work | Dedicated identity, repository and local tool smoke checks recorded | Unattended auth and remote-write credentials are deferred |
| 02 Agent orchestration and persistent state | Supervised trial complete | Fixed marker passed under the studio identity; fixture ownership and interruption reconciliation verified | Additional live runs require new approval |
| 03 Security and emergency controls | In progress | Scoped permissions, redaction and owner stop/latch verified across process crash and reboot | Phase 02 and owner-controlled stop implementation |
| 04 OBS and Twitch integration | Planned | Local recording and controlled integration checks prove scene privacy, scope boundaries and reconnect behavior | Phase 03, authorized test credentials and reviewed platform policy |
| 05 Automated Godot development workflow | Planned | Repeatable headless import and smoke checks, protected PR validation, and reproducible test build | Supported export templates and approved workflow |
| 06 Private autonomous development testing | Planned | Bounded private trial completes and exercises failure recovery with sanitized report | Phases 03–05, tested limits and approval for private autonomy |
| 07 Supervised public broadcast | Planned | Owner-approved and supervised first stream passes privacy and stop rehearsal and produces devlog | Phase 06, first broadcast permission and channel readiness |
| 08 Scheduled autonomous broadcasts | Planned | Owner explicitly authorizes schedule and rehearsals prove fail-closed restart and stop behavior | Phase 07, tested scheduler and approved budget |
| 09 Continuous game development | Planned | Recurring sessions produce validated increments and owner-playtested milestones | Proven sustainable operation and milestone acceptance |
