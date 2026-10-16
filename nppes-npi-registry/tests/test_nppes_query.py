"""Mocked-HTTP tests for nppes_query. Run: python -m pytest nppes-npi-registry/tests"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import nppes_query as nq  # noqa: E402


class FakeResp:
    def __init__(self, payload, status=200):
        self._p, self.status_code = payload, status

    def json(self):
        return self._p


def rec(i):
    return {"number": str(1000 + i), "enumeration_type": "NPI-1",
            "basic": {"first_name": "A", "last_name": "B%d" % i},
            "addresses": [{"address_purpose": "LOCATION", "city": "X",
                           "state": "VT", "postal_code": "05401"}],
            "taxonomies": [{"code": "1223G0001X", "desc": "Dentist", "primary": True}]}


def install(monkeypatch, total, calls):
    def fake_get(url, params=None, timeout=None):
        calls.append(dict(params))
        skip, limit = params["skip"], params["limit"]
        n = max(0, min(limit, total - skip))
        return FakeResp({"result_count": n, "results": [rec(skip + i) for i in range(n)]})
    monkeypatch.setattr(nq.requests, "get", fake_get)
    monkeypatch.setattr(nq.time, "sleep", lambda s: None)


def test_pagination_collects_all(monkeypatch):
    calls = []
    install(monkeypatch, 450, calls)
    recs, capped = nq.run_query({"state": "VT"})
    assert len(recs) == 450 and not capped
    assert [c["skip"] for c in calls] == [0, 200, 400]
    assert all(c["limit"] == 200 for c in calls)


def test_ceiling_flagged(monkeypatch):
    calls = []
    install(monkeypatch, 5000, calls)
    recs, capped = nq.run_query({"state": "TX"})
    assert len(recs) == 1200 and capped
    assert max(c["skip"] for c in calls) == 1000


def test_limit_pages(monkeypatch):
    calls = []
    install(monkeypatch, 5000, calls)
    recs, capped = nq.run_query({"state": "TX"}, limit_pages=2)
    assert len(recs) == 400 and not capped


def test_count_only_warning(monkeypatch, capsys):
    install(monkeypatch, 5000, [])
    rc = nq.main(["--taxonomy", "Dentist", "--state", "TX,VT", "--count-only"])
    out = capsys.readouterr()
    assert rc == 0
    assert "TX,1200,yes" in out.out and "VT,1200,yes" in out.out
    assert "ceiling" in out.err


def test_entity_param(monkeypatch):
    calls = []
    install(monkeypatch, 5, calls)
    nq.main(["--taxonomy", "Dentist", "--state", "VT", "--entity", "org", "--count-only"])
    assert calls[0]["enumeration_type"] == "NPI-2"
    assert calls[0]["taxonomy_description"] == "Dentist"


def test_network_failure_exits_1(monkeypatch, capsys):
    def boom(*a, **k):
        raise nq.requests.ConnectionError("blocked")
    monkeypatch.setattr(nq.requests, "get", boom)
    monkeypatch.setattr(nq.time, "sleep", lambda s: None)
    rc = nq.main(["--taxonomy", "Dentist", "--state", "VT", "--count-only"])
    assert rc == 1
    assert "Error" in capsys.readouterr().err


def test_retry_on_429(monkeypatch):
    seq = [FakeResp({}, 429), FakeResp({"results": []})]
    monkeypatch.setattr(nq.requests, "get", lambda *a, **k: seq.pop(0))
    monkeypatch.setattr(nq.time, "sleep", lambda s: None)
    assert nq.fetch_page({"skip": 0}) == {"results": []}
