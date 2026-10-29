# Rampart adapter

This experimental branch reuses Hallmark's static checker while preserving the project's approved design system and scoped preferences. Upstream is pinned to 8f6969f8922caabde9de1784959eae11ddf68073; its MIT notice remains in LICENSE. No upstream files are changed.

Run from a scratch evaluation directory:

```sh
python3 /path/to/hallmark/rampart/audit.py /path/to/page.html /path/to/style.css --output report.json
```

Use `--scope app` for a working application, `--scope component` for a component, and `--stage hero` for an opening-only experiment. The report retains every upstream finding, severity and suggested fix. `functional-review` identifies candidates for factual, accessibility or behavioral inspection; `design-review` identifies choices requiring contextual judgment. `finish` remains advisory. An upstream FAIL is not silently accepted or automatically treated as a defect in the project. Inspect it, document the reason and use actual browser evidence to decide.

The command's success means a report was written. It has no quality-pass exit code. Zero findings do not prove accessibility, correct behavior or strong design. Static inspection misses generated DOM, external services and runtime state. Browser rendering is intentionally excluded from this adapter; use the environment's supported browser controls for the actual page, keyboard behavior, motion and responsive states.

For a redesign, `--mode before` writes Hallmark's inventory in `.hallmark/` under the working directory. After revising a disposable copy, `--mode kept` compares the same target paths. Treat lost links/fields/handlers as findings to inspect. Names are not proof of behavior; generated controls can be absent from the static inventory.

## Process to transfer

1. Read the real brief, existing system, available assets and scoped taste evidence.
2. Separate visual material from task/content structure. A typography or surface reference cannot dictate the whole page's section order.
3. Prove the uncertain execution before expanding it. A website opening, placed ad, brand application, social format, narrative scene and software task are different tests.
4. Record the selected direction in the existing dossier with its actual composition, typography, color, asset and motion choices. Compare recent relevant builds; repeat a choice when identity or task warrants it. Variety alone is not evidence of fit.
5. Preserve working content and behavior. Inspect machine findings separately from visual quality. Get a separate reviewer when the environment and task allow one; otherwise label self-review.
6. Keep first outputs. Compare the next task using frozen criteria, and show how a saved preference changed the work.

Theme rotation is not machine learning. Human preference evidence, retrieval, application and later evaluation remain separate stages. Hallmark's website themes and checks do not assess brand strategy, advertising outcomes, community practice, narrative quality or software correctness.
