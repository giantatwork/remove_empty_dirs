from pathlib import Path

from folderfix import get_empty


def test_get_empty():
    start_dir = Path.cwd() / "fixtures"
    res = get_empty(start_dir)
    assert res is not None

    for r in res:
        print(r)

    assert res == [
        start_dir / "a/b/r/s/t",
        start_dir / "a/b/c/c2",
        start_dir / "q/r/s/s2",
        start_dir / "1/2/3/4",
        start_dir / "a/b/r/s",
        start_dir / "a/b/r",
    ]


# test_get_empty()
