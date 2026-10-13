"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { evaluateRules } = require("../app.js");
const basic = { task_id: "TASK", target_identifier: "EXAMPLE", primary_metric: 12, secondary_metric: 4, status_descriptor: "NOMINAL", is_critical_flag: false };
test("normal rules evaluation is unsigned", () => {
  const result = evaluateRules(basic);
  assert.equal(result.total_alerts, 0);
  assert.equal(result.overall_urgency, "ROUTINE");
  assert.equal(result.encryption, "NONE");
  assert.equal(Object.hasOwn(result, "audit_hash"), false);
});
test("three workers escalate flagged anomalous input", () => {
  const result = evaluateRules({ ...basic, primary_metric: 26, secondary_metric: 13, is_critical_flag: true, status_descriptor: "ANOMALY" });
  assert.equal(result.total_alerts, 3);
  assert.equal(result.critical_alerts_count, 1);
  assert.equal(result.overall_urgency, "CRITICAL_STAT_PANIC");
});
test("secondary bound is strictly greater than 12", () => {
  assert.equal(evaluateRules({ ...basic, secondary_metric: 12 }).total_alerts, 0);
  assert.equal(evaluateRules({ ...basic, secondary_metric: 12.1 }).overall_urgency, "ELEVATED_RISK");
});
test("input validation prevents invalid values", () => {
  for (const payload of [{ ...basic, task_id: " " }, { ...basic, primary_metric: NaN }, { ...basic, secondary_metric: Infinity }, { ...basic, status_descriptor: "" }])
    assert.throws(() => evaluateRules(payload));
});