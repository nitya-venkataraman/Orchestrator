from typing import TypedDict, List, Optional, Literal


class UXPipelineState(TypedDict):
    project_brief: str
    raw_research_data: Optional[str]
    synthesized_insights: Optional[str]
    persona_profile: Optional[str]
    journey_map: Optional[str]
    problem_statement: Optional[str]
    feature_matrix: Optional[str]
    concept_proposals: Optional[List[str]]
    selected_concept: Optional[str]
    sitemap: Optional[str]
    wireframe_specs: Optional[str]
    design_tokens_applied: Optional[bool]
    figma_wireframe_url: Optional[str]
    figma_design_system_url: Optional[str]
    hifi_screens: Optional[List[dict]]
    hifi_figma_page_url: Optional[str]
    design_system_gaps: Optional[List[dict]]
    developer_handoff_stories: Optional[str]
    microcopy: Optional[str]
    current_phase: Literal[
        "discovery", "discovery_review",
        "strategy", "strategy_review",
        "ideation", "ideation_review",
        "wireframe", "wireframe_review",
        "hifi", "hifi_review",
        "delivery", "delivery_review",
        "complete"
    ]
    feedback_loop: Optional[str]
    approved: bool
