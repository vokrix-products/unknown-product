import os
import time
import json
import uuid
from datetime import datetime, timezone, timedelta
import requests

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')
PRODUCT_ID = os.environ.get('PRODUCT_ID', '')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

HEADERS = {
    'apikey': SUPABASE_SERVICE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

def poll_jobs():
    url = f'{SUPABASE_URL}/rest/v1/jobs'
    params = {
        'status': 'eq.pending',
        'job_type': 'eq.process_upload',
        'product_id': f'eq.{PRODUCT_ID}',
        'select': '*',
        'limit': 1
    }
    resp = requests.get(url, headers=HEADERS, params=params)
    if resp.status_code != 200:
        print(f'Poll error: {resp.status_code} {resp.text[:200]}')
        return None
    data = resp.json()
    if not data:
        return None
    return data[0]

def download_file(file_path):
    url = f'{SUPABASE_URL}/storage/v1/object/uploads/{file_path}'
    headers = {
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}'
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f'Download failed: {resp.status_code}')
    return resp.text

def upload_result(file_data, job_id):
    file_name = f'{job_id}_{uuid.uuid4().hex}.json'
    url = f'{SUPABASE_URL}/storage/v1/object/results/{file_name}'
    headers = {
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/json'
    }
    resp = requests.post(url, headers=headers, data=file_data)
    if resp.status_code not in (200, 201):
        raise Exception(f'Upload failed: {resp.status_code}')
    return file_name

def create_records(records, job):
    url = f'{SUPABASE_URL}/rest/v1/records'
    now = datetime.now(timezone.utc).isoformat()
    rows = []
    for v in records:
        rows.append({
            'product_id': PRODUCT_ID,
            'customer_id': job.get('customer_id', ''),
            'title': v.get('description', 'Violation'),
            'status': v.get('severity', 'medium'),
            'details': json.dumps(v),
            'source_file_path': job.get('file_path', ''),
            'due_date': (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
            'created_at': now,
            'updated_at': now
        })
    resp = requests.post(url, headers=HEADERS, json=rows)
    if resp.status_code != 201:
        print(f'Create records warning: {resp.status_code} {resp.text[:200]}')

def update_job(job_id, status, output_path=None, summary=None):
    url = f'{SUPABASE_URL}/rest/v1/jobs'
    params = {'id': f'eq.{job_id}'}
    payload = {
        'status': status,
        'completed_at': datetime.now(timezone.utc).isoformat()
    }
    if output_path:
        payload['output_file_path'] = output_path
    if summary:
        payload['result_summary'] = summary
    resp = requests.patch(url, headers=HEADERS, params=params, json=payload)
    if resp.status_code != 204:
        print(f'Update job warning: {resp.status_code} {resp.text[:200]}')

def process_job(job):
    job_id = job['id']
    file_path = job.get('file_path', '')
    print(f'Processing job {job_id}: {file_path}')
    try:
        document_text = download_file(file_path)
    except Exception as e:
        update_job(job_id, 'failed', summary=str(e))
        return
    try:
        from backend.extract_violations import extract_violations_from_document
        result = extract_violations_from_document(document_text, mock=True)
    except Exception as e:
        update_job(job_id, 'failed', summary=str(e))
        return
    violations = result.get('violations', [])
    if violations:
        create_records(violations, job)
    result_json = json.dumps(result)
    try:
        output_path = upload_result(result_json, job_id)
    except Exception as e:
        update_job(job_id, 'failed', summary=str(e))
        return
    summary = f'Extracted {len(violations)} violations from {result.get("facility_name", "unknown")}'
    update_job(job_id, 'completed', output_path=output_path, summary=summary)
    print(f'Job {job_id} completed: {summary}')

def main():
    print('Poller started')
    while True:
        try:
            job = poll_jobs()
            if job:
                process_job(job)
            else:
                print('No pending jobs')
        except Exception as e:
            print(f'Poll loop error: {e}')
        time.sleep(60)

if __name__ == '__main__':
    main()
