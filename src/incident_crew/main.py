"""Installed command: incident-crew."""

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a three-agent incident investigation"
    )
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument(
        "--quiet", action="store_true", help="Hide CrewAI's verbose output"
    )
    args = parser.parse_args()
    load_dotenv(Path.cwd() / ".env")
    if not os.getenv("OPENAI_API_KEY", "").strip():
        parser.error("Set OPENAI_API_KEY in your environment or local .env file.")

    # Import after argument/credential checks so --help requires no model setup.
    os.environ.setdefault("OTEL_SDK_DISABLED", "true")
    os.environ.setdefault("CREWAI_TELEMETRY_DISABLED", "true")
    from crewai import LLM

    from incident_crew.crew import build_crew, load_evidence

    llm = LLM(
        model=os.getenv("MODEL", "openai/gpt-4o-mini"),
        temperature=0.2,
        timeout=90,
        max_tokens=2200,
    )
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    print("Investigator → Reviewer → Report writer")
    crew = build_crew(llm, output_dir, load_evidence(), verbose=not args.quiet)
    crew.kickoff()
    print(f"Saved diagnosis.md, review.md, and report.md to {output_dir}")


if __name__ == "__main__":
    main()
