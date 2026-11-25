# Goblin: Last Stop to Montauk

In Godot 4.6.2, choose **Import** and select `game/project.godot`. To play from the repository root, run `godot --path game`. This top-down 2D GDScript project uses the Compatibility renderer.

## Goblin Opens the Shop

Move with WASD or the arrow keys. Press **E** near the salvage tray, Pip, and the repair bench. Pick up scrap, talk to Pip about the lantern, then use the bench. The shop displays your progress and confirms the finished repair. Restart the game to replay the task.

The room, characters and props are drawn with original Godot shapes in the scene script. The prototype has no audio or saved progress.

## Validation and local export

From the repository root, with Godot 4.6.2 on PATH:

```bash
bash game/tests/validate-local.sh /tmp/goblin-opens-the-shop.pck
godot --main-pack /tmp/goblin-opens-the-shop.pck
```

The build script imports a clean copy, checks startup and the repair loop, exports
a Linux PCK, then repeats startup and the repair loop from the pack. Use a new
absolute output path. The PCK requires a compatible Godot executable. A native
standalone export requires the matching Godot export template.

## Development rule

Keep early systems simple. The goal is a playable loop before polish.
