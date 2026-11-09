import os
import subprocess

from crewai import BaseLLM

from incident_crew.crew import build_crew, load_evidence


class ScriptedLLM(BaseLLM):
    """Exercise real CrewAI orchestration without an external model service."""

    def __init__(self):
        super().__init__(model="scripted", temperature=0)
        self.prompts = []

    def call(self, messages, **kwargs):
        prompt = str(messages)
        self.prompts.append(prompt)
        replies = [
            "Final Answer: DIAGNOSIS_MARKER: connection pool exhausted after release.",
            "Final Answer: REVIEW_MARKER: rollback is proposed, not executed.",
            "Final Answer: # Incident report\nPool exhaustion. Recovery unverified.",
        ]
        return replies[len(self.prompts) - 1]

    def supports_function_calling(self):
        return False


def test_real_crew_passes_context_and_saves_all_outputs(tmp_path):
    llm = ScriptedLLM()
    crew = build_crew(llm, tmp_path, load_evidence(), verbose=False)
    result = crew.kickoff()
    assert len(llm.prompts) == 3
    assert "DIAGNOSIS_MARKER" in llm.prompts[1]
    assert "DIAGNOSIS_MARKER" in llm.prompts[2]
    assert "REVIEW_MARKER" in llm.prompts[2]
    assert "INC-0042" in llm.prompts[0]
    assert "INC-0042" in llm.prompts[1]
    assert "Incident report" in result.raw
    for name in ("diagnosis.md", "review.md", "report.md"):
        assert (tmp_path / name).read_text().strip()


def test_cli_missing_key_exits_without_creating_output(tmp_path):
    env = dict(os.environ)
    env.pop("OPENAI_API_KEY", None)
    result = subprocess.run(
        ["incident-crew", "--output-dir", str(tmp_path / "report")],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "OPENAI_API_KEY" in result.stderr
    assert not (tmp_path / "report").exists()


def test_cli_help_works_without_key():
    result = subprocess.run(
        ["incident-crew", "--help"], check=False, capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "--output-dir" in result.stdout
