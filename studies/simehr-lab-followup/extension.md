---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** SimEHR preview (GitHub, 2026-11-02): a GUI EHR, one task, two recorded sessions. The authors' PhysicianBench-UI (physician-authored long workflows) is announced but not released.
- **MedAgentBench** (same group; Jiang et al., NEJM AI 2025, [doi:10.1056/AIdbp2500144](https://doi.org/10.1056/AIdbp2500144)): EHR agent tasks through a FHIR API, not the screen.
- **HealthAdminBench** (Bedi et al., arXiv [2604.09937](https://arxiv.org/abs/2604.09937)): computer-use agents on healthcare administration tasks, not clinical results review.
- **Human-system context:** failure to follow up abnormal lab results is a known safety problem that labs try to fix with surveillance systems (J Appl Lab Med 2025, [doi:10.1093/jalm/jfaf073](https://doi.org/10.1093/jalm/jfaf073)).

**Searches run on 2026-11-06:**
- Crossref and Europe PMC (from 2024-06): "MedAgentBench virtual EHR environment benchmark medical LLM agents"; "computer-use agent electronic health record graphical interface benchmark"; "LLM agent abnormal laboratory result follow-up electronic health record"; "test result follow-up missed abnormal results inbox AI".
- arXiv: `all:EHR AND all:"computer-use"` (2 results, one relevant: HealthAdminBench).
- OpenAlex not used (daily budget used up earlier today).

No benchmark found that tests whether agents notice and act on abnormal lab results inside an EHR interface, or that compares the same clinical task through screenshots and through structured data.

### Gap 1: No lab-medicine or results-review tasks

- **Evidence:** the preview has one prescribing/communication task (demo_task/README.md). Results Review with trend graphs is implemented in the app (README, "What is implemented") but no task exercises it.
- **Novelty check:** searches above found no GUI-agent task set on results review.
- **Open data:** `simehr` (schema and app), `synthea` and hand-authored charts, `nhanes` (realistic value ranges).
- **Design sketch:**
  - *Hypothesis:* agents miss abnormal results that are not in the task message, above all slow trends and pre-analytical artefacts, even when they pass the stated task.
  - *Tasks:* 30–40 tasks written by Atul in five families:
    - critical values (K⁺ 6.8, Na⁺ 118, platelets 12);
    - slow trends (Hb falling 13.5 → 10.1 over a year with low MCV and no ferritin; creeping creatinine);
    - pre-analytical artefacts (high K⁺ with low Ca²⁺ and ALP suggesting EDTA contamination; haemolysed sample; drip-arm glucose);
    - pending or overdue follow-up (ferritin never ordered, unrepeated abnormal TSH);
    - distractors (normal variants such as Duffy-null associated neutrophil count).
    Each task starts from an unrelated patient message, so the abnormal result must be found unprompted.
  - *Grading:* audit-log checks (did it open Results Review, did it order or acknowledge) plus judged rubric items, with Atul double-scoring 20% to validate the judge.
  - *Metrics:* detection rate per family, harmful-action rate, actions and tokens per task, pass@1 and pass^3 over runs.
  - *Reporting guideline:* TRIPOD-LLM.
- **Rating:** feasibility 3, novelty 4, API, 6 weeks.

### Gap 2: The interface cost is unmeasured

- **Evidence:** SimEHR exists because API benchmarks (MedAgentBench) may overstate real-world ability. But nobody has run the same task and chart both ways.
- **Novelty check:** no paired GUI vs structured-data comparison found.
- **Design sketch:** each task in two arms with the same model, the same chart and the same rubric. Arm A is screenshots in SimEHR. Arm B gives the chart JSON (same content) plus tool calls for order, note and reply. The outcome is the difference in detection and pass rate, and where in the GUI the misses happen (never opened Results Review, opened it but missed the trend, misread the graph).
- **Rating:** feasibility 4, novelty 4, API, +2 weeks on top of Gap 1.

### Gap 3: Single runs, closed models only

- **Evidence:** one run per model (trajectories/README.md); both models are proprietary and accessed by API.
- **Design sketch:** three runs per task. Add an open-weight GUI agent (e.g. a Qwen-VL or UI-TARS class model on RunPod) for cost and deployability in India.
- **Rating:** feasibility 4, novelty 2, RunPod + API, +1 week.

### Gap 4: The LLM judge is not validated against a clinician

- **Evidence:** judged checkpoints use gpt-5.5 with one vote (trajectories/README.md); no human agreement is reported.
- **Design sketch:** Atul scores all judged checkpoints for a 20% sample, blinded; report κ with the judge and the judge's errors by family.
- **Rating:** feasibility 5, novelty 2, laptop, part of Gap 1.

## Recommended extension

**Gaps 1 + 2, with Gap 4 built in:** a pathologist-authored results-review task set in SimEHR, run both through screenshots and through structured data, with Atul validating the judge.

Why:
- It turns Atul's lab-medicine expertise directly into benchmark content that nobody else can write as well (pre-analytical artefacts, trend recognition, critical values).
- Everything is open and synthetic, so the whole task set can be published under CC BY 4.0.
- The paired design answers a question that matters beyond this benchmark: how much does working through a real interface hurt agent safety?

Main risk: PhysicianBench-UI may appear first. Lab-specific task families and the paired-interface design keep the work distinct. Contact the SimEHR team early, and consider contributing the tasks upstream. TRIPOD-LLM framing fits JAMIA or J Biomed Inform. About 8 weeks.
