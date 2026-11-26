---
description: Prepare an EUDR evidence pack for a consignment — check the plots, find the gaps in the supplier file, and assemble what is filable and what is not. Use when someone asks to prepare, assemble, or draft EUDR evidence, a due diligence file, or an Annex II statement for a shipment.
---

# EUDR evidence pack

An evidence pack is one consignment's answer to two questions the
Regulation asks separately, and a pack that blurs them is worse than
no pack:

- **Article 3(a), deforestation-free.** Observable from satellite.
  `eudr_check_plots` answers it.
- **Article 3(b), legality in the country of production.** Tenure,
  permits, consent, labour, tax. Documentary. Nothing here observes
  it, and no tool in this plugin can.

## How to work

**1. Establish the plots before anything else.** Ask for GeoJSON
boundaries, the commodity, and the country of production. Call
`eudr_check_plots` once per batch of up to eight plots. If the user has
coordinates but not GeoJSON, help them shape it; a Point is only
admissible for a plot under four hectares that is not forest.

**2. Read the finding, not just the verdict.** The response carries
`coverage.sampled_polygon_fraction`. Below 1.0 means part of the plot
was not inspected, and the claim is correspondingly narrower. Say so.
`observed.loss_years_observed` dates what was found. Report the dates.

**3. If any plot comes back `non_negligible`, stop and say so.**
Article 4(1) bars placing the goods on the market while the risk is not
negligible. Do not assemble a pack around it and do not soften it. The
useful next move is either excluding those plots from the consignment
or re-examining the boundary, and both are the user's decision.

**4. Run `eudr_assess_evidence_gaps` on the supplier file.** Pass what
the user actually holds. Absent fields are the point — they are what
the tool reports. The output separates gaps that block filing from
gaps that leave the file incomplete; keep that separation in your
summary.

**5. Only then consider `eudr_prepare_dds`.** It writes, so confirm
the operator, supplier, product and geolocation details with the user
first, in full, before calling it. It returns a task handle; read the
outcome with `eudr_get_dds`.

## What to hand back

A pack, not a paragraph. Something like:

- **Finding per plot** — verdict, loss years, cells evaluated, and how
  much of the polygon that covered.
- **Evidence anchor** — the `evidence_cid` and the fact count. Offer
  `eudr_fetch_evidence` rather than dumping the CIDs; nobody reads
  seven hundred content addresses in a chat window.
- **Article 9 gaps** — what is missing, by article limb, with the
  request to send the supplier.
- **Unresolved checks** — repeat the ones the check returned. Every
  response carries them, and they are the honest boundary of what has
  been established.
- **Status** — filable, blocked, or incomplete, and what would change
  it.

## Things to get right

- The cut-off is 31 December 2020. Loss before it is not in scope.
- A clean forest-loss result is not a clean due-diligence file. If you
  write a sentence that could be read as "this consignment is
  compliant", it is wrong unless the legality side is also closed, and
  the legality side is closed by documents nobody here has seen.
- A signature on a receipt establishes who signed and that the bytes
  are unchanged. It never establishes that the conclusion is true.
