"""
Data Models & Telemetry Definitions for HE-LogisticReg: Encrypted Gradient Descent & Clinical Risk Scorer Agent.
Domain: Privacy-Preserving Federated Healthcare & FHE
Standard: Homomorphic Machine Learning Standards
"""
import datetime
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class ExecutionStatus(str, Enum):
    NOMINAL = "NOMINAL_OPTIMAL"
    ELEVATED_RISK = "ELEVATED_RISK_WARNING"
    CRITICAL_INTERVENTION = "CRITICAL_INTERVENTION_REQUIRED"


def _validate_frontier_payload(task_id, target_identifier, primary_metric, secondary_metric, status_descriptor):
    """Validate FrontierPayload fields at construction time."""
    if not task_id or not str(task_id).strip():
        raise ValueError("task_id must be a non-empty string")
    if not target_identifier or not str(target_identifier).strip():
        raise ValueError("target_identifier must be a non-empty string")
    if math.isnan(primary_metric) or math.isinf(primary_metric):
        raise ValueError(f"primary_metric must be a finite number, got {primary_metric}")
    if math.isnan(secondary_metric) or math.isinf(secondary_metric):
        raise ValueError(f"secondary_metric must be a finite number, got {secondary_metric}")
    if not status_descriptor or not str(status_descriptor).strip():
        raise ValueError("status_descriptor must be a non-empty string")


@dataclass
class FrontierPayload:
    task_id: str
    target_identifier: str
    primary_metric: float
    secondary_metric: float
    status_descriptor: str
    is_critical_flag: bool = False
    attributes: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def __post_init__(self):
        _validate_frontier_payload(
            self.task_id, self.target_identifier,
            self.primary_metric, self.secondary_metric,
            self.status_descriptor,
        )


@dataclass
class AgentTelemetryAlert:
    alert_id: str
    origin_agent: str
    status: ExecutionStatus
    summary: str
    technical_details: str
    actionable_remediation: str
    standard_reference: str = "Homomorphic Machine Learning Standards"
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "origin_agent": self.origin_agent,
            "status": self.status.value,
            "summary": self.summary,
            "technical_details": self.technical_details,
            "actionable_remediation": self.actionable_remediation,
            "standard_reference": self.standard_reference,
            "timestamp": self.timestamp,
        }
