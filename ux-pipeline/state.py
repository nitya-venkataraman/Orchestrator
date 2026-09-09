"""
Typed state for the ux-pipeline LangGraph.

The artifact fields mirror the schemas in `rules/CONTRACTS.md`. They are typed as
`TypedDict`s so a misread field fails at author time rather than three stages
later; at runtime they are plain JSON-serializable dicts/lists threaded through
the graph and written to `output/<stage>/<stage>-<slug>.{json,md}`.

`total=False` throughout: the state fills in as the run advances, and a resumed
run rehydrates only the keys that were already approved.
"""
from __future__ import annotations

from typing import Dict, List, Literal, Optional, TypedDict

# --- Stage 1: discovery-synthesis -------------------------------------------------


class Quote(TypedDict, total=False):
    text: str
    source: str


class Theme(TypedDict, total=False):
    name: str
    insight: str
    frequency: int
    quotes: List[Quote]
    severity: Literal["high", "medium", "low"]


class SynthesisArtifact(TypedDict, total=False):
    themes: List[Theme]
    gaps: List[str]
    source_count: int


# --- Stage 2: strategy-definition -----------------------------------------------


class Persona(TypedDict, total=False):
    name: str
    type: Literal["primary", "secondary"]
    context: str
    goals: List[str]
    frustrations: List[str]
    quote: str
    grounded_in: List[str]


class JourneyStage(TypedDict, total=False):
    stage: str
    actions: List[str]
    emotion: str
    friction: List[str]
    dropoff_risk: Literal["high", "medium", "low"]


class HMW(TypedDict, total=False):
    statement: str
    derived_from: str


# --- Stage 3: ideation-concepting ----------------------------------------------


class Feature(TypedDict, total=False):
    name: str
    description: str
    hmw: str
    reach: float
    impact: float
    confidence: float
    effort: float
    rice_score: float


class DesignDirection(TypedDict, total=False):
    name: str
    summary: str
    differentiator: str
    hmws_addressed: List[str]
    tradeoff: str


# --- Stage 4: wireframe-ia ----------------------------------------------------
#
# Design-system agnostic. The stage owns no component library — a component's
# `name` is whatever the resolved design system calls it, and its `base` is a
# role from the fixed taxonomy in `validators/wireframe.py`.

TargetSurface = Literal["web", "mobile", "both"]
MobilePlatform = Literal["android", "ios"]


class DesignSystemTokens(TypedDict, total=False):
    color: List[str]
    typography: List[str]
    spacing: List[str]


class DesignSystemRef(TypedDict, total=False):
    name: str
    source: Literal["existing", "baseline"]
    tokens: DesignSystemTokens


class UXInterpretation(TypedDict, total=False):
    primary_user: str
    user_goal: str
    business_goal: str
    main_task: str
    context: str
    entry_point: str
    expected_outcome: str
    required_data: List[str]
    business_rules: List[str]
    constraints: List[str]
    dependencies: List[str]


class UserFlow(TypedDict, total=False):
    primary_journey: List[str]
    supporting_tasks: List[str]
    error_scenarios: List[str]


class ComponentRef(TypedDict, total=False):
    name: str            # "Component / KPI Card" — the design system's own name
    base: str            # a role from BASE_ROLES
    source: Literal["reused", "new"]
    variants: List[str]
    why_new: str         # required when source == "new"


class PageRequirements(TypedDict, total=False):
    data_dependencies: List[str]
    permissions: List[str]
    edge_cases: List[str]
    open_questions: List[str]


class PageSpec(TypedDict, total=False):
    page_name: str       # "02 - Dashboard" (web) / "M02 - Home" (mobile)
    purpose: str
    primary_user: str
    primary_action: str
    secondary_actions: List[str]
    content_structure: List[str]
    navigation: str
    components: List[ComponentRef]
    data: List[str]
    interactions: List[str]
    states: Dict[str, str]        # default/loading/empty/error [+ success/disabled]
    responsive: Dict[str, str]    # desktop/laptop/tablet/mobile
    accessibility: Dict[str, str]  # contrast/keyboard_focus/labels/touch_targets/reading_order
    requirements: PageRequirements


class SitemapNode(TypedDict, total=False):
    page: str
    path: str
    children: List[str]


class ResponsiveMatrixRow(TypedDict, total=False):
    component: str
    desktop: str
    tablet: str
    mobile: str


class PrototypeFlow(TypedDict, total=False):
    # keys mirror the JSON contract; `from` is a Python keyword, so this
    # TypedDict is documentation rather than a constructor target.
    trigger: str
    to: str
    interaction: str


class DesignSystemGap(TypedDict, total=False):
    need: str
    nearest_role: str
    why_insufficient: str


class ValidationSummary(TypedDict, total=False):
    ux: List[str]
    ui: List[str]
    responsive: List[str]
    accessibility: List[str]
    prototype: List[str]


# --- Stage 5: delivery-handoff -----------------------------------------------


class AcceptanceCriterion(TypedDict, total=False):
    given: str
    when: str
    then: str


class Story(TypedDict, total=False):
    id: str
    persona: str
    capability: str
    benefit: str
    screen: str
    acceptance_criteria: List[AcceptanceCriterion]


# --- The threaded state -------------------------------------------------------

Phase = Literal[
    "discovery", "discovery_review",
    "strategy", "strategy_review",
    "ideation", "ideation_review",
    "select_direction",
    "wireframe", "wireframe_review",
    "delivery", "delivery_review",
    "complete",
]

StageStatus = Literal[
    "PENDING", "RUNNING", "AWAITING_APPROVAL", "APPROVED", "ESCALATED"
]


class UXPipelineState(TypedDict, total=False):
    # run identity / bookkeeping
    run_id: str
    run_slug: str
    project_brief: str

    # inputs
    raw_research_data: Optional[str]

    # stage artifacts (see rules/CONTRACTS.md)
    synthesized_insights: Optional[SynthesisArtifact]
    persona_profile: Optional[List[Persona]]
    journey_map: Optional[List[JourneyStage]]
    problem_statement: Optional[List[HMW]]
    feature_matrix: Optional[List[Feature]]
    concept_proposals: Optional[List[DesignDirection]]
    selected_concept: Optional[str]
    selected_direction: Optional[str]
    target_surface: Optional[TargetSurface]
    mobile_platform: Optional[MobilePlatform]
    design_system_input: Optional[str]
    design_system: Optional[DesignSystemRef]
    ux_interpretation: Optional[UXInterpretation]
    user_flow: Optional[UserFlow]
    sitemap: Optional[List[SitemapNode]]
    wireframe_specs: Optional[List[PageSpec]]
    responsive_matrix: Optional[List[ResponsiveMatrixRow]]
    prototype_flows: Optional[List[Dict[str, str]]]
    design_system_gaps: Optional[List[DesignSystemGap]]
    assumptions: Optional[List[str]]
    validation: Optional[ValidationSummary]
    design_tokens_applied: Optional[bool]
    figma_file_url: Optional[str]
    developer_handoff_stories: Optional[List[Story]]
    microcopy: Optional[Dict[str, object]]

    # gate state
    current_phase: Phase
    attempts: Dict[str, int]
    stage_status: Dict[str, StageStatus]
    judge_scores: Dict[str, float]
    feedback_loop: Optional[str]
    approved: bool
    escalated: bool
