"""The input error every entry point raises, and the text reader for files a
person hands the engine. A leaf module (standard library only), so a reader
of systems can raise the same error as the writer without loading it."""
from __future__ import annotations


class InputError(ValueError):
    """A bad input. The message names the input and the fix."""


def _brief_text(data: bytes) -> str:
    """The text of a brief file. UTF-8, with Notepad's leading mark
    dropped; a file that starts with the UTF-16 mark (Windows PowerShell 5.1
    writes one) is read as UTF-16. Raises UnicodeDecodeError otherwise."""
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16")
    return data.decode("utf-8-sig")
