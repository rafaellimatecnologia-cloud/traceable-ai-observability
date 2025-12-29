from __future__ import annotations

from pathlib import Path

TARGET_EXTENSIONS = {".py", ".md", ".toml", ".yml", ".yaml", ".txt"}

REMOVE_CODEPOINTS = {
    "\ufeff",
    "\u200b",
    "\u200c",
    "\u200d",
    "\u2060",
    "\u200e",
    "\u200f",
    "\u061c",
    "\u202a",
    "\u202b",
    "\u202c",
    "\u202d",
    "\u202e",
    "\u2066",
    "\u2067",
    "\u2068",
    "\u2069",
    "\u2028",
    "\u2029",
}


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


def test_no_hidden_unicode() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    offenders: list[str] = []
    for path in iter_target_files(repo_root):
        text = path.read_text(encoding="utf-8", errors="surrogatepass")
        if any(char in text for char in REMOVE_CODEPOINTS):
            offenders.append(str(path.relative_to(repo_root)))
    assert offenders == [], f"Hidden unicode found in: {', '.join(offenders)}"
