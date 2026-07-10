#!/usr/bin/env python3

import re
import stat
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    print("error: validation requires Python 3.11 or newer", file=sys.stderr)
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
ROLE_ROOT = ROOT / "playbooks"
ALIAS_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
REQUIRED_RUNTIME_IGNORES = {
    ".claude.json",
    ".credentials.json",
    "backups/",
    "cache/",
    "history.jsonl",
    "plugins/",
    "projects/",
}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_manifest(directory: Path, expected_name: str) -> dict:
    manifest_path = directory / ".playbook"
    claude_path = directory / "CLAUDE.md"
    if not manifest_path.is_file():
        fail(f"missing manifest: {manifest_path.relative_to(ROOT)}")
    if not claude_path.is_file() or not claude_path.read_text().strip():
        fail(f"missing or empty CLAUDE.md: {claude_path.relative_to(ROOT)}")

    try:
        manifest = tomllib.loads(manifest_path.read_text())
    except tomllib.TOMLDecodeError as exc:
        fail(f"invalid TOML in {manifest_path.relative_to(ROOT)}: {exc}")

    for field in ("version", "name", "alias", "description"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            fail(f"{manifest_path.relative_to(ROOT)} has invalid {field!r}")
    if manifest["name"] != expected_name:
        fail(
            f"{manifest_path.relative_to(ROOT)} name is {manifest['name']!r}, "
            f"expected {expected_name!r}"
        )
    if not ALIAS_RE.fullmatch(manifest["alias"]):
        fail(f"{manifest_path.relative_to(ROOT)} has unsafe alias {manifest['alias']!r}")
    return manifest


def main() -> None:
    metadata_files = sorted(ROOT.rglob(".DS_Store"))
    if metadata_files:
        fail("macOS metadata found: " + ", ".join(str(path.relative_to(ROOT)) for path in metadata_files))

    ignore_lines = {
        line.strip()
        for line in (ROOT / ".gitignore").read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    missing_ignores = sorted(REQUIRED_RUNTIME_IGNORES - ignore_lines)
    if missing_ignores:
        fail("missing Claude runtime ignores: " + ", ".join(missing_ignores))

    root_manifest = load_manifest(ROOT, "awesome")
    source = root_manifest.get("source")
    if not isinstance(source, dict):
        fail("root manifest is missing [source] metadata")
    if source.get("repository") != "https://github.com/ramazanpolat/awesome-claude-playbooks":
        fail("root manifest has an unexpected source.repository")
    if source.get("update_script") != "bin/update-playbook.sh":
        fail("root manifest must delegate to bin/update-playbook.sh")

    manifests = [root_manifest]
    role_dirs = sorted(path for path in ROLE_ROOT.iterdir() if path.is_dir())
    if not role_dirs:
        fail("no role playbooks found")
    manifests.extend(load_manifest(path, path.name) for path in role_dirs)

    aliases = [manifest["alias"] for manifest in manifests]
    duplicates = sorted(alias for alias in set(aliases) if aliases.count(alias) > 1)
    if duplicates:
        fail("duplicate aliases: " + ", ".join(duplicates))

    updater = ROOT / "bin" / "update-playbook.sh"
    if not updater.is_file() or not updater.stat().st_mode & stat.S_IXUSR:
        fail("bin/update-playbook.sh is missing or not executable")

    print(f"validated {len(manifests)} playbooks and {len(aliases)} unique aliases")


if __name__ == "__main__":
    main()
