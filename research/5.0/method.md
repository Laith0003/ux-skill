# Method: users before screens

Input for ux-skill 5.0, Phase 6. It records how the owner ran product UX on two real multi-role back offices, reduced to method. It holds no client facts: every client noun is replaced by a role or an abstraction ("the operator team", "a pending decision", "a record sheet").


## 1. The method as practised

### 1.0 The shape

The work ran in two halves with a review gate between them:

1. Understand: check what exists, reduce the spec, research mature tools, personas, goals, every route to every goal.
2. Structure: conceptual model, IA decisions, site map, flows with failure paths, one shared rule set.
3. Prove: walk every goal by every route as each persona on the current build, recorded.
4. Decide and present: the one-page case, decisions taken by the standard, a short presentation. Gate: the owner says go.
5. Build inside the design system: shared contracts first, then parallel page lanes, fresh review, then the full walk again as a matrix at desktop and phone widths, then "what was not walked".

A common failure is to skip steps 1 to 4: pages get built straight from a spec's section list or a clickable prototype, and the structure has to be redone. The method exists to prevent that.

### 1.1 Check what exists

- **Audit the current build against the reference kit and the shipped product that uses it.** Not a reading of component files: open the shipped pages and record how they compose a page (frame, header, index anatomy, record sheet anatomy, settings, forms, report, cross-cutting rules for badges, confirms, empty states, phone). Then list where the build departs, per area, with file and line.
- **Reduce the spec to raw material, no design.** One extract with actors, jobs per actor, objects, relations, state machines per object, rules with numbers, gaps (the spec is silent), contradictions (the spec disagrees with itself), and differences between the spec and any prototype. Every line cites its page. "Derived" marks a fact that follows from two cited facts; "not stated" marks silence.
- **A stakeholder's prototype is a reference for screens and data, never a contract and never executed.** It is studied next to the spec, and its differences from the spec are numbered.
- **A first-time user pass.** Open each page cold as a new employee and write the questions they would ask ("where do I start?", "why can't I click this?", "which tab am I in?"). These are not kit findings; they become goals and routes later.
- **Static "expected missing" list.** From the route list and a code grep (not from running the app), list routes the goals will need that the build likely lacks, each marked "expected missing, verify".

### 1.2 Research mature tools for the same jobs

