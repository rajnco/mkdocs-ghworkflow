# MkDocs static SSI-like pattern

This project uses a static-site approach that mimics server-side include behavior without server code.

## Included patterns

- reusable header via the custom theme override in `overrides/main.html`
- page hit tracking stored in browser localStorage with `docs/javascripts/page_stats.js`
- no backend service required

## Notes

This is a static-only pattern. For real server-side persistence, use a hosted backend such as Azure Functions, Vercel, or another API service.

## Pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) to run Markdown checks before each commit. The hooks use
[markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) to check Markdown files and automatically fix
formatting issues where possible. If the linter finds an issue it cannot fix, the commit is stopped until the issue
is corrected.

### Enable the hooks

From the project root, install the development dependencies and register the Git hook:

```sh
uv sync --group dev
uv run pre-commit install
```

After setup, the hooks run automatically when you commit. To run them manually against all tracked files:

```sh
uv run pre-commit run --all-files
```

To run only the fixer or only the linter:

```sh
uv run pre-commit run markdownlint-cli2-fix --all-files
uv run pre-commit run markdownlint-cli2-lint --all-files
```

The Markdown lint rules are configured in `.markdownlint-cli2.yaml`; line length is not enforced so prose can wrap
naturally. To remove the Git hook later, run `uv run pre-commit uninstall`.
