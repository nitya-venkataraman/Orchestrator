# Discovery Synthesis — DENSO IPS Cloud MVP

**Stage 1 of 6** · Corpus: one client-authored RFQ (*IPS MVP — Cloud Components*, 9 pages). **Requirements-driven run:** there is no user research in this corpus, so every theme below is a stated requirement, not an observed behaviour.

**5 themes** · **source_count: 1** · 19 quotes, each machine-verified as a verbatim substring of the transcribed RFQ.

---

## 1. Identity is wanted on screen but kept out of the platform

`severity: medium` · `stated in 1 of 1 source`

The RFQ asks for two things that pull against each other. The IPS platform must never hold PII — it receives only an anonymous digital identity, and only client servers may map that back to a person — yet the dashboard requirements ask for each tracked device to show the logged-in user's identity. The document has two dashboards (the IPS Dashboard in §1 and the Customer Cloud example dashboard in §3B) and never says which one is allowed to show a real identity. Severity is medium rather than high only because this is one document: the consequence, real identities leaking into the vendor platform, is the most serious risk in the corpus.

**Evidence**

> To preserve PII for clients, the DENSO IPS system obtains an anonymous digital identity from the client cloud.
>
> — Doc-1 — client RFQ author, p.2 ID Management diagram

> Mapping between User Data and Digital ID can only be performed by Client servers.
>
> — Doc-1 — client RFQ author, p.2 ID Management diagram

> For each device, show the logged-in user’s identity, current coordinates, and details of the connected anchor (including signal strength).
>
> — Doc-1 — client RFQ author, §4 Device Tracking

> Associate location data with a user’s identity (via app login) for personalized services and analytics.
>
> — Doc-1 — client RFQ author, §2 Objectives

---

## 2. The map must show only who is really there, right now

`severity: medium` · `stated in 1 of 1 source`

The client defines success through presence rules more than through positioning accuracy. A device appears only while someone is logged in, disappears immediately on logout, moves with its user across a device switch, fades out when it leaves coverage, and stays continuous across an anchor handover. Five of the RFQ's demo scenarios test this lifecycle, so failing any of them fails acceptance, and that is why severity is medium. The latency target that bounds it is garbled in the source ('between 1 seconds'), and 'progressively' and 'eventually' are never given a duration.

**Evidence**

> Only logged-in devices (phones) should be tracked and displayed.
>
> — Doc-1 — client RFQ author, §4 Device Tracking

> A phone that logs out should immediately disappear from the dashboard.
>
> — Doc-1 — client RFQ author, §5D User Logout

> If a user logs out from one device and logs in on another, the system must reflect the change by removing the marker from the first device and showing it on the new device.
>
> — Doc-1 — client RFQ author, §5D Single User Switching Devices

> the system should progressively lose the connection and eventually remove the user’s marker from the dashboard.
>
> — Doc-1 — client RFQ author, §5D User Moves Out of Range

> The system must display updates with an overall latency between 1 seconds as a phone moves through the physical space.
>
> — Doc-1 — client RFQ author, §4 Data Flow & Latency

---

## 3. Operators watch infrastructure health and reach in to change it

`severity: medium` · `stated in 1 of 1 source`

The dashboard is expected to be an operations console as well as a map. Anchors and the store computer each show live connectivity and health, anchors also show firmware version, and clicking either opens configuration that can be changed, including calibration and over-the-air updates. A dead anchor or a disconnected store computer stops tracking for its whole area, so this blocks the core task and is medium on a single source. The RFQ does not say who may make these changes, or what happens to a site while an OTA update runs.

**Evidence**

> Display real-time anchor statuses (Online/Offline, health, firmware version).
>
> — Doc-1 — client RFQ author, §3A Remote Monitoring

> Provide a system status panel to show the connectivity status of the store computer.
>
> — Doc-1 — client RFQ author, §3A Remote Monitoring

> Allow users to click on an anchor or store computer to view and modify configuration settings (e.g., for calibration, OTA updates).
>
> — Doc-1 — client RFQ author, §4 Anchor and Store Computer Status

---

## 4. Operators check a position by reading the raw signal behind it

`severity: low` · `stated in 1 of 1 source`

Beyond the marker on the map, the client wants to see why the system placed a device there: which anchor it is connected to, the RSSI, each anchor's list of connected phones, and a live text feed of the raw coordinate stream. This is a separate need from health monitoring (theme 3). That theme asks whether the hardware is up; this one asks whether a specific reading can be trusted. It costs time and trust rather than blocking anything, so it is low on a single source. It may be a demo and commissioning need more than a day-to-day one, which the RFQ does not distinguish.

**Evidence**

> Allow users to view detailed telemetry including anchor-to-device connections and RSSI values.
>
> — Doc-1 — client RFQ author, §3B Dashboard Integration

> Each anchor should list all the phones currently connected to it.
>
> — Doc-1 — client RFQ author, §4 Device Tracking

> Provide a text-based overlay or side panel showing raw streaming data (timestamp, user/device ID, coordinates, anchor details).
>
> — Doc-1 — client RFQ author, §4 Streaming Data View

---

## 5. The customer cloud subscribes and hosts config, and never feeds the platform

`severity: medium` · `stated in 1 of 1 source`

The data paths run one way. Only the store computer may send data into the IPS Cloud, and the SDK never does. The customer cloud subscribes to the location stream for logged-in users, stores it for its own analysis, and hosts the remote configuration the SDK downloads at login, since the app ships with no anchor data. If either path fails, the system cannot track anyone: there is no stream to display and no config to start the SDK. That blocks the task, so severity is medium on a single source. The RFQ never says how an integrator would see that a subscription or a config endpoint has failed.

**Evidence**

