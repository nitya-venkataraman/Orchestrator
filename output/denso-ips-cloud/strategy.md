# Strategy & Definition — DENSO IPS Cloud MVP

**Stage 2 of 6** · built on the approved Stage-1 synthesis (5 themes, one client RFQ).

> **Read this first.** The RFQ has no user research behind it, so these personas are *roles the RFQ describes*, not people anyone has met. The journey is the flow the RFQ *specifies*. No product exists yet, so there is no current state to map. Every emotion is anticipated from how well the spec defines that moment, and the basis is given for each. No stage carries a `current_metric`.

---

## Personas

### Site Operator · `primary`

Watches the IPS dashboard for one site: the floor plan, its anchors, the store computer and the logged-in people moving through it. They are also the one who reaches in to recalibrate an anchor or push a firmware update. The RFQ only ever calls this person 'users', so the role is inferred. Who it really is (facility operations, airline IT, a field engineer or a demo presenter) is the first open question in Stage 1. The RFQ is shaped around a live demo, so the realistic hard case is this person doing everything with the client watching, on a site they may not have commissioned themselves. The floor plan is the main surface, so a keyboard-only or screen-reader operator still has to be able to answer 'who is near this anchor, and is it working' without the map.

**Goals**

- Trust that the map shows exactly the people who are logged in and present right now, and nobody else
- Know at a glance whether every anchor and the store computer is up
- Be able to explain why a device is shown where it is before acting on it
- Recalibrate an anchor or apply an update from the same place they spotted the problem

**Frustrations** (anticipated from gaps in the spec)

- 'Progressively lose the connection' and 'eventually remove' have no timings, so a marker for someone who left looks the same as a marker for someone who is there
- Checking one suspicious reading means cross-reading the map, the anchor's connected-phone list, the RSSI and a raw text stream
- Can change configuration and push OTA updates to live hardware, but nothing says who is allowed to, or what happens to tracking while it runs
- May be shown real identities on a dashboard the platform is meant to keep PII out of, with no rule for which dashboard that is

> Allow users to click on an anchor or store computer to view and modify configuration settings (e.g., for calibration, OTA updates).
>
> — Doc-1, client RFQ (the role this persona is built from)

**Grounded in:** *The map must show only who is really there, right now* · *Operators watch infrastructure health and reach in to change it* · *Operators check a position by reading the raw signal behind it* · *Identity is wanted on screen but kept out of the platform*

---

### Customer-Cloud Integrator · `secondary`

The engineer on the customer side who connects the customer cloud to the platform. In the RFQ's example this is a large global airline. They subscribe to the location stream for logged-in users, store it for their own analysis, host the remote configuration the SDK downloads at login, and run the customer's side of the PKI: the intermediate CA and the mapping from digital ID to real person. Their work is mostly invisible until it breaks. If the subscription drops or the config endpoint fails, nobody is tracked, and the first sign is likely an operator or employee noticing.

**Goals**

- Receive a continuous stream of location updates for every logged-in user
- Publish configuration that the SDK reliably picks up at login, since the app ships with no anchor data
- Keep the mapping from digital ID to real identity entirely inside their own systems

**Frustrations** (anticipated from gaps in the spec)

- Nothing specifies how they would see that a subscription or a config endpoint has failed
- They carry the identity mapping and a certificate authority, but the RFQ defines the PKI as architecture, with no process for issuing, rotating or revoking anything

> Host and serve remote configuration data for the SDK.
>
> — Doc-1, client RFQ (the role this persona is built from)

**Grounded in:** *The customer cloud subscribes and hosts config, and never feeds the platform* · *Identity is wanted on screen but kept out of the platform*

---

### Tracked Employee · `secondary`

Carries a phone with the customer's app and the embedded SDK, logs in to be tracked, logs out to stop, sometimes switches to a different phone, and walks in and out of anchor coverage. Every one of the RFQ's demo scenarios is an action this person takes. They are the subject of the system rather than its operator: the RFQ never describes what they see. Logout is the only control it gives them, and nothing says whether they know what is recorded about them or who sees it.

**Goals**

