# 2026-11-24 Approved local setup

The owner approved the dedicated OBS setup, protection of main, and provisioning work for future unattended operation. The Phase 01 sanity-check log remains a record of the original baseline.

- GitHub classic branch protection for main was applied and read back through the laptop CLI. Pull requests are required, including for administrators. Force pushes and deletion are disabled. No minimum review count was configured for this single-owner repository.
- The official Codex CLI 0.172.0 was tested in isolation and installed into the private project-specific user prefix. The system CLI was preserved. Using the existing ChatGPT login, a bounded workspace-write task produced the exact scratch marker, and an explicit resume returned the expected continuity word from the same session. Both exited 0 and emitted JSONL completion events. Reported input/output tokens were 31,045/63 for the first turn and 46,654/71 for resume. No API billing setup was used.
- The saved Code Goblin Local OBS profile and scene collection inherit the tested software x264 settings. They default to the safe scene and include static status text and exact X11 title/class matching for Game Preview. The first playback exposed a window-class mismatch. After correction, an isolated copy of the installed configuration recorded 237 frames, confirmed the Godot window and safe-scene playback, and shut down offline. The profile contains no stream credentials. No WebSocket was enabled.
- Host sudo was blocked by the no-new-privileges policy, so the initial setup handed account and STOP creation to the owner’s local terminal. No studio jobs were enabled.
- Before an unattended trial, provision a repository-only credential, test owner stop and recovery, and approve resource and usage ceilings. Twitch remains deferred to Phase 04.

## Verified account and fixture-only stop gate

The owner created the `code-goblin` system account. Host inspection confirmed its non-login shell, primary group only, and home at mode 0750 owned by that account. The active `/etc/code-goblin/STOP` is root-owned at mode 0644 in a root-owned directory at mode 0755. The studio account cannot remove the latch. The real file's inode, modification time and change time were unchanged by the dry run.

The dry run launches only a fixed fixture subprocess, using an empty environment. Its real-gate mode only checks and reports. All checks ran as the existing non-root session user in the default sandbox.

| Case | Observed result |
| --- | --- |
| Present test STOP | Exit 1, refused, no worker marker |
| New supervisor process with the same test STOP still set | Exit 1, refused, no worker marker |
| Test STOP mode 000 with a verified direct read denial | Exit 1, refused on latch presence, no worker marker |
| Test directory mode 0100 with a verified listing denial and no latch | Exit 1, refused, no worker marker |
| Readable test directory with no latch | Exit 0, exactly one fixture-worker marker |
| Real STOP, inspection-only | Exit 1, refused, no worker marker |

The fresh-process check proves that a new invocation consults the same on-disk test latch. It does not exercise a deployed service, service restart, laptop reboot, interrupted task recovery, or termination of an active worker group. Schedulers and services remained disabled for studio work. No GitHub credential, live Codex worker, OBS or Twitch operation was used by the dry run.

For one supervised orchestration trial, define one approved scratch task and one worker, verify the execution identity and supported login mode, and implement a single-run lock, task lease, sanitized checkpoint, deadline, process-group cleanup, and interruption reconciliation. Rehearse refusal and cleanup before the owner authorizes the trial and explicitly resets the real latch. The existing supervised Codex test does not establish unattended entitlement. The owner must confirm the allowed unattended auth and quota arrangement before unattended use, and approve CPU and memory guardrails, free disk floor, log retention, task and session deadlines, and per-session and daily usage ceilings. A local-only trial needs no GitHub credential. For a trial with remote writes, the owner must authorize the repository-only credential, its minimum required permissions and expiry, and its secure storage.

## Phase 02 local supervisor fixture

Extended the dry run with one nonblocking lock and one durable fixture-task record per test directory. An invocation records its unique owner, PID, start time and deadline before dispatch. Checkpoint replacement flushes both the file and directory. A terminal record prevents replay. After a supervisor crash, the bounded fixture group retains the lock until it exits. A fresh invocation then records the original owner's task as interrupted and refuses to replay it.