- Pick two mature products that serve the same kind of user and job (for a back office: a mature admin product and an accounting product).
- Research how each **routes a user to each kind of data and goal**, not how it looks: global routes (search, nav, notifications), index pages (views, filters, sort, bulk), then per data type (home, one record, a list filtered by state, a balance, a statement over a period, this period against the last, a ranking, a history of who did what, a setting's current value).
- Tag every claim by evidence: primary page read, excerpt only, community or third party, inference. Keep an explicit "could not verify" list; nothing is "seen in the product" unless a live session was used.
- Output three tables: patterns both share (conventions the user already knows), our objects mapped to the closest pattern with what to borrow, and patterns to avoid with the reason. Recommendation is kept apart from the facts.
- Add a **data-types table**: data type, personas who want it, the decision it serves, what they do next, the known convention.
- Add a **convention per entry point** table: what a user of the mature tools already expects from each entry point (home queue, home number, nav, search, saved view, status count, related record, notification, report drill-down, deep link).
- Later, when judging visual detail, the benchmark is read from source and live measurement (CSS, JS, a test account), never rebuilt from screenshots, and every option is placed against three references: the two mature tools and the original system.

### 1.3 Personas (who, job, why)

One record per persona, derived from the spec's roles. Roles that the spec gives identical powers collapse into one persona, with the missing difference logged as a gap. Custom roles are not personas; they are mixes.

Each persona states: who they are and their working day; what they are measured on; what they fear getting wrong; when, how often and on which device they open the product; what they may not see or do (from the permission model: pages, hidden fields, denied operations); density tolerance. Anything the spec does not state is marked "(assumption)". No invented names, photos or quotes.

### 1.4 Goals per persona

Every goal for every persona, as jobs to be done: the progress the persona wants in a circumstance. Each goal records trigger, data needed to decide, outcome and the risk if wrong or late, frequency, urgency or deadline (from the spec, else "not stated"), the one object and state it acts on, and the spec jobs it serves. A goal never introduces an object the spec lacks.

### 1.5 Every route to each goal

A route matrix: every goal against every entry point a reasonable user would try. Entry points used: home queue, home number, nav (rail), global search, index filter or saved view, status count, tabs, related record, notification, report drill-down, deep link from a message.

Each cell is a mark with a reason code from a fixed legend: **must** (with the reason, for example "the persona arrives holding an identifier from outside the product" makes search a must; "a hard clock with a consequence" makes a notification a must), **should**, or **not needed** (also with a reason). For related-record cells the cell names the parent record. Notifications the spec never defines are marked as proposals.

This matrix is the test plan the build is walked against.

### 1.6 Conceptual model

- **Objects** the users open, decide on or read: term, code name, standing (first-class with its own index or record sheet, or "inside" its parent), parent.
- **What is deliberately not an object.** A "task" or "decision" is a view over objects in a waiting state, never a stored object, so there is one record and one place to act. An internal handoff becomes an attribute, not an object.
- **Relations** as a diagram.
- **States per object with the work left in each**, naming who must act next; the states that wait on staff are marked, because they feed Home. State machines drawn per key object.
- **Vocabulary**: one term per concept, in both languages.
- **Action inventory**: object, action, who may, reversible (and its inverse), reason required, source. "Reversible" means the system gives a direct inverse; anything whose notice reaches an outside party counts as irreversible for the undo rule.

### 1.7 IA and site map

- **IA decisions**, each written as: what, alternatives with "why not", reason, evidence (goal ids, audit ids, research ids). Typical decisions: nav grouped by object family and ordered by daily volume from the goal inventory; a nav item shows only when the role can open one of its pages; a pending item is acted on in exactly one place (its record sheet) with one canonical address, and every other mention (home row, index, parent page, search result, message link) opens that same sheet; a parent record's page is one column of sections with pending first, not tabs; global search in the header over records the role may open, hidden fields not searchable; home filtered by role; saved views on every index named by the work left; time pressure shown in one place per row and used as the default sort; read-only objects are not a nav space.
- **Site map**: a tree, then a page table (route, label, parent, kind, personas, phase). Page kinds: home, index, details page, record sheet, form, settings, analytics. Phase is set by whether a core job cannot complete without the page.
- **Index definitions**: per index, default view (per role where they differ), default sort, saved views named by work left, status counts (each one a filter, capped).
- **Change list**: current page or part, target, change (kept, moved, merged, new, removed), so the build has a direct to-do.
- **Open points** first carry a "(default)" so work never stops; they are then closed as decisions (see 1.11).

### 1.8 Flows with decision points, failure paths and exits

- **One shared rule set, written once, for every flow**: denied by role (page and action), stale record (someone else acted first), validation, network failure, loading, empty (several distinct empty states), cancel (Escape closes only the top layer, input kept), undo (reversible runs at once with an undo window; irreversible confirms with a button that names the action and the count, then holds briefly with undo; outside parties are told only after the window), focus after a decision (next item in the same queue, or the empty-state heading after the last), keyboard (search shortcut, row movement, open, next and previous record, physical key codes so it works on any keyboard layout), and how clicks are counted.
- **Per flow**: jobs and goal served; entry points (the must and should marks from the matrix); the flow as a text breadboard (place, then the links and actions in it, then the data shown to decide in brackets); the happy path as a counted number of clicks from the first entry point to the committed decision; decision points; failures (each named, with what the user sees and the way out); empty; undo class; focus after; keyboard path. Only what differs from the shared rules is written per flow.
- **Accessibility is designed into the flows**, not audited later: landmarks per page kind, focus order, status without colour, numbers in right-to-left text, target sizes, what a screen reader hears on a row with a deadline.
- The click count makes "simpler" a number and lets the plan compare today against proposed for each job.

### 1.9 Prototype inside the design system

What "prototype in the DS" meant concretely:

- **The prototype is the product's own frontend**, on the real stack, running on mock data behind one swappable data seam (one API layer whose base query is a mock), so the same code becomes the product when the backend lands. Not a separate HTML mock and not a drawing.
- **Components only from the shipped kit, composed the way the shipped pages compose them.** Before writing any piece, find the shipped page that already uses that pattern and copy its composition. A table lists, per pattern (page header, filter bar, saved views, results line, table, row opens its sheet, sort from the head, phone list cards, side sheet parts, settings with a save bar, empty states, badges, count boxes, motion helpers), the kit piece and its canonical call site in the shipped product.
- **A missing piece is widened in the kit**, by an optional prop or variant that still serves the original product, and logged as a design-system candidate. Never forked, never hand-built beside the kit.
- **Tokens only, type only from the ramp, one control height per row, one page inset everywhere, strings in locale files in both languages, right-to-left first.**
- **Shared interaction contracts are built once, before any page**: the record sheet host (open over any page by a URL parameter, previous and next, advance after a decision), undo and hold, reason dialog (no reason, one-click preset, optional text), saved views, deadline cell and sort, list keyboard, global search, home by role, denied page (names the roles that can), denied action (disabled with "who can" as visible text). Pages are then built in parallel lanes that import these contracts and never copy them.
- **When the written rules and the shipped product disagree, the shipped product is the benchmark**, and the disagreement is recorded as an open conflict with both sides, never silently merged into the rules.

### 1.10 Walk every goal by every route as each persona, with evidence

- A scripted browser walk on the running build, one script per goal and route, signed in as the persona's role, at desktop width, and the phone width where the route matters on a phone.
- Each walk clicks what a reasonable user would click (highlighting each target), records every click, typed text, key, dialog text, toasts, console errors and the final address, asserts what should be seen, and ends with a status: **reached**, **reached with trouble**, **blocked**, or **route missing**. A route a reasonable user would try and cannot find is recorded as missing, even with nothing to record.
- **Evidence is rough on purpose**: one short video per goal and route, a still of the end state, a frame strip. Polish is waste. Every finding in the case points at a recording id.
- Walks find the joins, not the pages. Typical failures: numbers on home that open nothing, a quick search that knows only one identifier, checks that fail after the confirm instead of before, approvals with no undo, a role whose home is all dead ends, late items with no way to sort or filter for them, duplicate toasts.
- **After the build, walk every flow as a matrix** at both widths with its role, pass or fail per flow, then write down what was not re-walked (reject branches, stale record, network failure, denied-role variants, keyboard-only end to end, screen reader, the other language, dark). A sampled walk can pass while the full matrix fails, almost always at the joins (a back link, a kept period, focus after a decision).
- For every number on a home or overview that links to a list, check that the number equals the rows the link opens.

### 1.11 The one-page case, decisions, presentation

- **One page**, in this order: verdict (routes walked with counts per status), the worst findings, each with its recording ids, who uses it and why (persona, number of goals, what they come for, what they need first), routes the goals need that the build lacks, what the mature tools do for the same data (pattern we take, why the user wants it, and where we do better), the IA decisions in plain words, site map, the playable walkthrough grid (a card with no video is a route that does not exist), what changes (change, the findings it fixes), decisions taken, and "not tested in the walk".
- **Decisions table**: point, decision, the standard behind it (the reference product's behaviour, or the walk's evidence of the opposite's cost). None waits on anyone.
- A short slide presentation of the IA for the owner, then the go.

### 1.12 What was corrected along the way

| Correction (generic) | What was wrong | Rule now |
|---|---|---|
| "Structure first" | Pages built from a page table and a prototype | Personas, goals, routes, model, site map and flows are reviewed before any screen; screens mirror them |
| "Take every component from the shipped kit and normalise it" | The kit was copied as files, then tabs, badges, skeletons and sheet layouts were hand-built around it | No product-only component; widen the shared piece and log it |
| "Full tests for uses and goals, give me videos, make the case" | The audit was a reading with no evidence of use | Walk every goal by every route as each persona and record it, rough |
| "You are the UX lead, do your job" | Open UX points were queued as questions for the spec owner and the backend | Decide UX points from the studied cases and the standard; write a decisions table; ask only on a real trade-off the standard does not settle |
| "What do you mean, IA?" | Jargon in the report | Name the thing in plain words: the research and plan, the map of pages, the step-by-step paths |
| Home numbers below the queue | The first figures a role looks for were under the fold | On home, the role's numbers come first and each opens its rows; then the queue sorted by deadline |
| A typed reason on every forward move | Friction on routine work | A reason is asked only where the other party loses something, and is one click from a list |
| "Pressing anything should open its details, never nothing" | Dead numbers, dead cards | Anything that looks pressable opens what it counts; a number that cannot be opened is not shown |
| "Think about the user's goal at every combination of filters, don't guess" | A report opened blank, demanding a pick | Write the goal of each filter combination from what the system returns, then design the start; never open blank when a sensible default exists; an unserved combination says why and offers ways on |
| "Check all such cases, not one by one" | One finding fixed on one page | A finding is a class: fix it at the kit by a rule, sweep every page |
| "Never ask me a visual either/or without seeing both" | Text-only questions | Every visual option is rendered and shown side by side, then opened live to click through |
| "From the source, not from my screenshots" | Benchmark rebuilt from images | Read the reference's real component source and measure it live |
| "Lines should never be over two lines" | Rows wrapped to three or four lines | A row is at most two lines; measure with real data at the working widths |
| "I don't want the controls to move, muscle memory" | Controls shifted with text length and counts | A daily control sits at the same pixel on every page and state |


## 2. The artifacts and their schemas

Proposed home: `.ux/method/` in the project, one file per artifact, YAML for anything a tool reads, Markdown or HTML for what a person reads. Ids are stable and referenced across files. Every record carries `source` (spec page, research id, audit id, or `assumption`).

### 2.1 Persona record (`personas.yaml`)

```yaml
personas:
  - id: P-officer
    name: Case officer                # a role label, never a person's name
    covers_roles: [case_officer]           # permission roles this persona stands for
    day: "Works through the application queue and watches cases near their statutory clock."
    measured_on: ["days from application to decision (assumption)"]
    fears: ["a case passes its statutory deadline unseen"]
    opens: {frequency: "all day", devices: [desktop, phone], when: "start of shift"}
    may_not:
      pages: [settings.fees]
      hidden_fields: [applicant.tax_number]
      denied_actions: [case.reassign]
    density: high                        # low | medium | high
    assumptions: [measured_on, opens]    # which fields are assumed
    source: "spec section and page"
```

### 2.2 Goal record (`goals.yaml`)

```yaml
goals:
  - id: G-officer-decide
    persona: P-officer
    statement: "Decide a permit application before its statutory clock runs out"
    trigger: "an application is submitted"
    data_to_decide: [the application form, inspection results, earlier permits for the same site]
    outcome: "the applicant knows the answer and the reason"
    risk_if_wrong: "a permit is granted on a failed inspection"
    frequency: daily                     # or "not stated"
    urgency: "not stated"                # a clock only when the spec sets one
    object: application
    state: submitted
    jobs: [J1, J2]
    launch_critical: true
    source: "spec section and page"
```

### 2.3 Route matrix (`routes.yaml`)

One row per persona, goal and entry point. The plan columns are written at step 1.5; the walk columns are filled by the walk.

```yaml
entry_points: [nav, home_queue, home_number, search, view, status_count, tab,
               related_record, notification, report_drill, deep_link]
reasons:                                # the legend, so every mark is explained
  search.must: "the persona arrives holding an identifier from outside the product"
  notification.must: "a hard clock with a consequence if missed"
routes:
  - id: R-officer-decide-home_queue
    persona: P-officer
    goal: G-officer-decide
    entry: home_queue
    mark: must                           # must | should | not_needed
    reason: home_queue.must
    via: null                            # parent record name for related_record
    target: sheet.application        # a page or sheet id from sitemap.yaml
    # filled by the walk
    status: reached                      # reached | trouble | blocked | missing | not_walked
    clicks: 3
    walk: walks/g01-r1-home-queue.json
    evidence: [videos/g01-r1-home-queue.mp4, stills/g01-r1-home-queue.png]
    findings: [F-07]
```

Status meanings: **reached** completes with no friction worth a finding; **trouble** completes with a finding attached; **blocked** the route exists but the goal cannot complete (error, dead end, denied with no way on); **missing** a reasonable user would try it and it does not exist; **not_walked** listed so gaps stay visible.

### 2.4 Conceptual model (`model.yaml`)

```yaml
objects:
  - {id: application, term: {ar: "...", en: "application"}, standing: first_class,
     parent: applicant, home_index: applications.index}
  - {id: inspection, term: {...}, standing: inside, parent: application}
not_objects:
  - {name: task, why: "a view over waiting states; a stored task would drift from its record"}
relations:
  - {from: applicant, to: application, cardinality: "1..n"}
states:
  - {object: application, state: submitted, waits_on: officer, clock: {length: "as the law sets it", source: "brief"}}
  - {object: inspection, state: scheduled, waits_on: inspector, clock: null, source: "brief"}
actions:
  - {object: application, action: approve, from: under_review, to: approved,
     roles: [P-supervisor, P-officer], reversible: false, inverse: null,
     reason: none, notifies_outside: true, source: "spec section"}
  - {object: case, action: assign, from: unassigned, to: assigned,
     roles: [P-supervisor], reversible: true, inverse: unassign, reason: none}
vocabulary:
  - {concept: application, use: "application", never: ["synonyms the brief does not use"]}
```

### 2.5 Site map (`sitemap.yaml`)

```yaml
nav:
  order: [home, applications, inspections, reports]
  foot: [settings]
  visibility: "an item shows when the role can open at least one of its pages"
pages:
  - {id: applications.index, route: /applications, label: "...", parent: applications,
     kind: index, roles: [P-supervisor, P-officer], phase: launch,
     views: [{id: waiting, label: "...", default_for: [P-officer]}],
     default_sort: deadline_then_oldest, status_counts: [waiting, overdue]}
sheets:
  - {id: sheet.application, object: application, home_index: applications.index,
     address: "/applications?open={id}", opened_from: [home_queue, parent_page, search, deep_link]}
decisions_ref: decisions.yaml        # IA decisions that shaped the map
```

### 2.6 Flow (`flows/FL-<id>.yaml`)

```yaml
id: FL-decide
goals: [G-officer-decide]
personas: [P-supervisor, P-officer]
entries: [R-officer-decide-home_queue, R-officer-decide-view, R-officer-decide-deep_link]
steps:
  - place: home
    links: [{label: "queue row", to: applications.index, view: waiting}, {label: "item row", to: sheet.application}]
  - place: sheet.application
    shows: [application form, inspection results, earlier permits]
    actions:
      - {id: approve, opens: panel.approve}
      - {id: refuse, opens: dialog.reason}
      - {id: order_inspection, opens: panel.inspection}
decision_points: ["approve, refuse or order an inspection", "refuse needs a legal ground"]
happy_path: {from: home_queue, clicks: 3}
failures:
  - {kind: denied_action, sees: "action disabled with the role that can", exit: "read only, back to queue"}
  - {kind: stale, sees: "who acted and when; record refreshes", exit: "next item"}
  - {kind: validation, sees: "error under the field naming what is needed", exit: "fix and confirm"}
  - {kind: network, sees: "inputs kept, error names what failed, retry", exit: retry}
exits:
  success: "next item in the same view; after the last, focus on the empty-state heading"
  cancel: "Escape closes the top layer; focus returns to the row"
undo: irreversible                  # must match model.actions
reason: {refuse: preset_required, approve: none}
keyboard: "search, Enter; Tab to approve, Enter; Tab to confirm, Enter"
shared_rules: rules.yaml            # only differences are written here
```

`rules.yaml` holds the shared rule set from 1.8 with one entry per edge kind (denied page, denied action, stale, validation, network, loading, empty kinds, cancel, undo, focus after, keyboard, click counting).

### 2.7 Walk log (`walks/<id>.json`)

```json
{
  "id": "g01-r1-home-queue",
  "route": "R-officer-decide-home_queue",
  "persona": "P-officer", "role": "case_officer",
  "viewport": "1280x900", "locale": "ar", "theme": "light",
  "build": {"ref": "<commit>", "url": "http://localhost:3000"},
  "steps": [
    {"do": "goto", "target": "/"},
    {"do": "click", "target": "home queue row 'waiting applications'", "ok": true},
    {"do": "see", "expect": "application sheet title", "ok": true}
  ],
  "clicks": 3,
  "status": "reached",
  "final_url": "/applications?open=a-1",
  "notes": [],
  "console_errors": [],
  "toasts": ["..."],
  "evidence": {"video": "videos/g01-r1-home-queue.mp4", "still": "stills/g01-r1-home-queue.png"},
  "run_at": "<ISO8601>"
}
```

### 2.8 Decisions (`decisions.yaml`) and the case

```yaml
decisions:
  - id: D-home-by-role
    point: "Is home the same for every role?"
    decision: "Each role sees only the queues it can act on and its own numbers"
    alternatives:
      - {option: "one home for all", why_not: "a role meets queues it cannot open; the walk showed dead ends"}
    standard: "mature admin tools scope home tasks by permission"
    evidence: [R-review-*-home_queue, F-07]
    status: taken                    # default | taken
```

The case (`case.html`) is generated from these files plus the walk logs: verdict counts by status, worst findings with recording ids, personas, missing routes, research patterns, IA decisions, site map, walkthrough grid, change list, decisions, not tested.


## 3. What can be checked automatically

Two families. **Static** checks read `.ux/method/*.yaml` (cheap, no app). **Live** checks drive the running app (`lint` with a render URL, which PLAN-5.0 Phase 5 item 16 already plans). All start advisory.

| # | Check id | Input | Rule | Threshold (house default, to be measured) | How to build | False-positive risk |
|---|---|---|---|---|---|---|
| 1 | `goal-route-coverage` | goals, routes | Every goal has at least 2 routes marked must or should, at least one of them a cold-start route (nav or search); every must mark carries a reason from the legend | 2 routes; 0 must marks without reason | Pure YAML pass | Low. A rare, one-door goal (a setting) can legitimately have one; allow a `single_route_ok` reason |
| 2 | `matrix-sitemap-closure` | routes, sitemap | Every route's target is a page or sheet in the site map; every page is the target of at least one route (no orphan); every page is reachable from nav for at least one role that may open it | 0 dangling targets, 0 orphans | Graph pass over ids | Low. Orphans can be intentional (an error page); allow `kind: system` |
| 3 | `one-place-to-decide` | model, sitemap, routes | Every object with a waiting state has exactly one sheet; every route to a goal on that object targets that sheet; live: every entry lands on the same canonical address | 1 sheet per waiting object | YAML pass; live: compare final URLs across the route's walks | Medium. Inline quick actions on a row are a deliberate exception; mark them `also_inline` |
| 4 | `waiting-state-surfaced` | model, sitemap | Every state with `waits_on` set to a staff role appears in at least one queue (home row or a saved view) for a role allowed to act | 100 percent | YAML pass | Low |
| 5 | `flow-completeness` | flows, rules, model | Every flow has a success exit, a cancel exit, a focus-after, a counted happy path, and a failure entry for each applicable kind (denied action when any role lacks the action, stale when two roles can act, validation when there is input, network always); undo class matches the model's `reversible`; a `reason: required` action has a reason step | 0 missing exits; failure kinds per applicability | YAML pass with applicability derived from model and personas | Low to medium; applicability rules need tuning on real briefs |
| 6 | `role-nav-scope` | personas, sitemap, live app | Live, per role: nav shows exactly the spaces where the role can open a page; a direct link to a denied page shows a page that names who can and a way back; no 404 and no blank | 0 leaks, 0 bare denials | Playwright per role (role switch via a test hook or test accounts), read nav links, visit denied routes | Medium. Needs a reliable role switch; apps without one are `unmeasured` |
| 7 | `denied-action-says-who` | live app | Every disabled control has a visible or programmatic reason; a role-denied main action is shown disabled with the role that can; a state-disallowed action is absent | 0 silent disabled controls | DOM scan of `[disabled]`, `aria-disabled`, nearby text or `aria-describedby` | Medium. Disabled-while-loading is legitimate; re-check after network idle |
| 8 | `walk` (harness) | routes, flows, running app | For each persona, goal and route: attempt it with a scripted or generated walk, record status, clicks, video and still; a must route that is missing or blocked is a finding | Pass rate reported, not gated, in 5.0 | Playwright harness (see below) | Medium to high for generated walks (selectors guessed); low for scripted ones. Weak-walk guard below |
| 9 | `number-to-list-parity` | live app | Every number on home or an overview that links to a list equals the row count (or the header total) of the list it opens, in the same period | Exact match | Find linked figures, follow each, count rows or read the results line | Medium. Paginated or lazy lists need the results line; async refresh races |
| 10 | `dead-number` | live app | A figure or card that looks pressable opens something; a figure that does not open is not styled as pressable | 0 | Extends PLAN-5.0 `dead-click` to cards and figures | Low to medium (same as `dead-click`) |
| 11 | `deep-link-roundtrip` | sitemap, live app | Opening a record, copying the address and loading it in a fresh context opens the same record; back from it returns to the origin with view, filter and period kept | 100 percent of sheets | Playwright: open, read URL, new context, compare title and id; then back and compare query | Low |
| 12 | `click-budget` | flows, walks | The measured happy-path clicks equal the declared ones; a later build that adds clicks to a flow is flagged | Delta of 0 against the declared count | Diff walk clicks against `happy_path.clicks` | Low, if the counting rule (pointer activations only) is fixed |
| 13 | `focus-after-action` | live app | After a committed action or an undo, focus is never on `body`; it lands on the next record, the row, or the empty-state heading | 0 | Read `document.activeElement` after each action in walks | Low |
| 14 | `confirm-names-action` | live app | An irreversible action's confirm button names the action and the count, not "OK" or "Confirm" | 0 generic labels | Collect dialog primary buttons in walks; compare against a generic-label list per language | Medium in less common languages |

**Weak-walk guard.** Reuse the 4.1 complaint contract: a walk that is meant to prove a route was fixed must fail on the `before` build, or it proves nothing and stays "weak". This is the same rule as `engine/complaints.py`, applied to routes.

**The walk harness, how to build it.**

- Input: `routes.yaml` (what to attempt), `sitemap.yaml` (where each route should land), a role switch (test accounts, a header, or a local storage hook named in project config), base URL, widths (390 and 1280, the engine's existing sweep widths).
- Per route: a scripted walk when one exists in `.ux/method/walks/scripts/`; otherwise a generated attempt from the entry point's convention (nav: find a nav link whose text matches the target page label; search: open the search shortcut, type the identifier from fixture data, pick the matching group; home queue and home number: find the row or figure whose label matches the goal's object and state; deep link: load the sheet address directly; related record: open the parent and look for a link to the target).
- Records per walk: the JSON in 2.7, a video, a still, the click count, console errors and toasts. Ends with a status by rule: target reached with no finding is `reached`; reached with an error toast, console error, more clicks than declared, or a failed `see` is `trouble`; an exception or a dead end is `blocked`; no candidate control for the entry point is `missing`.
- Writes the walk columns back into `routes.yaml` and renders the case.
- Exit codes follow the complaint check: 0 all must routes reached, 3 at least one must route missing or blocked, 2 input error naming the field and the fix (for example: `routes[12].target "sheet.record" is not in sitemap.yaml; add it under sheets or fix the id`).


## 4. Gap table: method step against current ux-skill (feat/4.1-stageshow at 7785d962)

Paths are relative to the ux-skill repo.

| Method step | Where ux-skill touches it | Status |
|---|---|---|
| Check what exists: audit the build against the shipped kit and how shipped pages compose it | `references/process/refactor-existing.md:52` walks the existing UI into four lists, but its checklist (`:84` onward) is visual (fonts, colour, radius, states); `commands/ux-audit.md:29` reads one surface | partial |
| Reduce the spec to actors, jobs, objects, states, rules, gaps, contradictions | Nothing. `commands/ux-design.md:151` asks for "data shape: entities, metrics, relationships" in one line | missing |
| Research mature tools for the same jobs (routing, data types, entry-point conventions) | `commands/ux-research.md:177` to `:201` mines competitive sites only for `forbidden` and `reference_brands`; `commands/ux-discover.md:67` reference brands are for design language | missing |
| Personas: several roles, each with job, fears, may-not, density | `commands/ux-discover.md:62` one audience; `commands/ux-design.md:153` one of operator, analyst, exec; `commands/ux-design.md:230` pushes back until a single audience is picked | missing, and the dashboard rule contradicts the method for multi-role back offices |
| Goals per persona | `commands/ux-discover.md:63` "ONE job for this surface" | missing |
| Every route to each goal | `references/surfaces/dashboard.md:203` filter state in the URL, `:214` deep links to drill states, as patterns only; no matrix | missing |
| Conceptual model (objects, relations, states, work left, actions, reversibility) | Theory in `references/laws/norman.md:177` and `references/laws/laws-of-ux.md:673`; no artifact | partial (theory only) |
| IA decisions and site map | `references/process/refactor-existing.md:40` puts IA out of scope by default; PLAN-5.0 Phase 6 plans `references/foundations/navigation-ia.md` | missing (planned as guidance only) |
| Role-scoped navigation and permissions (absent page, disabled action with who can, hidden field) | `references/surfaces/dashboard.md:93` shows the signed-in user's role in the nav foot; nothing on permission-shaped IA | missing |
| Home as a task list by role, numbers that open their rows | `commands/ux-design.md:151` to `:153` key metrics first; `references/surfaces/dashboard.md` patterns are KPI and chart led | missing (the playbook is metric-led, the method is queue-led) |
| Flows with decision points, failure paths and exits | `commands/ux-audit.md:77` RECOVER lens judges one surface; `commands/ux-design.md:528` "missing states" per component; PLAN-5.0 Phase 6 plans `references/process/journeys-and-flows.md` | partial (planned as guidance only) |
| One shared rule set for undo, reasons, denied, stale, focus, keyboard | Fragments in `references/laws/norman.md` (error prevention) and the RECOVER lens | partial |
| Prototype inside the design system | `commands/ux-design.md:328` existing system is fixed input (agrees); `:338` reads the brand's own pages for page style, page mode only; dashboard mode `:164` builds a dark grid from engine picks | partial (no "compose as the shipped pages do", no canonical call sites, no widen-not-fork) |
| Walk every goal by every route as each persona | `commands/ux-research.md:47` plans human usability tests; `engine/complaints.py` measures selectors on one page; PLAN-4.1.md:47 plans `task` and `reach` probes | missing (probes are the seed) |
| Evidence as rough video or screenshot sequences tied to findings | `commands/ux-audit.md:94` `evidence_kind` per finding (agrees in spirit); no recording | partial |
| Decide by the standard, not by asking | `commands/ux-audit.md:94` cites sources and labels house defaults (agrees); `commands/ux-workshop.md` ends in a Game Plan | partial |
| The one-page case before the build | `commands/ux-case-study.md:13` is a post-ship editorial retrospective | partial (wrong moment, wrong purpose) |
| Click count per flow, today against proposed | Nothing | missing |
| Full matrix walk after the build, plus a "not walked" list | Nothing; the complaint check covers named complaints only | missing |
| Number-to-list parity, dead numbers | PLAN-5.0 Phase 5 item 1 `dead-click` covers part | partial (planned) |
| One finding fixes the class | `commands/ux-design.md:469` complaints are per page | partial |


## 5. Draft PLAN-5.0 phase: "Method: users before screens"

Placement: after Phase 5 (it needs the render URL mode and the `task` and `reach` probes from Phase 5 item 16) and absorbing the two Phase 6 files `navigation-ia.md` and `journeys-and-flows.md`, which become this phase's guidance so they are written once, with their checks.

Spec: this brief, sections 1 to 3. One PR into feat/4.1-stageshow.

**Command surface: no new command.**

- `/ux-discover` gains a `method` mode. The router picks it when the brief names more than one role, or the project type is admin panel, back office, portal or console. It writes `personas.yaml`, `goals.yaml` and the plan columns of `routes.yaml`, plus the research tables (jobs, data types, entry-point conventions) when the user names reference tools. Dashboard mode's "push back until one audience is picked" (`commands/ux-design.md:230`) changes to: one audience for a single-role dashboard; several roles route to `method` mode.
- `/ux-design` gains a `structure` mode: `model.yaml`, `sitemap.yaml`, `rules.yaml`, `flows/`, `decisions.yaml`. Dashboard and page modes read these when present, and in a multi-role project with no site map they print one advisory line naming the missing file and the mode that writes it.
- `/ux-audit` gains a `walk` mode: runs the harness on a running URL, fills the walk columns, writes the walk logs, recordings and the case page. The static checks run as part of `uxskill lint` when `.ux/method/` exists.
- CLI and MCP mirror these: `uxskill method check`, `uxskill method walk`, `ux_method_check`, `ux_method_walk`.

**Tasks**

| # | Task | Done when |
|---|---|---|
| M1 | Schemas for the seven artifacts as JSON Schema under `engine/method/schemas/`, with a loader whose errors name the file, the path and the fix | A broken fixture for each artifact produces one error per fault, each naming field and fix; ASCII only |
| M2 | Guidance: `references/process/users-before-screens.md` (the method in order, with its common failure modes), `references/foundations/navigation-ia.md` and `references/process/journeys-and-flows.md` from Phase 6, every claim with a source id; the dashboard playbook gains a back-office section (home as role-scoped queues, numbers that open rows, one sheet per pending item, saved views named by work left) | Every missing-guide row for IA and flows in the gap lists is written or parked with a reason |
| M3 | `/ux-discover` method mode and router rule | On the three method briefs (section 6) the router picks method mode; on single-role briefs it does not |
| M4 | `/ux-design` structure mode, including the "compose from the shipped kit" step: record, per pattern, the kit piece and its canonical call site in the project's own shipped pages; a missing piece is proposed as a widening of the kit, never a new component | On the back-office brief, every page in the site map lists its patterns with a call site or an explicit "widen" proposal |
| M5 | Static checks 1 to 5 and 12 from section 3, advisory, with the fixture standard (3 fail, 3 near-miss pass, 1 inapplicable, 1 right-to-left pass) | Each check has fixtures, runs clean on the method briefs' gold artifacts, and has a row in the method benchmark report |
| M6 | Walk harness: scripted and generated walks, recordings, statuses, weak-walk guard reusing the complaint `before` logic, exit codes 0, 2, 3 | Two runs on the same build give the same statuses; a seeded missing route is reported missing; a walk that passes on the `before` build is reported weak |
| M7 | Live checks 6, 7, 9, 10, 11, 13, 14 on top of the harness, advisory | Each runs on the seeded-defect apps with its precision measured |
| M8 | Case page generator from the artifacts and walks | The case for the back-office brief renders with every finding linked to a recording, at 390 and 1280, light and dark |
| M9 | Outcome benchmark (section 6): briefs, gold artifacts, seeded-defect apps, scoring script | `bench/method/report.md` lists every metric for engine runs with and without the method modes |

**Exit criteria**

- The three method briefs run end to end through method mode, structure mode, a build and walk mode, and produce a case page.
- Every static and live check is advisory with a measured precision row; none is blocking without the Phase 1 rule (precision at least 0.95, Wilson lower bound at least 0.90) measured on the method benchmark.
- `routes.yaml` round-trips: plan written by discover, walk columns written by audit, no manual edit needed.
- No new top-level command; the README command table changes only by the new modes.
- No client, vendor or person names in shipped files; examples use a generic multi-role back office.


## 6. Testing the engine on outcomes

Lint precision says whether a rule is right about a page. It cannot say whether the engine leads a builder to a product people can use. The method gives outcome measures.

**Fixed briefs.** Six briefs with fixed copy and fixture data, frozen in `bench/method/briefs/`:

1. A back office with at least four staff roles that differ in pages, hidden fields and denied actions, and several deadline-bound queues.
2. A field team's mobile app with a manager and a field role sharing one app by role switch.
3. A self-serve SaaS settings and billing area (single role, deep settings).
4. A case-management tool for a public office (two roles, a long state machine, reasons required on rejections).
5. A small shop owner's daily dashboard (single role, glance use): the control, where the method should not add weight.
6. A support desk (agents and supervisors, conversations linked to records).

Each brief has a **gold set** written by a person: personas, goals, must routes, objects and waiting states, and the flows that must exist. Gold sets are marked model-made until a person confirms them, as Phase 1 requires for labels.

**Runs.** Each brief is built end to end by the same tool twice: with ux-skill's method modes, and with ux-skill without them (discover, design, lint only). The build runs on mock data.

**Scores per run**

| Metric | How it is measured |
|---|---|
| Goal recall | Share of gold goals present in `goals.yaml`, matched by object, state and persona |
| Route coverage | Share of gold must routes present and marked must |
| Flow completeness | Share of flows passing `flow-completeness` |
| Walk pass rate | Share of gold must routes `reached` on the built app; `trouble`, `blocked`, `missing` reported separately |
| Dead ends | Count of `blocked` and `dead-number` findings |
| Role leakage | Pages or actions visible to a role the gold set denies them (`role-nav-scope`) |
| Parity | `number-to-list-parity` failures |
| Click cost | Happy-path clicks per gold flow, against the gold count |
| Joins | Failures of `deep-link-roundtrip` and `focus-after-action` |
| Control brief cost | On brief 5, artifacts produced and time added: the method must stay light where one role and one goal dominate |

**Seeded-defect apps.** Three small fixture apps built from brief 1, each with planted defects drawn from common back-office failures: a search that knows only one identifier, home numbers that do not open, a pending item decidable in two places with different actions, a sheet with no address, a disabled action with no reason, checks that fail after confirm, a filter that resets on back, focus dropped to the page body after an action. The harness and live checks are scored on recall and precision against the plant list, and every planted defect must make its walk fail (the weak-walk guard).

**Human round.** Pairwise comparison of the two case pages and the two built apps per brief by designers, as in the taste test phase's harness (randomised sides, repeated pairs, gold pairs), reported apart from the measured metrics. A model judge is a pre-filter only.

**Drift.** The weekly canary (the running-unattended phase) reruns the method benchmark; a drop in walk pass rate or route coverage opens the drift issue.
