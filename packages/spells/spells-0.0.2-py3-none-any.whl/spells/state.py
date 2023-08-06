from __future__ import annotations

import pathlib
import hashlib

def get_state() -> dict:
    files = {}

    for file in pathlib.Path(".").rglob("*"):

        if pathlib.Path.is_file(file):
            md5 = hashlib.md5()

            with open(file, "rb") as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    md5.update(data)

            files[file.absolute()] = md5.hexdigest()

    return files
