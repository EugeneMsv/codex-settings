#!/usr/bin/env python3
"""Sanity-check Codex TOML config files without reading secrets."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path
from typing import Any


SECRET_NAMES = {
    ".env",
    "auth.json",
    "id_rsa",
    "id_ed25519",
    "credentials",
    "credentials.json",
}

PATH_KEYS = {
    "additional_directories",
    "env_file",
    "include",
    "path",
    "paths",
    "rules",
    "script",
}


def default_config_paths() -> list[Path]:
    paths = [Path.home() / ".codex" / "config.toml"]
    project_config = Path.cwd() / ".codex" / "config.toml"
    if project_config not in paths:
        paths.append(project_config)
    return paths


def is_secret_path(path: Path) -> bool:
    names = {part.lower() for part in path.parts}
    return bool(names & SECRET_NAMES) or any("secret" in part or "token" in part for part in names)


def parse_config(path: Path) -> dict[str, Any]:
    with path.open("rb") as config_file:
        parsed = tomllib.load(config_file)
    if not isinstance(parsed, dict):
        raise ValueError("top-level TOML value is not a table")
    return parsed


def iter_path_values(config: Any, parent_key: str = "") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(config, dict):
        for key, value in config.items():
            key_path = f"{parent_key}.{key}" if parent_key else str(key)
            lower_key = str(key).lower()
            if lower_key in PATH_KEYS or lower_key.endswith("_path") or lower_key.endswith("_file"):
                found.extend((key_path, candidate) for candidate in scalar_paths(value))
            found.extend(iter_path_values(value, key_path))
    elif isinstance(config, list):
        for index, value in enumerate(config):
            found.extend(iter_path_values(value, f"{parent_key}[{index}]"))
    return found


def scalar_paths(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [candidate for item in value for candidate in scalar_paths(item)]
    return []


def check_path_references(config_path: Path, config: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    base_dir = config_path.parent
    for key_path, raw_value in iter_path_values(config):
        if "://" in raw_value or raw_value.startswith("$"):
            continue
        candidate = Path(raw_value).expanduser()
        if not candidate.is_absolute():
            candidate = base_dir / candidate
        if is_secret_path(candidate):
            warnings.append(f"{key_path}: skipped secret-looking path {raw_value!r}")
            continue
        if not candidate.exists():
            warnings.append(f"{key_path}: referenced path does not exist: {raw_value!r}")
    return warnings


def check_config(path: Path) -> int:
    expanded_path = path.expanduser()
    if is_secret_path(expanded_path):
        print(f"SKIP {path}: secret-looking path", file=sys.stderr)
        return 0
    if not expanded_path.exists():
        print(f"SKIP {path}: file not found")
        return 0

    try:
        config = parse_config(expanded_path)
    except tomllib.TOMLDecodeError as error:
        print(f"ERROR {path}: TOML parse failed: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"ERROR {path}: could not read file: {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"ERROR {path}: {error}", file=sys.stderr)
        return 1

    top_level = ", ".join(sorted(config.keys())) if config else "(empty)"
    print(f"OK {path}: valid TOML; top-level keys: {top_level}")

    for warning in check_path_references(expanded_path, config):
        print(f"WARN {path}: {warning}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Codex TOML config syntax and common local path references."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Config files to check. Defaults to ~/.codex/config.toml and .codex/config.toml.",
    )
    args = parser.parse_args()

    paths = args.paths or default_config_paths()
    exit_code = 0
    for path in paths:
        exit_code = max(exit_code, check_config(path))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
