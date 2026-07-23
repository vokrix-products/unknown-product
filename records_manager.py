import json
import os

RECORDS_FILE = "records.json"

def load_records() -> list:
    if not os.path.exists(RECORDS_FILE):
        return []
    with open(RECORDS_FILE, 'r') as f:
        return json.load(f)

def save_records(records: list) -> None:
    with open(RECORDS_FILE, 'w') as f:
        json.dump(records, f, indent=2)

def update_or_create_record(
    facility_name: str,
    jurisdiction: str,
    document_path: str,
    extracted_data: dict,
    status: str
) -> None:
    records = load_records()
    # Update existing record for the same facility
    for rec in records:
        if rec.get("facility_name") == facility_name:
            rec["status"] = status
            rec["extracted_violations"] = extracted_data.get("violations", [])
            rec["processed_at"] = extracted_data.get("inspection_date")
            rec["document_path"] = document_path
            break
    else:
        # Create a new record
        new_record = {
            "id": len(records) + 1,
            "facility_name": facility_name,
            "jurisdiction": jurisdiction,
            "document_path": document_path,
            "extracted_violations": extracted_data.get("violations", []),
            "status": status,
            "processed_at": extracted_data.get("inspection_date")
        }
        records.append(new_record)
    save_records(records)
