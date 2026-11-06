---
enriched: true
---
## What the original study did

SimEHR (HealthRex; preview released 2026-11-02, no paper yet) is a simulated outpatient EHR in which an AI agent works the way a physician does. The agent sees 1280 × 800 screenshots and acts with mouse clicks, typing, key presses and scrolling. It never sees the page code, the data files or the grading rubric.

Each chart is one synthetic JSON file in a FHIR-like format, coded with LOINC, RxNorm and ICD-10. Every screen is drawn from that one patient record, and every action is written to an audit log.

The preview ships one task, written with a clinician: a patient asks about blood-clot (VTE) prevention before long flights. It is graded on six checkpoints. Two read the audit log (a reply was sent, a note was saved) and four are judged by an LLM (gpt-5.5) on clinical reasoning, acceptable management, patient communication and overall safety. A task passes only if all six pass. In the recorded sessions:
- GPT-6 Astra passed 6 of 6 (58 actions, 8 minutes).
- Claude Opus 5.5 passed 5 of 6 (69 actions, 10 minutes). It failed patient communication: the judge found the reply did not tell the patient explicitly how to use the proposed heparin injections (LMWH).

The full benchmark (PhysicianBench-UI), the agent harness and the judge code are promised with the paper.

**Replicable in part.** The environment, chart, task, rubrics and recorded sessions are open: code under Apache-2.0, data under CC BY 4.0. Re-running agents needs our own harness until theirs is released.

## Data

| Item | What | Access |
| --- | --- | --- |
| SimEHR repo | App, `public/cases/vte-prophylaxis-travel.json`, `demo_task/` (instruction, `rubrics.json`, metadata), `trajectories/` (screenshots, actions, reasoning, final state, verdicts) | Open (`datasets/simehr`) |
| Synthea | Synthetic patient generator for new charts | Open, Apache-2.0 (`datasets/synthea`) |
| NHANES | Aggregate lab distributions to make synthetic lab values realistic | Open (`datasets/nhanes`) |
| MIMIC-IV demo | 100 real de-identified patients, open, ODbL; only for checking realism locally, never committed | Open (`datasets/mimic-iv-demo`) |

## Environment

- Node.js with Next.js 15.5, React 19 and Tailwind 3 (`package.json`). `npm install && npm run dev` serves the app on local port 8766; open a chart by adding `?case=<id>` to the URL.
- Playwright (already a dev dependency) to drive the browser and take screenshots.
- Python 3.11 for the agent loop: provider SDKs for Anthropic, OpenAI and Google, plus open-weight GUI agents served with vLLM on RunPod.

## Step-by-step replication

1. Clone SimEHR; `npm install`; `npm run dev`; check `npm run smoke` and `npm run contract` pass.
2. Open each `trajectories/<model>/trajectory_view.html` and read the recorded actions and reasoning.
3. Write a minimal harness:
   - load the case with `window.SimEHR.loadCase`;
   - send the text of `demo_task/task_instruction.md`;
   - loop: screenshot → model → one action (click, type, key or scroll) → Playwright, with a 200-action budget;
   - at the end, read `getState()` and `getAuditLog()`.
4. Grade with `rubrics.json`. Audit-log checks are deterministic. Judged checkpoints go to an LLM judge with the rubric text, plus a JSON bundle of the note, reply, orders, medication and problem lists, and sign-off status.
5. Run Claude Opus 5.5 and GPT-6 Astra 5 times each (the recorded sessions are single runs). Report pass rate per checkpoint, actions, wall time and tokens.

## Compute and cost

- The app runs on a laptop.
- Frontier models: roughly 60 screenshot turns per episode. The cost per episode depends on the provider's image-token pricing; take it from the token counts in `run.json` (verify). Ten episodes should cost tens of US dollars.
- LLM judge: one call per judged checkpoint per episode.

## Target numbers

- **Demo task, single runs (trajectories/README.md):** GPT-6 Astra PASS 6 of 6, 58 actions, 8 min; Claude Opus 5.5 FAIL 5 of 6, 69 actions, 10 min (failed `cp4_patient_communication`).
- No aggregate benchmark numbers exist yet.

## Known pitfalls

- **One task, one run per model:** no variance is known; expect run-to-run differences.
- **Our harness is not theirs:** screenshot scaling, action schema and system prompt all change results. Document every choice.
- **Judge dependence:** the official judge is gpt-5.5, with one vote per checkpoint. Use the same judge and add a human check.
- **Moving target:** the preview build changes. The README notes tab renames between the recording and the current build. Pin a commit hash.

## Claude Code task list

1. Clone SimEHR at a pinned commit outside this repo; run the dev server, smoke and contract scripts.
2. Write `harness/` (Python plus Playwright) with provider adapters and the 200-action budget.
3. Re-run the demo task five times per model; grade with `rubrics.json` and the same judge.
4. Compare with the recorded sessions; log any differences in actions or verdicts.
5. Commit only harness code, configs and aggregate result tables to this study's folder; no screenshots containing chart content beyond the CC BY demo chart.
