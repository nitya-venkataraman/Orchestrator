# Ideation & Concepting — DENSO IPS Cloud MVP

**Stage 3 of 6** · 12 features against the 5 approved HMWs, plus 3 design directions. The directions are bets for you to choose between; this stage does not pick one.

> **How reach was scored.** The RFQ gives no counts of sites, anchors, users or operators, so reach in people would be invented. Instead, **reach = the number of RFQ requirement lines the feature serves**, out of 41 numbered lines across §3A, §3B, §4, §5A, §5B and §5D. Each feature lists its lines, so the figure can be checked. The proxy has a known bias: it rewards features that touch many dashboard requirements and under-ranks features that address one serious risk. Confidence is at most 0.8, because the evidence is one RFQ, and is 0.5 wherever a feature answers something the RFQ is silent on. Effort is in person-months and is an estimate. **Every baseline is `unknown`.**

---

## RICE backlog (by score)

| # | Feature | HMW | Move | R | I | C | E | **RICE** |
|---|---|---|---|---|---|---|---|---|
| 1 | **Live, fading and gone states on every marker** | HMW 2 | serve the need better | 9 | 2 | 0.8 | 1 | **14.4** |
| 2 | **One panel that explains a reading** | HMW 3 | serve the need better | 5 | 2 | 0.8 | 1 | **8.0** |
| 3 | **Integration health panel** | HMW 5 | serve the need better | 6 | 2 | 0.5 | 1 | **6.0** |
| 4 | **Identity lives only in the customer dashboard** | HMW 1 | change who does it | 5 | 2 | 0.5 | 1 | **5.0** |
| 5 | **Names resolved at the operator's screen** | HMW 1 | change where it happens | 5 | 3 | 0.5 | 2 | **3.8** |
| 6 | **Heartbeat on the stream** | HMW 5 | change who does it | 3 | 1 | 0.5 | 0.5 | **3.0** |
| 7 | **Impact preview before a change** | HMW 4 | serve the need better | 4 | 1 | 0.5 | 1 | **2.0** |
| 8 | **Presence event timeline** | HMW 2 | change when it happens | 7 | 0.5 | 0.5 | 1 | **1.8** |
| 9 | **Pseudonymous markers, names revealed on purpose** | HMW 1 | serve the need differently | 3 | 1 | 0.5 | 1 | **1.5** |
| 10 | **Anchor drift check** | HMW 3 | change who does it | 4 | 1 | 0.5 | 2 | **1.0** |
| 11 | **Staged OTA with automatic rollback** | HMW 4 | change when it happens | 5 | 1 | 0.5 | 3 | **0.8** |
| 12 | **Role-gated configuration** | HMW 4 | remove the need | 1 | 1 | 0.5 | 1 | **0.5** |

**Read the ranking with one caution:** the answers to HMW 1 (the identity conflict, the most serious risk in Stage 1) rank 4th, 5th and 9th. That is the proxy's bias, not a judgement that identity matters less. HMW 1 is decided by which direction you choose, not by RICE.

### Feature detail

**1. Live, fading and gone states on every marker** · HMW 2

Each marker carries an explicit presence state with its last-seen age. It is live while readings arrive, fading after a defined silence, and removed at a defined timeout. Logout and a device switch skip straight to removal. The timings come from one agreed configuration rather than being implied.

- *Success metric:* Stale markers: people shown who have logged out, switched device, or been out of range past the agreed timeout · baseline **unknown** · target 0 across the five RFQ §5D scenarios
- *Measured by:* Measured by scripted run of the §5D demo scenarios, and in pilot by matching logout events to marker removal.
- *Reach basis:* 4-D4, 4-M3, 4-M4, 5D-2, 5D-3, 5D-4, 5D-5, 4-L1, 4-L2

**2. One panel that explains a reading** · HMW 3

Selecting a device opens one panel with its connected anchor, RSSI over the last minutes, the other anchors that can hear it, and the raw stream rows filtered to that device. Everything the RFQ asks for in telemetry, assembled around the question being asked.

- *Success metric:* Operators who correctly classify a suspicious reading as device-side or anchor-side · baseline **unknown** · target At least 4 of 5 usability-test participants
- *Measured by:* Measured in the Stage-6 usability test with seeded faults.
- *Reach basis:* 4-D5, 4-D6, 4-D7, 3B-7, 4-L2

**3. Integration health panel** · HMW 5

An integrator-facing view of the subscription (connected, last event received, lag) and the config feed (last SDK fetch, failed fetches), so a broken feed is visible on the integrator's side first.

