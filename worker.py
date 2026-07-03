import requests
import math

MASTER_URL = "http://13.53.170.213:8000"

worker_name = input("Enter worker name:")


# ==========================
# PRIME CHECK
# ==========================

def is_prime(n):

    if n < 2:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):

        if n % i == 0:
            return False

    return True


# ==========================
# REGISTER
# ==========================

register_response = requests.post(
    f"{MASTER_URL}/register",
    json={
        "name": worker_name
    }
)

print(register_response.json())


# ==========================
# GET TASK
# ==========================

task_response = requests.get(
    f"{MASTER_URL}/get_task"
)

task = task_response.json()

if "start" not in task:

    print("No task available")
    exit()

start = task["start"]
end = task["end"]

print(f"\nReceived task: {start} -> {end}")


# ==========================
# COMPUTE
# ==========================

count = 0

for num in range(start, end + 1):

    if is_prime(num):
        count += 1

print(f"Prime Count = {count}")


# ==========================
# SUBMIT RESULT
# ==========================

result = {
    "worker": worker_name,
    "count": count
}

submit_response = requests.post(
    f"{MASTER_URL}/submit_result",
    json=result
)

print(submit_response.json())

print("\nTask Completed Successfully")