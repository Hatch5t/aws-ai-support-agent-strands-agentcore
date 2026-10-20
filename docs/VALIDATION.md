# Attempt 2 validation record

Updated 20 October 2026. Source: dedicated remediation branch from main at c46a464. Offline checks precede any live deployment; AWS approval has not yet been supplied.

## Verified offline changes

| Gate | Status / result |
| --- | --- |
| Targeted source scope | Gateway lifecycle/error handling and loyalty result contract changed; RAG, Browser registration, MemoryHook, model/configuration, Lambda code, dependencies and reflection preserved |
| Python | Changed application and test sources compile; all existing Python sources parse |
| Gateway tests | 11 pass, including successful tools, entry/discovery timeouts and connection failures, unexpected exceptions, empty tools, constructor/cleanup failures, and model-error separation |
| Loyalty tests | 21 pass; all eight keys, all numerical expectations, tiers/rates, points/cap rounding, result formats and explicit tier-only fallback |
| Passing RAG regressions | 3 pass for Retrieve arguments/passage joining, missing-ID guard, and no-results response |
| Total | 35 offline tests pass; [actual output](../evidence/12_offline_regression_tests.txt) |
| Reflection | 285 body words; unchanged |
| Previous screenshots | Eight original images retained unchanged; reviewed as historical evidence, not new Attempt 2 executions |
| License | Original LICENSE.txt and archived instructions unchanged |
| Documentation | Maintained Markdown, file/heading/source links, examples and all three Mermaid diagrams validated |
| ZIP | Clean allowlist archive; no Git metadata, environments, credentials, deployment YAML, caches, raw private logs or nested generated archives |

The tests load the actual application module with external AWS/Strands dependencies mocked. The generated calculator code is executed locally by the mock, not in AgentCore Code Interpreter. Passing offline numerical tests does not establish actual sandbox execution or deployment.

## AWS and evidence status

No deployment, IAM write, refund action, memory write or live agent invocation was performed for these checks. Updated Runtime deployment, hosted order invocation and hosted two-session memory recall are AWAITING EXPLICIT APPROVAL. No genuine Attempt 2 cloud/memory transcripts exist yet, and none is included as a passing result.

The original [hosted invocation evidence](../evidence/CLOUD_INVOCATION_ORIGINAL.md) is prominent and remains genuine. Screenshot 04 shows a local two-session retry; it does not satisfy the reviewer's newly requested `agentcore invoke` A/B capture. The original deployment screenshot retains its trace-delivery warning.

## Security and visibility

GitHub initially reported PUBLIC during this task. Visibility was temporarily restored to private under the original instruction. The author then confirmed permission for public redistribution and explicitly requested PUBLIC visibility while retaining the existing configuration. Public visibility was restored under that updated authorization.

The repository retains the live Gateway URL and KB/Memory IDs as the author requested. The educational Gateway client is unsigned. Public copies of those access details may exist; changing repository visibility is not endpoint authorization. No AWS security setting was changed, and any Gateway authorization/rotation work requires separate explicit approval. No active access key, secret key, session token or bearer credential was detected in the previously reviewed source/evidence. Account IDs and ARNs alone are not treated as credentials.

Gitleaks scans working files, staged content, repository history and submission ZIP content with redaction. Binary screenshot text is reviewed visually rather than claimed to be scanned by Gitleaks. Final scan and remote/ZIP verification results are reported with delivery. No new credential values are logged or published by the tests.

## Submission limitations

The reviewer failed four criteria in Attempt 1; the earlier pre-review “ready” conclusion is superseded. Two code gaps are corrected and offline-tested. Updated deployment and hosted memory evidence remain outstanding; Attempt 2 is not claimed to have passed Udacity or to be fully live-verified. A draft submission ZIP may be reviewed now, but the final resubmission should wait for the genuine required live evidence or an explicit lab-expiry blocker.
