# F01 acceptance deferred

2026-09-11: source changes authorized; acceptance explicitly deferred by the user.
SKILL.md and references/routing.md now require inspecting accessible ownership
evidence before asking. No tests, model probes or runtime checks have run.

Pending cases:
- Source identifies PHP/Core: resolve it without a question.
- Relevant runtime remains unknowable: ask one specific question and withhold
  dependent recommendations while continuing independent checks.
- Source-only audit completes without requiring a browser.
- Excluded host surfaces remain excluded; preserve source/measurement/view order.

These are four small new instruction probes, not existing routing fixtures.
Do not resume or mark done the separate USER-DEFERRED-TESTS Work Item W-002.
Identify the actual loaded package/version when observing behavior. Resume these
cases only on user request; record results and limits rather than assuming a pass.
