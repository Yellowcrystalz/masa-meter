# MIT License
#
# Copyright (c) 2025 Justin Nguyen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Apply cahce-busting to frontend static assets.

This module provides functions to compute file hashes and modify HTML content
to include version query parameters, ensuring the browser loads the latest
CSS and JavaScript files instead of cached versions.
"""

import hashlib
from pathlib import Path
import re

from config import FRONTEND_DIR


def hash_file(file_path: str) -> str:
    """Compute an 8 character MD5 hash for a given file.

    Args:
        file_path: Path to the file to be hash.

    Returns:
        The first 8 chracters of the MD5 hash if the file exists; otherwise an
        empty string.
    """

    path: Path = Path(file_path)

    if not path.exists():
        return ""

    return hashlib.md5(path.read_bytes()).hexdigest()[:8]


def apply_cache_busting(html: str) -> str:
    """Apply cache-busting to static CSS and JavaScript files.

    This functions scans HTML content for tags referencing CSS and JS files in
    the static directory. Then computes the MD5 hash and appends to the file
    name and the HTML file. The CSS and JS files are queried using regular
    expressions.

    Args:
        html: The contents of a HTML file as a string.

    Returns:
        The modified HTML content with the hash cache-busting applied.
    """

    def replace(match):
        file_path: str = match.group(2)[len("/static/"):]
        hash: str = hash_file(FRONTEND_DIR / file_path)
        return f'{match.group(1)}="/static/{file_path}?v={hash}"'

    html: str = re.sub(r'(href|src)="([^"]+\.(css|js))"', replace, html)

    return html
