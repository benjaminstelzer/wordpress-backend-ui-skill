# WordPress 7.1 compatibility review

Date: 2026-09-03
Outcome: complete

## Scope

Two independent, read-only reviews of the uncommitted 7.0/7.1 Skill update.
The goal was correct Core-token and public-provider guidance without forcing
existing Classic pages to migrate. Both reviewers received the same initial
consultation and the same correction follow-ups. Their advice was verified
before changes were applied by the primary agent.

## Reviewers

- Fable: requested `claude-fable-5-1`, effort `high`, persistent session followed
  by two resumes. Session ID: `e87bca8e-4e6c-4bee-a835-b0352e0cee45`.
  The adapter returned no independent reported-model value. Local
  customizations were disabled. Final answer: no material correction remains.
- SOL: requested `gpt-5.6-sol`, effort `xhigh`, initial context mode `fresh`.
  Agent target: `/root/sol_wp71_skill_review`, continued for two re-reviews.
  Final answer: no material correction remains.

## Corrections applied

1. Require both an exact stable 7.1.x version shape and style registration for
   the documented Core-token branch. Do not mistake a 7.0 backport or foreign
   handle for the verified Core 7.1 capability.
2. Preserve the numeric layout fallback when the 7.1 handle is missing, but
   explicitly fail token acceptance. The rendered assertion follows the
   supported installation version, not the branch selected at runtime.
3. Reject prereleases and other minor lines from the verified 7.1 branch.
   Tests cover stable 7.1.1, 7.1.1-alpha and 7.2-alpha.
4. Replace the maintenance-branch release claim with the stable WordPress 7.1
   tag. Record the published `@wordpress/theme` 1.0.0 package contract.
5. Describe the provider's wrapper accurately: a `div` using
   `display: contents`, with a resolved radius attribute and no wrapper
   customization props. The initial suggestion that it necessarily creates
   an extra layout box was not adopted.
6. State that 7.1 exposes no public density switch. Distinguish authored token
   fallbacks from generated build-tool output.
7. Remove the unnecessary local spacing variable from the older example,
   document validation command requirements, and link historical specs to
   the current version addendum.
8. Narrow the provider validation claim to source checks. Preserve the
   existing 7.0 fixture graph and its historical rendered evidence.

## Executed evidence

The primary agent ran these successfully after the final corrections:

- `npm run check:contracts`, including the eight-case executable PHP example.
- `npm run check:local-wordpress -- PATH70 PATH71` against local stable
  WordPress 7.0 and 7.1 Core directories.
- Skill Creator `quick_validate.py`.
- Scoville Plan `validate_profile.py`, zero errors and warnings.
- `git diff --check`.

## Limits

Fable could inspect sources but could not execute the tests. SOL executed the
contract and PHP-example checks. Neither review replaces a rendered UI audit.
The 7.1 React provider example has not been tested through a separate plugin
build or browser fixture. Its exact npm build identity inside the released
Core bundle is not independently proven, although the stable Core bundle's
public export and the published package contract were inspected.

No installed Skill copy, customer plugin, GitHub branch, or release was changed.