- Be tracked only while logged in, and stop the moment they log out
- Show up as themselves on whichever phone they are using, and never on two phones at once
- Have their real identity stay with their employer, not with the vendor's platform

**Frustrations** (anticipated from gaps in the spec)

- On walking out of coverage they cannot tell whether they still appear on someone's dashboard, because removal is 'eventual'
- Their identity can appear on a dashboard they never see, and logout is the only control they have

> A phone that logs out should immediately disappear from the dashboard.
>
> — Doc-1, client RFQ (the role this persona is built from)

**Grounded in:** *The map must show only who is really there, right now* · *Identity is wanted on screen but kept out of the platform*

---

## Journey — the specified flow, through the Site Operator's eyes

| # | Stage | Actions | Emotion | Friction | Drop-off risk |
|---|---|---|---|---|---|
| 1 | **Bring the site up on the dashboard** | • Open the dashboard for a site and check that the floor plan matches the room<br>• Check that every ceiling anchor is marked where it physically hangs<br>• Confirm that the store computer is connected and sending | **uncertain** | • The RFQ specifies one floor plan and one store computer, but its PKI implies several sites. How an operator picks or switches site is undefined<br>• Anchor positions reach the app through customer-hosted config, but nothing says where the dashboard's anchor placement comes from or who keeps it correct | `medium` |
| 2 | **Confirm every anchor is up** | • Scan anchor status: online/offline, health, firmware version<br>• Read the store-computer status panel | **watchful** | • 'Health' is required but never defined, so a healthy and a degraded anchor may look the same<br>• There is no alerting in scope (notifications are a future enhancement), so an anchor dropping offline is only noticed if someone is looking | `medium` |
| 3 | **Watch people appear as they log in** | • A tracked employee logs in on their phone<br>• Their marker appears on the floor plan with identity, coordinates and connected anchor<br>• Two or more people are shown at once | **reassured** | • The latency bound is garbled in the source ('between 1 seconds'), so nobody can say whether a slow appearance is a fault<br>• Showing the logged-in user's identity conflicts with keeping PII out of the platform, and the RFQ does not say which dashboard may do it | `low` |
| 4 | **Follow someone across the floor** | • Watch a marker move as the person walks<br>• See the connected anchor change as they pass from one anchor's range into the next | **confident** | • The handover has to stay continuous within a latency bound that is itself unclear<br>• No accuracy target is given, so 'roughly the right place' and 'wrong' have no line between them | `low` |
| 5 | **Explain a marker that looks wrong** | • Open the device's detail: connected anchor, signal strength<br>• Open the anchor's list of connected phones<br>• Scan the raw streaming data panel for that device | **doubtful** | • The evidence is split across the map, the anchor list, RSSI values and a raw text stream, and the operator has to assemble it<br>• Nothing separates a bad reading for one device from an anchor that is drifting for everyone near it | `high` |
| 6 | **Fix an anchor or push an update** | • Click an anchor or the store computer<br>• View and modify its configuration for calibration<br>• Start an OTA update | **anxious** | • No permission model: the RFQ does not say who may change live hardware<br>• Nothing says what happens to tracking on that anchor, or to the people currently connected to it, while a change or update is applied | `high` |
| 7 | **Account for someone who has gone** | • A person logs out, and their marker should vanish immediately<br>• A person switches phones, and their marker should move to the new device<br>• A person walks out of coverage, and their marker should fade and then be removed | **unsure** | • 'Progressively' and 'eventually' have no timings, so stale and live markers are indistinguishable<br>• During a device switch nothing rules out a moment with two markers, or none, for the same person | `medium` |

**Why the emotion moves the way it does**

- **uncertain** (Bring the site up on the dashboard): Two inputs the operator depends on, which site they are looking at and where the anchor placement comes from, are undefined before anything is visible.
- **watchful** (Confirm every anchor is up): Status is specified, but 'health' is undefined and there is no alerting, so the operator has to keep looking.
- **reassured** (Watch people appear as they log in): This is the most fully specified moment in the RFQ (login, marker appears, several people at once) and the first visible proof that the system works.
- **confident** (Follow someone across the floor): Handover is specified as automatic and continuous. The latency and accuracy gaps only bite when something looks off, which is the next stage.
- **doubtful** (Explain a marker that looks wrong): The evidence exists (anchor, RSSI, phone list, raw stream) but has to be assembled by hand, and nothing separates a device fault from an anchor fault.
- **anxious** (Fix an anchor or push an update): This is the only stage that changes live hardware, with no permission model and no stated effect on the people currently being tracked.
- **unsure** (Account for someone who has gone): Logout has a rule ('immediately'); leaving coverage does not ('progressively', 'eventually'), so one of the three exits is undefined.