| Test | Observed result |
| --- | --- |
| Overlap during a live hold fixture | Second invocation exited 1. The running checkpoint and owner were preserved. |
| 1.5-second deadline on a fixture with a child | Supervisor exited 124 and recorded `timed_out`. The child PID was gone from `/proc`. Replay was refused. |
| Supervisor killed with SIGKILL after fixture dispatch | A fresh invocation refused while the fixture retained the lock. After fixture exit, another invocation recorded `interrupted` under the original owner. Neither invocation dispatched a second fixture. Later replay was refused. |
| Corrupt checkpoint | Refused and preserved the checkpoint. |
| Prior STOP checks and real refusal | Present and unreadable test latches, unreadable directory, and a fresh invocation with STOP set all refused. A readable clear directory produced one fixture marker. The real gate refused and its inode and change times were unchanged. |

The crash case demonstrates fresh-process reconciliation after the *bounded fixture* exits. It does not establish cleanup of a real worker after supervisor failure, cgroup containment, a deployed service restart, or reboot recovery. These tests used the existing non-root session user and scratch directories. No live Codex worker or studio service was launched.

### Proposed one-run supervised trial

Use one manually started worker for one owner-approved scratch marker task. Keep the checkout and outputs local. If the trial uses live Codex inference, allow only the supported model connection through the existing ChatGPT entitlement and record sanitized JSONL usage. No GitHub credential is needed. Use one turn and one launch, with no resumes, retries, scheduled dispatch, OBS or Twitch. Require an explicit owner reset of the real latch immediately before the trial, then re-arm it at wrap-up.

Proposed limits for owner approval, based on approximately 1.7 GiB memory available and 16 GiB disk free at this check:

- One CPU core equivalent and 768 MiB maximum memory for the worker group. Require at least 1.25 GiB available RAM and 12 GiB free disk before starting.
- 90 seconds maximum worker runtime and five minutes maximum for the supervised session. Cap combined sanitized logs at 5 MiB and scratch output at 100 MiB. Retain sanitized logs for seven days.
- One model turn per session and per day for this trial. Use 50,000 reported input tokens and 1,000 output tokens as post-run review thresholds. These thresholds are audit limits until a supported in-flight hard cap is verified. Authorize no additional spend.

Before starting, extend the fixture-only interface for an explicitly approved worker, verify the execution identity and usable login, and validate real process containment, cleanup after supervisor failure, and resource enforcement. Confirm the owner-approved entitlement separately before any unattended trial. Keep a repository-scoped credential deferred until a trial requires remote writes.

### Phase 02 supervised trial preparation

**No-go for live dispatch.** The production STOP refused dispatch and retained its root ownership, mode, inode and timestamps. Disposable diagnostic units ran under the desktop user's existing systemd manager with scoped host approval and were removed after testing. No studio service or scheduler was enabled. No Codex model turn or credential transfer occurred.

| Control | Fixture evidence and remaining work |
| --- | --- |
| Worker entry point and login | The private Codex CLI 0.172.0 returned its version, advertised JSON output and workspace-write execution, and reported ChatGPT login under the desktop identity. The current supervisor only accepts fixed fixtures. The dedicated account has a non-login shell and a private home, and the verified CLI is behind desktop-only directory permissions. Dedicated CLI access, login, and a fixed one-turn scratch entry point remain unverified. |
| Identity and scratch | A fresh desktop-owned scratch directory was mode 0700. The session cannot switch to the studio identity because host sudo fails under no-new-privileges. Verify scratch create, write and cleanup as the studio UID before a trial. |
| CPU and memory | With CPUQuota=100%, competing fixture processes produced cgroup throttling. The cgroup reported memory.max=805306368 and memory.swap.max=0. An 800 MiB allocation child was killed and memory events advanced. Retest in the actual trial cgroup under the chosen identity. |
| Worker deadline and crash | A three-second systemd runtime limit removed a child in a separate process session and recorded a timeout. When the transient unit's main supervisor process was SIGKILLed, systemd removed the detached child and recorded a signal failure. The 90-second worker setting was accepted in a separate CPU fixture. Verify the integrated five-minute session deadline and cleanup with the 90-second worker limit. |
| Launch floors | The scratch filesystem had 16,459,100,160 bytes free and MemAvailable was 1,785,393,152 bytes. A boundary fixture accepted 1.25 GiB available RAM and 12 GB free disk and refused values a byte below either floor. Wire the checks into the same preflight that launches the worker. |
| Log, retention and scratch | Per-file limits refused one byte above 5 MiB and 100 MiB. Two files could each reach either limit, so per-file limits cannot enforce the combined 5 MiB log budget or 100 MiB scratch budget. A retention fixture selected the eight-day-old log and preserved the six-day-old one. Implement and test a bounded sanitized log sink, seven-day retention, and a size-limited scratch volume or quota before dispatch. |
| Turn count and token evidence | Trial remains one scratch task and one turn with no retries, resumes or remote writes. Review structured usage after the run against 50,000 input and 1,000 output tokens. These are review thresholds. |

