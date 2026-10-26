# Wireframes & IA — DENSO IPS Cloud MVP

**Stage 4 of 6** · **Target:** web (1440 / 1280 / 768 / 375) · **Design system:** Material 3, *baseline* (none supplied) · **Direction:** B + C, *One pane, names resolved at the glass* + *The system watches itself* · **Validator:** Tier-1 PASS, 0 errors

**Figma:** not rendered. No Figma connection is available in this session, so `figma_file_url` is `null`. The spec is complete and can be rendered to the EPAM Pro team once Figma is connected.

---

## UX interpretation

| | |
|---|---|
| **Primary user** | Site Operator — whoever watches the IPS dashboard for a site and adjusts its anchors (role inferred from the RFQ; facility operations, airline IT, field engineer or demo presenter is still open) |
| **User goal** | Trust that the floor shows exactly who is present now, explain any reading that looks wrong, and keep the anchors working without interrupting the people being tracked |
| **Business goal** | Demonstrate the IPS MVP's core value (accurate indoor location tied to a logged-in identity, plus live system status) to the airline example customer, while proving that the vendor platform never holds PII |
| **Main task** | Watch the live floor, drill from a suspicious marker to the reading and the anchor behind it, and recalibrate or update that anchor safely |
| **Context** | An operations or demo setting on one site (the pilot is a single room with four corner anchors), often with the client watching. Positions update roughly every second. Names come from the customer's systems, never from the vendor's. |
| **Entry point** | 01 - Sign In through the customer's identity provider, landing on 02 - Live Floor |
| **Expected outcome** | The operator can say who is on the floor and where with confidence, can tell a bad reading from a bad anchor, and can change an anchor without anyone silently losing tracking |

**Business rules (from the RFQ)**

- Only logged-in devices are tracked and displayed (RFQ §4)
- A logged-out device disappears immediately (RFQ §5D)
- A user switching devices shows on the new device only (RFQ §4, §5D)
- A user leaving coverage fades and is then removed, and returning restores them (RFQ §5D)
- The IPS platform never holds PII; mapping from digital ID to person happens only on customer servers (RFQ ID Management)
- The IPS Cloud ingests data only from the store computer (RFQ §3A, §4)
- Anchor and store-computer configuration is viewable and modifiable from the dashboard (RFQ §4)

**Constraints**

- Overall latency target as stated in the RFQ ('between 1 seconds', bound to be confirmed)
- SDK, store-computer software and anchor firmware are out of scope, so staged OTA and rollback depend on teams outside this RFQ
- Web only for this stage; the demo phone app is not wireframed

**Dependencies**

- Customer identity provider for operator sign-in
- Customer identity service exposing signed digital-ID resolution
- Store computer streaming positions and equipment status
- Anchor firmware reporting post-update health

---

## User flow

**Primary journey**

1. 01 - Sign In: operator signs in through the customer IdP; names policy and roles are loaded
2. 02 - Live Floor: operator sees anchors and live people; system status chips are green
3. 02 - Live Floor: a person's marker looks wrong; operator opens them
4. 03 - Person Detail: verdict says only one anchor hears this phone strongly; signal chart shows Anchor NE weak for everyone
5. 05 - Equipment Detail: drift card says phones near Anchor NE are placed 2.4 m off their neighbours' estimate
6. 06 - Change Settings: editor adjusts calibration and checks the impact preview (3 phones, all covered by neighbours)
7. 05 - Equipment Detail: calibration applied; snackbar offers revert
8. 02 - Live Floor: the person's marker settles; operator returns to watching

**Supporting tasks**

- Review site health and drift flags (04)
- Run a staged firmware update and monitor it (06, 07)
- Reveal one person's name with a reason under the anonymous-ID policy (03)
- Find out how and when someone left the floor (08)
- Search for one person on a busy floor (02)

**Error scenarios**

- The store computer goes offline and markers freeze (02 error, 04 edge case)
- The customer identity service is down and names degrade to anonymous IDs (01, 02, 03)
- An anchor fails verification during a rollout, rolls back automatically and the rollout pauses (07 error)
- An anchor disconnects mid-review of a settings change (06 error)
- A person logs out while their detail sheet is open (03 empty)
- Two editors change the same anchor (06 edge case)

---

## Sitemap

```
01 - Sign In   /sign-in
02 - Live Floor   /sites/:siteId/floor
    03 - Person Detail   /sites/:siteId/floor/people/:digitalId
04 - Site Health   /sites/:siteId/health
    05 - Equipment Detail   /sites/:siteId/health/equipment/:equipmentId
        06 - Change Settings   /sites/:siteId/health/equipment/:equipmentId/settings
    07 - Rollout Progress   /sites/:siteId/health/rollouts/:rolloutId
08 - Activity Timeline   /sites/:siteId/activity
```

---

## Pages created

### 01 - Sign In

**Purpose.** Authenticate the operator through the customer's identity provider, establish which site they may see, whether they may change equipment settings, and obtain the signed token the browser uses to resolve names from the customer's identity service.

**Primary action:** `Sign in` · **Secondary:** Get help signing in

**Navigation.** No app chrome. On success, routes to 02 - Live Floor for the operator's default site.

**Content, top to bottom**

1. Product name and environment label (for example 'Pilot')
2. Sign-in panel: a single 'Sign in' button that hands off to the customer identity provider
3. Status line for the hand-off (redirecting, returning, failed)
4. Privacy line: 'This dashboard never stores who people are. Names are fetched from your organisation for this session only.'

**Interactions**

- Sign in redirects to the customer IdP and returns with a session
- On return, the browser requests a signed identity-resolution token; failure to obtain it does not block sign-in, it degrades names to anonymous IDs

**States**

| State | Treatment |
|---|---|
| `default` | Centered card on md.sys.color.surface with the filled 'Sign in' button and the privacy line beneath. |
| `loading` | After return from the IdP the button is replaced by a linear progress bar labelled 'Opening your site…' while roles and the site list load. |
| `empty` | Operator authenticated but holds no site permission: card reads 'Your account isn't assigned to a site yet', names the customer administrator role to contact, and offers one action, 'Sign out'. |
| `error` | IdP hand-off failed or timed out: banner 'Sign-in didn't complete — your organisation's sign-in service didn't respond' with 'Try again'; nothing the operator typed is lost because nothing is typed here. |
| `success` | No interstitial; the operator lands on 02 - Live Floor and a snackbar confirms the site name. |
| `disabled` | While the hand-off is in flight the button shows the Loading variant and ignores repeat clicks, so a double-click cannot start two sessions. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| desktop | Card 400px wide, centred vertically and horizontally on a md.sys.color.surface-container-low field. |
| laptop | Identical to desktop; the card does not scale with the viewport. |
| tablet | Card 400px, centred; the privacy line wraps to two lines. |
| mobile | Card goes full-bleed with md.sys.spacing.edge-margin side insets; button is full width and pinned above the keyboard-safe area. |

**Accessibility (WCAG 2.2 AA)**

| Key | Decision |
|---|---|
| contrast | Button label md.sys.color.on-primary on md.sys.color.primary; privacy line md.sys.color.on-surface-variant on md.sys.color.surface checked at 4.5:1 or better because it is body-size text. |
| keyboard focus | Focus starts on 'Sign in'; Tab reaches 'Get help signing in' next. The focus ring is a 2px md.sys.color.primary outline offset by 2px, never suppressed on mouse use. |
| labels | The button's accessible name is 'Sign in with your organisation', which is more specific than the visible label. The error banner names the failing service in words, not an error code. |
| touch targets | Sign-in button 48px tall at full card width; help link padded to a 44x44px hit area. |
| reading order | h1 product name, then the sign-in panel, then the privacy line. A single h1 and no other headings. |
| status messages | 'Opening your site…' and the sign-in failure are both set in an assertive live region, because each changes what the operator can do next and there is nothing else on the page to read. |
| motion | Under prefers-reduced-motion the indeterminate progress bar is replaced by static text 'Opening your site…' with no sweep. |

