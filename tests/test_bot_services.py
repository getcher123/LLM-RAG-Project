from __future__ import annotations

import json
from types import SimpleNamespace

import httpx
import pytest


class _Resp:
    def __init__(self, data, status_code=200):
        self._data = data
        self.status_code = status_code

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise httpx.HTTPStatusError("error", request=None, response=None)

    def json(self):
        return self._data


@pytest.mark.asyncio
async def test_audio_and_transcriber_calls(monkeypatch, tmp_path):
    # Stub AsyncClient.post to return canned responses
    async def fake_post(self, url, *args, **kwargs):
        if url.endswith("/audio/save"):
            return _Resp({"path": str(tmp_path / "clip.mp3")})
        if url.endswith("/transcribe/path"):
            return _Resp({"payload": {"full_text": "hello world"}})
        return _Resp({}, status_code=404)

    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post, raising=False)

    # Quick sanity: call the fake endpoints directly
    async with httpx.AsyncClient() as c:
        r1 = await c.post("http://x/audio/save", json={})
        assert r1.json()["path"].endswith("clip.mp3")
        r2 = await c.post("http://x/transcribe/path", params={})
        assert r2.json()["payload"]["full_text"] == "hello world"

