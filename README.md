# MkDocs static SSI-like pattern

This project uses a static-site approach that mimics server-side include behavior without server code.

## Included patterns

- reusable header via the custom theme override in `overrides/main.html`
- page hit tracking stored in browser localStorage with `docs/javascripts/page_stats.js`
- no backend service required

## Notes

This is a static-only pattern. For real server-side persistence, use a hosted backend such as Azure Functions, Vercel, or another API service.
