#!/usr/bin/env python

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Find and remove empty directories except hidden directories."
    )
    parser.add_argument("start_dir", help="Starting directory")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show empty directories and quit."
    )
    parser.add_argument(
        "--no-interaction",
        action="store_true",
        help="Skip confirmation and delete all empty directories immediately.",
    )

    args = parser.parse_args()
    start_dir = args.start_dir

    if start_dir == ".":
        start_dir = Path.cwd()

    start_dir = Path(start_dir).expanduser()

    if not Path.exists(start_dir):
        print(f"Path '{start_dir}' does not exist")
        return 1

    empty_dirs = get_empty(start_dir)

    if not empty_dirs:
        print("Could not find any empty directories")
        return 0

    print_directories(empty_dirs)
    if args.dry_run:
        return 0

    if args.no_interaction:
        return remove_directories(empty_dirs)

    confirm = input("Delete empty directories? (y/N)\n")
    if confirm.lower() != "y":
        print("Skipped")
        return 0

    return remove_directories(empty_dirs)


def print_directories(paths: list[Path]):
    print("Empty directories:\n")
    for path in paths:
        print(f"- {path}")
    print()


def remove_directories(paths: list[Path]) -> bool:
    for path in paths:
        try:
            path.rmdir()
        except Exception as ex:
            print(f"Failed to remove directory '{path}, skipping ...', error: {ex}")
            return False
        else:
            print(f"Removed directory '{path}'")

    return True


def get_directory_paths(start_dir: Path) -> list[str]:
    return [
        path
        for path in start_dir.glob("*/**")
        if path.is_dir() and not any(part.startswith(".") for part in path.parts)
    ]


def contains_file(dir: Path) -> bool:
    for path in dir.glob("**/*"):
        if path.is_file() or any([part.startswith(".") for part in path.parts]):
            return True
    return False


def get_empty(start_dir: Path) -> list[Path] | None:
    empty_list = []

    directory_paths = get_directory_paths(start_dir)
    if not directory_paths:
        return None

    for dir_path in directory_paths:
        if not contains_file(dir_path):
            empty_list.append(dir_path)

    empty_list.sort(key=lambda x: len(str(x)), reverse=True)

    return empty_list


if __name__ == "__main__":
    sys.exit(main())
