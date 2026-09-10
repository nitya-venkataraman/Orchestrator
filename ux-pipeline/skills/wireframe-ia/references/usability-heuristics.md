# Usability heuristics — the Stage 4 self-critique

Nielsen's ten heuristics, written for this pipeline. Step 12 walks the primary
journey against this list and records what it finds in `heuristic_review`.

This is the only evaluative pass before a human sees the spec, so it has one job:
find the problems the earlier steps structurally cannot. Steps 7–10 already force
responsive recomposition, four UI states, accessibility and build requirements.
None of those catch a flow that gives the user no way out, an action with no
undo, or a system that makes someone remember what it could have shown them.
**Look for those.** A review that only restates the states block found nothing.

## How to run it

Walk `user_flow.primary_journey` step by step, then the error scenarios. At each
step ask what the ten heuristics ask. Record a finding when the answer is
unsatisfactory *for this design*, naming the page it lands on.

Findings are honest, not decorative. Two or three real ones beat ten padded.
Where a heuristic is genuinely well served, record it as `"none"` with a one-line
reason — that reason is the evidence you actually checked, and a `heuristic_review`
of all-`none` with no reasons reads as a review that was not run.

**A finding you can fix, fix.** Change the page spec, then record the finding
with what you changed as the `fix`. The point is a better spec, not a longer
list of known defects. Only leave a finding unfixed when the fix is a decision
above your pay grade — a scope or policy call — and say so in the `fix`.

## The ten

| Heuristic | What to look for in a page spec |
|---|---|
| **Visibility of system status** | Does every action get a response? Long operations — the ones step 8's `loading` state exists for — need progress, not just a spinner. Does the user know where they are in a multi-step flow? |
| **Match between system and the real world** | Do page names, labels and `content_structure` use the persona's vocabulary or the data model's? A sitemap ordered by table name is this failure wearing an IA costume. |
| **User control and freedom** | Is there a way out of every state? Can a destructive or expensive action be undone, or at minimum confirmed? An "emergency exit" is a real requirement, not a nicety. |
| **Consistency and standards** | Does the same thing get the same name and the same component across pages? Does the design system's convention win over a local invention? Cross-check `components` for two roles doing one job. |
| **Error prevention** | Better than a good error message: could the design make the error impossible? Constrain the input, default sensibly, confirm the irreversible. Look at `requirements.edge_cases` and ask which of those should never have been reachable. |
| **Recognition rather than recall** | Is the user asked to remember something from a previous page? If a figure, a filter, or an entered value matters here, show it here. |
| **Flexibility and efficiency of use** | Is there a path for the person who does this thirty times a day as well as the person doing it once? Keyboard paths, saved views, bulk actions — where the persona warrants them. |
| **Aesthetic and minimalist design** | Does each page carry one primary action and content ordered by importance, or is it a dumping ground? Every element competing for attention weakens the ones that matter. |
| **Help users recognize, diagnose and recover from errors** | Does each `error` state say what happened, in plain language, and what to do next? Does it preserve the work the user had done? |
| **Help and documentation** | Where the task genuinely needs explanation, is it available in context rather than in a manual? Prefer making the step self-evident to documenting it. |

## Severity

Use the same scale the rest of the pipeline uses for consequence, and be honest —
inflating severity is as unhelpful as omitting the finding.

- **high** — blocks the primary journey, risks data loss, or has no workaround.
- **medium** — a real cost to the task, but the user gets there.
- **low** — friction worth fixing when convenient.

## What a finding looks like

```json
{
  "heuristic": "User control and freedom",
  "page": "06 - Risk Review",
  "severity": "high",
  "finding": "Sign-off is irreversible and has no confirmation step, so a mis-click closes a review that took twenty minutes to build.",
  "fix": "Added a confirm dialog naming the profile and the unverifiable-figure count, and a 10-minute undo window on the sign-off action. Spec updated on 06."
}
```

And a clean one:

```json
{
  "heuristic": "Error prevention",
  "page": "none",
  "severity": "none",
  "finding": "none",
  "fix": "Commit is blocked while two documents define a term differently (03), and sign-off is blocked on unverifiable figures (06) — the two ways bad data could enter are closed by design rather than by a message."
}
```
