## What & why

<!-- What does this change and why? Link any issue. -->

## Checklist

- [ ] If I edited `.agents/`, I ran `bash scripts/sync-skill.sh` and committed the result
- [ ] `python3 scripts/validate_manifests.py` and `python3 scripts/validate_commands.py` pass
- [ ] `python3 plugins/obsidian-knowledge/scripts/validate_links.py examples/output` passes
- [ ] Shell scripts parse (`bash -n`)
- [ ] Docs/CHANGELOG updated if behavior changed
- [ ] **If this changes a validator, hook, or the installer:** `python3 scripts/test_validators.py` and `bash scripts/test_hooks.sh` pass, and I followed the review checklist in [CONTRIBUTING.md](../CONTRIBUTING.md)
