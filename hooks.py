import subprocess
from pathlib import Path


def on_page_markdown(markdown, page, config, files):
    page_path = page.file.src_path
    file_path = Path(config['docs_dir']) / page_path

    if not file_path.exists():
        return markdown

    try:
        log = subprocess.check_output(
            ['git', 'log', '--follow', '--date=short', '--pretty=format:%h | %ad | %an', '--', str(file_path)],
            cwd=config['site_dir'].parent if config.get('site_dir') else '.',
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return markdown

    history_lines = [line.strip() for line in log.splitlines() if line.strip()]
    if not history_lines:
        return markdown

    history_html = "\n".join(
        f"<li><code>{entry}</code></li>" for entry in history_lines[:5]
    )

    footer = f"""

## Page history

<ul>
{history_html}
</ul>
"""

    return markdown + footer
