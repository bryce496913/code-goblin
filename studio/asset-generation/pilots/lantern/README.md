# Lantern asset pilot

- Task: `creative-pilot-lantern`. Prepare one repaired subway lantern as a 64 × 64 RGBA prop candidate.
- Assignment: supervised Creative handoff in the current chat with one built-in generation call, no retry, and work restricted to this pilot and disposable Godot validation.
- Source: original AI-generated image using the built-in OpenAI image generation tool on November 24, 2026. The tool did not report a model version. No reference image, externally sourced art or branding was supplied.
- Source SHA-256: `51e926d2cee9e4e4b4938136d446f787be71dafeafd1758a438b43d078c28e99`. The full-resolution source is retained in the local private workspace. The candidate checksum is `2eabebbcc63b779d2b36233ffcc95c2961628eca6ff57e75010bd671fcb887d3`.
- Processing: crop to alpha bounds and fit with nearest-neighbor resampling on a transparent 64 × 64 canvas. Initial visual inspection confirmed a readable warm lantern silhouette with a transparent surround. No formal gameplay palette was applied.
- Technical check: Godot 4.6.2 imported the prepared PNG in a clean scratch project, loaded it as a 64 × 64 Texture2D, verified transparent and occupied pixel samples, and instantiated a Sprite2D.
- Review status: asset-workflow candidate. This did not change the playable shop. Independent pilot QA passed. Release review is pending. The built-in call did not expose numeric usage or cost.

## Generation prompt

> Use case: stylized-concept. Generate one original isolated 2D game prop sprite for Goblin: Last Stop to Montauk: a repaired squat brass subway lantern, with a chunky carry handle, scuffed copper casing and a bright warm amber glass center. Top-down three-quarter view consistent with a cute scrappy subway repair shop, low-resolution pixel-art shapes, limited muted colors, strong readable silhouette at 64 pixels. Center the whole object with padding. True transparent background. No floor, cast shadow, text, logos, characters or other objects.

## Prepare from the retained source

```bash
python3 studio/asset-generation/prepare_png.py source.png lantern-64.png --trim --size 64 64
```

## Independent QA

A separate reviewer verified PNG integrity, 64 × 64 RGBA, transparent outer pixels, and a visible amber silhouette at native size. Both source and candidate checksums matched the provenance record. Reprocessing the retained original produced a byte-identical candidate. The Godot import remains the separately recorded supervised check.
