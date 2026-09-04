from langgraph.graph import StateGraph, END
from langgraph.types import interrupt, Command
from state import UXPipelineState
from claude_skill_client import invoke_skill


def discovery_node(state: UXPipelineState) -> dict:
    result = invoke_skill("discovery-synthesis", state)
    return {"synthesized_insights": result["synthesized_insights"],
            "current_phase": "discovery_review"}


def strategy_node(state: UXPipelineState) -> dict:
    result = invoke_skill("strategy-definition", state)
    return {**result, "current_phase": "strategy_review"}


def ideation_node(state: UXPipelineState) -> dict:
    result = invoke_skill("ideation-concepting", state)
    return {**result, "current_phase": "ideation_review"}


def wireframe_node(state: UXPipelineState) -> dict:
    result = invoke_skill("wireframe-ia", state)
    return {**result, "current_phase": "wireframe_review"}


def delivery_node(state: UXPipelineState) -> dict:
    result = invoke_skill("delivery-handoff", state)
    return {**result, "current_phase": "delivery_review"}


def next_phase(state: UXPipelineState) -> str:
    order = ["discovery", "strategy", "ideation", "wireframe", "delivery", "complete"]
    current = state["current_phase"].replace("_review", "")
    idx = order.index(current)
    return order[idx + 1] if idx + 1 < len(order) else END


def human_review_gate(state: UXPipelineState) -> Command:
    decision = interrupt({
        "phase": state["current_phase"],
        "message": f"Review output for phase '{state['current_phase']}'. Approve, request revision, or reject?",
    })
    if decision.get("approved"):
        return Command(update={"approved": True, "feedback_loop": None}, goto=next_phase(state))
    return Command(
        update={"approved": False, "feedback_loop": decision.get("feedback")},
        goto=state["current_phase"].replace("_review", ""),
    )


builder = StateGraph(UXPipelineState)
builder.add_node("discovery", discovery_node)
builder.add_node("strategy", strategy_node)
builder.add_node("ideation", ideation_node)
builder.add_node("wireframe", wireframe_node)
builder.add_node("delivery", delivery_node)
builder.add_node("human_review", human_review_gate)

for node in ["discovery", "strategy", "ideation", "wireframe", "delivery"]:
    builder.add_edge(node, "human_review")

builder.set_entry_point("discovery")
graph = builder.compile(checkpointer=None)  # plug in a persistent checkpointer, e.g. SqliteSaver
