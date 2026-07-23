# Unknown Product

## Product Description
Backend processing pipeline for health inspection violation monitoring using AI (DeepSeek) extraction and threshold evaluation.

## Archetype
This is a **backend data processing service** that ingests health inspection report text, extracts structured violation data via large language model (deepseek-v4-flash), evaluates risk thresholds, and persists records.

## System Components
- `extract_violations.py` – Calls DeepSeek API to parse report text into JSON (facility, jurisdiction, violations).
- `threshold_evaluator.py` – Determines if violations exceed critical or high threshold.
- `records_manager.py` – Loads/saves `records.json` for persistent storage of processing results.
- `run_demo.py` – Demonstration script that processes two mock reports.
- `run_tests.py` – Unit tests using pytest.

## Poller Input Expectations
The system (poller) expects as input:
- **Document text** (string) – raw health inspection report content.
- Optionally, `mock=True` flag for testing without API calls.

It outputs JSON with facility name, jurisdiction, inspection date, and violations array. The poller then evaluates threshold and updates the records file.

## Setup
```bash
pip install -r requirements.txt
python run_demo.py
```

Dashboard: https://unknown-product.vokrix.co
Vercel: unknown-product
Railway: 3337a58d-5c87-4553-9833-ec56eabcc2dc

Billing: price_1TwLOQ2c9uGCcgMSfSPoPL0C

Landing: https://vokrix.co/unknown-product

Outreach: active

Outreach: active
