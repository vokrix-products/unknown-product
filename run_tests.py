import pytest
import os
from threshold_evaluator import evaluate_status
from records_manager import (
    RECORDS_FILE,
    load_records,
    save_records,
    update_or_create_record
)

# ----- Threshold evaluator tests -----
def test_evaluate_status_critical_direct():
    violations = [{"severity": "critical"}]
    assert evaluate_status(violations) == "above_threshold:critical"

def test_evaluate_status_high_threshold_met():
    violations = [{"severity": "high"}] * 3
    assert evaluate_status(violations) == "above_threshold:critical"

def test_evaluate_status_within_threshold():
    violations = [{"severity": "high"}] * 2 + [{"severity": "medium"}]
    assert evaluate_status(violations) == "within_threshold:good"

# ----- Records manager tests -----
def test_update_and_load(tmp_path, monkeypatch):
    # Use a temporary file for records
    monkeypatch.setattr("records_manager.RECORDS_FILE", str(tmp_path / "test_records.json"))
    # Ensure clean state
    save_records([])

    # Create a new record
    update_or_create_record("Test Facility", "Test Jurisdiction", "doc.txt",
                            {"violations": [], "inspection_date": "2024-01-01"},
                            "within_threshold:good")
    records = load_records()
    assert len(records) == 1
    rec = records[0]
    assert rec["facility_name"] == "Test Facility"
    assert rec["status"] == "within_threshold:good"

    # Update the same facility with critical status
    update_or_create_record("Test Facility", "Test Jurisdiction", "doc2.txt",
                            {"violations": [{"severity": "critical"}], "inspection_date": "2024-01-02"},
                            "above_threshold:critical")
    records = load_records()
    assert len(records) == 1
    assert records[0]["status"] == "above_threshold:critical"
    assert records[0]["extracted_violations"] == [{"severity": "critical"}]
    assert records[0]["document_path"] == "doc2.txt"

    # Create a second facility
    update_or_create_record("New Place", "Anywhere", "doc3.txt",
                            {"violations": [], "inspection_date": "2024-02-01"},
                            "within_threshold:good")
    records = load_records()
    assert len(records) == 2
    assert records[1]["facility_name"] == "New Place"
