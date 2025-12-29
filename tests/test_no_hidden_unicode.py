from __future__ import annotations

import subprocess
from pathlib import Path

TARGET_EXTENSIONS = {".py", ".md", ".toml", ".yml", ".yaml", ".txt"}

BOM_BYTES = b"\xef\xbb\xbf"

REMOVE_CODEPOINTS = {
    0xFEFF,
    0x200B,
    0x200C,
    0x200D,
    0x2060,
    0x061C,
    0x200E,
    0x200F,
    0x202A,
    0x202B,
    0x202C,
    0x202D,
    0x202E,
    0x2066,
    0x2067,
    0x2068,
    0x2069,
    0x2028,
    0x2029,
}


def iter_target_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        cwd=root,
        capture_output=True,
        text=True,
    )
    paths: list[Path] = []
    for line in result.stdout.splitlines():
        path = root / line.strip()
        if not path.exists():
            continue
        if path.suffix.lower() in TARGET_EXTENSIONS:
            paths.append(path)
    return paths


def test_no_hidden_unicode() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    offenders: list[str] = []
    for path in iter_target_files(repo_root):
        data = path.read_bytes()
        has_bom = data.startswith(BOM_BYTES)
        if has_bom:
            data = data[len(BOM_BYTES) :]
        text = data.decode("utf-8", errors="strict")
        if has_bom or any(ord(char) in REMOVE_CODEPOINTS for char in text):
            offenders.append(str(path.relative_to(repo_root)))
    assert offenders == [], f"Hidden unicode found in: {', '.join(offenders)}"
