# Aegis Series-7 HCS — Knowledge Ingestion Challenge

A provenance-first ingestion and question-answering system for the fictional Aegis Series-7 Hydraulic Control System documentation package.

## What this submission demonstrates

- Ingestion of all supplied formats: PDF, scanned PDF, HTML, XLSX, DOCX, PNG, JSON and PPTX.
- Explicit trust/source metadata and document supersession handling.
- A small intermediate knowledge representation (entities, facts, conflicts, evidence).
- Alias and identifier normalization (for example `P.S.04-A` → `PS-04A`).
- Version-scoped facts (180 bar before software 3.2 vs 200 bar on 3.2+).
- Explicit conflict representation rather than silent overwrite.
- Provenance attached to every answer claim.
- Abstention for questions unsupported by the package.
- A deterministic evaluation harness over the 23 supplied questions.
- CLI query interface plus an optional Streamlit UI (`app.py`).

## Architecture

```text
                    ┌─────────────────────────────┐
                    │       Raw documents         │
                    │ PDF/scan/HTML/XLSX/DOCX/PNG │
                    │ JSON/PPTX                   │
                    └──────────────┬──────────────┘
                                   │
                         format-specific parsers
                                   │
                    ┌──────────────▼──────────────┐
                    │ normalized source chunks    │
                    │ text + page/sheet/slide     │
                    │ + source metadata           │
                    └──────────────┬──────────────┘
                                   │
                  deterministic extraction + OCR
                                   │
              ┌────────────────────▼────────────────────┐
              │ intermediate knowledge representation  │
              │ entities | aliases | facts | evidence  │
              │ applicability | confidence | conflicts │
              └────────────────────┬────────────────────┘
                                   │
                         retrieval / intent routing
                                   │
                    ┌──────────────▼──────────────┐
                    │ answer synthesizer          │
                    │ answer + claims + evidence  │
                    │ + uncertainty/gaps          │
                    └─────────────────────────────┘
```

### Why deterministic first?

This package is small, structured, and safety-relevant. A deterministic extraction layer is easier to audit than asking an LLM to ingest everything and silently resolve conflicts. Model-based generation can be placed above this layer later, but it should consume structured facts and evidence rather than invent them.

## Knowledge representation

A fact has:

- `subject`
- `predicate`
- `value`
- `unit` (optional)
- `applicability` (software revision / configuration / time scope)
- `source_id`
- `location` (page, section, sheet, slide, image)
- `trust`
- `confidence`
- `evidence_type`

A source has:

- `source_id`, path, format
- trust class
- revision/effective date where known
- supersession notes

Conflicting facts are retained as separate records. A resolver selects the applicable fact only when scope and source precedence justify it.

## Trust policy

1. Controlled operator/maintenance manuals and controlled reference registers: high.
2. Released Engineering Change Notices: highest for the change they introduce.
3. Revision history/configuration: high for their own domains; configuration is machine-specific.
4. Screenshots/training material: corroborating evidence; not a replacement procedure.
5. Field notes: low trust and never silently override controlled documents.
6. Irrelevant SDS: ingested but excluded from HCS Q&A unless explicitly queried.

## Running

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt

python build_knowledge.py
python -m src.evaluation.evaluate
python cli.py "What is the current normal operating pressure for the HPU?"
```

Optional UI:

```bash
pip install streamlit
streamlit run app.py
```

## Design decisions / what I chose not to do

- I did not make a vector database a prerequisite. For a small corpus, structured retrieval is more reproducible and auditable.
- I did not silently treat every document as equally authoritative.
- I did not use a low-trust field observation to replace a controlled value.
- I did not invent answers for temperature, calibration interval, ECN approver, MTBF, or 3-phase compatibility where the supplied package is silent.
- Diagram topology and screenshot interpretation are represented as visual evidence records. These are deliberately kept separate from ordinary text extraction because line/shape relationships cannot be recovered reliably from OCR alone.
- The supplied maintenance manual file is a compact synthetic artifact even though the task description describes a larger page count; the implementation uses the actual supplied bytes, not assumptions about missing pages.

## Evaluation metrics

The evaluator reports:

- claim coverage: whether expected claims are present in the generated answer;
- evidence coverage: whether each expected answer is backed by evidence;
- citation precision: whether cited source IDs are among the expected evidence sources;
- abstention accuracy: whether unsupported questions are correctly marked indeterminate;
- overall question score.

The gold set is intentionally claim-oriented rather than exact-string-oriented so harmless wording differences do not count as failures.
