"use strict";
// Local-only mirror of the three deterministic rules in agents/workers.py.
// These operations do not perform encryption, training, inference, or clinical scoring.
function evaluateRules(p) {
  if (!p || typeof p.task_id !== "string" || !p.task_id.trim() ||
      typeof p.target_identifier !== "string" || !p.target_identifier.trim() ||
      typeof p.status_descriptor !== "string" || !p.status_descriptor.trim() ||
      !Number.isFinite(p.primary_metric) || !Number.isFinite(p.secondary_metric)) {
    throw new Error("Non-empty identifiers and finite numeric metrics are required.");
  }
  const alerts = [];
  const add = (origin_worker, urgency, summary) => alerts.push({ origin_worker, urgency, summary });
  if (p.primary_metric > 25) add("InvariantQCWorker", "ELEVATED_RISK", "Primary value exceeds illustrative threshold 25.");
  if (p.is_critical_flag || p.secondary_metric > 12)
    add("SafetyEscalationWorker", p.is_critical_flag ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK", "Critical flag or secondary value exceeds illustrative threshold 12.");
  if (["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"].some(term => p.status_descriptor.toUpperCase().includes(term)))
    add("ProtocolConformanceWorker", "ELEVATED_RISK", "Status descriptor contains an anomaly marker.");
  const critical = alerts.filter(a => a.urgency === "CRITICAL_STAT_PANIC").length;
  return {
    evaluation_type: "UNSIGNED_BROWSER_RULES_DEMO",
    encryption: "NONE",
    task_id: p.task_id.trim(),
    target_identifier: p.target_identifier.trim(),
    overall_urgency: critical ? "CRITICAL_STAT_PANIC" : alerts.length ? "ELEVATED_RISK" : "ROUTINE",
    integrity_status: critical ? "RECALIBRATION_REQUIRED" : alerts.length ? "DISCORDANT_ANOMALY" : "VALIDATED_OPTIMAL",
    total_alerts: alerts.length,
    critical_alerts_count: critical,
    alerts: alerts,
    note: "Illustrative non-clinical rules. No homomorphic encryption, trained model or HMAC signature."
  };
}
if (typeof module !== "undefined" && module.exports) module.exports = { evaluateRules };
if (typeof document !== "undefined") {
  const el = id => document.getElementById(id);
  const form = el("audit-form"), output = el("output"), message = el("message"), dl = el("download");
  let result = null, count = 0;
  function modeChanged() {
    const api = el("mode").value === "api";
    el("m-mode").textContent = api ? "Python API" : "Local demo";
    el("mode-help").textContent = api ? "Requires a Python service at this origin. Connection failures are displayed, never simulated." : "Illustrative rules run entirely in the browser without encryption or HMAC.";
  }
  el("mode").addEventListener("change", modeChanged);
  form.addEventListener("submit", async event => {
    event.preventDefault();
    result = null; dl.disabled = true; message.textContent = "";
    const primary = el("primary_metric").value.trim(), secondary = el("secondary_metric").value.trim();
    const payload = {
      task_id: el("task_id").value.trim(), target_identifier: el("target_id").value.trim(),
      primary_metric: primary === "" ? NaN : Number(primary),
      secondary_metric: secondary === "" ? NaN : Number(secondary),
      status_descriptor: el("status_descriptor").value.trim(), is_critical_flag: el("is_critical").checked
    };
    try {
      if (!form.checkValidity() || !Number.isFinite(payload.primary_metric) || !Number.isFinite(payload.secondary_metric))
        throw new Error("Please complete all fields using finite numeric values.");
      const api = el("mode").value === "api";
      if (api) {
        output.textContent = "Requesting /api/audit…";
        const response = await fetch("/api/audit", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(payload) });
        const data = await response.json();
        if (!response.ok) throw new Error("API HTTP " + response.status + ": " + JSON.stringify(data.detail || data));
        result = data;
        el("m-audit").textContent = "Server-managed";
      } else {
        result = evaluateRules(payload);
        el("m-audit").textContent = "None (local)";
      }
      count++; el("m-tasks").textContent = String(count);
      output.textContent = JSON.stringify(result, null, 2);
      message.textContent = api ? "Python API response received." : "Local evaluation complete (unsigned).";
      dl.disabled = false;
    } catch (error) {
      output.textContent = "No result: " + (error instanceof Error ? error.message : String(error));
      message.textContent = "Evaluation failed.";
    }
  });
  el("normal").addEventListener("click", () => {
    el("task_id").value = "DEMO-NORMAL"; el("target_id").value = "EXAMPLE-B";
    el("primary_metric").value = "12"; el("secondary_metric").value = "4";
    el("status_descriptor").value = "NOMINAL"; el("is_critical").checked = false;
  });
  el("clear").addEventListener("click", () => {
    result = null; message.textContent = ""; dl.disabled = true;
    output.textContent = "Submit the form to evaluate a sample task.";
  });
  dl.addEventListener("click", () => {
    if (!result) return;
    const url = URL.createObjectURL(new Blob([JSON.stringify(result, null, 2) + "\n"], { type: "application/json" }));
    const anchor = document.createElement("a"); anchor.href = url; anchor.download = "evaluation-result.json"; anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 0);
  });
  modeChanged();
}