from pathlib import Path

from pocket_agent.core.skill_loader import load_skills, load_system_prompt


def test_load_skills():
    root = Path(__file__).resolve().parents[1]
    skills = load_skills(root / "agent" / "skills")
    names = [s.name for s in skills]
    assert "general" in names


def test_load_system_prompt():
    root = Path(__file__).resolve().parents[1]
    prompt = load_system_prompt(root / "agent" / "prompts")
    assert "Pocket Agent" in prompt
