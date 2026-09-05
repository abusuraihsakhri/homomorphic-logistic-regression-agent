"""
Pydantic v2 schemas and data definitions for Homomorphic Logistic Regression Agent.
Domain: Post-Quantum Cryptography & Hardware Security
Standard: NIST FIPS 203/204/205 / ISO/IEC 17825 Standards
"""
import datetime
import math
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator


class UrgencyLevel(str, Enum):
    ROUTINE = "ROUTINE"
    ELEVATED = "ELEVATED_RISK"
    CRITICAL_STAT = "CRITICAL_STAT_PANIC"


class SystemIntegrityStatus(str, Enum):
    VALIDATED = "VALIDATED_OPTIMAL"
    DISCORDANT = "DISCORDANT_ANOMALY"
    RECALIBRATION_REQUIRED = "RECALIBRATION_REQUIRED"


def _validate_finite_float(value: float, field_name: str) -> float:
    """Ensure metric values are finite (not NaN or infinity)."""
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"{field_name} must be a finite number, got {value}")
    return value


def _validate_non_empty_str(value: str, field_name: str) -> str:
    """Ensure string identifiers are non-empty after stripping."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


class SystemTaskPayload(BaseModel):
    task_id: str = Field(..., description="Unique task / case identifier", max_length=256)
    target_identifier: str = Field(..., description="Entity, patient key, or genomic/cryptographic target", max_length=256)
    primary_metric: float = Field(..., description="Primary domain measurement or score")
    secondary_metric: float = Field(default=0.0, description="Secondary kinetic or confidence score")
    status_descriptor: str = Field(default="NOMINAL", description="Status code or phenotype descriptor", max_length=128)
    is_critical_flag: bool = Field(default=False, description="Emergency escalation or high priority trigger")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Metadata key-value pairs")
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    @field_validator("primary_metric")
    @classmethod
    def validate_primary_metric(cls, v):
        return _validate_finite_float(v, "primary_metric")

    @field_validator("secondary_metric")
    @classmethod
    def validate_secondary_metric(cls, v):
        return _validate_finite_float(v, "secondary_metric")

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v):
        return _validate_non_empty_str(v, "task_id")

    @field_validator("target_identifier")
    @classmethod
    def validate_target_identifier(cls, v):
        return _validate_non_empty_str(v, "target_identifier")


class AgentAlert(BaseModel):
    alert_id: str
    origin_worker: str
    urgency: UrgencyLevel
    summary: str
    technical_details: str
    actionable_remediation: str
    standard_reference: str = "NIST FIPS 203/204/205 / ISO/IEC 17825 Standards"
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class ConsensusDossier(BaseModel):
    dossier_id: str
    system_slug: str = "homomorphic-logistic-regression-agent"
    domain: str = "Post-Quantum Cryptography & Hardware Security"
    task_id: str
    target_identifier: str
    overall_urgency: UrgencyLevel
    integrity_status: SystemIntegrityStatus
    total_alerts: int
    critical_alerts_count: int
    alerts: List[AgentAlert]
    standard_reference: str = "NIST FIPS 203/204/205 / ISO/IEC 17825 Standards"
    consensus_summary: str
    audit_hash: str
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
