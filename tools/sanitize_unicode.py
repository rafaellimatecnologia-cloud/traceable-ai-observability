"""Sanitize hidden and bidirectional Unicode characters from text files."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
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


@dataclass(frozen=True)
class SanitizationResult:
    path: Path
    bom_removed: bool
    codepoints_removed: set[int]
    removed_count: int
    rewritten: bool


def find_hidden_unicode(data: bytes) -> tuple[bool, set[int], str]:
    has_bom = data.startswith(BOM_BYTES)
    if has_bom:
        data = data[len(BOM_BYTES) :]
    text = data.decode("utf-8", errors="strict")
    found = {ord(char) for char in text if ord(char) in REMOVE_CODEPOINTS}
    return has_bom, found, text


def strip_hidden(text: str) -> tuple[str, int]:
    removed = 0
    chars = []
    for char in text:
        if ord(char) in REMOVE_CODEPOINTS:
            removed += 1
        else:
            chars.append(char)
    return "".join(chars), removed


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sanitize_file(path: Path) -> SanitizationResult:
    raw_bytes = path.read_bytes()
    has_bom, found, raw_text = find_hidden_unicode(raw_bytes)
    normalized = normalize_newlines(raw_text)
    sanitized, removed = strip_hidden(normalized)

    rewritten = False
    removed_count = removed + (1 if has_bom else 0)
    if has_bom or found or sanitized != raw_text:
        path.write_text(sanitized, encoding="utf-8", newline="\n")
        rewritten = True

    return SanitizationResult(
        path=path,
        bom_removed=has_bom,
        codepoints_removed=found,
        removed_count=removed_count,
        rewritten=rewritten,
    )


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


def main() -> int:
    root = Path(".").resolve()
    results = [sanitize_file(path) for path in iter_target_files(root)]
    removed_total = sum(result.removed_count for result in results)
    rewritten_total = sum(1 for result in results if result.rewritten)
    print(f"Sanitized {rewritten_total} files, removed {removed_total} characters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