- *Success metric:* Feed failures the integrator learns of before an operator or employee reports them · baseline **unknown** · target All injected stream and config failures
- *Measured by:* Measured by fault-injection test against the customer cloud.
- *Reach basis:* 3A-5, 3B-2, 3B-4, 4-S1, 3A-8, 5A-2

**4. Identity lives only in the customer dashboard** · HMW 1

Split the two dashboards the RFQ describes along the trust boundary. The IPS dashboard is an infrastructure console (anchors, store computer, anonymous markers). Only the customer-cloud dashboard, which already holds the identity mapping, shows names.

- *Success metric:* Identity fields in IPS Dashboard API responses · baseline **unknown** · target 0
- *Measured by:* Measured by contract test on the IPS Dashboard API.
- *Reach basis:* 3B-6, 4-D5, 3A-3, 3A-4, 4-D2

**5. Names resolved at the operator's screen** · HMW 1

The IPS dashboard receives only digital IDs. When the operator's session opens, it fetches names from the customer's own identity service using a signed token, and they are held in the browser for that session only. The vendor platform stores and logs digital IDs and nothing else.

- *Success metric:* Real identities found in IPS platform stores, logs and API responses · baseline **unknown** · target 0 in a platform data audit after the pilot
- *Measured by:* Measured by audit of IPS databases, logs and API traffic.
- *Reach basis:* 3B-6, 4-D5, 3A-7, 3B-5, 4-T1

**6. Heartbeat on the stream** · HMW 5

The stream emits a heartbeat even when nobody is moving. Silence becomes a detectable signal that the customer's existing monitoring can alert on, with no new UI.

- *Success metric:* Stream outages longer than one heartbeat interval missed by customer monitoring · baseline **unknown** · target 0
- *Measured by:* Measured by fault-injection test against the customer's monitoring.
- *Reach basis:* 3A-5, 3B-2, 4-S1

**7. Impact preview before a change** · HMW 4

Before calibration or an OTA update is applied, the operator sees which phones are on that anchor right now and which neighbouring anchors will cover them, then confirms.

- *Success metric:* Configuration changes that interrupted tracking without a prior warning · baseline **unknown** · target 0
- *Measured by:* Measured by correlating the change log with tracking gaps.
- *Reach basis:* 4-D3, 4-D6, 4-L2, 5B-2

**8. Presence event timeline** · HMW 2

A per-person feed of logins, logouts, device switches, entering and leaving coverage, and anchor handovers. The operator can see how someone left rather than infer it from a missing dot.

- *Success metric:* Operators who can correctly state how and when a person left the floor · baseline **unknown** · target At least 4 of 5 usability-test participants
- *Measured by:* Measured in the Stage-6 usability test.
- *Reach basis:* 4-M3, 4-M4, 5D-2, 5D-3, 5D-4, 5D-5, 4-D7

**9. Pseudonymous markers, names revealed on purpose** · HMW 1

Markers show a stable alias by default. An operator reveals a person's name deliberately, one person at a time, and every reveal records who did it and why.

- *Success metric:* Name reveals that carry an operator and a reason · baseline **unknown** · target Every reveal attributable (100%)
- *Measured by:* Measured from the reveal audit log.
- *Reach basis:* 4-D5, 3B-6, 5D-1

**10. Anchor drift check** · HMW 3

The platform compares each anchor's readings against its neighbours and flags an anchor whose devices consistently disagree with the rest, so the system rather than the operator spots a failing anchor.

- *Success metric:* Drifting anchors flagged by the system before an operator reports them · baseline **unknown** · target All seeded drift faults flagged first
- *Measured by:* Measured by fault-injection test on the demo site.
- *Reach basis:* 3A-3, 4-D2, 3B-7, 4-D6

**11. Staged OTA with automatic rollback** · HMW 4

Updates roll out one anchor at a time while neighbours cover, and an anchor that does not come back healthy reverts automatically. Depends on store-computer and firmware support, which are outside this RFQ's scope.

- *Success metric:* Tracking gaps longer than the latency bound during OTA updates · baseline **unknown** · target 0
- *Measured by:* Measured by correlating the OTA log with tracking gaps.
- *Reach basis:* 4-D3, 3A-3, 4-D2, 4-L2, 5B-2

**12. Role-gated configuration** · HMW 4

Viewing anchor and store-computer configuration is open to operators. Changing it or starting an OTA update needs an explicit permission, and every change is logged.

- *Success metric:* Configuration changes made by users without change permission · baseline **unknown** · target 0
- *Measured by:* Measured from the change log against the permission model.
- *Reach basis:* 4-D3

---

## How might we (from Stage 2)

