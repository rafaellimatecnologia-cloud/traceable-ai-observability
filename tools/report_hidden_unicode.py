"""Report hidden/bidirectional Unicode characters in tracked files."""

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


def scan_file(path: Path) -> tuple[bool, set[int]]:
    data = path.read_bytes()
    has_bom = data.startswith(BOM_BYTES)
    if has_bom:
        data = data[len(BOM_BYTES) :]
    text = data.decode("utf-8", errors="strict")
    found = {ord(char) for char in text if ord(char) in REMOVE_CODEPOINTS}
    return has_bom, found


def format_codepoints(codepoints: set[int]) -> str:
    return ", ".join(f"U+{codepoint:04X}" for codepoint in sorted(codepoints))


def main() -> int:
    root = Path(".").resolve()
    flagged = 0
    scanned = 0
    for path in iter_target_files(root):
        scanned += 1
        has_bom, found = scan_file(path)
        if not has_bom and not found:
            continue
        flagged += 1
        bom_status = "yes" if has_bom else "no"
        codepoints = format_codepoints(found) if found else "none"
        print(f"{path.relative_to(root)} -> bom={bom_status}; codepoints: {codepoints}")
    if flagged == 0:
        print(f"No hidden unicode found in {scanned} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
