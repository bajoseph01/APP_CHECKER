---
name: app-checker
description: Evidence-led quality assurance for websites, web apps, dashboards, browser games, educational apps, interactive prototypes, and accessible mobile or desktop applications. Use when asked to check, test, QA, review, playtest, bug-hunt, regression-test, validate, or assess release readiness; when an app has just been built or meaningfully changed; or when a user wants software, UX, accessibility, device/input, performance, or learning-design findings backed by real execution and visual evidence.
---

# APP_CHECKER

Test the real artifact as a user would experience it. Establish a quality bar, run reproducible checks before subjective exploration, inspect rendered output, and report evidence without overstating confidence.

## Choose the run mode

- Use **micro** for a small localized change. Re-run the affected journey, one adjacent journey, hard regression gates, and a targeted visual check.
- Use **focused** for a feature, bug investigation, or ordinary QA request. Cover the main journey, failure paths, representative devices/inputs, accessibility basics, and visual quality.
- Use **full** for a new app, major redesign, release candidate, browser game, educational app, or explicit comprehensive audit. Cover all critical journeys, a wider device/input matrix, seeded behaviour runs, accessibility, performance signals, and independent final critique.
- Default to **focused** when the user does not specify scope. Increase scope when failure risk is clearly higher; state the reason.

## Start with the contract

1. Read repository instructions and existing test configuration.
2. Search for `app-checker.json`, then compatible manifests such as `jogo-swarm.json`.
3. If a manifest exists, read [references/manifest-contract.md](references/manifest-contract.md) and validate it with:

   ```text
   python <skill-dir>/scripts/validate_manifest.py <manifest-path>
   ```

4. If no manifest exists, infer the minimum contract from the repository, running app, and user request. Do not block a first check merely because a manifest is absent. Offer or create one only when the user asked for implementation or durable QA setup.
5. Identify the app type, start method or URL, intended audience, critical journeys, supported inputs, target viewports/devices, and any data or account constraints.
6. Define the bar before testing: what must work, what evidence is required, and what would block release.

Use [assets/app-checker.example.json](assets/app-checker.example.json) as a starting manifest when needed.

## Run the evidence ladder

### 1. Baseline and hard gates

- Preserve the user's running services when practical; otherwise launch the app with its documented command.
- Confirm the viewing URL responds before interactive testing.
- Run the project's existing build, type, lint, unit, and integration checks that are relevant to the requested scope.
- Inspect startup output, browser console errors, failed network requests, and obvious runtime crashes.
- Record the exact commands, URL, environment, device/viewport, and seed where relevant.

Never claim that an app works merely because it builds.

### 2. Deterministic journeys

- Test each critical journey from a clean, known state.
- Cover success, empty, error, restart/recovery, and persistence paths where they exist.
- Exercise supported pointer, keyboard, and touch input rather than assuming one input represents all others.
- Reproduce suspected failures at least once. Reproduce BLOCKER and HIGH findings from a reset state before finalizing them whenever possible.
- Capture the shortest reliable reproduction path.

### 3. Seeded behaviour and abuse

- Run cheap, repeatable behaviour policies before using AI personas: rapid taps, double activation, skipped instructions, invalid order, repeated restart, navigation interruption, resize/orientation change, refresh, stale storage, and slow or failed network where appropriate.
- Use fixed random seeds and record them. Keep failures replayable.
- Never treat chaos volume as proof of coverage; map each run to a risk or journey.

### 4. Visual and accessibility inspection

- Inspect the rendered app at representative desktop and narrow/touch-oriented sizes.
- Check clipping, overlap, unreadable hierarchy, broken responsive states, awkward whitespace, off-screen controls, contrast, focus visibility, keyboard reachability, labels, motion, and feedback timing.
- Capture screenshots of important states, not only the landing screen.
- Use automated accessibility scans when available, then manually inspect the affected flows. Automated scans do not replace keyboard and visual checks.
- Compare against a supplied reference only with reproducible side-by-side evidence. Do not claim that the app “matches” or “beats” a reference from memory.

### 5. Optional persona and educational evaluation

- Use AI personas only after deterministic checks, and only when their cost and added judgment are justified.
- Model personas as bounded behaviours and constraints, not as authentic representations of people.
- For learning apps, separately assess whether a failure is caused by the academic concept, interface confusion, unclear feedback, reading load, or accessibility.
- Never represent a synthetic persona opinion as evidence about real learners.

Read [references/qa-standard.md](references/qa-standard.md) before a full check, an educational-app check, or any release recommendation.

## Classify every finding

Assign one severity:

- **BLOCKER** — prevents a critical journey, causes data loss/security exposure, or makes the app unusable for a required audience or platform.
- **HIGH** — materially breaks an important feature or repeatedly causes users to fail, with no reasonable workaround.
- **MEDIUM** — meaningful defect or friction with a workaround or limited scope.
- **LOW** — minor polish, consistency, or low-impact issue.

Assign one primary type:

- **SOFTWARE BUG**
- **UX FRICTION**
- **ACCESSIBILITY**
- **DEVICE / INPUT ISSUE**
- **PERFORMANCE / RELIABILITY**
- **LEARNING-DESIGN RISK**
- **PERSONA OBSERVATION**

Do not turn taste into a bug. Report subjective concerns as observations unless evidence shows task failure or violation of an explicit requirement.

## Require finding-level evidence

For every material finding, include:

- concise title and stable ID;
- severity, type, and confidence;
- affected journey and environment;
- preconditions;
- minimal numbered reproduction steps;
- expected and actual behaviour;
- frequency or reproduction count;
- screenshot, trace, console excerpt, or other evidence path when available;
- likely impact;
- suggested next action, clearly separated from verified facts.

Label anything that could not be reproduced as **unconfirmed**. Never invent a test result, screenshot, trace, device pass, or user reaction.

## Fix only within authority

- For requests to **check**, audit and report. Do not modify the app.
- For requests to **fix**, make the smallest evidence-backed change, then rerun the exact reproduction, affected journey, adjacent regression path, and relevant hard gates.
- Do not alter a target app merely because a persona disliked something.
- Do not create test accounts, seed production data, spend money, send messages, or run destructive production tests without explicit authority.
- If login, unavailable hardware, external services, or protected production state blocks testing, complete every safe check and state the precise remaining gap.

## Deliver the result

- Lead with release status: **PASS**, **PASS WITH RISKS**, **FAIL**, or **BLOCKED**.
- State the tested scope and important exclusions.
- Summarize hard-gate results and the device/input matrix.
- List findings in severity order; keep verified defects separate from observations.
- Name the top recommended actions.
- Link the report and evidence artifacts.
- If the app is running locally, provide the verified viewing URL and exact relaunch command.

Use [assets/APP-CHECK-REPORT.template.md](assets/APP-CHECK-REPORT.template.md) for a durable report. Store evidence in a project-local QA results folder unless the repository specifies another location.

## Stop only at a defensible boundary

Stop when the selected scope is complete, hard gates and critical journeys have evidence, material failures have been reproduced or marked unconfirmed, visual inspection is complete, and the report distinguishes facts from inference. If a required surface cannot be tested, return **BLOCKED** only for that surface and report the completed evidence separately.
