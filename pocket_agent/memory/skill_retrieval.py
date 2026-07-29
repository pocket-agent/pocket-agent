import re

from pocket_agent.core.skill_loader import Skill


def _tokenize(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[a-zA-Z0-9_]+", text) if len(t) > 2}


def score_skill(query: str, skill: Skill) -> float:
    query_tokens = _tokenize(query)
    if not query_tokens:
        return 0.0
    skill_tokens = _tokenize(skill.content)
    if not skill_tokens:
        return 0.0
    overlap = len(query_tokens & skill_tokens)
    return overlap / len(query_tokens)


def retrieve_skills(query: str, skills: list[Skill], top_k: int = 3) -> list[Skill]:
    if not skills:
        return []
    ranked = sorted(skills, key=lambda s: score_skill(query, s), reverse=True)
    top = [s for s in ranked if score_skill(query, s) > 0][:top_k]
    if top:
        return top
    return ranked[:min(top_k, len(ranked))]
