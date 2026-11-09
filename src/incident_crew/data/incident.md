# Fictional incident INC-0042

All names, timestamps, logs, and metrics below are synthetic training data.
Service: checkout-api. Window: 2026-11-09 10:00–10:20 UTC.
Impact observed: checkout requests returned HTTP 503; payment completion impact
has not been measured. No recovery action has been performed in this exercise.

## Change record
E1: 10:02 UTC: checkout-api v2.4.0 deployed to all 4 replicas.
E2: v2.3.9 used DB_POOL_MAX=10 per replica. v2.4.0 uses DB_POOL_MAX=80.
E3: Database max_connections=200; 30 connections are reserved for other services.

## Metrics
E4: At 10:00: database connections=65, checkout 5xx=0.2%, p95=180ms.
E5: At 10:05: database connections=200, checkout 5xx=38%, p95=5200ms.
E6: At 10:15: database connections=200, checkout 5xx=42%, p95=6100ms.
E7: Database CPU=35%, memory=58%; checkout CPU=40%, memory=49% at 10:15.

## Logs
E8: 10:03:15 checkout-api: connection acquisition timed out after 5000ms.
E9: 10:03:16 postgres: FATAL: remaining connection slots are reserved.
E10: 10:04:12 checkout-api: POST /checkout 503 database unavailable.

## Runbook excerpt
R1: Confirm the timing of the release and connection saturation before changing anything.
R2: Consider rolling back to the last known healthy release with operator approval;
    use a staged rollout to avoid a reconnection surge. Confirm schema compatibility first.
R3: Check active sessions and connection counts. Avoid blindly killing sessions or
    increasing the database connection limit.
R4: Verify checkout error rate, latency, database connections, and a synthetic checkout
    before declaring recovery. Observe for at least 15 minutes.
R5: Prevent recurrence by enforcing a total connection budget across replicas and
    validating pool settings in deployment checks.

## Unknowns
No query-level traces, per-replica connection counts, or post-recovery observations
are supplied. Correlation is evidence for a hypothesis, not proof of sole causation.
