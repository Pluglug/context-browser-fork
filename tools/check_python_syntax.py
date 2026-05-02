"""Check source files against a target Python syntax version."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path
import sys


DEFAULT_TARGETS = ("src/context_browser",)
DEFAULT_FEATURE_VERSION = "3.7"


def parse_feature_version(value: str) -> tuple[int, int]:
    parts = value.split(".")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("feature version must use MAJOR.MINOR, e.g. 3.7")

    try:
        major, minor = (int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("feature version must contain integers") from exc

    if major != 3 or minor < 7:
        raise argparse.ArgumentTypeError("feature version must be Python 3.7 or newer")

    return major, minor


def iter_python_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file():
            if path.suffix == ".py":
                files.append(path)
            continue

        if path.is_dir():
            files.extend(sorted(path.rglob("*.py")))
            continue

        raise FileNotFoundError(path)

    return sorted(set(files))


def check_file(path: Path, feature_version: tuple[int, int]) -> SyntaxError | None:
    source = path.read_text(encoding="utf-8")
    try:
        ast.parse(source, filename=str(path), feature_version=feature_version)
    except SyntaxError as exc:
        return exc

    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Parse Python files with an older Python grammar. "
            "This catches syntax that would break older supported Blender versions."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=DEFAULT_TARGETS,
        help="Files or directories to check. Defaults to src/context_browser.",
    )
    parser.add_argument(
        "--feature-version",
        type=parse_feature_version,
        default=parse_feature_version(DEFAULT_FEATURE_VERSION),
        help="Python grammar version to check against. Defaults to 3.7.",
    )
    args = parser.parse_args()

    root = Path.cwd()
    paths = [Path(path) for path in args.paths]

    try:
        files = iter_python_files(paths)
    except FileNotFoundError as exc:
        print(f"error: path not found: {exc.args[0]}", file=sys.stderr)
        return 2

    errors: list[tuple[Path, SyntaxError]] = []
    for path in files:
        error = check_file(path, args.feature_version)
        if error is not None:
            errors.append((path, error))

    if errors:
        for path, error in errors:
            try:
                display_path = path.relative_to(root)
            except ValueError:
                display_path = path

            print(
                f"{display_path}:{error.lineno}:{error.offset}: "
                f"{error.__class__.__name__}: {error.msg}",
                file=sys.stderr,
            )

        return 1

    version = ".".join(str(part) for part in args.feature_version)
    print(f"Checked {len(files)} Python files with Python {version} grammar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
