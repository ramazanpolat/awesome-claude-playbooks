#!/bin/sh
# Update script for the awesome-claude-playbooks router.
#
# Invoked by `claude-playbook update awesome` with:
#   - working directory: this top-level playbook's root
#   - CLAUDE_CONFIG_DIR set to the same path
#   - any extra CLI args forwarded as "$@"
#
# Strategy: this playbook is git-backed, so a fast-forward pull is enough.
set -e
cd "$(dirname "$0")/.."
git pull --ff-only
