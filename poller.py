import os
import time
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise Exception("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def process_task(task):
    # Implement task processing logic here
    print(f"Processing task {task['id']}: {task}")
    supabase.table("tasks").update({"status": "completed"}).eq("id", task["id"]).execute()

def poll_tasks():
    while True:
        try:
            response = supabase.table("tasks").select("*").eq("status", "pending").execute()
            tasks = response.data
            for task in tasks:
                process_task(task)
        except Exception as e:
            print(f"Error polling: {e}")
        time.sleep(10)

if __name__ == "__main__":
    poll_tasks()
