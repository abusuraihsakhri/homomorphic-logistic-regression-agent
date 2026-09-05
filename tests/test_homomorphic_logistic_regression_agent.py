"""
Automated Pytest Test Suite for Homomorphic Logistic Regression Agent.
Domain: Post-Quantum Cryptography & Hardware Security
Standard: NIST FIPS 203/204/205 / ISO/IEC 17825 Standards
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import PHIGuard, AuditLogger, SecurityException
from agents.models import SystemTaskPayload, UrgencyLevel, SystemIntegrityStatus
from agents.workers import InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker
from agents.supervisor import SystemSupervisor
from cli import main


def test_phi_guard_enforcement():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient MRN-994827 blood culture positive for Staphylococcus")

    # Clean text passes
    PHIGuard.assert_no_phi("Analytical assay specimen KEY-001 optimal")


def test_phi_guard_redaction():
    redacted = PHIGuard.redact_phi("Contact patient at 555-123-4567 for results")
    assert "555-123-4567" not in redacted
    assert "[REDACTED_IDENTIFIER]" in redacted


def test_specialized_workers():
    # Worker 1: QC Invariant
    p1 = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=35.0)
    alerts1 = InvariantQCWorker.evaluate(p1)
    assert len(alerts1) == 1
    assert alerts1[0].urgency == UrgencyLevel.ELEVATED

    # Worker 2: Safety
    p2 = SystemTaskPayload(task_id="T2", target_identifier="KEY-02", primary_metric=10.0, is_critical_flag=True)
    alerts2 = SafetyEscalationWorker.evaluate(p2)
    assert len(alerts2) == 1
    assert alerts2[0].urgency == UrgencyLevel.CRITICAL_STAT

    # Worker 3: Protocol Conformance
    p3 = SystemTaskPayload(task_id="T3", target_identifier="KEY-03", primary_metric=10.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = ProtocolConformanceWorker.evaluate(p3)
    assert len(alerts3) == 1


def test_supervisor_consensus_and_audit():
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="TASK-PROD-01",
        target_identifier="KEY-PROD-01",
        primary_metric=12.0,
        secondary_metric=4.0,
        status_descriptor="NOMINAL"
    )
    dossier = supervisor.process_task(payload)
    assert dossier.overall_urgency == UrgencyLevel.ROUTINE
    assert dossier.integrity_status == SystemIntegrityStatus.VALIDATED
    assert dossier.audit_hash != ""

    # Verify cryptographic audit trail
    assert AuditLogger.verify_integrity() is True

    # CLI tests
    assert main(["audit", "--task-id", "CLI-TEST-01"]) == 0
    assert main(["chat", "Explain", "specifications"]) == 0
    assert main(["verify-audit"]) == 0


def test_input_validation_rejects_nan():
    """NaN metric values should be rejected."""
    with pytest.raises(ValueError, match="primary_metric must be a finite number"):
        SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=float("nan"))


def test_input_validation_rejects_infinity():
    """Infinity metric values should be rejected."""
    with pytest.raises(ValueError, match="primary_metric must be a finite number"):
        SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=float("inf"))


def test_input_validation_rejects_negative_infinity():
    """Negative infinity metric values should be rejected."""
    with pytest.raises(ValueError, match="secondary_metric must be a finite number"):
        SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=10.0, secondary_metric=float("-inf"))


def test_input_validation_rejects_empty_strings():
    """Empty string identifiers should be rejected."""
    with pytest.raises(ValueError, match="task_id must be a non-empty string"):
        SystemTaskPayload(task_id="", target_identifier="KEY-01", primary_metric=10.0)

    with pytest.raises(ValueError, match="target_identifier must be a non-empty string"):
        SystemTaskPayload(task_id="T1", target_identifier="   ", primary_metric=10.0)


def test_batch_cli_handles_missing_file():
    """CLI batch command should handle missing input file gracefully."""
    exit_code = main(["batch", "-i", "nonexistent_file.csv", "-o", "out.csv"])
    assert exit_code == 1


def test_batch_cli_processes_valid_csv():
    """CLI batch command should process valid CSV and produce output."""
    import tempfile
    import os
    csv_content = "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\nTASK-B1,TARGET-B1,28.4,14.2,True,DISCORDANT\nTASK-B2,TARGET-B2,12.0,4.1,False,NOMINAL\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
        f.write(csv_content)
        tmp_path = f.name
    try:
        exit_code = main(["batch", "-i", tmp_path, "-o", "test_output.csv"])
        assert exit_code == 0
        assert os.path.exists("test_output.csv")
        os.remove("test_output.csv")
    finally:
        os.unlink(tmp_path)
