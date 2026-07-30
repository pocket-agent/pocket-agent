from dataclasses import dataclass
from pathlib import Path


@dataclass
class Skill:
    name: str
    path: Path
    content: str


def load_skills(skills_dir: Path) -> list[Skill]:
    if not skills_dir.is_dir():
        return []

    skills: list[Skill] = []
    for path in sorted(skills_dir.glob("*.md")):
        skills.append(
            Skill(
                name=path.stem,
                path=path,
                content=path.read_text(encoding="utf-8"),
            )
        )
    return skills


def load_system_prompt(prompts_dir: Path) -> str:
    system_path = prompts_dir / "system.txt"
    if not system_path.is_file():
        return "You are Pocket Agent, a private personal assistant. Be concise and action oriented."

    parts = [system_path.read_text(encoding="utf-8").strip()]
    identity_path = prompts_dir / "identity.txt"
    if identity_path.is_file():
        parts.append(identity_path.read_text(encoding="utf-8").strip())
    return "\n\n".join(parts)
