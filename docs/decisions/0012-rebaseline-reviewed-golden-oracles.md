---
format_version: 1
id: ADR-0012
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: tests/golden-oracles
---

# Rebaseline review-corrected golden oracles

## Decision

The golden corpus corrected after final review is the reproducible baseline for
W-006. Its six files and SHA-256 values are listed in
`tests/cases/MANIFEST.sha256`; the contract validator recalculates every hash
and rejects missing, additional, or changed case files.

The 28th spacing case, `wpds-heading-intro`, was added during W-005 because the
review found a real gap between specification and oracle. The historical
pre-W-005 state with 27 cases is therefore no longer the semantically correct
oracle. W-006 tests the explicitly rebaselined state instead of claiming that
an unsaved earlier state remained unchanged.

## Problem

The Plan required oracles frozen before W-005, but stored neither Git history
nor file hashes. After the necessary heading-to-intro correction, the old state
was neither correct nor reproducible. A case count alone could not detect later
silent changes.

## Drivers

- Material review corrections must not be discarded to preserve a process
  claim.
- W-006 needs a reproducible, machine-checkable baseline.
- Every later oracle change must be visible and justified.
- Case count and content must be protected separately.

## Considered alternatives

1. Remove the 28th case: would reopen the evidenced heading-to-intro gap.
2. Document only the count of 28: would not detect content changes.
3. Reconstruct a historical state from memory: would not be reliable evidence.

## Consequences

- The current corpus is frozen from the time of this Decision.
- A semantically necessary change requires a new or superseding Decision, an
  updated manifest, and rerun affected checks.
- W-006 must not claim that the 27-case state remained unchanged.
- The manifest is test evidence, not a replacement for fresh-agent or runtime
  validation.

## Confirmation

The Decision is implemented when `MANIFEST.sha256` contains each of the six
case files exactly once, the contract validator verifies the current SHA-256
values, and W-006 references ADR-0012 as its Decision.

## Revisit when

A golden case must change semantically, new case files are added, or version
control assumes responsibility for baseline evidence.