> The IPS Cloud must ingest data solely from the store computer, ensuring the SDK does not send data directly to the cloud.
>
> — Doc-1 — client RFQ author, §4 Data Ingestion

> Subscribe to the streaming events from the DENSO IPS Cloud for all logged-in users.
>
> — Doc-1 — client RFQ author, §3B Data Subscription & Processing

> Host and serve remote configuration data for the SDK.
>
> — Doc-1 — client RFQ author, §3B Remote Configuration Hosting

> No pre-loaded anchor information exists on the app.
>
> — Doc-1 — client RFQ author, §5A Configuration Loading

---

## Corpus

- **Method:** Desk review of one client-authored Request for Quote: 9 pages of requirements prose, two architecture diagrams (ID management, PKI hierarchy) and a floor-plan mock-up. There were no interviews, no observation and no usage data. Quotes come from the document's text layer and its diagram text.
- **Participants:** 1
- **Segments:** Client product and engineering team, the RFQ author: buyer-side requirements only, with no operator, integrator or end-user voice
- **Collection window:** RFQ received on or before 2026-10-15; authoring date not stated

**Known bias**

- An RFQ states what a buyer wants to be quoted for, not what anyone does today. Each theme here is a stated requirement, not an observed behaviour, and the reasons behind requirements are almost never given.
- The whole document is shaped around a demo. Section 5 is a demo script, and the demo-scenario framing over-represents what is visible in a sales walkthrough (markers appearing and disappearing) relative to what an operator lives with daily (alerts, stale data, permissions, multi-site).
- One author means each frequency is 1 of 1. Frequency here cannot separate a strongly held need from a passing line, so severity has been derived on the 'one or two participants' row, with consequence stated in each insight.
- The example customer is an airline. Requirements may be tuned to that one environment and may not generalize to the manufacturing and retail markets the RFQ also names.

---

## Gaps — what this corpus cannot tell us

1. There is no user voice in this corpus. The only source is a buyer-side RFQ. No dashboard operator, site administrator, customer-cloud integrator or tracked employee has been interviewed or observed, so every persona in Stage 2 is a role inferred from the document, not a person found in research.
2. Nobody is named as the dashboard's user. The RFQ says 'users' can click anchors and change configuration but never says who they are: facility operations, airline IT, DENSO field engineers or a demo presenter. Each would need a different information density and different permissions.
3. The RFQ describes two dashboards, the IPS Dashboard (§1) and the Customer Cloud example dashboard (§3B), with near-identical feature lists. It does not say whether they are one product, or who sees which. This decides where the identity conflict in theme 1 is resolved.
4. The people being tracked are absent. The RFQ tracks employees indoors by identity at a global airline and says nothing about consent, notice, retention, or how a tracked person sees what is recorded about them. Logout is the only control it gives them. This is the largest unaddressed risk in the document. SOC2 is mentioned only as a future enhancement, and no jurisdiction-specific privacy regime is mentioned at all.
5. The latency requirement is garbled ('an overall latency between 1 seconds'). The bound, and whether it is end-to-end or cloud-only, have to be confirmed with the client before anything is designed against it.
6. No timings are given for 'immediately disappear', 'progressively lose the connection' or 'eventually remove'. How a fading or stale marker should look, and when it should go, is undefined.
7. No scale figures: sites, floors, anchors per site, concurrent tracked users, operators. Every Stage-3 reach figure will be an assumption, and so will any floor-plan design decision about density.
8. The PKI hierarchy (root CA, customer intermediate CA, site intermediate CA, per-user digital ID) is specified as architecture. Who manages certificates, how one is revoked, and whether any person ever does that through a UI is not stated.
9. The diagram names 'Store Historical Data', 'Build Dashboards', 'Account Management' and 'Integration with SaaS Partners' as platform offers, but the body text never asks for them. It is unclear whether they are in MVP scope.
10. The demo mobile app is specified in detail (login, welcome message, config download), but the SDK is out of scope and the RFQ covers cloud components only. Who builds the demo app is not stated.
11. There is no multi-site story. The PKI diagram has a 'Site Intermediate CA' and a site called 'Area 50', which implies more than one site, but the dashboard requirements describe one floor plan with one store computer.
12. No positioning accuracy target is given, only latency. 'Accurately locate' appears without a figure.
13. Asset-tag tracking is deferred to a later update. Nothing here should be designed around it, but the floor plan's marker model should not rule it out.

---

## Gate result

**Tier 1 — structural: PASS.** `ux-pipeline/validators/synthesis.py` returned 0 errors with the transcribed RFQ supplied as `raw_research_data`; all quotes are verbatim substrings.

**Tier 2 — rubric: 4.0 / 5 — PASS** (`min>=4 or (min>=3 and weighted_mean>=4.0)`)

| Dimension | Weight | Score | Note |
|---|---|---|---|
| `evidence_grounding` | 0.40 | 4 | Every insight is a close read of its quotes, and the reasons the RFQ does not give are left as gaps. Not a 5: theme 2's framing that success is defined by presence rules over accuracy is a reading of emphasis rather than a statement in the document, and theme 4's demo-vs-daily-use caveat is a labelled hypothesis. |
| `theme_distinctness` | 0.25 | 4 | Themes 3 and 4 are adjacent, since both are drill-downs from the map. They stay separate because they answer different questions (is the hardware up, versus can this reading be trusted) and would be solved with different panels. A reviewer could fairly merge them. |
| `signal_coverage` | 0.35 | 4 | The most severe signal in the source, the PII-vs-identity conflict, leads as theme 1. Every requirement section lands in a theme or a gap. Not a 5: PKI token exchange is covered only as one strand of theme 1 and as a certificate-management gap, not as its own theme, because no person-facing behaviour is specified for it. |
