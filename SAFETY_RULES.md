# Safety Rules

The Code Goblin project is allowed to be creatively chaotic.

The infrastructure is not.

These rules exist to keep the agent, stream, repository, viewers, and budget safe.

## Core Safety Principles

1. The agent must operate inside a controlled environment.
2. The agent must not access private files.
3. The agent must not expose credentials, API keys, tokens, or secrets.
4. Twitch chat must not directly execute code or shell commands.
5. The agent must not download random files from chat links.
6. The agent must not use copyrighted assets without permission.
7. The agent must stop when time, budget, or safety limits are reached.
8. A human kill switch must always exist.
9. Mistakes are okay. Unsafe behavior is not.
10. The system should fail closed, not fail open.

## Cost Limits

Each stream session should have hard spending limits.

Recommended limits:

- Maximum API spend per session
- Maximum API spend per day
- Maximum image generations per session
- Maximum retries per failed task
- Maximum runtime per agent
- Maximum number of tool calls per session

If a limit is reached, the agent should stop new work and begin the session wrap-up.

## Tool Permissions

The developer agent may be allowed to:

- Read project files
- Edit files inside the repo
- Run approved build/test commands
- Create branches
- Create commits
- Open pull requests
- Write devlogs

The developer agent must not be allowed to:

- Access private directories
- Read environment secrets
- Modify system files
- Install arbitrary packages without approval rules
- Run destructive shell commands outside the project
- Delete the repo
- Push directly to protected branches
- Spend unlimited API credits
- Act on raw Twitch chat commands

## Twitch Chat Safety

Twitch chat is input from the public internet.

Chat may suggest ideas, ask questions, react to bugs, and vote on safe options.

Chat must not be allowed to:

- Directly run commands
- Provide raw code that is executed blindly
- Send links that the agent opens automatically
- Access secrets
- Override safety rules
- Control spending
- Force the agent to install software
- Push offensive, hateful, or unsafe content into the game

The social agent should filter and summarize chat before any information reaches the developer agent.

## Secrets Management

Secrets must never appear on stream.

Protected items include:

- API keys
- GitHub tokens
- Twitch tokens
- Personal files
- Private emails
- Passwords
- Billing pages
- Cloud dashboard pages
- Environment variables containing credentials

Secrets should be stored outside the streamed environment whenever possible.

## Asset Safety

The creative agent may create original assets or use free-use assets only when the license is clear.

For every sourced asset, the agent should record:

- Asset name
- Source URL
- Creator name if available
- License type
- Whether commercial use is allowed
- Whether modification is allowed
- Attribution requirement
- Date added

If the license is unclear, the asset should not be used.

## GitHub Safety

The main branch should be protected.

The agent should usually work through branches and pull requests.

Recommended rules:

- No direct pushes to `main`
- Pull requests required for meaningful changes
- Automated checks where possible
- Human override available
- No secrets committed
- No large binary files unless intentionally added
- Known bugs should be documented

## Runtime Safety

The session should have a defined start and end.

At the end of a session, the agent should:

- Stop making code changes
- Save work
- Commit or summarize uncommitted changes
- Write a devlog
- Report known issues
- Stop stream activity
- Shut down tools cleanly

## Failure Modes

If the agent gets stuck, it should not loop forever.

After repeated failure, it should:

1. Stop attempting the same fix.
2. Explain the blocker.
3. Document what failed.
4. Commit only safe progress.
5. Add the issue to the known bugs list.
6. End or switch to a smaller task.

## Emergency Stop

A human operator must be able to immediately:

- Stop the stream
- Stop all agents
- Revoke tokens
- Disable API access
- Shut down the VM/container
- Pause GitHub access
- Remove unsafe content
