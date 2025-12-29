"""Sanitize hidden and bidirectional Unicode characters from text files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

TARGET_EXTENSIONS = {".py", ".md", ".toml", ".yml", ".yaml", ".txt"}

REMOVE_CODEPOINTS = {
    "\ufeff",  # BOM
    "\u200b",  # zero-width space
    "\u200c",  # zero-width non-joiner
    "\u200d",  # zero-width joiner
    "\u2060",  # word joiner
    "\u200e",  # left-to-right mark
    "\u200f",  # right-to-left mark
    "\u061c",  # arabic letter mark
    "\u202a",  # left-to-right embedding
    "\u202b",  # right-to-left embedding
    "\u202c",  # pop directional formatting
    "\u202d",  # left-to-right override
    "\u202e",  # right-to-left override
    "\u2066",  # left-to-right isolate
    "\u2067",  # right-to-left isolate
    "\u2068",  # first strong isolate
    "\u2069",  # pop directional isolate
    "\u2028",  # line separator
    "\u2029",  # paragraph separator
}


@dataclass
class SanitizationResult:
    path: Path
    removed_count: int
    rewritten: bool


def sanitize_text(text: str) -> tuple[str, int]:
    removed = 0
    for char in REMOVE_CODEPOINTS:
        count = text.count(char)
        if count:
            removed += count
            text = text.replace(char, "")
    return text, removed


def sanitize_file(path: Path) -> SanitizationResult:
    raw = path.read_text(encoding="utf-8", errors="surrogatepass")
    sanitized, removed = sanitize_text(raw)
    rewritten = False
    if sanitized != raw:
        path.write_text(sanitized, encoding="utf-8", newline="\n")
        rewritten = True
    return SanitizationResult(path=path, removed_count=removed, rewritten=rewritten)


def iter_target_files(root: Path) -> list[Path]:
    paths = []
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if ".git" in path.parts:
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