The minimum owner action now is to authorize a one-time, fixture-only host test under the dedicated UID and provide a narrow way to launch it, such as running a reviewed transient unit from the owner terminal. Keep STOP set. Use an owner-approved CLI location and supported sign-in flow for that identity. If aggregate scratch enforcement needs host privileges, authorize only a capped temporary volume or quota for the trial scratch path. Finish the integrated preflight and cleanup tests before requesting approval of a live run and a separate latch reset.

## Work queue — fixed trial fixture

The owner approved supervised game work while the real STOP remains active. This scope decision leaves automated dispatch gated. Milestone 1 uses a separate worktree and branch.

The desktop-user transient Phase 02 fixture ran one fixed scratch-marker write and read under a private 100 MiB mount and offline systemd limits of one CPU core, 768 MiB RAM, zero swap and 300 seconds. The integrated fixture checked available RAM and backing-disk space, bounded its worker by the earlier of 90 seconds and the session deadline, and refused replay independently of log retention. Synthetic checks verified the shared 5 MiB stdout/stderr cap, stale-log removal at seven days, a bounded stream wait, and refusal without a capped mount. Two files filled the same mount to 100 MiB and a further block failed with ENOSPC.

Dedicated-UID validation is pending. The owner can run `bash scripts/check-studio-uid.sh` in the studio checkout to launch the reviewed offline transient fixture as `code-goblin` and report CLI version and login status. The current verified 0.172.0 CLI and ChatGPT login belong to the desktop account. No personal credentials were copied. A supported dedicated CLI installation and sign-in remain to be verified before requesting one live trial and a separate latch reset. The current fixture has a fixed harmless command and captures its output only. Live-worker log sanitization and the final execution path remain gated.

No scheduler or permanent service was enabled, and no model turn was launched. Deployed active-stop, restart and reboot recovery are pending. The OBS/Twitch rehearsal is outside the owner’s supervised-game-only authorization while STOP is set.

