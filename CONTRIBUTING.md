# Contributing

Thanks for your interest in improving this project.

## Development setup

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format --check .
pyright
pytest -q
```

## Pull requests

- Keep changes focused and small.
- Add or update tests for behavior changes.
- Update documentation when user-facing behavior changes.
