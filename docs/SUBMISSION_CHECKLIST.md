# Submission checklist and source review

[Evidence instructions](../evidence/README.md) · [Reflection](../REFLECTION.md) · [Validation](VALIDATION.md) · [Original project instructions](upstream/UDACITY_PROJECT_INSTRUCTIONS.md)

## Review basis

The inspected project includes an upstream README with implementation guidance, six scenarios, and a submission checklist. A separate scoring rubric was not supplied or found during the original inspection. This table maps those available requirements to source and reported outcomes; it is not a claim that an unavailable rubric was fully verified or that Udacity has graded the submission.

| Requirement | Source / available basis | Status and remaining verification |
| --- | --- | --- |
| App initialization and configuration | One `BedrockAgentCoreApp`; Nova/model and AWS clients in `main.py` | Present; real resource constants retained privately |
| MCP tool integration | `MCPClient`, Streamable HTTP, dynamic discovery | Present; live discovery was not rerun during preparation |
| Order tracking | API proxy handler with three GET routes | Local success reported; screenshot 01 pending |
| Simulated refunds | Direct Gateway handler and three-tool schema | Local success reported; screenshot 02 pending |
| Knowledge Base retrieval | `search_knowledge_base()` calls `retrieve()` | Local RAG success reported; screenshot 03 pending |
| Semantic/user-preference memory | Namespace discovery, retrieval/save hooks | Cross-session success after retry reported; screenshot 04 pending; live strategies not re-queried |
| Loyalty calculation | Decimal Python code, `executeCode`, tier-only fallback | Correct complete numbers reported; screenshot 05 pending; sandbox execution independently unverified |
| Browser integration | `AgentCoreBrowser.browser` registered as a tool | Live retrieval success reported; screenshot 06 pending |
| Runtime deployment | App entry point and Python toolkit deployment procedure | READY reported; screenshot 07 pending |
| Cloud order invocation | Reported `ORD-001` request and answer | Successful reported; screenshot 08 pending; not all-six cloud coverage |
| Completed source | Implemented TODO sections inspected | Present; original TODO comments retained; no source changes made for publication |
| 200–400 word reflection | `REFLECTION.md` | Prepared; exact word count recorded in validation report |
| Required screenshots or terminal evidence | Eight filenames specified in evidence guide | PENDING manual addition; no manufactured evidence |
| Copyright/license retention | Original `LICENSE.txt` and archived instructions | Preserved; redistribution questions remain documented |

## Final student actions

- [ ] Add the eight actual screenshots using the names in [evidence/README.md](../evidence/README.md).
- [ ] Ensure each capture clearly distinguishes local execution from cloud Runtime execution.
- [ ] Show both sessions for memory recall and the full loyalty calculation breakdown.
- [ ] Include sandbox/tool execution evidence if claiming independently verified Code Interpreter execution; otherwise retain the current qualification.
- [ ] Redact credentials, tokens, account IDs, resource ARNs, private endpoints, and personal information before adding screenshots.
- [ ] Review the reflection to ensure its first-person account matches your experience and the course's authorship requirements.
- [ ] Compare against the current classroom rubric, which was not supplied for this review.
- [ ] Confirm Udacity access/submission instructions before giving anyone private repository access.
- [ ] Submit through the required Udacity channel; a GitHub push alone is not a course submission.

Updating a screenshot status requires an actual reviewed file. Presence alone does not prove what a capture shows. Keep the repository private and do not change the original Udacity repository or deployed AWS resources to complete these documentation items.
