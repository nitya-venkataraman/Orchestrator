---
name: discovery-synthesis
description: Use this skill when raw qualitative UX research (interview transcripts, survey CSVs, support tickets, competitor notes) needs to be synthesized into thematic insights. Triggered as Node 1 of the UX pipeline.
---

# Discovery & Research Synthesis

## Steps
1. Ingest `raw_research_data` from state.
2. Extract recurring pain points and verbatim user quotes.
3. Cluster findings into thematic affinity groups (max 6 themes).
4. Output a markdown "Research Synthesis Report" with: theme name, supporting quotes, frequency signal, and a one-line behavioral insight per theme.

## Output contract
Return only `synthesized_insights` (markdown string). Do not invent data not present in the input — flag gaps explicitly.
