import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from he_logistic_reg.models import FrontierPayload, ExecutionStatus
from he_logistic_reg.engine import FrontierDomainEngine
from he_logistic_reg.agents import TaylorSigmoidApproximatorAgent, EncryptedWeightUpdaterAgent, ROCConvergenceTrackerAgent, HELogisticRegCoordinator
from he_logistic_reg.cli import main


def test_sub_agents():
    a1 = TaylorSigmoidApproximatorAgent()
    p1 = FrontierPayload("T1", "KEY-01", primary_metric=35.0, secondary_metric=4.0, status_descriptor="NOMINAL")
    alerts1 = a1.audit(p1)
    assert len(alerts1) == 1
    assert alerts1[0].status == ExecutionStatus.ELEVATED_RISK

    a2 = EncryptedWeightUpdaterAgent()
    p2 = FrontierPayload("T2", "KEY-02", primary_metric=10.0, secondary_metric=15.0, status_descriptor="NOMINAL", is_critical_flag=True)
    alerts2 = a2.audit(p2)
    assert len(alerts2) == 1
    assert alerts2[0].status == ExecutionStatus.CRITICAL_INTERVENTION

    a3 = ROCConvergenceTrackerAgent()
    p3 = FrontierPayload("T3", "KEY-03", primary_metric=10.0, secondary_metric=4.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = a3.audit(p3)
    assert len(alerts3) == 1


def test_coordinator():
    coord = HELogisticRegCoordinator()
    p_nominal = FrontierPayload("T4", "KEY-04", primary_metric=12.0, secondary_metric=4.0, status_descriptor="NOMINAL")
    dossier = coord.process(p_nominal)
    assert dossier["overall_status"] == ExecutionStatus.NOMINAL.value
    assert dossier["total_alerts"] == 0

    ans = coord.query_supervisory_chat("What standard is applied?")
    assert "Homomorphic Machine Learning Standards" in ans or "specifications" in ans


def test_cli():
    assert main(["audit", "--task-id", "CLI-01"]) == 0
    assert main(["chat", "What", "is", "the", "system", "status?"]) == 0


def test_frontier_payload_rejects_nan():
    """NaN metric values should be rejected."""
    with pytest.raises(ValueError, match="primary_metric must be a finite number"):
        FrontierPayload("T1", "KEY-01", primary_metric=float("nan"), secondary_metric=4.0, status_descriptor="NOMINAL")


def test_frontier_payload_rejects_infinity():
    """Infinity metric values should be rejected."""
    with pytest.raises(ValueError, match="secondary_metric must be a finite number"):
        FrontierPayload("T1", "KEY-01", primary_metric=10.0, secondary_metric=float("inf"), status_descriptor="NOMINAL")


def test_frontier_payload_rejects_empty_strings():
    """Empty string identifiers should be rejected."""
    with pytest.raises(ValueError, match="task_id must be a non-empty string"):
        FrontierPayload("", "KEY-01", primary_metric=10.0, secondary_metric=4.0, status_descriptor="NOMINAL")

    with pytest.raises(ValueError, match="target_identifier must be a non-empty string"):
        FrontierPayload("T1", "", primary_metric=10.0, secondary_metric=4.0, status_descriptor="NOMINAL")


def test_frontier_payload_rejects_empty_status():
    """Empty status descriptor should be rejected."""
    with pytest.raises(ValueError, match="status_descriptor must be a non-empty string"):
        FrontierPayload("T1", "KEY-01", primary_metric=10.0, secondary_metric=4.0, status_descriptor="   ")
