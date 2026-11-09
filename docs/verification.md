# Verification record

Local verification on 2026-11-09, Python 3.12:

- Three automated tests passed. The full workflow test executes the real CrewAI
  sequential crew against a scripted BaseLLM, checks both context handoffs, and
  verifies the three saved files. This is not a live model-quality test.
- Ruff lint and format checks passed.
- Source distribution and wheel built successfully. The wheel includes the
  bundled fictional evidence.
- A live run using openai/gpt-4o-mini was attempted. OpenAI returned HTTP 429,
  code credit_balance_exhausted. No agent output completed. Live model behavior
  is therefore not verified. Fund the account and rerun to complete that check.
- The committed examples/report.md is explicitly hand-written and illustrative.

CrewAI 1.15.39 emits internal deprecation warnings and a warning about checkpoint
serialization of partial callbacks. This example does not restore checkpoints;
its callbacks are exercised by the integration test. Checkpoint resume is outside
its scope.
