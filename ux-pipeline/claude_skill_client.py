"""
Thin wrapper around the Claude Agent SDK's container.skills mechanism.
Replace `anthropic_client` with your configured SDK client.
"""
import json
from pathlib import Path

SKILLS_DIR = Path(__file__).parent / "skills"


def invoke_skill(skill_name: str, state: dict) -> dict:
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    skill_md = skill_path.read_text()

    # Attach any referenced/asset files (e.g. wireframe-ia's design tokens)
    ref_dir = SKILLS_DIR / skill_name / "references"
    assets_dir = SKILLS_DIR / skill_name / "assets"
    attachments = []
    for d in (ref_dir, assets_dir):
        if d.exists():
            attachments.extend(str(p) for p in d.glob("*"))

    # Pseudo-call — swap for real Claude Agent SDK invocation:
    # response = anthropic_client.messages.create(
    #     model="claude-...",
    #     container={"skills": [skill_name]},
    #     messages=[{"role": "user", "content": json.dumps(state)}],
    # )
    # return json.loads(response.content)

    raise NotImplementedError(
        f"Wire this to your Claude Agent SDK client. "
        f"Skill '{skill_name}' loaded with attachments: {attachments}"
    )
