# EUDR compliance plugin

Checks agricultural plots against Regulation (EU) 2023/1115 (the EU
Deforestation Regulation) and prepares the Due Diligence Statement an
operator files before placing goods on the EU market.

Built for exporters, cooperatives, and procurement teams working on
farm-to-consignment traceability — the people who have to produce
evidence, not the people asking for farming advice.

## Install

```
/plugin marketplace add Vortx-AI/eudr-plugin
/plugin install eudr@eudr
```

Or point Claude Code at a checkout of this repository:

```
claude --plugin-dir ./eudr-plugin
```

## What it connects to

A remote MCP server at `https://eudr.dev/mcp`. No account, no API key,
no credential to hand over: every tool below is reachable with an
HTTP client. Nothing is installed or run on your machine; the plugin
is the server address, three skills, and this file.

## Tools

| Tool | What it does | Writes |
|---|---|---|
| `eudr_check_plots` | Forest loss after the 31 Dec 2020 cut-off, per plot | no |
| `eudr_fetch_evidence` | Pages the signed satellite facts behind a check | no |
| `eudr_assess_evidence_gaps` | Missing Article 9(1) information, per supplier | no |
| `eudr_lookup_reference` | Country risk tiers, Annex I commodity mapping | no |
| `eudr_verify_receipt` | Signature and content address on a statement | no |
| `eudr_prepare_dds` | Starts compiling an Annex II statement | **yes** |
| `eudr_get_dds` | Reads the outcome of a compile | no |
| `eudr_execution_trace` | The full derivation chain behind a verdict | no |
| `eudr_import_shipments` | Reads a CSV or GS1 EPCIS consignment list | no |
| `eudr_export_statement` | TRACES XML, Annex II JSON, or plot GeoJSON | no |

## Prompts

Served by the MCP server, so they appear whether you install the plugin
or add the connector on its own: `check_plots`, `supplier_gaps`,
`evidence_pack`, `verify_counterparty`.

## Skills

- `/eudr:evidence-pack` — assemble a consignment's evidence
- `/eudr:supplier-gaps` — which suppliers need chasing, and for what
- `/eudr:verify-statement` — audit evidence a counterparty supplied

## Scope, stated plainly

This covers **Article 3(a)**, deforestation-free, which is observable
from satellite. It does **not** cover **Article 3(b)**, legality in the
country of production — tenure, permits, free prior and informed
consent, labour, tax. Those are documentary checks the operator
carries out, and every tool response names them as unresolved rather
than letting a clean forest-loss result read as a clean file.

Verdicts are reproducible from the signed per-cell evidence chain.
Nothing is filed with any authority by this plugin.

## Data

The plugin talks to one host. What goes where, and how long it stays:

| Endpoint | What is sent | Kept |
|---|---|---|
| `https://eudr.dev/mcp` (MCP, operated by Vortx AI Private Limited) | Whatever a tool is given: plot boundaries (GeoJSON) or points, commodity, HS code, country of production, quantity; for `eudr_assess_evidence_gaps`, the supplier fields you pass (name, postal address, email, plot counts, dates); for `eudr_prepare_dds`, the operator, supplier and product details of the statement; for `eudr_import_shipments`, the CSV or EPCIS file | A compiled statement and its signed receipt are kept as the operator's record for five years from submission (Regulation (EU) 2023/1115, Art. 4(3), 9(1), 12(5)). Working memory for a task is kept 7 days by default. The evidence handle behind a plot check is held for about a day |
| `https://emem.dev` (the Earth-observation service eudr.dev calls on its own side, same legal person) | From eudr.dev, never from your machine: plot geometry, HS code, country of production and quantity, to be measured and independently signed. No operator or supplier identity | The signed satellite facts are public and content-addressed; they carry no identity |

The plugin itself sends nothing anywhere else, stores nothing locally,
and needs no credentials. The links in a result (for example a fact at
`https://emem.dev/v1/facts/<cid>`) are only opened if you open them.
Who does what with the data, the lawful basis, the processors and your
rights are set out in the privacy notice: <https://eudr.dev/privacy>.

## Licence

Apache-2.0. The eudr.dev runtime is closed;
[emem](https://github.com/Vortx-AI/emem), the Earth-memory protocol
the evidence comes from, is open source. Both are operated by Vortx AI
Private Limited.
