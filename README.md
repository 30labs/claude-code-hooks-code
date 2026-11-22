# Hooks in Python for Claude Code: code

This repository contains the complete hooks, helper modules and tests from the book, in the state its last chapter leaves them. Run `uv sync` and then `uv run pytest` to run the test suite. To install the hooks in a project, copy `.claude/hooks/` and merge `.claude/settings.json` into that project’s settings.

The code is released under the MIT License (see `LICENSE`).

Claude and Claude Code are trademarks of Anthropic, PBC. This code is independent and is not affiliated with, endorsed by, or sponsored by Anthropic.

## Files by chapter

- `.claude/hooks/after_edit.py` — chapter 5.
- `.claude/hooks/after_edit_tools.py` — chapter 5.
- `.claude/hooks/audit.py` — chapter 8.
- `.claude/hooks/audit_capture.py` — chapter 8.
- `.claude/hooks/audit_text.py` — chapter 8.
- `.claude/hooks/branch.py` — chapter 2.
- `.claude/hooks/files.py` — chapter 4.
- `.claude/hooks/files_rules.py` — chapter 4.
- `.claude/hooks/guard.py` — chapter 3.
- `.claude/hooks/guard_rm.py` — chapter 3.
- `.claude/hooks/guard_shell.py` — chapter 3.
- `.claude/hooks/hookkit.py` — chapter 2.
- `.claude/hooks/prompt_guard.py` — chapter 6.
- `.claude/hooks/rm_guard.py` — chapter 10.
- `.claude/hooks/start.py` — chapter 6.
- `.claude/hooks/start_report.py` — chapter 6.
- `.claude/hooks/stop_check.py` — chapter 7.
- `.claude/hooks/stop_check_tools.py` — chapter 7.
- `.claude/settings.json` — chapter 11.
- `checks/test_python.py` — chapter 11.
- `.python-version` — chapter 11.
- `pyproject.toml` — chapters 5 and 9.
- `scripts/hook_gate.py` — chapter 10.
- `scripts/hook_gate_stream.py` — chapter 10.
- `scripts/report.py` — chapter 8.
- `scripts/report_sections.py` — chapter 8.
- `scripts/settings.py` — chapter 11.
- `scripts/settings_build.py` — chapter 11.
- `scripts/settings_show.py` — chapter 11.
- `scripts/usage.py` — chapter 8.
- `scripts/usage_table.py` — chapter 8.
- `tests/hooks/hooktest.py` — chapter 9.
- `tests/hooks/hooktest_cases.py` — chapter 9.
- `tests/hooks/hooktest_events.py` — chapter 9.
- `tests/hooks/hooktest_result.py` — chapter 9.
- `tests/hooks/hooktest_settings.py` — chapter 9.
- `tests/hooks/test_files.py` — chapter 9.
- `tests/hooks/test_guard.py` — chapter 9.
- `tests/hooks/test_recorded.py` — chapter 9.
- `tests/hooks/test_settings.py` — chapter 9.
- `tests/hooks/events/guard/allow-status.json` — chapter 9.
- `tests/hooks/events/guard/block-reset.json` — chapter 9.
- `.gitignore` — chapter 11.
- `pyproject.toml` — chapters 5 and 9.