1. How might we let an operator see who is where on the floor without the vendor's platform ever holding who that person is?
2. How might we make it unmistakable whether a person on the map is present now, fading out of range, or already gone?
3. How might we help an operator tell a bad reading for one person from a failing anchor before they act on either?
4. How might we give an operator confidence that changing a live anchor will not silently interrupt tracking for the people on it?
5. How might we let an integrator learn that the location stream or the SDK config feed has stopped before anyone on the floor notices tracking is gone?

---

## Design directions

### A. The trust boundary is the product boundary

Two products, split where the PII rule splits them. The IPS dashboard is an infrastructure console that shows anchors, the store computer and anonymous markers, and never a name. The customer-cloud dashboard, which already owns the identity mapping, is where people are seen by name. The integrator gets a health panel and a heartbeat so their side of the split is observable.

**Bet:** Identity never enters any surface the vendor runs, so PII safety is enforced by which product you are in, not by careful engineering inside one.

**Tradeoff:** Two dashboards to build and keep consistent, and an operator who needs both 'is the anchor up' and 'who is near it' switches tools. DENSO's own demo of 'who is where' depends on the customer-side build being ready.

**Addresses:** HMW 1, HMW 2, HMW 4, HMW 5

### B. One pane, names resolved at the glass

A single dashboard for everything: map, people, anchors, telemetry, configuration. The vendor platform holds digital IDs only. Names are fetched from the customer's identity service into the operator's browser per session, with pseudonymous markers and on-purpose reveals as the fallback. The operator's drill-down and change flows are built for confidence: one panel explains a reading, and a preview shows who a change will affect.

**Bet:** The operator works in one place and PII safety is an architectural guarantee inside it. It is the most direct reading of the RFQ's single-dashboard feature list.

**Tradeoff:** The demo cannot show a single name until the customer exposes a signed identity-lookup endpoint, so it is gated on customer engineering. If that endpoint is down mid-demo, every marker falls back to an alias. Browser-side resolution is also harder to audit than a server-side split.

**Addresses:** HMW 1, HMW 2, HMW 3, HMW 4

### C. The system watches itself

Automation first. The platform decides presence states, flags drifting anchors, stages and rolls back OTA updates, and emits a heartbeat so a silent stream raises an alarm. The operator handles exceptions and reads a timeline of what happened instead of watching a map for things going wrong.

**Bet:** It moves the work of noticing from the operator to the system, which fits an operations product better than a demo one.

**Tradeoff:** It is the most effort (drift detection and staged OTA alone are about 5 person-months) and depends on store-computer and firmware behaviour this RFQ puts out of scope. False drift alarms would erode the trust it is meant to build. The RFQ still requires the raw telemetry views, so this adds to the operator surfaces rather than replacing them, and it leaves the identity conflict (HMW 1) unanswered.

**Addresses:** HMW 2, HMW 3, HMW 4, HMW 5

**What separates them:**
- **A vs B** is where identity is allowed to live, in a separate customer product or resolved inside one shared pane. You cannot build both.
- **C** differs on who does the noticing, the system or the operator. It leaves HMW 1 unanswered, so choosing C still means choosing A's or B's answer to identity.

**The choice is yours.** At the fork you also pick the target surface (web, mobile or both), the mobile platform if relevant, and the design system.

---

## Gate result

**Tier 1 — structural: PASS.** `ux-pipeline/validators/ideation.py` returned 0 errors with the Stage-2 artifact as `problem_statement`. All 12 RICE scores recompute, every `hmw` matches a Stage-2 statement verbatim, and every feature carries a `success_metric`.

**Tier 2 — rubric: 4.0 / 5 — PASS** (`min>=3 and weighted_mean>=3.7`)

| Dimension | Weight | Score | Note |
|---|---|---|---|
| `hmw_linkage` | 0.30 | 5 | Every HMW has two or three features, and every feature answers exactly one. Within each HMW the features differ in kind, not size: serving the need better, removing it, changing who does it, or changing when. |
| `rice_integrity` | 0.30 | 3 | Inputs are honest, and no input was adjusted to move a feature. Impact is discriminated (0.5 to 3), every baseline is `unknown`, and each metric names an outcome rather than usage. Held at 3 because the reach proxy counts requirement lines rather than people, so the ranking does not reflect real priority: HMW 1's answers sit 4th, 5th and 9th. Effort figures are estimates for a team nobody has scoped. |
| `direction_distinctness` | 0.40 | 4 | A and B are mutually exclusive bets on where identity lives, and C is a different bet on who does the work. Not a 5: C borrows features (presence states, heartbeat) that A and B could also include, so it is partly an add-on rather than a pure alternative. |
