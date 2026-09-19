import subprocess
from pathlib import Path


def on_page_markdown(markdown, page, config, files):
    page_path = page.file.src_path
    file_path = Path(config['docs_dir']) / page_path

    if not file_path.exists():
        return markdown

    try:
        log = subprocess.check_output(
            ['git', 'log', '--follow', '--date=short', '--pretty=format:%h|%ad|%an', '--', str(file_path)],
            cwd=config['site_dir'].parent if config.get('site_dir') else '.',
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return markdown

    rows = []
    for line in log.splitlines():
        entry = line.strip()
        if not entry:
            continue
        commit, date, author = [part.strip() for part in entry.split('|', 2)]
        rows.append(f"| `{commit}` | {date} | {author} |")

    if not rows:
        return markdown

    table = """

## Page history

| Commit | Date | Author |
| --- | --- | --- |
{rows}
""".format(rows="\n".join(rows[:5]))

    return markdown + table
