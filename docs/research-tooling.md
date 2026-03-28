# Research Tooling Note

## Purpose

This note captures the kinds of tools that would most improve the research workflow as the project grows.

The current repository works well as a markdown-first workspace. Over time, stronger research support will likely come from better source collection, extraction, comparison, and citation handling rather than from heavier product infrastructure.

## High-value research tooling

### 1. Web access and page capture

Useful for:

- searching open-web material quickly
- loading JavaScript-heavy pages
- capturing unstable or changing web content

Examples:

- browser automation such as `playwright`
- improved page fetch and extraction tools

## 2. Document ingestion

Useful for:

- reading PDFs, reports, and long-form source documents
- extracting text from researcher-provided files
- treating user-supplied documents as first-class research inputs

Examples:

- PDF text extraction
- document parsers for reports and academic papers

## 3. Source extraction and cleanup

Useful for:

- turning messy web pages into clean text
- separating article content from navigation and boilerplate
- preparing notes from web material with less manual cleanup

Examples:

- `trafilatura`
- `beautifulsoup4`

## 4. Structured comparison and evidence tables

Useful for:

- comparing scenario families across criteria
- building lightweight evidence matrices
- tracking claims, sources, uncertainty, and contradictions

Examples:

- `pandas`
- simple CSV or markdown table workflows

## 5. Citation and bibliography support

Useful for:

- keeping source references consistent
- generating bibliographies from notes and syntheses
- reducing citation drift across the repo

Examples:

- BibTeX or CSL-based citation tooling
- DOI-aware reference collection

## 6. Exploratory analysis environments

Useful for:

- trying lightweight analysis without overcommitting to a product
- inspecting datasets or evidence tables
- pairing narrative notes with quick quantitative checks

Examples:

- `jupyter`
- notebooks for comparative analysis and source review

## 7. Method infrastructure tooling

Useful for:

- reducing coordination overhead across sessions
- tracking branch maturity and next recommended passes
- validating whether loop runs are missing critical artifacts
- generating branch dossiers and next-pass packets

Examples:

- a small Python CLI
- JSON manifests for branches and runs
- generated markdown dossiers or check reports

## Working principle

Tooling should strengthen rigor, traceability, and source handling. It should not make the project look more certain than the evidence allows.

It should also improve accessibility. The long-term aim is not a workflow that is impressive only when paired with expensive frontier access. It is a workflow whose high-capability components are justified, bounded, and eventually complemented by cheaper or local tooling where quality allows.

## Near-term recommendation

If the repo adds any tooling soon, the highest-value order is:

1. better web and PDF capture
2. cleaner source extraction
3. simple citation support
4. structured evidence tables
5. lightweight method infrastructure

That order keeps the project focused on research quality before automation complexity.

## Model-use design principle

As the project matures, model and tooling choices should follow a `right-sized capability` rule:

- use frontier capability where it shapes the method or prevents major quality loss
- use cheaper or local tools where tasks are repetitive, well-bounded, or easy to verify
- redesign the process itself when a step is only expensive because the workflow is poorly structured

This should be read broadly. The available AI ecosystem is diverse and expanding, so the method should learn to allocate work across many possible tool types rather than treat model choice as a binary frontier-versus-cheap question.

The goal is not merely lower cost. The goal is a leaner research process that remains rigorous and broadly runnable.

The first CLI layer should therefore automate method overhead rather than research judgment.
