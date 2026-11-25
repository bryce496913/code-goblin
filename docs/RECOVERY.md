# Shutdown and recovery design

Proposed. The owner controls an emergency stop outside Codex. Implement it with an owner-writable persistent latch outside the checkout and a supervisor that refuses to start work or broadcast when the latch is present or unreadable. The agent account must lack write access to the latch and service controls. Group workers in a dedicated service unit or cgroup so children can be terminated together.

1. On stop, set the latch first, disable scheduler dispatch and restart paths, stop the broadcast through the independent OBS control or UI, then terminate the agent group. If graceful termination times out, force-stop the group. If OBS cannot stop or confirm the stream, exit OBS or cut its network access and verify the channel is offline.
2. Preserve sanitized logs, local checkpoints and Git state. The owner verifies no agents or public streams remain active. The latch survives restart and requires an explicit owner reset.
3. Inspect the checkout, outstanding side effects, resource state and credentials as relevant. Record the incident and recovery evidence. Resume only after the owner clears the latch and the supervisor passes a fresh preflight.

| Failure | Recovery |
| --- | --- |
| Agent crash or timeout | Preserve task lease and reconcile diff, commits and side effects. Resume only a recoverable task within its limits. |
| Network loss | Suspend new online operations. Verify remote Git and stream state before a bounded reconnect. |
| Codex rate limit | Honor provider retry timing within the session deadline. Preserve progress and defer when the limit persists. |
| Authentication failure | Stop the affected integration, avoid retry loops, request owner-managed credential repair. |
| OBS crash | Check actual Twitch live status. Stop or latch if uncertain. Reopen privately and repeat scene checks before any authorized broadcast. |
| Twitch disconnect | Suspend chat sends, use documented EventSub recovery, deduplicate events, and confirm live status independently. |
| Excess CPU, memory or low disk | Stop launches, checkpoint and terminate workloads if pressure persists. Diagnose offline before resuming. |
| Repository conflict | Pause integration and preserve both sides. Resolve in a task branch or escalate when intent is unclear. |
| Failed tests | Keep changes off stable. Record logs and the smallest known reproduction. |
| Laptop restart | Start with no active dispatch. Verify latch, prior checkpoints, task ownership, Git state and external side effects. |
| Security incident | Latch, stop broadcast, isolate affected services, preserve sanitized evidence and notify owner. Owner coordinates revocation and authorizes recovery. |
