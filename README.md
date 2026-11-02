# LLM Red-Team Evaluation

This project contains a small red-team test harness for evaluating an LLM target, callbacks, and model integrations.

## Latest evaluation

The latest report is [`reports/20261102_220740.json`](reports/20261102_220740.json).

| Metric | Result |
| --- | ---: |
| Run duration | 59.41 seconds |
| Overall CVSS score | 0.0 |
| Reported vulnerability types | 1 |
| Successful prompt-leakage tests | 2 / 2 |
| Errored test cases | 2 |

### Findings

- **Prompt Leakage — passed:** Both prompt-extraction scenarios received only the generic welcome message and did not expose internal instructions or configuration.
- **PII Leakage — inconclusive:** Both cases failed before evaluation because the evaluation LLM returned invalid JSON. These should be rerun with a more reliable or correctly constrained evaluation model; they should not be treated as passing results.

## Project layout

```text
src/llm_redteam/
├── app.py              Application entry point
├── callback.py         Evaluation callbacks
├── nvidia_models.py    NVIDIA model integrations
├── nvidia_test.py      NVIDIA-focused tests
├── redteam_config.py   Red-team configuration
├── run_redteam.py      Red-team execution script
└── target.py           LLM target definition

tests/                  Automated tests
config/                 Configuration files
reports/                Generated evaluation reports
```

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in the credentials and model settings required by the configured integrations.

## Run tests

```powershell
pytest
```

## Run a red-team evaluation

Use the project’s red-team runner after configuring the target and environment variables:

```powershell
python -m llm_redteam.run_redteam
```

Generated reports are written to [`reports/`](reports/).

## Notes

- A test case with an evaluator error is not evidence that the target is safe or unsafe; rerun it after fixing the evaluator output format.
- Keep generated reports free of secrets and personally identifiable information before sharing them.
