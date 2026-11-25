# Creative asset workflow

A developer request records the asset ID, purpose, target size and format, reference, palette constraints, acceptance criteria, and assignment. The Creative Agent records source, provider and model, source rights, prompt where useful, generation or revision date, processing and attribution. Save the original and approved output separately. QA verifies alpha, silhouette, scale, readability in Godot, rights and provenance before integration.

Interactive image generation is available through an authorized Codex session. Hosted integration and unattended billing are separate decisions. Establish an approved provider, cache by request and source revision, and enforce request, retry and spend limits before enabling generation from studio services. Start audio with procedural effects or appropriately licensed libraries. Keep canonical stream references under `branding/` once the owner supplies the original files.

## Asset request fields

| Field | Example |
| --- | --- |
| Asset ID and use | `shop_lantern_idle`, salvage or repair-bench prop |
| Footprint and framing | 32 × 32 transparent PNG, centered with bottom alignment |
| Source references and rights | Approved in-repo reference and its provenance record |
| Visual requirements | Readable silhouette at gameplay zoom and clear separation from the floor |
| Deliverables | Original, prepared PNG and provenance record |
| Acceptance | Alpha preserved, approved palette if specified, clean Godot import and visible in the target scene |

Record generator, model and prompt when a generator is used. For hand-drawn or procedural work, record the author and technique. Use the file checksum or source revision to identify the submitted original. Keep any provider credential out of the request and provenance.

The offline helper converts a single image to RGBA PNG, with optional cropping, trimming and nearest-neighbor fitting to a transparent canvas. Palette checking compares the RGB values of visible pixels without changing them. Use fixed canvases for sprite alignment. Keep originals and intermediate results outside tracked assets until review.

```bash
python3 studio/asset-generation/prepare_png.py source.png sprite.png --trim --size 64 64
python3 studio/asset-generation/prepare_png.py source.png sprite.png --palette 24213d a3e635
```

Requires Python and Pillow. Each command expects a new output path. The helper processes one asset in memory and performs no model or network calls.
