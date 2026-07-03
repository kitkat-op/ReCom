from fastapi import FastAPI

app = FastAPI()

# ==========================
# STORAGE
# ==========================

workers = []
tasks = []
results = []


# ==========================
# HOME
# ==========================

@app.get("/")
def home():

    return {
        "status": "master online",
        "workers": workers,
        "tasks": tasks,
        "results": results
    }


# ==========================
# REGISTER WORKER
# ==========================

@app.post("/register")
def register(worker: dict):

    workers.append(worker)

    return {
        "message": "worker registered",
        "workers": len(workers)
    }


# ==========================
# CREATE JOB
# ==========================

@app.post("/create_job")
def create_job(job: dict):

    start = job["start"]
    end = job["end"]

    num_workers = len(workers)

    if num_workers == 0:

        return {
            "error": "No workers available"
        }

    chunk_size = (end - start + 1) // num_workers

    current_start = start

    for i in range(num_workers):

        current_end = current_start + chunk_size - 1

        # Last worker gets remainder
        if i == num_workers - 1:
            current_end = end

        tasks.append({
            "start": current_start,
            "end": current_end
        })

        current_start = current_end + 1

    return {
        "message": "Job created",
        "workers": num_workers,
        "tasks_created": len(tasks)
    }


# ==========================
# GET TASK
# ==========================

@app.get("/get_task")
def get_task():

    if len(tasks) == 0:

        return {
            "message": "no task available"
        }

    return tasks.pop(0)


# ==========================
# SUBMIT RESULT
# ==========================

@app.post("/submit_result")
def submit_result(result: dict):

    results.append(result)

    return {
        "message": "result received"
    }


# ==========================
# AGGREGATED RESULTS
# ==========================

@app.get("/summary")
def summary():

    total = 0

    for result in results:

        total += result["count"]

    return {
        "workers": len(workers),
        "completed_tasks": len(results),
        "total_count": total
    }