#!/usr/bin/env python3
"""Prepare a bounded, transparent PNG for review and Godot import."""

import argparse
from pathlib import Path

from PIL import Image

MAX_PIXELS = 4096**2


def palette_color(value: str) -> tuple[int, int, int]:
    try:
        color = tuple(bytes.fromhex(value.removeprefix("#")))
        if len(color) == 3:
            return color
    except ValueError:
        pass
    raise argparse.ArgumentTypeError("expected a six-digit RGB color")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--crop", type=int, nargs=4, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"))
    parser.add_argument("--trim", action="store_true")
    parser.add_argument("--size", type=int, nargs=2, metavar=("WIDTH", "HEIGHT"))
    parser.add_argument("--palette", type=palette_color, nargs="+")
    args = parser.parse_args()

    if args.output.suffix.lower() != ".png":
        parser.error("output must use the .png extension")
    if args.size and (min(args.size) < 1 or max(args.size) > 4096):
        parser.error("output dimensions must be between 1 and 4096")

    with Image.open(args.source) as source:
        if source.width * source.height > MAX_PIXELS:
            parser.error("input exceeds 16,777,216 pixels")
        image = source.convert("RGBA")

    if args.crop:
        left, top, right, bottom = args.crop
        if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
            parser.error("crop must be a nonempty rectangle inside the input")
        image = image.crop((left, top, right, bottom))
    if args.trim:
        bounds = image.getchannel("A").getbbox()
        if bounds is None:
            parser.error("cannot trim a fully transparent image")
        image = image.crop(bounds)
    if args.size:
        width, height = args.size
        scale = min(width / image.width, height / image.height)
        fitted = image.resize((max(1, round(image.width * scale)),
                               max(1, round(image.height * scale))), Image.Resampling.NEAREST)
        image = Image.new("RGBA", (width, height))
        image.paste(fitted, ((width - fitted.width) // 2, (height - fitted.height) // 2))
    if args.palette:
        allowed = set(args.palette)
        if any((r, g, b) not in allowed for r, g, b, a in image.getdata() if a):
            parser.error("visible pixels fall outside the approved palette")

    try:
        with args.output.open("xb") as output:
            image.save(output, format="PNG", optimize=True)
    except FileExistsError:
        parser.error("output already exists")


if __name__ == "__main__":
    main()
