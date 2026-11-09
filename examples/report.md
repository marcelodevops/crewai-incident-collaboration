# INC-0042 — illustrative incident report

**Fictional training exercise. This report is hand-written to illustrate the
expected shape of the output; it is not output from a successful live model run.**

## Summary
Checkout errors increased shortly after release v2.4.0. The leading hypothesis
is database connection exhaustion following a pool-size increase (E1–E6, E8–E10).
Recovery is unverified; no actions were executed.

## Impact
Checkout 5xx errors rose from 0.2% to 42%, while p95 latency increased from 180ms
to 6100ms (E4, E6). Payment completion impact has not been measured.

## Timeline
- 10:00 UTC: low error rate; 65 database connections (E4).
- 10:02: release v2.4.0 deployed to four replicas (E1).
- 10:03: connection timeouts and reserved-slot errors appeared (E8–E9).
- 10:05–10:15: connections stayed at 200; checkout errors remained elevated (E5–E6).

## Likely cause
Four pools of up to 80 connections permit potential demand of 320 connections
(E1–E2), against an application budget of 200 − 30 = 170 (E3). Previously, four
pools of 10 permitted potential demand of 40. This arithmetic describes capacity,
not measured per-replica usage. Saturation and logs support the hypothesis but
do not establish that this change is the sole cause. Long transactions or leaked
connections remain possible contributors. CPU and memory show no comparable
saturation at the sampled time (E7).

## Proposed recovery
An operator should verify the rollout timing and active sessions, confirm schema
compatibility, and consider a staged rollback to v2.3.9 with approval (R1–R3).
Do not blindly raise the database limit or kill sessions. No commands were run.

## Validation
Check connection count, error rate, latency, and a synthetic checkout. Observe
for at least 15 minutes before declaring recovery (R4). No post-recovery
observations are available, so the incident cannot be declared resolved.

## Prevention
Enforce a connection budget across replicas and validate pool settings before
release (R5). Account for rollout overlap and other services when allocating it.

## Open questions
- What are the actual per-replica connection counts?
- Are long transactions or connection leaks contributing?
- What is the measured payment completion impact?
- Do post-mitigation metrics demonstrate sustained recovery?
