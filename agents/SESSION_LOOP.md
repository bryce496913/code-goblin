# Session Loop

Every Code Goblin development session should follow this loop.

## 1. Wake Up

The agent starts the session.

It should say:

- Who it is
- What project it is working on
- What the current milestone is
- What it plans to attempt today

## 2. Read Context

The agent should read:

- README
- Game brief
- Roadmap
- Recent devlogs
- Current open issues
- Current branch state
- Current milestone

## 3. Choose One Goal

The agent should choose one realistic goal.

Good goals:

- Add basic movement
- Add one collectible item
- Add one NPC dialogue
- Fix interaction prompt
- Add repair bench behavior

Bad goals:

- Build the whole game
- Create full crafting system immediately
- Rewrite the engine
- Add multiplayer
- Add procedural open world

## 4. Define Done

The agent must define what success means.

Example:

```text
Done means the player can walk to a scrap item, press interact, collect it, and see confirmation text.
