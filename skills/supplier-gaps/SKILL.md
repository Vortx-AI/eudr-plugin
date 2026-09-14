---
description: Find which suppliers still need documentation under EUDR Article 9(1), and draft what to request from each. Use when asked which suppliers are missing information, what to chase, or whether a supplier file is ready to file on.
---

# Supplier documentation gaps

Article 9(1) of Regulation (EU) 2023/1115 is a closed list of seven
items an operator must collect and keep for five years. Whether a
supplier file satisfies it is a question of which fields are present,
not a judgement call — so run it through `eudr_assess_evidence_gaps`
rather than reasoning about it yourself.

## How to work

**Gather what the user holds, per supplier.** Name, postal address,
email, country of production, commodity, HS code, product description,
quantity, how many plots the supplier declares and how many of those
you hold coordinates for, the production date range, any
deforestation-free evidence already held, and which legality documents
exist.

**Absent is a valid answer.** If the user does not know whether a
supplier's email is on file, leave the field out. The tool reports
missing fields; guessing them fills the file with fiction.

**Pass everything in one call.** The tool takes up to fifty suppliers
and returns a row each, which is what makes a portfolio view possible.

**Sort the output by consequence.** `blocking_gaps` is the number that
matters — those stop a statement being filed at all. Items that are
not blocking still leave the file incomplete and are worth chasing,
but they are a different conversation.

## What to hand back

Lead with the count: how many files are complete, how many are
blocked. Then, per supplier that needs work, the article limb, what is
missing in the Regulation's own words, and the request to send. The
tool's `request` field is already phrased as an instruction the
operator can forward — use it rather than rewriting it.

Where a supplier is missing Article 9(1)(f) evidence and you have
their plot boundaries, offer to run `eudr_check_plots` and close that
gap directly.

## The limit worth stating

This compares supplied fields against the article. It reads no
documents. A supplier who has a land title on file and a supplier who
has an expired, forged, or irrelevant land title on file look
identical here. Holding a document is not the same as the document
being valid, and validating it is the operator's job.