**Build requirements**

*Data dependencies*

- `Customer IdP OIDC authorize and token endpoints`
- `POST /v1/sessions` — IPS Cloud API (proposed): exchanges the IdP token for a dashboard session and returns roles + permitted sites
- `POST /v1/identity-tokens` — IPS Cloud API (proposed): returns a short-lived token signed under the customer intermediate CA for browser-side name resolution

*Permissions*

- Any authenticated operator may sign in
- Role 'equipment-editor' is read from IdP claims and governs 06 - Change Settings

*Edge cases*

- Operator's IdP session is valid but the identity-token request fails: sign in succeeds, names degrade to anonymous IDs, and 02 shows the names-unavailable banner
- Operator permitted on more than one site: lands on the most recently viewed site, switchable from the top bar
- Clock skew between browser and token issuer rejects the signed token: retried once with server time, then degraded as above

*Open questions*

- Which identity provider does the customer use, and will it carry an equipment-editor role claim?
- Does the demo require a username/password form (the RFQ's 'JohnDoe / demo123' is the phone app, not the dashboard)?

---

### 02 - Live Floor

**Purpose.** Show exactly who is present on the floor right now, where they are, and whether the system behind that picture is healthy, so the operator can trust or question the map at a glance.

**Primary action:** `Open person` · **Secondary:** Search people, Switch to raw stream, Open anchor, Switch site

**Navigation.** Navigation rail destinations: Live floor (current), Site health, Activity. Selecting a person opens 03 - Person Detail as a side sheet over the floor; selecting an anchor or the store computer opens 05 - Equipment Detail.

**Content, top to bottom**

1. Top app bar: site selector, system status chips (store computer, anchors online n/N, stream heartbeat), operator menu
2. Page-level banner slot (positions frozen, names unavailable, drift suspected) shown only when a condition is active
3. Floor plan canvas: room outline, doors, anchor markers by status, person markers by presence state with name or anonymous ID
4. Right panel with tabs 'People | Raw stream': People is a searchable list (name or ID, presence state, nearest anchor, signal strength label); Raw stream is the live log
5. Legend explaining marker shapes (always visible, collapsible)

**Interactions**

- Markers move as position events arrive; no animation longer than the update interval
- Click or Enter on a marker or list row opens 03 for that person
- Click or Enter on an anchor marker or the store-computer chip opens 05
- '/' focuses people search; results filter the list and highlight matching markers
- Tab 'Raw stream' swaps the people list for the stream log in the same panel, rather than adding a third column
- Legend toggles open and closed; its state persists per operator

**States**

| State | Treatment |
|---|---|
| `default` | Floor plan fills the canvas with anchors at the four corners (pilot layout) and live markers; People tab lists everyone present, sorted by name or ID. |
| `loading` | Canvas shows the room outline from cached geometry with anchor markers as skeleton triangles, and the people list shows six skeleton rows. The top bar status chips read 'Connecting…' until the first live event arrives. |
| `empty` | Live data is flowing but nobody is logged in on this floor: the canvas shows anchors only, and the list reads 'Nobody is being tracked on this floor. People appear here when they sign in to the app.' Its one action is 'View recent activity' (to 08). |
| `error` | The store computer stops sending: every marker switches to the Frozen variant (hatched) at its last position, the list's presence column reads 'Frozen', and the banner reads 'Positions frozen since 10:42:07 — the store computer is offline. People may have moved.' Its action is 'View site health'. Markers are never left looking live on stale data. |
| `disabled` | When names cannot be resolved, the 'Reveal name' action elsewhere is unavailable and markers show anonymous IDs; the banner explains 'Names unavailable — your organisation's identity service isn't responding. Showing anonymous IDs.' |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| desktop | Navigation rail 80px, canvas flexible, right panel 360px fixed with People and Raw stream tabs; legend docked bottom-left of the canvas. |
| laptop | Same structure as desktop with the right panel at 320px and tighter md.sys.spacing.edge-margin. |
| tablet | Rail stays, the right panel collapses into a standard bottom sheet peeking 96px (count of people present), and the canvas takes the full width; dragging the sheet up reveals the list. |
| mobile | Rail becomes a modal navigation drawer behind a menu icon. A segmented button 'Map | List' leads the page and defaults to List: rows show name or ID, presence state and nearest anchor. Map is full-bleed with pinch and zoom, and the raw stream moves to 03 only. |

**Accessibility (WCAG 2.2 AA)**

| Key | Decision |
|---|---|
| contrast | Marker labels md.sys.color.on-surface on md.sys.color.surface-container-lowest canvas at 4.5:1 or better; marker outlines and anchor glyphs md.sys.color.outline against the canvas at 3:1 or better as non-text UI. Presence and anchor status are encoded by shape plus a text label, never colour alone. |
| keyboard focus | Tab order is top bar, then banner action, then canvas, then right panel tabs, then list. Inside the canvas, arrow keys move between objects in reading order (anchors first by label, then people by name), Enter opens, and Escape returns focus to the canvas container. The focus ring is a 2px md.sys.color.primary outline around the marker's 48px hit area. |
| labels | Each marker's accessible name states the person, state and nearest anchor, for example 'Person 7F3A, live, nearest Anchor NE, signal good'. The canvas has a text alternative: 'Floor plan, DN-20 Atrium, 4 anchors, 3 people present.' The search field has a visible label 'Search people'. |
| touch targets | Person and anchor markers have 48x48px hit areas regardless of drawn size; list rows 56px tall; status chips 32px tall inside a 48px hit area. |
| reading order | h1 is the site and floor name (visually in the top bar), h2 'Floor plan', h2 'People' / 'Raw stream'. The DOM order matches the visual order and has no skipped levels. |
| status messages | People arriving or leaving are summarised in a polite live region at most every 10 seconds ('2 people arrived, 1 left'), so the operator is not interrupted per event. Positions freezing and names becoming unavailable are announced assertively once, because they change what every marker means. |
| motion | Under prefers-reduced-motion markers jump to new positions instead of gliding, the fading state uses a static dashed ring instead of a pulse, and skeleton shimmer is replaced by flat placeholder blocks. |

**Build requirements**

*Data dependencies*

- `GET /v1/sites/{siteId}/floorplan` — IPS Cloud API (proposed)
- `GET /v1/sites/{siteId}/anchors` — IPS Cloud API (proposed): position, status, health, firmware, drift flag
- `WS /v1/sites/{siteId}/live` — IPS Cloud API (proposed): position and presence events for logged-in digital IDs only
- `POST /v1/resolve` — Customer identity service (customer-hosted, proposed): digital IDs to display names, called from the browser with the signed token; never proxied through IPS
- `GET /v1/sites/{siteId}/stream-health` — IPS Cloud API (proposed): store-computer last-seen, heartbeat interval, subscriber count

*Permissions*

- Any operator on the site may view
- Names are shown only when the organisation policy and the identity service both allow; otherwise anonymous IDs

*Edge cases*

- Same person logs in on a second phone before the first logs out: one marker only, on the newest device; the activity timeline records the switch
- A person is between anchors and the stream lags past the latency bound: the marker enters Fading rather than snapping
- Floor plan geometry is missing for a new site: the canvas is replaced by the list view with a banner asking an administrator to upload the plan
- Over 200 people present: markers cluster by anchor with a count badge, and the list stays complete
- WebSocket reconnects: positions are re-synced from a snapshot before deltas resume, so no ghost markers remain

*Open questions*

- What are the fade and remove timings? The RFQ says 'progressively' and 'eventually' without numbers
- Is the latency bound 1 second end-to-end? The RFQ text is garbled ('between 1 seconds')
- Should the map default to names or anonymous IDs on a shared screen in an operations room?

---

### 03 - Person Detail

**Purpose.** Explain one person's position: which anchor they are connected to, how strong the signal is, which other anchors hear them, the raw readings behind the marker and their recent presence history, so the operator can decide whether the reading or the anchor is at fault.

**Primary action:** `Open nearest anchor` · **Secondary:** Reveal name, Pause raw readings, View in activity

**Navigation.** Opens as a side sheet over 02 on desktop and laptop, and as a full page on tablet and mobile with a back arrow. 'Open nearest anchor' goes to 05 carrying this person as context.

**Content, top to bottom**

1. Header: name or anonymous ID, presence state with last-seen age, current coordinates
2. Verdict line: 'Reading looks consistent' or 'Only one anchor hears this phone — position is approximate'
3. Connected anchor card: anchor label, signal strength label with dBm secondary
4. Signal strength chart: per hearing anchor, last 10 minutes, with a 'Show as table' toggle
5. Raw readings: the stream log filtered to this digital ID
6. Recent presence events for this person (last 30 minutes)

**Interactions**

- 'Open nearest anchor' routes to 05 with this person highlighted in the anchor's connected-phones list
- 'Reveal name' (only under the anonymous-ID policy) opens a dialog asking for a reason from a short list plus free text; on confirm the name shows for this session and the reveal is logged
- 'Pause raw readings' freezes the log so rows can be read; a 'Resume' replaces it
- 'Show as table' swaps the chart for a data table of the same series

**States**

| State | Treatment |
|---|---|
| `default` | Header, verdict line, connected anchor card, chart with one line per hearing anchor, the last 50 raw rows, and presence events. |
| `loading` | Header renders immediately from the live state already on 02. The chart area shows a skeleton block of the chart's height, and the raw log and events show four skeleton rows each. |
| `empty` | The person logged out while the sheet was open: content dims and a banner reads 'This person signed out at 10:51:22 and is no longer tracked.' Its one action is 'Back to floor'. No data for a logged-out person stays visible. |
| `error` | Telemetry history failed to load: the chart area reads 'Signal history didn't load — live readings are still shown below' with 'Retry'. Header and raw log stay live. |
| `success` | After a reveal, a snackbar reads 'Name shown for this session. Your reveal was recorded.' and the header updates in place. |
| `disabled` | 'Reveal name' is disabled with the helper text 'Names are unavailable while your organisation's identity service is down' when resolution has failed, and hidden entirely when the policy already shows names. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| desktop | Side sheet 480px wide over the floor plan, which stays visible and keeps the person's marker highlighted. |
| laptop | Side sheet 440px; the chart's height drops from 200px to 160px. |
| tablet | Full page with a top app bar and back arrow. The connected anchor card and verdict sit side by side above the chart. |
| mobile | Full page, single column: header, verdict, anchor card, then the chart defaults to the table view. The raw log is collapsed behind 'Show raw readings'. |

**Accessibility (WCAG 2.2 AA)**

| Key | Decision |
|---|---|
| contrast | Verdict text md.sys.color.on-surface on md.sys.color.surface-container-low at 4.5:1 or better; chart lines are distinguished by md.sys.color.primary, md.sys.color.tertiary and md.sys.color.secondary plus distinct line dashes and end labels, each at 3:1 or better against the chart surface. |
| keyboard focus | When the sheet opens, focus moves to its heading. Tab runs primary action, reveal, chart toggle, log pause, then events. Escape closes the sheet and returns focus to the marker or row that opened it. The reveal dialog traps focus and returns it to 'Reveal name'. |
| labels | Signal strength is shown as words ('Good', 'Fair', 'Weak') with dBm as secondary text, so the label works for an operator who isn't RF-literate. The reveal reason is a required labelled field whose error 'Choose a reason to reveal this name' sits below it. |
| touch targets | All buttons are at least 40px tall inside 48x48px hit areas; chart data points are not targets, and the table view is the interactive equivalent. |
| reading order | h2 person heading (the sheet is a region within 02's h1), h3 'Connection', h3 'Signal history', h3 'Raw readings', h3 'Recent activity'. |
| status messages | The verdict line is a polite live region and announces only when the verdict changes. New raw rows are not announced individually; pausing announces 'Raw readings paused at 10:52:03'. Sign-out while the sheet is open is assertive, because the content is no longer valid. |
| motion | Under prefers-reduced-motion the sheet appears without a slide, and chart lines redraw without easing. |

**Build requirements**

*Data dependencies*

- `GET /v1/sites/{siteId}/devices/{digitalId}/telemetry?window=10m` — IPS Cloud API (proposed): signal strength per hearing anchor
- `GET /v1/sites/{siteId}/stream?digitalId={id}&limit=50` — IPS Cloud API (proposed): raw rows
- `GET /v1/sites/{siteId}/events?digitalId={id}&since=30m` — IPS Cloud API (proposed)
- `POST /v1/resolve` — Customer identity service (customer-hosted, proposed): on reveal
- `POST /v1/audit/reveals` — IPS Cloud API (proposed): records operator, digital ID, reason, timestamp; stores no name

*Permissions*

- Any operator may view a person's telemetry
- Reveal is available to any operator under the anonymous-ID policy and is always logged

*Edge cases*

- Only one anchor hears the phone: verdict states the position is approximate rather than showing false precision
- The person switches device while the sheet is open: the sheet follows the person to the new device and the events list shows the switch
- Telemetry history exists only from the last reconnect: the chart starts at that point with a 'No data before 10:40' marker
- Reveal requested while the identity service is down: blocked with the disabled explanation, never queued

*Open questions*

- Is a logged reason for revealing a name acceptable to the customer's works council or privacy office, or is a stricter policy needed?
- How long should a reveal last: this session, or until the person next logs out?

---

### 04 - Site Health

**Purpose.** Show at a glance whether every anchor, the store computer and the outbound customer stream are working, and surface anchors the system suspects are drifting before an operator notices bad readings.

**Primary action:** `Open equipment` · **Secondary:** Filter by status, View active rollout

**Navigation.** Rail destination 'Site health'. A row or summary card opens 05 - Equipment Detail. The rollout strip opens 07 - Rollout Progress.

**Content, top to bottom**

1. Summary cards: store computer (connected, last data received), anchors online (n of N), drift suspected (count), customer stream (heartbeat last sent, subscribers connected)
2. Active rollout strip if a staged update is running (links to 07)
3. Equipment table: label, type, status, health, firmware, connected phones, drift flag, last seen

**Interactions**

- Filter chips 'Offline', 'Drift suspected', 'Updating' narrow the table
- Sort by any column
- Row click or Enter opens 05
- The rollout strip opens 07

**States**

| State | Treatment |
|---|---|
| `default` | Four summary cards over a table of five rows for the pilot (four anchors and one store computer), sorted with problems first. |
| `loading` | Summary cards show skeleton values with their labels already rendered, and the table shows five skeleton rows at final row height. |
| `empty` | A site with no equipment registered: the table area reads 'No equipment registered for this site yet. Anchors appear once the store computer reports them.' Its one action is 'View setup guide'. |
| `error` | Health data unavailable: the banner reads 'Equipment status couldn't be loaded — last known status from 10:38 is shown'. Values are shown with a 'Last known' label and the table stays usable. |
| `disabled` | When no rollout is active the rollout strip is absent rather than disabled, so there is nothing to explain. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| desktop | Four summary cards in one row, with a full-width data table below and all eight columns. |
| laptop | Four cards in one row, and the 'last seen' column collapses into the status cell's secondary line. |
| tablet | Cards in a 2x2 grid. The table keeps label, status, drift and phones; the other columns move to a row-expansion panel. |
| mobile | Cards stack as a single column of compact rows, and the table recomposes to a list. Each item shows label, status glyph with text, and drift flag, and tapping it opens 05. |

**Accessibility (WCAG 2.2 AA)**

| Key | Decision |
|---|---|
| contrast | Status text md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; the 'Offline' and 'Drift suspected' treatments use md.sys.color.on-error-container on md.sys.color.error-container plus a distinct glyph and the word itself. |
| keyboard focus | Tab order is summary cards left to right, then filter chips, then table. In the table, arrow keys move between cells in grid mode and Enter on a row opens 05. The focus ring wraps the whole row. |
| labels | The table has a caption 'Equipment on DN-20 Atrium' and column headers marked as headers. The drift flag cell reads 'Drift suspected: readings differ from neighbours', not just an icon. |
| touch targets | Table rows 52px tall, filter chips 32px tall inside 48px hit areas, and summary cards fully clickable at a minimum of 96px tall. |
| reading order | h1 'Site health', h2 'Summary', h2 'Equipment'. The rollout strip, when present, sits between them as an h2 'Update in progress'. |
| status messages | An anchor going offline or a new drift flag is announced politely ('Anchor SW went offline'), throttled to one summary per 15 seconds. The store computer disconnecting is assertive. |
| motion | There is no decorative motion. Under prefers-reduced-motion the rollout strip's progress bar updates in steps rather than animating. |

**Build requirements**

*Data dependencies*

- `GET /v1/sites/{siteId}/equipment` — IPS Cloud API (proposed)
- `GET /v1/sites/{siteId}/drift` — IPS Cloud API (proposed): per-anchor drift flag with evidence summary
- `GET /v1/sites/{siteId}/stream-health` — IPS Cloud API (proposed)
- `GET /v1/sites/{siteId}/rollouts?status=active` — IPS Cloud API (proposed)
- `WS /v1/sites/{siteId}/equipment-events` — IPS Cloud API (proposed): status changes

*Permissions*

- Any operator on the site may view

*Edge cases*

- Store computer offline: anchor statuses become 'Unknown since 10:42' rather than staying 'Online', because they report through it
- An anchor reports a firmware version no rollout has issued: flagged 'Unexpected firmware'
- Drift check has under 10 minutes of data after a restart: flag column reads 'Checking…' rather than 'OK'
- Customer stream has zero subscribers: the stream card reads 'No customer system is listening' as a warning, not an error

*Open questions*

- What does 'health' measure beyond online/offline? The RFQ requires it but does not define it
- Should drift detection alert anyone, or only display? Notifications are out of MVP scope in the RFQ

---

### 05 - Equipment Detail

**Purpose.** Show everything about one anchor or the store computer — status, health, firmware, the phones connected to it, and the drift evidence — so the operator can decide whether it needs recalibration or an update.

**Primary action:** `Change settings` · **Secondary:** View on floor, View setting history

**Navigation.** Breadcrumb 'Site health › Anchor NE'. 'Change settings' opens 06. 'View on floor' returns to 02 with this anchor selected.

**Content, top to bottom**

1. Header: equipment label and type, status with text, firmware version, last seen
2. Context chip if arriving from 03: 'From Person 7F3A' with that person highlighted below
3. Drift card (anchors only): verdict sentence with evidence, for example 'Phones near this anchor are placed 2.4 m from where neighbouring anchors place them, over the last 10 minutes', and what usually fixes it
4. Connected phones list: name or ID, signal strength label, time connected
5. Current settings summary (read-only)
6. Setting history: last five changes with who, when and a revert action

**Interactions**

- 'Change settings' opens 06 for this equipment (shown only to equipment editors)
- 'View on floor' returns to 02 with this anchor focused
- A phone row opens 03 for that person
- 'Revert' on a history row opens a confirmation naming the change being undone and the phones connected now

**States**

| State | Treatment |
|---|---|
| `default` | Header, drift card (if flagged; otherwise a one-line 'Readings agree with neighbouring anchors'), connected phones, settings summary, history. |
| `loading` | The header renders from 04's row data. The drift card, phones list and history each show skeleton blocks at final height. |
| `empty` | No phones connected: the list reads 'No phones are connected to this anchor right now.' with one action, 'View on floor'. No history yet: 'No setting changes since installation.' |
| `error` | Equipment unreachable: the banner reads 'Anchor NE hasn't reported since 10:31. Settings can't be changed until it reconnects.' Its action is 'View site health'. 'Change settings' becomes disabled. |
| `success` | After a revert, a snackbar reads 'Settings reverted to 10:05 configuration' with 'View history', and the history list gains the revert entry. |
| `disabled` | 'Change settings' is disabled with the helper text 'You can view settings but not change them. Ask an equipment editor.' for operators without the role, and 'Anchor offline — reconnect to change settings' when unreachable. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| desktop | Two columns: left 2/3 holds the header, drift card and connected phones; right 1/3 holds the settings summary and history. |
| laptop | Two columns at 60/40, with the history truncated to three rows and a 'Show all' link. |
| tablet | Single column ordered header, drift, phones, settings, history. The primary action stays in the header. |
| mobile | Single column. The primary action moves to a full-width button pinned at the bottom above the safe area. History is collapsed behind 'Setting history (5)'. |

**Accessibility (WCAG 2.2 AA)**

| Key | Decision |
|---|---|
| contrast | Drift card text md.sys.color.on-tertiary-container on md.sys.color.tertiary-container at 4.5:1 or better; the 'Drift suspected' state also carries an exclamation glyph and the words, so colour is not the signal. |
| keyboard focus | Tab order is breadcrumb, primary action, 'View on floor', context chip, drift card link, phone rows, history revert buttons. The revert dialog traps focus, puts initial focus on 'Cancel' (the safe choice), and returns focus to the revert button. |
| labels | Each revert button names its change ('Revert calibration change from 10:05'). A disabled 'Change settings' exposes its reason through aria-describedby pointing at the helper text. |
| touch targets | Phone rows 56px; revert buttons are text buttons padded to 44x44px; the pinned mobile button is 48px tall. |
| reading order | h1 equipment label, h2 'Drift check', h2 'Connected phones', h2 'Settings', h2 'Setting history'. |
| status messages | The connected-phones count is a polite live region ('3 phones connected'). The anchor going offline while open is assertive, because it disables the primary action. A revert result is announced politely with the snackbar. |
| motion | There is no motion beyond list updates. Under prefers-reduced-motion new phone rows appear without a slide-in. |

**Build requirements**

*Data dependencies*

- `GET /v1/sites/{siteId}/equipment/{equipmentId}` — IPS Cloud API (proposed)
- `GET /v1/sites/{siteId}/equipment/{equipmentId}/connections` — IPS Cloud API (proposed)
- `GET /v1/sites/{siteId}/drift/{anchorId}` — IPS Cloud API (proposed)
- `GET /v1/sites/{siteId}/equipment/{equipmentId}/config/history?limit=5` — IPS Cloud API (proposed)
- `POST /v1/sites/{siteId}/equipment/{equipmentId}/config/revert` — IPS Cloud API (proposed)

*Permissions*

- View: any operator on the site
- Change settings and revert: role 'equipment-editor'

*Edge cases*

- Store computer detail has no drift card and no connected-phones list; it shows per-anchor link status instead
- Revert targets firmware rather than settings: offered as a rollout (06) because a firmware downgrade is an OTA, not a settings write
- Arriving from 03 for a person who has since moved to another anchor: the context chip reads 'Person 7F3A is now on Anchor SE' with a link

*Open questions*

- Which settings are exposed for calibration (transmit power, angle offsets, position)? The RFQ names calibration without listing parameters
- Is the store computer's configuration changed from the cloud at all in the MVP?

---

### 06 - Change Settings

**Purpose.** Let an equipment editor change calibration settings or start a firmware update with a clear preview of who is affected, and with a rollout plan that keeps every tracked person covered.

**Primary action:** `Review and apply` · **Secondary:** Cancel, Choose rollout plan

**Navigation.** Breadcrumb 'Site health › Anchor NE › Change settings'. 'Cancel' returns to 05 without changes. A firmware apply lands on 07; a calibration apply returns to 05 with a success snackbar.

**Content, top to bottom**

1. Header: equipment label, current firmware, current settings
2. Change type: 'Calibration settings' or 'Firmware update' (radio)
3. Settings form (calibration) or firmware version picker (update)
4. Impact preview: phones connected now, the neighbouring anchors that will cover them, and any phone with no other covering anchor
5. Rollout plan (firmware only): staged by default, one anchor at a time while neighbours cover; 'All at once' available only when nobody is present
6. Review step: summary of change, impact, plan; 'Apply' confirm

**Interactions**

- Choosing 'Firmware update' reveals the version picker and rollout plan; choosing 'Calibration settings' reveals the settings form
- The impact preview recomputes live as people move and shows the time it was computed
- 'Review and apply' opens a review dialog repeating the change, the affected phones and the plan; 'Apply' writes
- If the preview shows phones with no other coverage, 'Apply' stays available but requires ticking 'I understand 2 people will lose tracking for about 90 seconds'

**States**

| State | Treatment |
|---|---|
| `default` | Calibration settings selected, the form prefilled with current values, the impact preview listing connected phones and their covering neighbours. |
| `loading` | Form fields render with current values. The impact preview shows three skeleton rows labelled 'Checking who would be affected…'. |
| `empty` | Nobody is connected to this anchor: the impact preview reads 'Nobody is connected to this anchor — the change won't interrupt tracking.' 'All at once' becomes available. |
| `error` | Apply rejected by the cloud (for example the anchor went offline mid-review): the dialog closes, the banner reads 'Settings weren't applied — Anchor NE disconnected. Nothing was changed.', and form values are kept for retry. |
| `success` | Calibration: returns to 05 with the snackbar 'Calibration applied to Anchor NE' and a 'Revert' action. Firmware: routes to 07 showing the rollout starting. |
| `disabled` | 'Review and apply' is disabled until a value differs from the current configuration, with helper text 'Change a setting to continue'. The 'All at once' radio is disabled with 'Only available when nobody is on the floor' while anyone is present. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| desktop | Two columns: the form on the left (2/3) and a sticky impact preview card on the right (1/3) that stays visible while editing. |
| laptop | Same two columns at 60/40. |
| tablet | Single column with the impact preview directly under the change type, above the form, so it is read before editing. |
| mobile | Single-column form with stacked full-width actions at the bottom. The impact preview is a collapsible card, expanded by default and showing the count in its header ('3 phones affected'). |

**Accessibility (WCAG 2.2 AA)**

| Key | Decision |
|---|---|
| contrast | Form labels md.sys.color.on-surface and helper text md.sys.color.on-surface-variant on md.sys.color.surface at 4.5:1 or better; the 'loses tracking' warning uses md.sys.color.on-error-container on md.sys.color.error-container with a warning glyph. |
| keyboard focus | Tab order is change type radios, then form fields, then rollout plan, then 'Review and apply', then 'Cancel'. The review dialog opens with focus on its heading, Tab cycles inside it, and Escape cancels back to the form with values intact. |
| labels | Every field has a visible label and unit ('Transmit power (dBm)'). Out-of-range values show an inline error naming the allowed range below the field and are announced on blur. The acknowledgement checkbox's label states the people and duration. |
| touch targets | Radios and checkbox have 48x48px hit areas; slider thumb 44px with arrow-key steps; action buttons 40px tall inside 48px hit areas. |
| reading order | h1 'Change settings for Anchor NE', h2 'What to change', h2 'Who this affects', h2 'Rollout plan', then actions. |
| status messages | When the impact preview recomputes and its count changes, a polite live region announces it ('Now 4 phones affected'). An apply failure is assertive. Success is announced on the destination page. |
| motion | Under prefers-reduced-motion the preview card does not animate its height when people are added or removed, and the dialog appears without a scale transition. |

**Build requirements**

*Data dependencies*

- `GET /v1/sites/{siteId}/equipment/{equipmentId}/config` — IPS Cloud API (proposed)
- `GET /v1/firmware?model={model}` — IPS Cloud API (proposed)
- `POST /v1/sites/{siteId}/equipment/{equipmentId}/impact` — IPS Cloud API (proposed): returns affected phones and coverage gaps
- `PUT /v1/sites/{siteId}/equipment/{equipmentId}/config` — IPS Cloud API (proposed): calibration write, returns change id
- `POST /v1/sites/{siteId}/rollouts` — IPS Cloud API (proposed): firmware rollout with plan

*Permissions*

- Role 'equipment-editor' only; other operators reaching the URL see 05 with the disabled explanation

*Edge cases*

- People move while the review dialog is open: the dialog shows 'Updated 4s ago' and re-confirms if the count of uncovered people rises
- Two editors change the same anchor: the second apply is rejected with 'Anchor NE was changed by another editor at 10:47 — review their change first'
- Firmware version older than the installed one: labelled 'Downgrade' and requires the acknowledgement checkbox
- Staged rollout requested on a site where an anchor has no neighbour coverage: that anchor is scheduled last and flagged

*Open questions*

- Staged rollout and automatic rollback depend on the store computer and anchor firmware, which this RFQ puts out of scope. Can those teams support them?
- How long does an OTA take per anchor? The '90 seconds' in the acknowledgement copy is a placeholder until this is known

---

### 07 - Rollout Progress

**Purpose.** Track a staged firmware update anchor by anchor, show who is covered while each anchor is down, and let the operator pause or stop and roll back at any point.

**Primary action:** `Pause rollout` · **Secondary:** Stop and roll back, Resume rollout, Back to site health

**Navigation.** Breadcrumb 'Site health › Update to 2.4.1'. Reached from 06 on apply, or from the rollout strip on 04.

**Content, top to bottom**

1. Header: firmware version, started by and at, overall progress
2. Rollout tracker: one step per anchor with state (waiting, updating, verifying, done, rolled back) and the covering anchors during its update
3. Coverage line: 'Everyone stayed tracked' or 'Person 2B91 lost tracking for 40s at 10:58'
4. Event log for this rollout

**Interactions**

- 'Pause rollout' finishes the anchor currently updating, then holds
- 'Resume rollout' continues from the next anchor
- 'Stop and roll back' opens a confirmation listing the anchors that will revert; on confirm, updated anchors revert one at a time
- An anchor that fails verification rolls back automatically and the rollout pauses itself

**States**

| State | Treatment |
|---|---|
| `default` | Tracker with completed anchors marked done, one updating, the rest waiting. Overall progress 'Anchor 2 of 4'. |
| `loading` | The header renders from the rollout id. The tracker shows four skeleton steps at final height. |
| `empty` | Rollout id not found (an old link): the page reads 'This update isn't running any more.' Its one action is 'Back to site health'. |
| `error` | An anchor failed verification and rolled back automatically: the tracker marks that step 'Rolled back — didn't come back healthy', the rollout pauses, and the banner reads 'Update paused: Anchor SW reverted to 2.3.0. Other anchors are unaffected.' 'Resume' and 'Stop and roll back' both stay available. |
| `success` | All anchors done: the banner reads 'All 4 anchors updated to 2.4.1. Everyone stayed tracked.' Its action is 'Back to site health'. |
| `disabled` | 'Pause rollout' becomes 'Pausing…' (disabled) until the current anchor finishes, with helper text 'Finishing Anchor NE before pausing'. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| desktop | Vertical tracker in a centred 720px column, with the event log in a right column. |
| laptop | Same layout; the event log narrows to 320px. |
| tablet | Single column with the event log below the tracker. Actions stay in the header. |
| mobile | Single column. The tracker compresses each step to one line (anchor label and state) with an expand control, and the actions stack full-width at the bottom. |

**Accessibility (WCAG 2.2 AA)**

| Key | Decision |
|---|---|
| contrast | Step labels md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; done, updating and rolled-back steps differ by glyph (check, rotating arc, undo arrow) and by text, and the md.sys.color.primary and md.sys.color.error accents are secondary. |
| keyboard focus | Tab order is primary action, then 'Stop and roll back', then each tracker step's expand control, then the event log. The stop dialog opens with focus on 'Keep updating' (the safe option); Escape cancels. |
| labels | Each step's accessible name is the anchor and its state ('Anchor NE, updating, covered by Anchor N and Anchor E'). The stop dialog names the anchors that will revert. |
| touch targets | Action buttons 40px tall inside 48px hit areas; step expand controls 48x48px. |
| reading order | h1 'Updating to 2.4.1', h2 'Progress', h2 'Coverage', h2 'Events'. |
| status messages | Each step completing is announced politely ('Anchor NE updated'). An automatic rollback and pause is announced assertively, because the operator must decide what to do next. |
| motion | The updating step's rotating arc stops under prefers-reduced-motion and is replaced by the static text 'Updating'. |

**Build requirements**

*Data dependencies*

- `GET /v1/sites/{siteId}/rollouts/{rolloutId}` — IPS Cloud API (proposed)
- `WS /v1/sites/{siteId}/rollouts/{rolloutId}/events` — IPS Cloud API (proposed)
- `POST /v1/sites/{siteId}/rollouts/{rolloutId}/pause` — IPS Cloud API (proposed)
- `POST /v1/sites/{siteId}/rollouts/{rolloutId}/resume` — IPS Cloud API (proposed)
- `POST /v1/sites/{siteId}/rollouts/{rolloutId}/abort` — IPS Cloud API (proposed): aborts and rolls back updated anchors

*Permissions*

- View: any operator on the site
- Pause, resume, stop: role 'equipment-editor'

*Edge cases*

- The operator closes the browser mid-rollout: the rollout continues server-side and the strip on 04 shows it to whoever opens the site next
- The store computer disconnects mid-rollout: the rollout pauses automatically, because anchor verification cannot be read
- Rollback itself fails for one anchor: that step is marked 'Needs attention — couldn't revert' with the anchor's last reported firmware

*Open questions*

- Can anchors report post-update health to drive automatic rollback? This depends on out-of-scope firmware

---

### 08 - Activity Timeline

**Purpose.** Record what happened on the floor and to the equipment — sign-ins, sign-outs, device switches, people leaving coverage, drift flags, settings changes, rollouts, name reveals and stream silences — so the operator can see how someone left or why something changed instead of inferring it from a missing marker.

**Primary action:** `Filter events` · **Secondary:** Search by person, Jump to time, Open related item

**Navigation.** Rail destination 'Activity'. An event's link opens 03 (presence events for someone still present), 05 (equipment), or 07 (rollouts).

**Content, top to bottom**

1. Filter chips: Presence, Equipment, Settings, Stream, Reveals
2. Time range selector (last 15 min, 1 h, today)
3. Event list in reverse chronological order: time, type glyph with text, subject (name or ID, or equipment), description, link to related page

**Interactions**

- Filter chips combine; the result count updates
- Search by name or ID filters to one person
- 'Jump to time' scrolls to the nearest event
- New events insert at the top only when the operator is scrolled to the top; otherwise a 'N new events' chip appears

**States**

| State | Treatment |
|---|---|
| `default` | The last hour of events, all types, newest first. |
| `loading` | Filter chips render immediately and the list shows eight skeleton rows at final height. |
| `empty` | No events match the filters: 'No events in the last hour for these filters.' Its one action is 'Clear filters'. |
| `error` | Event history failed to load: the banner reads 'Activity couldn't be loaded — new events will still appear as they happen' with 'Retry'. |
| `disabled` | The Reveals filter is visible only to roles permitted to see the reveal audit; otherwise it is absent, not disabled. |

**Responsive**

| Breakpoint | Behaviour |
|---|---|
| desktop | Filters and time range in one row above a full-width list with five columns (time, type, subject, description, link). |
| laptop | Same layout; the description truncates to one line and expands on focus. |
| tablet | Filters wrap onto two rows, and list rows become two-line (time and type on top, subject and description below). |
| mobile | Filters move into a horizontally scrollable chip row, time range becomes a menu, and rows are three-line cards. The 'N new events' chip floats above the list. |

**Accessibility (WCAG 2.2 AA)**

| Key | Decision |
|---|---|
| contrast | Event text md.sys.color.on-surface on md.sys.color.surface at 4.5:1 or better; type glyphs md.sys.color.on-surface-variant at 3:1 or better and always paired with the type word. |
| keyboard focus | Tab order is filter chips, then search, then time range, then the 'new events' chip when present, then the list. Each row is one focusable link to its related page, and arrow keys move between rows. |
| labels | Each row reads as one sentence ('10:51:22, presence, Person 7F3A signed out on Pixel 7'). The chips are a labelled group 'Event types'. |
| touch targets | Rows at least 56px; chips 32px tall inside 48px hit areas; the 'new events' chip 40px inside 48px. |
| reading order | h1 'Activity', h2 'Filters', h2 'Events'. Rows are a list, not a table, because they are read in sequence. |
| status messages | When filters change, the result count is announced politely ('42 events'). New events arriving while scrolled are summarised politely by the chip ('3 new events') rather than read individually. |
| motion | Under prefers-reduced-motion new rows appear without sliding in, and the list never auto-scrolls. |

**Build requirements**

*Data dependencies*

- `GET /v1/sites/{siteId}/events?types=&since=&until=&digitalId=` — IPS Cloud API (proposed)
- `WS /v1/sites/{siteId}/events/live` — IPS Cloud API (proposed)
- `POST /v1/resolve` — Customer identity service (customer-hosted, proposed)
- `GET /v1/audit/reveals?siteId=` — IPS Cloud API (proposed)

*Permissions*

- Presence, equipment, settings and stream events: any operator on the site
- Reveal audit: role to be defined by the customer

*Edge cases*

- A person's events after logout show their anonymous ID even under the names policy, because names are resolved only for people currently logged in
- Stream silence longer than one heartbeat interval logs a 'Stream silent' event with its duration once heartbeats resume
- The time range spans a store-computer outage: a single 'Store computer offline 10:42–10:49' event marks the gap instead of an unexplained absence

*Open questions*

- How long are events retained? The RFQ says the customer cloud stores location data, but says nothing about the IPS side
- Should name resolution be allowed for logged-out people in the timeline, or does that defeat 'no longer appear on the dashboard'?

---

## Components used

**25 reused** from Material 3 · **10 new**, each with a reason

| Component | Role | Source | Pages | Why new |
|---|---|---|---|---|
| Component / Assist Chip | Chip | reused | 02, 03, 05 |  |
| Component / Badge | Badge | reused | 02, 04 |  |
| Component / Dialog | Confirmation | reused | 03, 05, 06, 07 |  |
| Component / Divider | Divider | reused | 03, 05, 08 |  |
| Component / Event Row | List | reused | 03, 07, 08 |  |
| Component / Exposed Dropdown Menu | Select | reused | 02, 06, 08 |  |
| Component / Filled Button | Button | reused | 01, 03, 05, 06, 07 |  |
| Component / Filter Chip | Chip | reused | 04, 08 |  |
| Component / Icon Button | Button | reused | 03 |  |
| Component / Linear Progress Indicator | ProgressIndicator | reused | 01, 04, 06, 07 |  |
| Component / List | List | reused | 02, 03, 04, 05, 06, 07, 08 |  |
| Component / Navigation Rail | Navigation | reused | 02, 04, 05, 06, 07, 08 |  |
| Component / Outlined Button | Button | reused | 03, 05, 06, 07 |  |
| Component / Outlined Card | Card | reused | 01, 03, 04, 05, 06 |  |
| Component / Outlined Text Field | Input | reused | 03, 06 |  |
| Component / Plain Tooltip | Tooltip | reused | 02 |  |
| Component / Radio Button | Radio | reused | 06 |  |
| Component / Search Bar | Search | reused | 02, 08 |  |
| Component / Secondary Tabs | Tabs | reused | 02 |  |
| Component / Segmented Button | Tabs | reused | 02 |  |
| Component / Side Sheet | Drawer | reused | 03 |  |
| Component / Slider | Slider | reused | 06 |  |
| Component / Snackbar | Toast | reused | 02, 03, 05, 06, 07 |  |
| Component / Text Button | Button | reused | 01, 05, 08 |  |
| Component / Top App Bar | Header | reused | 02, 04, 05, 06, 07, 08 |  |
| Component / Anchor Marker | Icon | new | 02, 04, 05 | An anchor's status needs four shape-distinct glyphs (filled triangle, outlined triangle with slash, triangle with exclamation, triangle with rotating arc) placed on the canvas; M3 icons are not stateful. |
| Component / Banner | Banner | new | 01, 02, 03, 04, 05, 06, 07, 08 | Material 3 dropped the Material 2 banner but these pages need a persistent, page-level condition (positions frozen, names unavailable) that a transient snackbar cannot carry; rebuilt on the M2 banner anatomy with M3 colour and type tokens. |
| Component / Breadcrumb | Breadcrumb | new | 05, 06, 07 | Material 3 has no breadcrumb component; built from M3 text buttons separated by a chevron icon in md.sys.typescale.label-large, shared by 05, 06 and 07. |
| Component / Data Table | Table | new | 04 | Material 3 ships no data table; anchors and events are multi-column comparable data. Built from M3 list-row anatomy, md.sys.typescale.body-medium and md.sys.color.outline-variant row dividers. |
| Component / Floor Plan Canvas | Chart | new | 02 | No Material 3 component positions live objects on a scaled floor plan. Logged as a design-system gap. |
| Component / Presence Marker | Badge | new | 02 | Encodes presence state by shape and label, not colour: solid disc = live, dashed ring with last-seen age = fading, hatched disc = frozen. No M3 badge or avatar carries a time-based state. Logged as a design-system gap. |
| Component / Rollout Tracker | Stepper | new | 07 | Material 3 has no stepper. Shows staged OTA waves anchor by anchor with per-anchor outcome and rollback. |
| Component / Signal Strength Chart | Chart | new | 03 | Material 3 has no charts. A small line chart of signal strength per hearing anchor over the last 10 minutes, with a data-table equivalent. |
| Component / Skeleton | Skeleton | new | 02, 03, 04, 05, 07, 08 | Material 3 specifies loading indicators but no skeleton placeholder; built from md.sys.color.surface-container-high blocks at the loaded content's exact dimensions so layout never shifts. |
| Component / Stream Log | List | new | 02, 03 | The RFQ requires a raw streaming-data view. An append-only, pausable, monospace log with follow-tail semantics is not an M3 list. Logged as a design-system gap. |

---

## Responsive behaviour

| Component | Desktop | Tablet | Mobile |
|---|---|---|---|
| Navigation Rail | Rail 80px with labels | Rail 80px, icons with labels | Modal navigation drawer behind a menu icon |
| Floor Plan Canvas | Fills the space between rail and 360px right panel | Full width; people list becomes a peeking bottom sheet | Behind a 'Map | List' segmented button, defaulting to List; full-bleed with pinch-zoom when chosen |
| People / Raw stream panel | Right panel 360px with tabs | Bottom sheet peeking 96px with count | List view of the segmented control; raw stream moves to 03 only |
| Person Detail | Side sheet 480px over the floor | Full page with back arrow | Full page, chart defaults to table, raw log collapsed |
| Equipment Data Table | All eight columns | Four columns plus row expansion | Recomposes to a list of status rows |
| Impact preview | Sticky right card beside the form | Placed above the form | Collapsible card, expanded by default, count in header |
| Rollout Tracker | Vertical steps in a 720px column with the log at right | Steps then log, single column | One-line steps with expand controls; stacked actions |
| Primary actions | Inline in page header | Inline in page header | Full-width, pinned above the bottom safe area on 05 and 06; stacked elsewhere |

---

## Accessibility

Every page carries its own seven-key WCAG 2.2 AA block (see each page above). Across the set:

- Seven accessibility keys on every page, each written for that page
- The floor plan has a keyboard model and a text alternative
- Presence and equipment states use shape plus text, never colour alone
- Async results announced with deliberate politeness: frozen positions, names unavailable and rollback are assertive; arrivals, counts and step completion are polite

---

## Prototype

| From | Trigger | To | Interaction |
|---|---|---|---|
| 01 - Sign In | Click 'Sign in' and return from IdP | 02 - Live Floor | Navigate, instant |
| 02 - Live Floor | Click a person marker or People row | 03 - Person Detail | Open overlay: side sheet from right |
| 03 - Person Detail | Click 'Open nearest anchor' | 05 - Equipment Detail | Navigate, carrying person context |
| 03 - Person Detail | Press Escape or close | 02 - Live Floor | Close overlay |
| 02 - Live Floor | Click an anchor marker or store-computer chip | 05 - Equipment Detail | Navigate |
| 02 - Live Floor | Rail: Site health | 04 - Site Health | Navigate, instant |
| 02 - Live Floor | Rail: Activity | 08 - Activity Timeline | Navigate, instant |
| 04 - Site Health | Click an equipment row | 05 - Equipment Detail | Navigate |
| 04 - Site Health | Click the active rollout strip | 07 - Rollout Progress | Navigate |
| 05 - Equipment Detail | Click 'Change settings' | 06 - Change Settings | Navigate |
| 05 - Equipment Detail | Click 'View on floor' | 02 - Live Floor | Navigate, anchor focused |
| 06 - Change Settings | Firmware: 'Review and apply' then 'Apply' | 07 - Rollout Progress | Navigate after dialog confirm |
| 06 - Change Settings | Calibration: 'Review and apply' then 'Apply', or 'Cancel' | 05 - Equipment Detail | Navigate back with snackbar |
| 07 - Rollout Progress | Click 'Back to site health' | 04 - Site Health | Navigate |
| 08 - Activity Timeline | Click an equipment event | 05 - Equipment Detail | Navigate |
| 08 - Activity Timeline | Click a presence event for someone present | 03 - Person Detail | Navigate, open as side sheet over 02 |

---

## Heuristic review

| Heuristic | Page | Severity | Finding | Fix (applied) |
|---|---|---|---|---|
| Visibility of system status | 02 - Live Floor | `high` | When the store computer stopped sending, markers would stay where they were and still look live. An operator would read a frozen floor as people standing still, which is the 'show only who is really there' failure in its worst form. | Added a Frozen marker variant (hatched) that every marker switches to on store-computer loss, a banner stating the freeze time, and an assertive announcement. Anchor statuses on 04 become 'Unknown since…' for the same reason. Spec updated on 02 (error state, components) and 04 (edge cases). |
| Match between system and the real world | 03 - Person Detail | `medium` | The first draft labelled signal as 'RSSI −71 dBm' and the person as 'digital ID'. That is the data model's vocabulary, and the operator role is not known to be RF-literate. | Signal is now shown as 'Good / Fair / Weak' with dBm as secondary text, the ID is labelled 'Anonymous ID', and a verdict sentence states in plain words whether the reading looks consistent. Spec updated on 03 (content structure, labels). |
| User control and freedom | 07 - Rollout Progress | `high` | Once a firmware update started there was no way to stop it, and a calibration change had no way back. These are the two most expensive actions in the product, on live hardware with people being tracked. | Added 'Pause rollout' and 'Stop and roll back' on 07 (stop confirms, with the safe option focused), an automatic pause when an anchor fails verification, and setting history with per-change revert on 05. Spec updated on 05 and 07. |
| Consistency and standards | 03 - Person Detail | `medium` | The draft had a map-wide 'Show names' toggle on 02 and a per-person 'Reveal name' on 03: two controls with near-identical names and very different scope and privacy consequences. | Removed the map-wide toggle. Whether names show by default is an organisation policy read at sign-in, and the only operator control is per-person 'Reveal name' on 03, which asks for a reason and is logged. Spec updated on 02 and 03. |
| Error prevention | 06 - Change Settings | `high` | A firmware update could be applied to every anchor at once while people were on the floor, taking the whole floor dark. Nothing in the flow prevented it. | Rollout defaults to staged (one anchor at a time while neighbours cover), and 'All at once' is disabled whenever anyone is present. Any change that leaves a phone uncovered needs an acknowledgement naming the people and the duration. Spec updated on 06. |
| Recognition rather than recall | 05 - Equipment Detail | `medium` | An operator who suspected a person's reading on 03 and went to the anchor on 05 had to remember which person they were checking in order to find them in the connected-phones list. | Navigation from 03 to 05 carries the person as context: a 'From Person 7F3A' chip, with that person highlighted in the list, or a note that they have moved to another anchor. Spec updated on 05 (content structure, edge cases). |
| Flexibility and efficiency of use | 02 - Live Floor | `low` | Finding one person on a busy floor meant scanning the map or scrolling the list, with no fast path for an operator doing it repeatedly. | Added people search focused by '/', which filters the list and highlights matching markers, plus arrow-key navigation between canvas objects. Spec updated on 02 (interactions, keyboard focus). |
| Aesthetic and minimalist design | 02 - Live Floor | `medium` | The draft gave the raw stream a third column beside the map and the people list, so the busiest page carried three live-updating regions competing for attention. | The raw stream now shares the right panel with People as a tab, and is filtered per person on 03, where it answers a question rather than scrolling for its own sake. Spec updated on 02 (content structure, interactions). |
| Help users recognize, diagnose and recover from errors | 02 - Live Floor | `medium` | When names failed to resolve, an operator could not tell whether they lacked permission or the customer's identity service was down. Both looked like anonymous IDs. | A banner names the cause ('your organisation's identity service isn't responding'), sign-in degrades rather than failing when the token cannot be issued, and 'Reveal name' is disabled with the same explanation. Spec updated on 01 (edge cases), 02 (disabled state) and 03 (disabled state). |
| Help and documentation | none | `none` | none | The two concepts that need explaining explain themselves in place: presence states carry a text label and last-seen age plus an always-available legend on 02, and the drift flag on 05 states its evidence and the usual remedy in one sentence. No separate help is needed for the primary journey. |

---

## Design system gaps

| Need | Nearest role | Why it falls short |
|---|---|---|
| A scaled floor plan on which live person markers and anchor markers are positioned by (x, y), panned and zoomed, and navigable by keyboard as an ordered list of objects | `Chart` | A chart plots data on axes. This is a spatial map of a real room, where position is the content, objects are interactive, and a non-visual user needs an equivalent structure ('3 people near Anchor NE'). |
| A person marker whose state is time-based (live, fading with a last-seen age, frozen when upstream data stops) and readable without colour | `Badge` | A badge is a static count or dot. It has no notion of time since last update, and its states are colour-coded by convention. |
| A live append-only log with follow-tail, pause, and filter-to-one-device, whose updates must not flood assistive technology | `List` | A list renders a stable set of rows. A log grows several times a second, needs a paused or following mode, and needs announcements throttled to a summary rather than one per row. |

---

## Assumptions

- Design system: none was supplied, so the documented Material 3 baseline is used (human decision at the fork). Token names come from ux-pipeline/skills/wireframe-ia/references/material-design-tokens.json. Where Material 3 lacks a component (data table, breadcrumb, banner, skeleton, stepper, charts) it is built from M3 anatomy and tokens and marked new.
- Direction: B+C composite. From B: one dashboard, names resolved in the operator's browser, pseudonymous fallback with per-person reveal, the reading-explainer panel, the impact preview and role-gated settings. From C: drift check, staged OTA with rollback, the presence/activity timeline, and the stream heartbeat (surfaced on 04 and 08).
- The integration health panel (A-only) is not in this composite. The integrator persona's HMW 5 is served only by the heartbeat, which the customer's own monitoring consumes, and has no integrator UI here.
- Every API endpoint named in data_dependencies is a proposal. The RFQ defines no API surface.
- The operator role is the RFQ's unnamed 'users'. Two capabilities are assumed: view (all operators) and 'equipment-editor' (change settings, run rollouts), read from the customer IdP.
- Whether names show by default is an organisation policy ('names on' or 'anonymous IDs with reveal') read at sign-in, not an operator toggle.
- Single site per view, with a site selector in the top bar because the PKI design implies several sites. The pilot layout is one room with four corner anchors and two doors (RFQ p.6 mock-up).
- Fade and remove timings for out-of-range people are configurable per site. The RFQ gives no values, so none are specified.
- The demo phone app (login, welcome, config download) is not wireframed: target surface is web, and the app sits with the out-of-scope SDK.
- The '90 seconds' OTA duration in 06's acknowledgement copy is a placeholder until real per-anchor update times are known.

---

## Validation

**ux**

- Primary journey walks 01 → 02 → 03 → 05 → 06 → 05 → 02 without dead ends
- Every RFQ dashboard requirement (§4 dashboard, device tracking, streaming view; §5C) maps to a page: floor plan with anchors (02), status and health (02, 04), click to configure (05, 06), logged-in only (02), identity + coordinates + anchor + signal (02, 03), anchor's phones (05), raw stream (02, 03)
- All five RFQ §5D scenarios have a defined visible behaviour on 02

**ui**

- Every component carries a Material 3 name or is marked new with why_new
- Colour is referenced only by md.sys.color tokens
- One primary action per page, sentence case, at most four words

**responsive**

- All 8 pages specify desktop 1440, laptop 1280, tablet 768 and mobile 375
- The floor plan recomposes to a list-first view at 375, and the equipment table recomposes to a list
- Side sheets become full pages below 1280

**accessibility**

- Seven accessibility keys on every page, each written for that page
- The floor plan has a keyboard model and a text alternative
- Presence and equipment states use shape plus text, never colour alone
- Async results announced with deliberate politeness: frozen positions, names unavailable and rollback are assertive; arrivals, counts and step completion are polite

**prototype**

- 16 prototype flows; every page reachable from 01 - Sign In
- Figma render not run: no Figma connection in this session (figma_file_url null)

---

## Gate result

**Tier 1 — structural: PASS.** `ux-pipeline/validators/wireframe.py` returned 0 errors with the Stage-3 feature matrix in context. Base roles, naming, raw-colour ban, states, all seven accessibility keys with contrast and touch-target evidence, no duplicate accessibility blocks, four breakpoints per page, prototype reachability from 01, all ten heuristics, and sitemap↔pages parity all pass.

**Tier 2 — rubric: 4.85 / 5 — PASS** (`min>=4 and ds_compliance>=5 and accessibility_rigor>=4`). Before scoring, two issues were fixed: the breadcrumb was defined three times with different justifications, and 02 carried a filler 'not applicable' success state.

| Dimension | Weight | Score | Note |
|---|---|---|---|
| `ds_compliance` | 0.20 | 5 | Components carry Material 3 names, and 25 reused outnumber 10 new. Each new component is something M3 genuinely lacks (data table, breadcrumb, banner, skeleton, stepper, charts, floor plan), with a reason. Colour is tokens only, and the three needs outside the taxonomy are logged as gaps rather than stretched onto Card. |
| `ia_coherence` | 0.15 | 4 | The sitemap could only belong to this product: live floor, then the reading, then the anchor, then a safe change. Not a 5: 01 - Sign In is close to generic, and two of the three personas (integrator, tracked employee) have no surface in this composite, a direction consequence the human should see. |
| `state_and_responsive_coverage` | 0.15 | 5 | Every state names its treatment, including frozen markers on store-computer loss and sign-out while the detail sheet is open. Success and disabled appear wherever a page writes or gates. The floor plan goes list-first at 375 and the equipment table becomes a list. |
| `accessibility_rigor` | 0.20 | 5 | Each block is page-specific, cites token pairs or ratios and measured targets, and gives the floor plan a keyboard model and a text alternative. Politeness is chosen deliberately: frozen positions, names unavailable and rollback are assertive; counts and step completion are polite. Shape plus text everywhere, never colour alone. |
| `heuristic_rigor` | 0.15 | 5 | Nine findings, each naming a page and a consequence (3 high, 5 medium, 1 low), all fixed in the spec. One clean verdict, with its reason. Several are things the structural steps could not catch: frozen data reading as live, no way to stop an OTA, two controls with one name and different privacy scope. |
| `requirements_completeness` | 0.15 | 5 | Every page names concrete (proposed) endpoints, edge cases specific to that page, and honest open questions. The 16 prototype flows walk the primary journey end to end. |
