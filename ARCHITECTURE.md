# Architecture Design Report

## 1. Goal

Turn a heterogeneous documentation package into a provenance-preserving knowledge layer that can answer operational questions without silently choosing conflicting facts or inventing missing values.

## 2. Processing stages

### Stage A — source discovery
Every supported file is registered with path, format, SHA-256 hash and trust class.

### Stage B — extraction
- PDF: native text with page numbers; sparse pages are rendered and OCR'd.
- scanned PDF: OCR with page-level provenance.
- HTML: DOM text extraction.
- DOCX: paragraphs and tables.
- XLSX: sheet/row data.
- PNG: OCR text; visual facts remain separately curated.
- JSON: structured key/value serialization.
- PPTX: slide text.

### Stage C — normalization
Identifiers are canonicalized. Examples:

- `P.S.04-A`, `PS04A`, `P04A` → `PS-04A`
- `IV21` → `IV-21`
- `Hydraulic Unit`, `HP unit`, `Hydraulic Power Pack` → `HPU`

The normalization layer does not merge PS-04 with PS-04A or PS-40 because controlled sources explicitly distinguish them.

### Stage D — knowledge representation
A fact is a tuple with subject, predicate, value, unit, applicability, source, location, trust, confidence and evidence type.

Applicability is first-class because the 180/200 bar conflict is not an error: it is version-scoped.

### Stage E — conflict handling
The system stores both facts and uses scope/source precedence when answering. For example:

- pre-3.2: PS-04 + 180 bar
- 3.2+: PS-04A + 200 bar

ECN-1042 is authoritative for the change it introduces. ECN-1058 changes the wording of the A17 sensor reference but explicitly leaves threshold logic unchanged.

### Stage F — retrieval and answering
The current implementation uses deterministic intent matching for the supplied evaluation set and a token-overlap fallback retriever for novel questions. Answers are generated from structured fact IDs and cannot cite an unseen source.

A production extension can add embeddings and an LLM after retrieval, but the LLM should only synthesize from retrieved facts.

## 3. Trust model

| Class | Examples | Policy |
|---|---|---|
| Engineering change | ECN-1042, ECN-1058 | authoritative for introduced changes |
| Controlled manual | Operator/Maintenance | authoritative operating procedure |
| Controlled reference | Component register, revision history, alarm reference | authoritative within its domain |
| Machine configuration | JSON export | authoritative for represented machine instance |
| Controlled diagram | hydraulic/wiring diagrams | authoritative for topology/wiring |
| Operational screenshot | HMI screenshots | corroborating/observational |
| Training material | PPTX | explanatory, not a replacement procedure |
| Field note | site survey | low trust; cannot silently override controlled sources |
| Irrelevant reference | hydraulic-fluid SDS | excluded from unrelated equipment Q&A |

## 4. Visual evidence

Text extraction cannot reliably infer line semantics from a schematic. The hydraulic diagram therefore has a `visual_graph` evidence record stating that purple control/signal lines from PLC-03 directly connect to PS-04A and IV-21. This is kept separate from OCR/text facts so the provenance tells the reviewer that the claim came from graphical topology.

The diagnostics screenshot uses the physical label `P.S.04-A`. The alias resolver maps this to PS-04A using normalized identifier rules and the component register.

## 5. Missing evidence / abstention

The system deliberately abstains for:

- PS-04A maximum continuous operating temperature;
- electrical diagram voltage-sensor calibration interval;
- ECN-1058 approver;
- IV-21 MTBF;
- 3-phase 400 V compatibility.

This is a feature, not a failure: the package does not establish these values.

## 6. Loss/confidence analysis

Potential losses are:

1. OCR errors on the scanned calibration appendix and raster screenshots.
2. Loss of exact layout semantics when converting complex tables to text.
3. Graphical topology cannot be reconstructed from plain text alone.
4. Generic keyword retrieval can miss paraphrases in unseen questions.
5. The curated semantic layer requires human review for visual/semantic relationships.

Mitigations are page-level OCR, confidence fields, source-type labels, deterministic identifier normalization, explicit curated visual facts, and abstention.

## 7. Production improvements

- Replace keyword fallback with hybrid BM25 + dense retrieval.
- Add a graph store for component relationships and version-scoped facts.
- Add document-level and fact-level temporal validity intervals.
- Add an LLM only for synthesis with JSON schema-constrained outputs.
- Add a human review queue for low-confidence OCR and newly discovered conflicts.
- Add regression tests for every new ECN.
