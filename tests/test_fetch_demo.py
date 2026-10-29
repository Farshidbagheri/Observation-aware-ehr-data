"""Offline tests for resilient, checksum-gated PhysioNet acquisition."""
from io import BytesIO
from pathlib import Path
import urllib.error

import pytest

from scripts.fetch_demo import _download_atomic


def test_download_recovers_from_transient_http_502(tmp_path, monkeypatch):
    target = tmp_path / "public.csv.gz"
    state = {"calls": 0}

    def fake_open(request, timeout):
        state["calls"] += 1
        if state["calls"] == 1:
            raise urllib.error.HTTPError(request.full_url, 502, "Bad Gateway", {}, None)
        return BytesIO(b"verified bytes")

    monkeypatch.setattr("scripts.fetch_demo.urllib.request.urlopen", fake_open)
    monkeypatch.setattr("scripts.fetch_demo.time.sleep", lambda delay: None)
    _download_atomic("https://physionet.org/files/test", target, attempts=3)
    assert state["calls"] == 2
    assert target.read_bytes() == b"verified bytes"
    assert not (tmp_path / "public.csv.gz.part").exists()


def test_download_does_not_retry_http_404_or_leave_partial(tmp_path, monkeypatch):
    target = tmp_path / "absent.csv.gz"

    def fake_open(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 404, "Not Found", {}, None)

    monkeypatch.setattr("scripts.fetch_demo.urllib.request.urlopen", fake_open)
    with pytest.raises(urllib.error.HTTPError):
        _download_atomic("https://physionet.org/files/absent", target)
    assert not target.exists()
    assert not (tmp_path / "absent.csv.gz.part").exists()


def test_download_rejects_empty_response(tmp_path, monkeypatch):
    target = tmp_path / "empty.csv.gz"
    monkeypatch.setattr("scripts.fetch_demo.urllib.request.urlopen",
                        lambda request, timeout: BytesIO(b""))
    monkeypatch.setattr("scripts.fetch_demo.time.sleep", lambda delay: None)
    with pytest.raises(OSError):
        _download_atomic("https://physionet.org/files/empty", target, attempts=2)
    assert not target.exists()
    assert not (tmp_path / "empty.csv.gz.part").exists()
