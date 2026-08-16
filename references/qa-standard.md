# APP_CHECKER quality standard

Read this standard for full checks, release recommendations, educational apps, or disputed severity.

## Quality lanes

Evaluate these lanes independently so a strong build does not hide a poor user experience:

1. **Functional reliability** — launches, core journeys, state transitions, recovery, persistence, and error handling.
2. **Interaction reliability** — pointer, keyboard, touch, rapid activation, focus, orientation, and viewport changes.
3. **Visual integrity** — layout, hierarchy, responsive behaviour, readability, feedback states, clipping, overlap, and consistency.
4. **Accessibility** — semantic names, focus order and visibility, keyboard completion, contrast, zoom/reflow, reduced motion, and meaningful status feedback.
5. **Performance and resilience** — startup, responsiveness, long tasks, loading feedback, network failure, console errors, and resource failures.
6. **Trust and safety** — privacy, destructive actions, permissions, data loss, misleading confirmation, and unsafe production mutation.
7. **Learning design** when relevant — clarity of instruction, reading load, correctness, feedback usefulness, misconception risk, and distinction between concept failure and interface failure.

## Severity decision test

Choose the highest level whose definition is supported by evidence:

| Severity | User impact | Scope | Workaround | Release effect |
| --- | --- | --- | --- | --- |
| BLOCKER | Critical outcome impossible, data/security harm, or required audience excluded | Critical or widespread | None | Do not release |
| HIGH | Important outcome broken or repeated severe confusion | Common or important | None or unreasonable | Fix before normal release |
| MEDIUM | Meaningful defect or friction | Limited or intermittent | Practical | Schedule and disclose |
| LOW | Minor polish or consistency issue | Narrow | Easy or unnecessary | Does not block |

Raise confidence only when the reproduction is stable and evidence is direct. Keep severity and confidence separate: a rare crash may be BLOCKER with medium confidence.

## Minimum matrices

### Micro

- Affected journey.
- One adjacent journey.
- Primary supported viewport/input.
- Relevant existing automated checks.
- Before/after visual state if changed.

### Focused

- Main critical journey and important failure paths.
- Desktop plus one narrow/touch-oriented viewport when supported.
- Pointer plus keyboard; touch when supported.
- Clean start, refresh/reload, and recovery.
- Console/network inspection.
- Accessibility basics and screenshots of key states.

### Full

- Every declared critical journey.
- All declared input modes and representative viewports.
- Existing hard gates plus deterministic end-to-end paths.
- Seeded behaviour/abuse runs mapped to risks.
- Accessibility automation plus manual keyboard and visual inspection.
- Performance and resilience signals.
- Independent critic pass when the host allows it; otherwise perform a fresh final pass after setting aside builder assumptions.
- Educational evaluation for learning products.

## Behaviour policies

Prefer replayable policies over vague “AI users.” Useful policies include:

- skip onboarding or instructions;
- double-tap or rapid-tap a primary control;
- choose an invalid sequence;
- navigate away and return mid-task;
- refresh during a save or transition;
- repeat pause/resume, undo/redo, start/restart, or open/close;
- switch viewport or orientation;
- use stale or empty local storage;
- simulate slow, failed, or recovered requests;
- wait without acting to test timeouts and idle feedback.

Record the policy, seed, actions, and resulting state. Use volume to discover candidates, then reduce each failure to a small deterministic reproduction.

## Educational overlay

For each learner failure, test these competing explanations:

- academic misunderstanding;
- unclear instruction or vocabulary;
- excessive reading or memory load;
- ambiguous control or state;
- feedback that does not explain how to recover;
- accessibility or input barrier;
- synthetic-persona artifact.

Classify only what the evidence supports. Recommend real learner testing for claims about motivation, comprehension, age suitability, or classroom behaviour.

## Release statuses

- **PASS**: Selected scope completed; no unresolved BLOCKER/HIGH finding; hard gates pass; exclusions are not material.
- **PASS WITH RISKS**: No confirmed release blocker, but material MEDIUM findings, untested secondary surfaces, or explicit limitations remain.
- **FAIL**: A confirmed BLOCKER/HIGH finding or failed hard gate makes the selected release bar unacceptable.
- **BLOCKED**: A required surface could not be assessed because evidence access, environment, credentials, hardware, or external state was unavailable. Do not label completed surfaces blocked.

## Evidence integrity

- Cite artifact paths and exact test conditions.
- Separate observed fact, inference, and recommendation.
- Preserve failure artifacts before fixing.
- Do not call an untested surface a pass.
- Do not silently discard flaky failures; report frequency and investigate isolation, state leakage, timing, and environment.
- Re-run after fixes with the same conditions first, then adjacent regression coverage.
