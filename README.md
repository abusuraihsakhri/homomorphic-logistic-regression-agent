# Homomorphic Logistic Regression Agent

**Current implementation:** a deterministic three-worker threshold/anomaly audit demonstration, not homomorphic encryption or logistic regression.

The CLI and FastAPI service evaluate two numeric metrics, a status descriptor, and an optional critical flag, then return structured alerts. A standalone browser demonstration can evaluate the same primary rules locally or connect to the API.

**Scientific and clinical limitations:** The main rules use primary > 25 and secondary > 12, which are arbitrary example thresholds, not validated clinical cutoffs. The repository has no logistic-regression training, CKKS/BFV implementation, encrypted gradient descent, formal validation, or NIST/CAP/CLSI certification. Do not use it for clinical decisions or enter patient-identifying information.

## Interfaces

- **Browser:** open web/index.html, or host the web/ directory statically. Local mode makes no network requests and exports JSON. API mode sends POST /api/audit to a Python backend on the same origin, and shows a real error when unavailable.
- **Main CLI:** single task audit, mock chat, CSV batch processing, and in-process audit verification.
- **FastAPI:** GET /health, GET /metrics, POST /api/audit, POST /api/chat, and protected GET /api/audit/logs.
- **Legacy he_logistic_reg package:** a separate set of illustrative checks. It uses secondary > 10, compared with the main API's > 12. Neither interface performs homomorphic encryption.

## Local installation

Python 3.10 or later:

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python cli.py audit --task-id DEMO-1 --target EXAMPLE-1 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
python cli.py batch -i sample.csv -o results.csv
python cli.py verify-audit
python cli.py serve --host 127.0.0.1 --port 8000
~~~

The installed homomorphic-logistic-regression-engine entry point invokes the **legacy** he_logistic_reg CLI, whereas python cli.py invokes the main API's rule set.

~~~bash
curl -sS http://127.0.0.1:8000/api/audit -H 'Content-Type: application/json' \
  -d '{"task_id":"DEMO-1","target_identifier":"EXAMPLE-1","primary_metric":28.5,"secondary_metric":14.2,"status_descriptor":"DISCORDANT","is_critical_flag":true}'
~~~

**Access control:** POST /api/audit is unauthenticated; use the backend only on a trusted local interface, not as a public clinical service. GET /api/audit/logs returns HTTP 503 unless AUDIT_LOG_READ_TOKEN is configured. Then supply the value via the X-Audit-Token request header.

## Audit and privacy limitations

The main Python API maintains **in-memory** HMAC-SHA256-chained metadata. Set AUDIT_SECRET_KEY to a strong random secret for controlled deployments; otherwise an ephemeral key is generated at startup. Verification recomputes each MAC and checks links. Records are **not persisted** across restarts; chain verification cannot detect deletion of the entire log, and this is not an externally anchored audit mechanism.

The identifier guard uses limited regex patterns: this **does not guarantee PHI removal, de-identification, or HIPAA Safe Harbor compliance**. The chat adapter is a mock; provider aliases are not real Ollama, Anthropic, or OpenAI integrations. Browser local mode keeps inputs in memory only, uses no browser storage, analytics, or network requests, and produces **unsigned and unencrypted** JSON. API mode submits input to the running backend.

## Docker

Generate a fresh secret and export it before running:

~~~bash
python -c "import secrets; print(secrets.token_hex(32))"
export AUDIT_SECRET_KEY='replace-with-the-generated-secret'
docker compose up --build
~~~

Compose binds the service to 127.0.0.1:8000 on the host. **Rotate the former committed signing key** if it was used outside a demo; removing it from the current tree does not remove its historical exposure.

## Tests

~~~bash
python -m pytest -v
node --check web/app.js
node --test web/tests/*.test.cjs
~~~

CI tests Python 3.10, 3.11 and 3.12, package installation and dependency checks, and browser JavaScript tests. The static web/ folder can be deployed via GitHub Pages, but GitHub Pages cannot run the FastAPI backend or execute homomorphic computation.

## Repository structure

agents/ contains the primary rules, supervisor, mock chat, audit and API; he_logistic_reg/ is the alternate interface; enrichment.py holds further generic threshold evaluators; web/ is the static browser demo; tests/ and web/tests/ are regression tests.

## License

MIT; see [LICENSE](LICENSE).
