from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import sys

from src.audio.downloader import save_mp3_from_url


class _StubYDL:
    def __init__(self, opts):
        self.opts = opts

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    # Simulate yt_dlp download by creating an mp3 file matching outtmpl
    def download(self, urls):
        outtmpl = self.opts.get("outtmpl")
        # Derive path: if outtmpl contains %(ext)s, replace with mp3
        if "%(ext)s" in outtmpl:
            out_path = outtmpl.replace("%(ext)s", "mp3")
        else:
            out_path = outtmpl
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        Path(out_path).write_bytes(b"fake-mp3")


def test_save_mp3_from_url_with_filename(tmp_path, monkeypatch):
    # Patch yt_dlp module with stub
    module_stub = SimpleNamespace(YoutubeDL=_StubYDL)
    monkeypatch.setitem(sys.modules, "yt_dlp", module_stub)

    out = save_mp3_from_url("https://www.youtube.com/shorts/pNOrDC8NyEo", out_dir=tmp_path, filename="clip")
    assert out == tmp_path / "clip.mp3"
    assert out.exists()


def test_save_mp3_from_url_autoname(tmp_path, monkeypatch):
    module_stub = SimpleNamespace(YoutubeDL=_StubYDL)
    monkeypatch.setitem(sys.modules, "yt_dlp", module_stub)

    out = save_mp3_from_url("https://www.youtube.com/shorts/pNOrDC8NyEo", out_dir=tmp_path)
    # Autoname path is most recent .mp3 created by stub
    assert out.suffix == ".mp3"
    assert out.exists()