The shape is the finding. Confidence peaks at the two moments the RFQ specifies best (people appearing, following them across the floor), then falls through *doubtful* to *anxious* at the two moments it barely specifies at all, which are explaining a bad reading and changing live hardware. Those two are the `high` drop-off stages.

---

## How Might We

1. **How might we let an operator see who is where on the floor without the vendor's platform ever holding who that person is?**
   *Derived from:* Watch people appear as they log in: showing the logged-in user's identity conflicts with keeping PII out of the platform (theme: Identity is wanted on screen but kept out of the platform)

2. **How might we make it unmistakable whether a person on the map is present now, fading out of range, or already gone?**
   *Derived from:* Account for someone who has gone: 'progressively' and 'eventually' have no timings, so stale and live markers are indistinguishable (theme: The map must show only who is really there, right now)

3. **How might we help an operator tell a bad reading for one person from a failing anchor before they act on either?**
   *Derived from:* Explain a marker that looks wrong: evidence split across map, anchor list, RSSI and raw stream; nothing separates a bad reading from a drifting anchor (themes: Operators check a position by reading the raw signal behind it; Operators watch infrastructure health and reach in to change it)

4. **How might we give an operator confidence that changing a live anchor will not silently interrupt tracking for the people on it?**
   *Derived from:* Fix an anchor or push an update: no permission model, and the effect on tracking during a change or OTA update is unspecified (theme: Operators watch infrastructure health and reach in to change it)

5. **How might we let an integrator learn that the location stream or the SDK config feed has stopped before anyone on the floor notices tracking is gone?**
   *Derived from:* Customer-Cloud Integrator frustration: nothing specifies how a failed subscription or config endpoint becomes visible (theme: The customer cloud subscribes and hosts config, and never feeds the platform)

**Not covered by an HMW:** whether the tracked employee knows when, and by whom, they are visible. It is the largest gap in Stage 1, but the RFQ holds no evidence of what that person needs, so framing it here would be invention. It is carried as a research question into Stage 6.

---

## Gate result

**Tier 1 — structural: PASS.** `ux-pipeline/validators/strategy.py` returned 0 errors with the Stage-1 artifact as `synthesized_insights`. All 8 `grounded_in` entries resolve to Stage-1 themes, and every persona quote is a verbatim Stage-1 quote.

**Tier 2 — rubric: 4.0 / 5 — PASS on attempt 2.** Attempt 1 scored 3.65 and failed: `journey_realism` was 3 because the emotions had no stated basis and the journey did not admit it was a specified flow rather than a current state. The retry tied each emotion to its evidence and labelled the journey honestly.

| Dimension | Weight | Score | Note |
|---|---|---|---|
| `persona_grounding` | 0.30 | 4 | Every goal and frustration traces to a named theme, and no demographics, tools or habits were added. Not a 5: these are roles, not people. The stress cases in the Site Operator's context (a live demo, an unfamiliar site, keyboard or screen-reader use) are design obligations rather than traits the RFQ establishes, and they are labelled as such. |
| `hmw_quality` | 0.35 | 4 | All five are friction-framed and solution-neutral, and each admits several answers. HMW 1, for example, could be answered by client-side identity resolution, a customer-hosted dashboard, or pseudonymous markers revealed on demand. Not a 5: HMWs 3 and 4 both sit on the operator's drill-down and could converge in ideation. |
| `journey_realism` | 0.35 | 4 | The stages are specific to this product and use the RFQ's own terms (OTA, store computer, out of range), and the emotion has a shape with a stated basis. Capped below 5 because the affect is anticipated rather than observed, and the journey is a specified future flow, not a current state. |
