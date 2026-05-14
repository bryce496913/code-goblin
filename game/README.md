# Game Folder

This folder contains the Godot project for the first Code Goblin game.

Current game:

# Goblin: Last Stop to Montauk

Recommended engine:

- Godot 4
- 2D top-down project
- GDScript

## Opening Locally

From a Linux laptop with Godot 4 installed:

1. Open Godot.
2. Click **Import**.
3. Select this file:

```text
game/project.godot
```

4. Open the imported project.
5. Run the project to load the placeholder main scene.

You can also start the editor from the repository root:

```sh
godot --path game
```

## Current Project State

This is only the initial Godot project skeleton.

It includes:

- `project.godot`
- A minimal placeholder main scene
- A placeholder project icon

It does not include player movement, repair interactions, collectibles, NPCs, inventory, or gameplay systems yet.

## First Prototype Goal

The first game prototype should include:

- A simple repair shop room
- A controllable Goblin character
- One collectible scrap item
- One NPC customer
- One repair bench
- One basic repair interaction
- One completion message

## Development Rule

Keep early systems simple.

The goal is a playable loop before polish.
