"""Regression tests for audit integrity and restricted API access."""
import pytest
from fastapi.testclient import TestClient
from agents.base import AuditTrail, AuditLogger
from agents.api import app


def test_chain_rejects_mutated_entry():
    ledger = AuditTrail(secret_key="test-only-random-signing-key")
    ledger.log("supervisor", "test", "TASK", {"id": "T01"})
    ledger.log("supervisor", "test", "TASK", {"id": "T02"})
    assert ledger.verify_integrity()
    ledger.logs[0]["actor"] = "forged"
    assert not ledger.verify_integrity()


def test_chain_rejects_recomputed_links_without_key():
    ledger = AuditTrail(secret_key="test-only-random-signing-key")
    ledger.log("supervisor", "test", "TASK", {"id": "T01"})
    ledger.logs[0]["current_hash"] = "0" * 64
    assert not ledger.verify_integrity()


def test_exposing_trail_does_not_mutate_ledger():
    ledger = AuditTrail(secret_key="test-only-random-signing-key")
    ledger.log("supervisor", "test", "TASK", {"id": "T01"})
    snapshot = ledger.get_trail()
    snapshot[0]["actor"] = "modified"
    assert ledger.verify_integrity()


def test_audit_logs_disabled_without_token(monkeypatch):
    monkeypatch.delenv("AUDIT_LOG_READ_TOKEN", raising=False)
    client = TestClient(app)
    response = client.get("/api/audit/logs")
    assert response.status_code == 503


def test_audit_logs_require_token(monkeypatch):
    monkeypatch.setenv("AUDIT_LOG_READ_TOKEN", "test-only-secret")
    client = TestClient(app)
    assert client.get("/api/audit/logs").status_code == 403
    assert client.get("/api/audit/logs", headers={"X-Audit-Token": "incorrect"}).status_code == 403
    response = client.get("/api/audit/logs", headers={"X-Audit-Token": "test-only-secret"})
    assert response.status_code == 200
    assert response.json()["verified"] is True


def test_phi_returns_client_error_without_echoing_value():
    response = TestClient(app).post("/api/audit", json={
        "task_id": "MRN-999999",
        "target_identifier": "T01",
        "primary_metric": 1.0
    })
    assert response.status_code == 400
    assert "999999" not in response.text
