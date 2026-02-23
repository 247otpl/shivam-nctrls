import threading


class JobManager:
    def __init__(self):
        self.jobs = {}
        self.lock = threading.Lock()

    def create_job(self, run_id, total_devices):
        with self.lock:
            self.jobs[run_id] = {
                "total": total_devices,
                "completed": 0,
                "cancel": False,
                "status": "RUNNING",
            }

    def mark_completed(self, run_id):
        with self.lock:
            if run_id in self.jobs:
                self.jobs[run_id]["completed"] += 1

    def cancel_job(self, run_id):
        with self.lock:
            if run_id in self.jobs:
                self.jobs[run_id]["cancel"] = True
                self.jobs[run_id]["status"] = "CANCELLED"

    def is_cancelled(self, run_id):
        return self.jobs.get(run_id, {}).get("cancel", False)

    def finalize_job(self, run_id):
        with self.lock:
            if run_id in self.jobs:
                if not self.jobs[run_id]["cancel"]:
                    self.jobs[run_id]["status"] = "COMPLETED"

    def get_status(self, run_id):
        job = self.jobs.get(run_id)
        if not job:
            return None

        total = job["total"]
        completed = job["completed"]

        percent = 0
        if total > 0:
            percent = round((completed / total) * 100, 2)

        return {
            "run_id": run_id,
            "status": job["status"],
            "progress_percent": percent,
            "completed_devices": completed,
            "total_devices": total,
        }


job_manager = JobManager()
