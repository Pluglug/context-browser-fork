# Development

This repository maintains Context Browser as a small Blender developer tool.

## Public Project Rules

- Public documentation, commit messages, issues, and pull requests must be written in English.
- Preserve the original behavior unless a task explicitly changes it.
- Keep changes scoped to the affected feature or maintenance boundary.
- Do not run broad formatters over the imported source unless that is the explicit task.

## Blender Support Policy

- Main validation target: Blender 4.5 LTS.
- Latest stable Blender support matters and should be checked for user-facing changes.
- Next LTS releases should be evaluated early. When Blender 5.2 LTS becomes available, add it to the validation target set.
- Blender 2.80+ compatibility is best-effort unless explicitly tested.
- Blender 2.79 and older are out of scope.

The development stubs are pinned to `fake-bpy-module-4.5` for reproducibility. Newer Blender compatibility should be validated with a real Blender build until matching stubs are available.

## Code Style

- Keep the existing imported source style unless a focused cleanup is being reviewed.
- Prefer clear local names for new code.
- Comments and docstrings should be useful and concise.
- Avoid introducing Python syntax that breaks Blender 2.80-era Python parsing unless the compatibility policy is changed first.

Blender lifecycle surfaces need extra care:

- `bpy` registration and unregistration
- handlers and timers
- modal operators
- keymaps
- `PropertyGroup` definitions
- add-on preferences and persistence

## Development Setup

Install development dependencies with:

```powershell
uv sync --extra dev
```

Run the lightweight checks with:

```powershell
uv run ruff check .
uv run pyright
uv run python tools/check_python_syntax.py
```

The syntax check currently parses `src/context_browser` with Python 3.7 grammar as a best-effort guard for Blender 2.80+ compatibility. This does not guarantee Blender API compatibility.

## Blender Validation

For user-facing or Blender lifecycle changes, validate in Blender when possible:

- Enable the add-on with no registration errors.
- Open the add-on preferences.
- Open Context Browser from the header button or operator search.
- Browse context and data paths.
- Verify relevant clipboard or editing behavior for the changed feature.

When Blender cannot be run, state that clearly and include the static checks that were run.
