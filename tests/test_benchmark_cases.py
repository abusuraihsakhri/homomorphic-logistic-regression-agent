"""Behavioral checks against the repository's illustrative benchmark cases."""
import json
from pathlib import Path
import pytest
from agents.base import PHIGuard, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor

BENCHMARK = json.loads((Path(__file__).parents[1] / "benchmark_dataset.json").read_text(encoding="utf-8"))

@pytest.mark.parametrize("case", BENCHMARK["test_cases"][:3], ids=lambda case: case["case_id"])
def test_example_benchmark_cases(case):
    payload = SystemTaskPayload(**case["payload"])
    dossier = SystemSupervisor().process_task(payload)
    assert dossier.overall_urgency.value == case["expected_urgency"]
    assert dossier.integrity_status.value == case["expected_integrity"]

def test_example_phi_pattern_is_rejected():
    case = BENCHMARK["test_cases"][3]
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi(case["adversarial_prompt"])
