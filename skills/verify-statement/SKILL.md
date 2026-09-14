---
description: Verify the evidence behind an EUDR due diligence statement or supplier report — check the signature, re-derive the content address, and page the satellite facts it rests on. Use when asked to verify, audit, or check the integrity of a statement, receipt, or evidence someone else supplied.
---

# Verify a statement someone else supplied

Verification here answers a narrow question precisely, and the
precision is the value. Be careful not to let it read as more.

## What each check establishes

- **`eudr_verify_receipt`** re-derives the receipt's content address
  from its canonical payload and checks the ed25519 signature. A pass
  means: these exact bytes were signed by that key, and nothing has
  changed since. It does **not** mean the conclusion inside is
  correct, and it does not mean the signer is trustworthy.
- **`eudr_fetch_evidence`** pages the satellite facts a check rested
  on. Each entry is a content address that resolves at emem.dev and
  verifies offline against the responder's key — a signing layer
  independent of eudr.dev, which is what makes the chain worth having.
  One party attesting to its own measurements would not be.
- **`eudr_check_plots`** re-runs the question from the boundary. This
  is the strongest check available: if the counterparty's claim and a
  fresh check disagree, that gap is the finding.

## How to work

Start from whatever the user has. A receipt: verify it. An
`evidence_cid`: page it. A plot boundary and a claim: re-run the check
and compare.

If a receipt fails to verify, say which way it failed — an address
that does not match the payload means the document was edited after
signing, which is a different and more serious finding than a
signature that does not match the key.

If an `evidence_cid` does not resolve, that is not evidence of
withdrawal. Handles are held for a day and do not survive a redeploy.
Re-running the check gets you the same measurements, but under new
addresses: each satellite fact is signed with the moment it was signed,
so a fresh read is a fresh receipt. The durable citation is the
statement's receipt CID, not the evidence handle.

## What to hand back

State what was checked, what passed, and what that licenses the user
to conclude. Then state what remains open. A verified signature over a
statement whose legality section was never substantiated is a verified
statement with an unsubstantiated legality section, and it should be
described that way.
