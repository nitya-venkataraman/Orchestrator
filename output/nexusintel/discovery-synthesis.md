# Discovery Synthesis — NexusIntel

**Stage 1 of 6** · Corpus: 3 discovery interviews (P01 associate, P02 credit risk reviewer, P03 managing director), plus a product brief, competitive analysis and PRD read as framing only.

**6 themes** · **source_count: 3** · every quote below machine-verified as a verbatim substring of the corpus.

---

## 1. Sourcing crowds out analysis

`severity: high` · `raised by 2 of 3 participants`

The associate and the MD both describe the profile build as data logistics rather than judgment — Alex times it at 70% finding and formatting against 30% analysis and pushes the actual leverage math to the second night — because every input arrives as a filing, a vendor pull, a PDF or a macro feed that has to be re-keyed into one Excel template before any two of them can be compared.

**Evidence**

> It’s incredibly manual. An associate will spend 48 to 72 hours just building the foundational profile.
>
> — P03 — managing director, private credit and liquid strategies, discovery interview

> It’s probably 70% finding and formatting, and 30% actual analysis. I feel like a glorified data entry clerk for the first two days.
>
> — P01 — investment banking and portfolio associate, discovery interview

> That mapping alone easily sucks up 4 to 5 hours of the first day.
>
> — P01 — investment banking and portfolio associate, discovery interview

---

## 2. Firm memory hunted manually

`severity: high` · `raised by 2 of 3 participants`

Both the MD and the associate open a new target by canvassing internal systems by hand for any prior firm contact — Salesforce, the credit document repository, another desk's drive — and accept that whatever lives only in a personal inbox will be missed, so the firm re-underwrites companies it has already met.

**Evidence**

> But the real friction is internal data silos. An infrastructure team or a buyout team in Europe might have looked at a subsidiary of this exact company two years ago.
>
> — P03 — managing director, private credit and liquid strategies, discovery interview

> Their notes are buried in a legacy PDF on an internal drive somewhere, or worse, just sitting in someone's Outlook inbox. We lose massive leverage by not knowing what the firm already knows.
>
> — P03 — managing director, private credit and liquid strategies, discovery interview

> Then I check our internal CRM, Salesforce, and our credit document repository to see if we’ve ever touched this client, their sponsors, or any subsidiaries before.
>
> — P01 — investment banking and portfolio associate, discovery interview

---

## 3. Deal terms trapped in documents

`severity: high` · `raised by 2 of 3 participants`

The figures that decide the credit — covenant definitions, leverage ratios, amortization schedules, the guarantee package and the org structure — exist only as prose inside 300-page agreements, so the associate re-types them into a template and the reviewer has no route back to the sentence they came from short of reopening the PDF herself.

**Evidence**

> I'm stuck parsing through hundreds of pages of PDF credit agreements or pitch books just to build the org chart in PowerPoint.
>
> — P01 — investment banking and portfolio associate, discovery interview

> If an AI could read a 300-page PDF credit agreement, pull out the leverage ratios, definition of EBITDA, and the amortization schedule, and auto-populate my template, it would save me an entire day of work.
>
> — P01 — investment banking and portfolio associate, discovery interview

> I want to be able to click on a leverage ratio metric and see a pop-up showing the exact sentence in the source credit agreement it came from.
>
> — P02 — director, credit risk and portfolio operations, discovery interview

---

## 4. One error voids the profile

`severity: high` · `raised by 2 of 3 participants`

The reviewer treats a single unadjusted figure as evidence about the whole model rather than a local mistake — an accepted EBITDA add-back or an unadjusted pro-forma pull costs her confidence in everything else in the file — and the associate spends time on font consistency specifically to preempt that judgment.

**Evidence**

> sometimes they blindly trust the Capital IQ or Bloomberg pull without adjusting for pro-forma numbers from a recent acquisition
>
> — P02 — director, credit risk and portfolio operations, discovery interview

> If I catch an error like that, I lose trust in the whole profile.
>
> — P02 — director, credit risk and portfolio operations, discovery interview

> adjusting the formatting so the Credit Risk Officer doesn't complain about mismatched fonts
>
> — P01 — investment banking and portfolio associate, discovery interview

---

## 5. Email round-trips burn the deadline

