# Incident collaboration example

Build an educational Python CLI with three CrewAI agents: investigator, reviewer,
and report writer. A bundled fictional incident supplies logs, metrics, a change
record, and a runbook. The investigator receives this evidence; the reviewer
receives the evidence and diagnosis; the writer receives both prior outputs.
All agents run sequentially with explicit Task.context dependencies. This is
collaboration through shared artifacts, not autonomous delegation or parallel work.

Save diagnosis.md, review.md, and report.md in a user-selected output directory.
Use an OpenAI model configured through environment variables. Never execute
recovery commands. Keep credentials outside the repository. Verify real CrewAI
execution with a deterministic test LLM, then perform a separate live model run.
