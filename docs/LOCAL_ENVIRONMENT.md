# Local development environment

Code Goblin runs on Linux Mint 22.3 with the Godot Compatibility renderer and an existing project-pinned Codex CLI. The [laptop baseline](LAPTOP_BASELINE.md) records exact versions and hardware limits.

## Setup and repair

Run these commands from the repository root as the supervised development user:

```bash
python3 scripts/preflight-environment.py --setup
python3 scripts/preflight-environment.py --online --godot-smoke --asset-smoke
```

The first command creates or repairs the private runtime directory modes and verifies installed tools. A normal check does not repair paths. The online check reads the GitHub main ref without prompting for credentials. The Godot and asset checks use temporary inputs and remove them on exit. Codex is checked through its executable and non-interactive help. Neither command starts a model, installs packages, clears STOP, or authorizes unattended operation.

If the preflight reports a missing required tool, install or restore only that dependency using the approved host package source. The Mint/Ubuntu package names are `bash`, `git`, `gh`, `python3`, `python3-pil`, `nodejs`, `npm`, and `obs-studio`. Keep the existing Godot 4.6.2 installation or restore the matching official Linux executable. The supervised CLI was verified with Codex 0.172.0. The check prefers the existing pinned desktop installation and falls back to PATH when unavailable. Review the reported version before using that fallback for execution. No required tools were missing on the audited laptop.

For a disposable setup, pass `--root /absolute/path/to/runtime`. The root must be outside this checkout. A wrong owner, unreadable directory, symlink or restrictive host sandbox needs inspection before repair. The check never requests a credential or copies a login. Run the local game delivery checks separately through [Godot validation](../game/README.md).

## Runtime storage

The default root is `${XDG_STATE_HOME:-$HOME/.local/state}/code-goblin/runtime`. The root and its children are owned by the invoking user and use mode `0700`.

| Directory | Purpose |
| --- | --- |
| `config/` | Private, non-secret local overrides |
| `tmp/` | Disposable checks and staging |
| `logs/` | Sanitized local logs subject to retention limits |
| `generated-assets/` | Unreviewed sources and intermediate assets |
| `cache/` | Rebuildable local caches |
| `state/` | Local checkpoints and leases |

Commit reviewed code, asset outputs, provenance and sanitized devlogs. Keep private runtime data and credentials outside Git. Existing account authentication, OBS recording storage, and the root-controlled STOP retain their own locations. The setup does not move, import or modify them and does not provision a service account’s runtime.

The laptop uses integrated graphics. Software encoding is the verified OBS path. Sustained concurrent application work still requires the thermal follow-up in the baseline.
