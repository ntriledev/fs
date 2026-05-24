---
name: infographic-creator
description: Automatically transforms complex data, articles, transcripts, or research topics into professional, production-ready visual infographics. Trigger this skill whenever the user mentions data visualization, charts, layout design, summaries, or explicitly requests an infographic.
metadata:
  version: 1.0.0
  framework: AntV-Infographic-Syntax
---

# Infographic Creator Skill

## CONSTRAINTS
* **Code Only**: Output exactly one plain Markdown code block containing the infographic data. Do not add conversational text or intros.
* **Scannability**: The final structure must be cleanly scannable in under 30 seconds.
* **Indentation**: Must use two spaces for hierarchy blocks. Do not use tabs.
* **Icons Requirement**: Every major semantic data point must include an icon. Use precise IDs (e.g., `mingcute/server-line`) or raw keyword phrases without hyphens (e.g., `rocket launch`, not `rocket-launch`).

## WORKFLOW

### 1. Information Extraction & Structural Analysis
Analyze the user's raw text or data inputs to extract:
* Main Title & Objective Subtitle.
* Core data metrics, chronological markers, or conceptual entities.
* Structural grouping pattern (Sequential, Comparative, Hierarchical, or List-based).

### 2. Layout Selection Rules
Match the underlying data pattern to one of these 4 primary infographic layouts:
* **`sequence-*`**: Use for timelines, step-by-step instructions, or chronological workflows.
* **`compare-*`**: Use for pros/cons, before/after, or two-sided comparisons. *Constraint: Must have exactly two root nodes with children.*
* **`hierarchy-*`**: Use for org charts, value chains, or nested technical architectures.
* **`list-*` / `chart-*`**: Use for standalone data points, statistics, or general summaries.

### 3. Syntax Generation Specification
The generated file must strictly obey the syntax prefix:
* Must begin with a root `layout:` declaration matching the selected layout from Step 2.
* Must include global `title:` and `subtitle:` strings.
* All data points must be nested inside a `nodes:` array.
* Each node block must declare `title:`, `icon:`, and `content:`.
* Nodes may optionally include `value:` (for metrics/percentages) or `children:` (for nested sub-points).
* Two-space indentation must be strictly maintained for all nested arrays and objects.

### 4. Output Generation
Synthesize the extracted data into the final YAML-style syntax structure. 

#### Example Output:
```yaml
layout: sequence-timeline
title: "Deployment Pipeline Workflow"
subtitle: "Standard continuous integration process"
nodes:
  - title: "Build"
    icon: "mingcute/box-3-line"
    content: "Compile application code and resolve dependencies."
    value: "Phase 1"
  - title: "Test"
    icon: "mingcute/check-circle-line"
    content: "Execute automated unit and integration tests."
    value: "Phase 2"
    children:
      - title: "Code Coverage"
        icon: "target"
        content: "Must exceed 85%"
```

## FALLBACK MECHANISMS

* **Ambiguous Data**: If the user's input lacks a clear chronological or comparative structure, default to the `list-standard` layout.
* **Icon Resolution**: If a precise icon ID cannot be determined, fall back to a generic descriptive keyword string (e.g., `data chart` or `document`).
* **Formatting Errors**: If the generated structure violates the two-space indentation rule or lacks required root nodes for the `compare-*` layout, automatically regenerate the structure to comply before outputting.