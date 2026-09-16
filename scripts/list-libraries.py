#!/usr/bin/env python3
"""List libraries configured in libraries.yaml."""
import argparse
from pathlib import Path

import yaml

def list_libraries(config_path: Path) -> None:
    with config_path.open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file) or {}
    for library in config.get("libraries", []):
        print(f"{library['name']}\t{library.get('version_check', 'unknown')}\t{library['doc_source']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "libraries.yaml",
    )
    args = parser.parse_args()
    list_libraries(args.config)
