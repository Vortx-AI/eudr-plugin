# EUDR compliance plugin

Checks agricultural plots against Regulation (EU) 2023/1115 (the EU
Deforestation Regulation) and prepares the Due Diligence Statement an
operator files before placing goods on the EU market.

Built for exporters, cooperatives, and procurement teams working on
farm-to-consignment traceability — the people who have to produce
evidence, not the people asking for farming advice.

## Install

```
/plugin install eudr --marketplace Vortx-AI/eudr-plugin
```

That one line needs Claude Code 2.1.275 or later. On an older version, add the marketplace first:

```
/plugin marketplace add Vortx-AI/eudr-plugin
/plugin install eudr@eudr
```

Or point Claude Code at a checkout of this repository:

```
claude --plugin-dir ./eudr-plugin
```

## One repository, two directories

Claude and ChatGPT read different files, and Claude's directory refuses fields it does not know.

| Directory | Files it reads | Where they are |
|---|---|---|
| Claude | `.claude-plugin/plugin.json`, `.mcp.json`, `skills/` | This repository, which Claude's directory reads from the root. |
| ChatGPT | `plugin.json`, `mcp.json` (Agent Plugins format, with the OpenAI sign-in settings) | Not stored here. Built from this repository into a zip by the eudr.dev team. |

Claude's directory scans this whole repository and refuses it if it holds a script or program (any `.py`, `.sh`, `.js` or file starting with `#!`), or a field Claude Code does not read. So:

- keep `.mcp.json` to `type` and `url`, with no OpenAI fields;
- keep scripts, including the ChatGPT package builder, out of this repository.

Before a push, run `claude plugin validate . --strict`.

## What it connects to

A remote MCP server at `https://eudr.dev/mcp`. No account, no API key,
no credential to hand over: every tool below is reachable with an
HTTP client. Nothing is installed or run on your machine; the plugin
is the server address, three skills, and this file.

## What the tools can do

Most tools only read. These are the ones that do more, in plain words:

- **Pay.** `eudr_prepare_dds` spends credits from the organisation's wallet:
  5 for a statement, plus 1 for each plot after the first. Credits are
  refunded if the compile fails. No other tool costs anything, and no tool
  takes a card payment or buys credits.
- **Send to another service.** `eudr_check_plots`, `eudr_prepare_dds`,
  `eudr_create_farm` and `eudr_set_farm_boundary` send plot geometry (and,
  for a statement, HS code, country and quantity) from eudr.dev to emem.dev to be
  measured and signed. Operator and supplier names and contact details are
  not sent there. No tool sends email or messages to anyone.
- **Publish.** `eudr_prepare_dds` makes a share link for the statement's
  report, valid for 7 days, that opens without signing in. The organisation
  can withdraw it from its account.
- **Change access.** `eudr_request_supplier_evidence` creates a one-time link
  that lets whoever holds it submit plot boundaries and production details
  into the organisation's account. The tool returns the link; it does not
  send it to anyone.
- **Replace data.** `eudr_set_farm_boundary` replaces a farm's boundary. The
  old outline is kept in the farm's history, but the call does not undo
  itself, and the compliance answers change with the boundary.
- **Write records.** `eudr_create_farm` adds a farm, `eudr_decide_lot` stores
  a buying decision, `eudr_prepare_dds` stores the compile, and the first
  `eudr_account_usage` call opens the wallet with its free credits.

No tool deletes a record, files anything with an authority (TRACES or any
other), or changes who is a member of an organisation.

## Tools

| Tool | What it does | Does more than read |
|---|---|---|
| `eudr_check_plots` | Forest loss after the 31 Dec 2020 cut-off, per plot | sends plot geometry to emem.dev |
| `eudr_fetch_evidence` | Pages the signed satellite facts behind a check | no |
| `eudr_assess_evidence_gaps` | Missing Article 9(1) information, per supplier | no |
| `eudr_lookup_reference` | Country risk tiers, Annex I commodity mapping | no |
| `eudr_verify_receipt` | Signature and content address on a statement | no |
| `eudr_prepare_dds` | Compiles and signs an Annex II statement | **pays** credits, **sends** plot data to emem.dev, **publishes** a 7-day share link, writes |
| `eudr_get_dds` | Reads the outcome of a compile | no |
| `eudr_execution_trace` | The full derivation chain behind a verdict | no |
| `eudr_import_shipments` | Reads a CSV or GS1 EPCIS consignment list | no |
| `eudr_export_statement` | TRACES XML, Annex II JSON, or plot GeoJSON | no (exporting is not filing) |
| `eudr_list_statements` | The organisation's statements, newest first | no |
| `eudr_compliance_status` | How many statements are filable, blocked or unresolved | no |
| `eudr_mitigation_status` | Open Article 11 risk-mitigation plans | no |
| `eudr_account_usage` | Credit balance and what it covers | the first call opens the wallet |
| `eudr_list_supplier_requests` | Supplier evidence requests issued, and their state | no |
| `eudr_request_supplier_evidence` | A one-time link for a supplier to submit evidence | **changes access**: whoever holds the link can submit data |
| `eudr_list_farms` | The organisation's farms | no |
| `eudr_create_farm` | Adds a farm, with its boundary if known | writes; **sends** the boundary to emem.dev |
| `eudr_set_farm_boundary` | Sets a farm's boundary | **replaces** the old boundary; **sends** it to emem.dev |
| `eudr_procurement_overview` | Farms and recent buying decisions | no |
| `eudr_decide_lot` | Runs the buying process on a banana lot | writes a decision |

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
| `https://eudr.dev/mcp` (MCP, operated by Vortx AI Private Limited) | Whatever a tool is given: plot boundaries (GeoJSON) or points, commodity, HS code, country of production, quantity; for `eudr_assess_evidence_gaps`, the supplier fields you pass (name, postal address, email, plot counts, dates); for `eudr_prepare_dds`, the operator, supplier and product details of the statement; for `eudr_import_shipments`, the CSV or EPCIS file; for `eudr_create_farm` and `eudr_set_farm_boundary`, the farm's name, crop, location and boundary; for `eudr_decide_lot`, the lot's details | A compiled statement and its signed receipt are kept as the operator's record for five years from submission (Regulation (EU) 2023/1115, Art. 4(3), 9(1), 12(5)). Working memory for a task is kept 7 days by default. The evidence handle behind a plot check is held for about a day |
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