`severity: medium` · `raised by 2 of 3 participants`

Work passes between associate, deal team, sponsor and reviewer as email with no shared state, so a missing cash flow statement or a wrong leverage figure converts directly into a 24-hour round trip against a live closing date, and the reviewer quietly repairs small defects herself rather than start one.

**Evidence**

> It’s always missing information or a blocked dependency.
>
> — P01 — investment banking and portfolio associate, discovery interview

> If they take 24 hours to reply, my clock is still ticking, but I can't finish the model.
>
> — P01 — investment banking and portfolio associate, discovery interview

> It delays my sign-off, which means the Credit Committee gets postponed, and suddenly we are risking missing the closing date for a live transaction.
>
> — P02 — director, credit risk and portfolio operations, discovery interview

---

## 6. Late, undifferentiated risk signals

`severity: high` · `raised by 1 of 3 participants`

The MD reads portfolio risk from covenant compliance keyed into spreadsheets once a quarter and from dashboards that raise fifty flags at once, so he learns of a breach roughly three months after it happened and still cannot tell which flag is worth his afternoon.

**Evidence**

> The problem with quarterly data is that by the time you see a covenant breach or a major dip in coverage ratios, you’re already three months too late to structure a workout or a refinancing package.
>
> — P03 — managing director, private credit and liquid strategies, discovery interview

> I don't need another messy dashboard with 50 flashing lights.
>
> — P03 — managing director, private credit and liquid strategies, discovery interview

> It needs to tell me the problem, our exposure, and the immediate trigger point.
>
> — P03 — managing director, private credit and liquid strategies, discovery interview

---

## Gaps — what this corpus cannot tell us

1. Only three participants, and all three sit on the same side of one firm's deal chain — an MD, an associate, a credit risk director. Nothing here tests whether the workflow generalizes to another manager, and the Portfolio Operations team named as a secondary user in the brief was not interviewed.
2. No participant described the predictive deal-sourcing use case. All three talked about building and reviewing a profile for a target already on the desk; the value proposition's claim to identify targets before they launch formal auction processes has no user evidence behind it in this corpus.
3. Deployment isolation was raised only by Marcus, in one sentence, and no security, compliance or IT stakeholder was interviewed — so the PRD's single-tenant VPC and the RBAC wall between Private Equity and Liquid Strategies are asserted requirements, not validated ones.
4. No participant gave a volume figure: deals screened per quarter, profiles built per associate, portfolio companies monitored per risk officer. Any reach estimate downstream will be an assumption.
5. The alternative-data signals in the PRD — employee sentiment indexes, shipping volumes — were named by the product team, not by a participant. Marcus named executive turnover, supply chain delays and accounts payable patterns.
6. Nobody described what happens after an alert fires: who acts, in which tool, on what timeline, and what an acceptable false-positive rate would be. The 1.5σ threshold and the Credit Health Score are PRD constructs no participant was asked to react to.
7. Elena described the review of a finished profile and Alex described building one, but no participant walked through the moment of handoff itself, so the rework loop is described from both ends and observed from neither.
8. The Product Brief, competitive analysis and PRD in the same document are product-team authored. They were read as context and framing; no theme above is grounded in them, and source_count counts only the three interviews.

---

## Gate result

**Tier 1 — structural: PASS.** `ux-pipeline/validators/synthesis.py` returned 0 errors with the full corpus supplied as `raw_research_data`; all 18 quotes are verbatim substrings.

**Tier 2 — judge: 0.88** (threshold 0.75)

| Criterion | Weight | Score | Note |
|---|---|---|---|
| `evidence_grounding` | 0.40 | 0.92 | Three verbatim quotes per theme; PRD framing explicitly excluded from evidence. Theme 4 leans partly on an oblique associate quote. |
| `theme_distinctness` | 0.25 | 0.80 | Weakest dimension: themes 1 and 3 are adjacent — both touch re-keying data into the template. They are kept apart because the causes differ (volume of scattered sources vs. figures locked in prose), but a reviewer could fairly merge them. |
| `signal_coverage` | 0.35 | 0.88 | Every signal raised by 2+ participants landed in a theme. Elena's review-priority ordering (leverage ratio → liquidity runway → guarantee package) is only implicit in themes 3 and 4. |
