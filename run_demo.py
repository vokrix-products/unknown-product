from extract_violations import extract_violations_from_document
from threshold_evaluator import evaluate_status
from records_manager import update_or_create_record, load_records

def main():
    # Simulated inspection reports (raw text, only used to choose mock behaviour)
    doc1_text = "HEALTH INSPECTION REPORT: Sunrise Diner, New York City. Various violations observed."
    doc2_text = "HEALTH INSPECTION REPORT: Green Cafe, Los Angeles. Critical findings noted."

    # ----- Process first document (mock extraction) -----
    print("Processing document 1 ...")
    extracted1 = extract_violations_from_document(doc1_text, mock=True)
    status1 = evaluate_status(extracted1.get("violations", []))
    update_or_create_record(
        facility_name=extracted1["facility_name"],
        jurisdiction=extracted1["jurisdiction"],
        document_path="data/doc1.txt",
        extracted_data=extracted1,
        status=status1
    )
    print(f"Record for {extracted1['facility_name']}: status = {status1}")

    # ----- Process second document (manually defined data, still uses evaluator) -----
    print("\nProcessing document 2 ...")
    extracted2 = {
        "facility_name": "Green Cafe",
        "jurisdiction": "Los Angeles",
        "inspection_date": "2024-03-16",
        "violations": [
            {"description": "Mold in ice machine", "severity": "critical"},
            {"description": "Expired food", "severity": "high"},
            {"description": "Dirty floors", "severity": "medium"}
        ]
    }
    status2 = evaluate_status(extracted2["violations"])
    update_or_create_record(
        facility_name=extracted2["facility_name"],
        jurisdiction=extracted2["jurisdiction"],
        document_path="data/doc2.txt",
        extracted_data=extracted2,
        status=status2
    )
    print(f"Record for {extracted2['facility_name']}: status = {status2}")

    # ----- Display final records -----
    print("\nCurrent records.json content:")
    records = load_records()
    for r in records:
        print(f"ID {r['id']:>2}: {r['facility_name']:<20} | {r['status']}")

if __name__ == "__main__":
    main()
