import subprocess
from html import escape
from pathlib import Path


def on_page_markdown(markdown, page, config, files):
    repo_root = Path(__file__).resolve().parent
    page_path = page.file.src_path
    file_path = repo_root / config['docs_dir'] / page_path

    if not file_path.exists():
        return markdown

    try:
        log = subprocess.check_output(
            ['git', 'log', '--follow', '--date=format:%Y-%m-%d %H:%M', '--pretty=format:%h|%ad|%an|%s', '--', str(file_path.relative_to(repo_root))],
            cwd=str(repo_root),
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except Exception:
        return markdown

    commits = []
    for line in log.splitlines():
        entry = line.strip()
        if not entry:
            continue
        parts = [part.strip() for part in entry.split('|', 3)]
        if len(parts) != 4:
            continue
        commit, date, author, summary = parts
        commits.append((commit[:4], date, author, summary))

    if not commits:
        return markdown

    rows = [
        f"| `{commit}` | {date} | {author} | {summary.replace('|', '\\|')} |"
        for commit, date, author, summary in commits[:5]
    ]
    latest_commit, latest_date, latest_author, latest_summary = commits[0]
    history_rows = "\n".join(
        "<tr>"
        f"<td><code>{escape(commit)}</code></td>"
        f"<td>{escape(date)}</td>"
        f"<td>{escape(author)}</td>"
        f"<td>{escape(summary)}</td>"
        "</tr>"
        for commit, date, author, summary in commits
    )

    table = """

## Page history

| Commit | Date & time | Author | Summary |
| --- | --- | --- | --- |
{rows}

<details class="page-history-details">
<summary>+ Latest commit: <code>{latest_commit}</code> | {latest_date} | {latest_author} | {latest_summary}</summary>

<table>
<thead>
<tr><th>Commit</th><th>Date &amp; time</th><th>Author</th><th>Summary</th></tr>
</thead>
<tbody>
{history_rows}
</tbody>
</table>
</details>
""".format(
        rows="\n".join(rows),
        latest_commit=escape(latest_commit),
        latest_date=escape(latest_date),
        latest_author=escape(latest_author),
        latest_summary=escape(latest_summary),
        history_rows=history_rows,
    )

    return markdown + table
