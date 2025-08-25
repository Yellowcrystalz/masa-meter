import hashlib
from pathlib import Path
import re

from config import FRONTEND_DIR


def hash_file(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        return ""

    return hashlib.md5(path.read_bytes()).hexdigest()[:8]


def apply_cache_busting(html: str) -> str:

    def replace(match):
        file_path = match.group(2)[len("/static/"):]
        hash = hash_file(FRONTEND_DIR / file_path)
        return f'{match.group(1)}="/static/{file_path}?v={hash}"'

    html = re.sub(r'(href|src)="([^"]+\.(css|js))"', replace, html)

    return html
