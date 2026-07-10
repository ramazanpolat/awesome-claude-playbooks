#!/bin/sh
set -e

echo "Installing awesome root playbook..."
claude-playbook install ./ --name awesome --alias ap

echo "Installing individual playbooks..."
for pb in playbooks/*; do
  if [ -d "$pb" ] && [ -f "$pb/.playbook" ]; then
    # Extract alias from .playbook file
    alias_name=$(grep '^alias\s*=' "$pb/.playbook" | cut -d'"' -f2)
    name=$(basename "$pb")
    
    if [ -n "$alias_name" ]; then
      echo "Installing $name as $alias_name..."
      claude-playbook install ./ --subdir "$pb" --name "$alias_name" --alias "$alias_name"
    else
      echo "Skipping $name: no alias found in .playbook"
    fi
  fi
done

echo "Done! You can now use the aliases (e.g. ap, ap-dba, ap-sre, etc.)."