The separate game worktree passed a visible desktop playthrough from the exported pack. The [Milestone 1 draft PR](https://github.com/bryce496913/code-goblin/pull/3) is open for owner playtesting.

### Dedicated account fixture result

The owner terminal reported that the offline transient fixture passed as UID 997 with exit 0, 146 ms runtime, and 1.8 MiB peak memory. The account could execute system Codex CLI 0.130.0 and reported `Not logged in`. This verifies the fixed fixture under the intended identity. The next gate is access to the previously tested Codex CLI 0.172.0 and a fresh device sign-in under the studio identity. The owner should authorize the intended ChatGPT account directly. The real STOP remains active and live dispatch still requires separate approval and reset.

The owner subsequently ran the pinned 0.172.0 CLI's login status under `code-goblin` and reported `Logged in using ChatGPT`. This closes the dedicated-account sign-in check. Model execution under this identity, aggregate controls for a live worker, and unattended entitlement remain unverified. STOP was confirmed active. No worker was dispatched.

## Supervised trial launcher review

The proposed launch method uses a root-owned one-time claim, a named transient unit under the dedicated identity, a fixed read-only Codex prompt, a 90-second worker deadline and a five-minute unit deadline. The launcher disables plugins, apps, shell and web search. The supervisor writes its own scratch marker only after one exact model answer and a successful exit. It counts stdout and stderr against a combined 5 MiB cap and saves only a start record and allowlisted marker, numeric usage and review-threshold fields. Raw tool text, JSONL, stderr, account identifiers and error details are excluded from the report. It keeps the real auth file outside scratch and does not copy it. A required credential refresh may fail safely under the read-only host filesystem.

The desktop-user transient protocol fixture passed with one simulated turn. Additional checks refused a second turn, a completed tool action, malformed JSON, more than 5 MiB combined output, and a stalled stream. The exact live shell entry point refused while the real STOP was active, without creating the one-time claim. A mount precedence error initially caused the fixture to refuse. Removing the redundant writable bind made the private 100 MiB tmpfs take effect. The new dedicated-UID offline protocol fixture and auth-file readability check remain owner-terminal gates.

The live envelope specifies CPUQuota=100%, MemoryMax=768M, MemorySwapMax=0, KillMode=control-group, a private 100 MiB scratch mount, 1.25 GiB available RAM and 12 GB free disk floors, and no additional spend. Usage review thresholds are 50,000 input and 1,000 output tokens. One model turn, no retry, resume, repository write or broadcast is proposed. The fixed prompt and disabled tools limit the application path. The current systemd unit has no network destination allowlist, so approval must explicitly accept relying on the pinned client for the available network path or require a separately verified endpoint restriction. No automatic retention job is added. The owner deletes the sanitized trial log by day seven after reviewing it, while the root one-time claim stays in place.

### Owner launch, stop and re-arm procedure for review

Keep STOP active while running the exact offline fixture from the owner terminal.

```bash
bash 'scripts/check-trial-launch.sh'
```

After the dedicated fixture passes and explicit trial approval is recorded, the owner separately resets STOP and starts the reviewed one-run launcher from the laptop terminal. These are review commands only until then.

```bash
sudo rm -- /etc/code-goblin/STOP
bash 'scripts/launch-one-trial.sh' --approved-one-run
```

From another owner terminal, re-arm first, then stop the whole transient group. After normal completion, verify the latch is present even if the launcher reports automatic re-arm.

```bash
sudo touch /etc/code-goblin/STOP
sudo systemctl stop code-goblin-supervised-trial.service
sudo test -f /etc/code-goblin/STOP
```

The unit may already be collected after a normal exit. Inspect only the sanitized report at `/var/lib/code-goblin-supervised-trial/trial-live.log`. After reviewing it, remove it within seven days using `sudo rm -- /var/lib/code-goblin-supervised-trial/trial-live.log`. Preserve the root-owned one-time claim. Deployed restart, active-worker stop and recovery remain future tests.

### Owner playtest

GitHub reports that PR #3 is merged. The desktop launcher **Play Code Goblin — Milestone 1** was installed and verified to open the local, byte-reproducible pack. Owner playtest acceptance remains a separate gate for Milestone 2. Ask whether movement feels right, whether the salvage, Pip, and bench prompts lead naturally through the repair, and whether the success state is clear.

The owner-terminal offline launcher fixture passed as UID 997 with exit 0, a 163 ms runtime and a reported 1.7 MiB memory peak. Its sanitized result verified the marker and reported 7 input and 2 output tokens from the fixture. The dedicated auth-file readability check passed. This was simulated output, with no model usage. The real STOP was confirmed active and the live claim was absent. The next gate is bundled owner approval of the trial, limits and network requirement, followed by a separate STOP reset.

The owner approved the one-run trial and its proposed resource and usage ceilings. The approval did not select one of the two mutually exclusive network options. The real STOP remains set and the live claim remains absent. No model turn was launched.

The owner selected network option 1 for the single supervised run. The pinned CLI may use its existing network path with shell, web search, apps and plugins disabled. This does not authorize unattended or future runs. STOP was still present and the one-time claim absent before handing off the owner-only reset and launch commands.

### Approved supervised trial result

The owner reset STOP and launched the one authorized run. The pinned CLI completed the fixed marker task as `code-goblin` (UID 997). The sanitized report showed `marker_verified: true`, 12,028 input and 11 output tokens, and usage within the 50,000 input / 1,000 output review thresholds. The transient unit returned exit 0. The owner terminal reported 5.660 s service runtime, 1.500 s CPU, 1.5 MiB memory peak and no swap.

Read-only host verification after exit found the root-owned STOP file present at mode 0644, the root-owned one-run claim present at mode 0700, and the named unit inactive and collected. No Code Goblin units were listed. The one-run authorization is spent. Retain the claim and remove the sanitized log by December 1, 2026.

The successful exit verifies the approved launch and normal cleanup. Phase 03 still needs an owner-issued stop during an active deployed fixture, crash recovery, and refusal after restart and an authorized reboot. Scheduling remains disabled. Milestone 2 still awaits explicit owner acceptance of the Milestone 1 playtest.

### Direct host authorization

Codex launched a system-level transient identity check and the full offline protocol fixture directly through the laptop's native interactive authorization. The first returned UID 997. The full fixture passed as UID 997 with the private network and the configured CPU, memory, scratch and runtime limits. It exited 0 in 538 ms and the unit was collected. No terminal command had to be relayed to the owner. A noninteractive launch was refused by host policy, so future privileged actions may prompt for desktop authorization. STOP remained active. No persistent privilege, unit, or scheduler was added.
