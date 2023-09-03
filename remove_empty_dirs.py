#!/usr/bin/env python

import argparse
import os
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
    """
    Only look for directories that do not start with a '.'
    """
    return [
        f"{path}{os.sep}"
        for path in start_dir.glob("*/**")
        if path.is_dir() and not any(part.startswith(".") for part in path.parts)
    ]


def get_excluded_paths(start_dir: Path) -> list[str]:
    """
    Exclude all directories containing files and directories starting with a '.'
    """
    return [
        str(path)
        for path in start_dir.glob("**/*")
        if path.is_file()
        or (path.is_dir() and any([part.startswith(".") for part in path.parts]))
    ]


def get_empty(start_dir: Path) -> list[Path] | None:
    empty_list = []
    result = None

    directory_paths = get_directory_paths(start_dir)
    if not directory_paths:
        return None
    excluded_paths = get_excluded_paths(start_dir)

    for dir_path in directory_paths:
        exclude = False
        for path in excluded_paths:
            if dir_path in path:
                exclude = True
                continue
        if not exclude:
            empty_list.append(dir_path)

        empty_list.sort(key=len, reverse=True)
        result = [Path(x) for x in empty_list]

    return result


if __name__ == "__main__":
    sys.exit(main())
