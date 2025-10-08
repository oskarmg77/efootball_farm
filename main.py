"""CLI utility to analyze eFootball screenshots using the Gemini API.

The script expects the Google AI Studio API key to be available in the
``GEMINI_API_KEY`` environment variable. Usage example::

    python main.py analyze assets/menu.png

The output is a textual description of the detected menu elements and any
high-level gameplay insights that Gemini can infer from the screenshot.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable, List

import google.generativeai as genai

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - import guard
    raise SystemExit(
        "Pillow is required to load images. Install it with 'pip install pillow'."
    ) from exc


DEFAULT_PROMPT = """You are an assistant for eFootball. Describe the on-screen "
"menus, match information, and any highlighted options. Mention important "
"player names, teams, competition types, and actionable items such as "
"buttons or navigation hints. Keep the explanation structured in bullet "
"points."""


class GeminiConfigurationError(RuntimeError):
    """Raised when the Gemini API cannot be configured."""


def configure_gemini(api_key: str | None = None) -> None:
    """Configure the Gemini SDK with the provided API key."""

    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise GeminiConfigurationError(
            "Missing Gemini API key. Set the GEMINI_API_KEY environment variable "
            "or pass --api-key on the command line."
        )

    genai.configure(api_key=key)


def load_images(paths: Iterable[Path]) -> List[Image.Image]:
    """Load image files and return Pillow images for Gemini consumption."""

    images: List[Image.Image] = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")
        if not path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        with path.open("rb") as file:
            image = Image.open(file)
            image.load()
            images.append(image)
    return images


def analyze_images(
    image_paths: Iterable[Path],
    prompt: str,
    model_name: str = "gemini-1.5-flash",
) -> str:
    """Send the prompt and images to Gemini and return the textual response."""

    model = genai.GenerativeModel(model_name)
    images = load_images(image_paths)
    # Gemini expects the content as a list mixing text and image parts.
    content = [prompt, *images]
    response = model.generate_content(content)
    return response.text or "No description returned by Gemini."


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze one or multiple eFootball screenshots"
    )
    analyze_parser.add_argument(
        "images",
        type=Path,
        nargs="+",
        help="Paths to PNG/JPEG screenshots captured from eFootball",
    )
    analyze_parser.add_argument(
        "-p",
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Custom analysis prompt to send alongside the images.",
    )
    analyze_parser.add_argument(
        "--api-key",
        default=None,
        help="Gemini API key. Defaults to the GEMINI_API_KEY environment variable.",
    )
    analyze_parser.add_argument(
        "-m",
        "--model",
        default="gemini-1.5-flash",
        help="Gemini model to use (e.g., gemini-1.5-pro).",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if args.command == "analyze":
        try:
            configure_gemini(args.api_key)
        except GeminiConfigurationError as exc:
            print(str(exc), file=sys.stderr)
            return 1

        try:
            result = analyze_images(args.images, args.prompt, args.model)
        except (FileNotFoundError, ValueError) as exc:
            print(str(exc), file=sys.stderr)
            return 1
        except Exception as exc:  # pragma: no cover - network/API errors
            print(f"Gemini request failed: {exc}", file=sys.stderr)
            return 1

        print(result)
        return 0

    print("No command specified", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
