#!/usr/bin/env python3
"""Print the configured document download strategy for a library."""
import argparse
from pathlib import Path

import yaml

def get_strategy(library_name: str, config_path: Path) -> None:
    with config_path.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file) or {}
    for library in config.get("libraries", []):
        if library["name"].lower() == library_name.lower():
            print(library["doc_source"])
            return
    raise SystemExit(f"Library not found: {library_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("library")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "libraries.yaml",
    )
    args = parser.parse_args()
    get_strategy(args.library, args.config)
