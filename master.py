from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# ====================================
# STORAGE
# ====================================

workers = []
tasks = []
results = []

# ====================================
# HOME
# ====================================

@app.get("/")
def home():

    return {
        "status": "master online",
        "workers": workers,
        "tasks": tasks,
        "results": results
    }

# ====================================
# REGISTER WORKER
# ====================================

@app.post("/register")
def register(worker: dict):

    workers.append(worker)

    return {
        "message": "worker registered",
        "workers": len(workers)
    }

# ====================================
# CREATE JOB
# ====================================

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

        # Last worker gets the remainder
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

# ====================================
# GET TASK
# ====================================

@app.get("/get_task")
def get_task():

    if len(tasks) == 0:

        return {
            "message": "no task available"
        }

    return tasks.pop(0)

# ====================================
# SUBMIT RESULT
# ====================================

@app.post("/submit_result")
def submit_result(result: dict):

    results.append(result)

    return {
        "message": "result received"
    }

# ====================================
# SUMMARY
# ====================================

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

# ====================================
# DASHBOARD
# ====================================

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    worker_html = ""

    for worker in workers:
        worker_html += f"<li>{worker['name']}</li>"

    task_html = ""

    for task in tasks:
        task_html += f"<li>{task['start']} → {task['end']}</li>"

    result_html = ""

    for result in results:
        result_html += (
            f"<li>{result['worker']} : "
            f"{result['count']} primes</li>"
        )

    return f"""
    <html>
    <head>
        <title>ReCom Dashboard</title>

        <meta http-equiv="refresh" content="3">

        <style>

            body {{
                font-family: Arial;
                margin: 40px;
            }}

            h1 {{
                color: #1f4e79;
            }}

            .card {{
                border: 1px solid #ccc;
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 10px;
            }}

        </style>

    </head>

    <body>

        <h1>🚀 ReCom Dashboard</h1>

        <div class="card">
            <h2>Status</h2>

            <p><b>Workers Online:</b> {len(workers)}</p>
            <p><b>Tasks Pending:</b> {len(tasks)}</p>
            <p><b>Results Received:</b> {len(results)}</p>
        </div>

        <div class="card">
            <h2>Workers</h2>
            <ul>
                {worker_html}
            </ul>
        </div>

        <div class="card">
            <h2>Tasks Queue</h2>
            <ul>
                {task_html}
            </ul>
        </div>

        <div class="card">
            <h2>Results</h2>
            <ul>
                {result_html}
            </ul>
        </div>

    </body>
    </html>
    """