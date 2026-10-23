#!/usr/bin/env python3

from dataclasses import dataclass
from math import lcm
import csv

@dataclass(frozen=True)
class Task:
    name: str
    C: int
    T: int
    D: int

@dataclass
class Job:
    task: Task
    jid: int
    release: int
    deadline: int
    remaining: int
    first_start: int | None = None
    completion: int | None = None
    executed: int = 0
    requested: bool = False
    in_cs: bool = False
    cs_remaining: int = 0
    wait_start: int | None = None
    resource_wait: int = 0
    block_ticks: int = 0
    @property
    def label(self):
        return f"{self.task.name}{self.jid}"

def simulate(tasks, policy, sync, horizon=None):
    """Run one policy/synchronization pair; returns summary, job rows, Gantt rows."""
    if policy not in ("FIFO", "RM", "EDF"):
        raise ValueError("policy must be FIFO, RM, or EDF")
    if sync not in ("SEM", "MON"):
        raise ValueError("sync must be SEM or MON")
    H = lcm(*(t.T for t in tasks))
    horizon = H if horizon is None else horizon
    jobs, ready, waiters, gantt = [], [], [], []
    running = None
    owner = None
    ids = {t.name: 0 for t in tasks}

    for now in range(horizon):
        for t in tasks:
            if now % t.T == 0:
                ids[t.name] += 1
                j = Job(t, ids[t.name], now, now + t.D, t.C)
                jobs.append(j)
                ready.append(j)

        if policy == "FIFO":
            if running is None and ready:
                running = min(ready, key=lambda j: (j.release, j.task.name, j.jid))
                ready.remove(running)
        else:
            key = (lambda j: (j.task.T, j.release, j.task.name, j.jid)) if policy == "RM" else \
                  (lambda j: (j.deadline, j.release, j.task.name, j.jid))
            candidates = list(ready)
            if running is not None:
                candidates.append(running)
            if candidates:
                chosen = min(candidates, key=key)
                if chosen is not running:
                    if running is not None:
                        ready.append(running)
                    if chosen in ready:
                        ready.remove(chosen)
                    running = chosen

        if running is not None:
            cs_len = min(2, running.task.C)
            non_cs = running.task.C - cs_len
            if not running.requested and running.executed >= non_cs:
                running.requested = True
                if owner is None:
                    owner = running
                    running.in_cs = True
                    running.cs_remaining = cs_len
                else:
                    running.wait_start = now
                    waiters.append(running)
                    running = None

        if running is None:
            gantt.append((now, now + 1, "IDLE"))
            for w in waiters:
                if w.wait_start is not None:
                    w.block_ticks += 1
            continue

        if running.first_start is None:
            running.first_start = now
        running.remaining -= 1
        running.executed += 1
        gantt.append((now, now + 1, running.label))

        if running.in_cs:
            running.cs_remaining -= 1
            if running.cs_remaining == 0:
                running.in_cs = False
                if waiters:
                    nxt = waiters.pop(0)
                    if nxt.wait_start is not None:
                        elapsed = now + 1 - nxt.wait_start
                        nxt.resource_wait += elapsed
                        nxt.wait_start = None
                    nxt.in_cs = True
                    nxt.cs_remaining = min(2, nxt.task.C)
                    owner = nxt
                    ready.append(nxt)
                else:
                    owner = None

        if running.remaining == 0:
            running.completion = now + 1
            running = None

    completed = [j for j in jobs if j.completion is not None]
    def avg(values):
        return round(sum(values) / len(values), 3) if values else 0.0
    details = []
    for j in jobs:
        turnaround = j.completion - j.release if j.completion is not None else None
        details.append({
            "sync": sync, "policy": policy, "job": j.label, "task": j.task.name,
            "release": j.release, "deadline": j.deadline, "execution_time": j.task.C,
            "first_start": j.first_start, "completion": j.completion,
            "waiting_time": turnaround - j.task.C if turnaround is not None else None,
            "turnaround_time": turnaround,
            "response_time": j.first_start - j.release if j.first_start is not None else None,
            "resource_waiting_time": j.resource_wait, "block_time": j.block_ticks,
            "deadline_missed": bool(j.completion is not None and j.completion > j.deadline)
        })
    summary = {
        "sync": sync, "policy": policy, "hyperperiod": H,
        "jobs_released": len(jobs), "jobs_completed": len(completed),
        "avg_waiting_time": avg([j.completion - j.release - j.task.C for j in completed]),
        "avg_turnaround_time": avg([j.completion - j.release for j in completed]),
        "avg_response_time": avg([j.first_start - j.release for j in completed if j.first_start is not None]),
        "avg_resource_waiting_time": avg([j.resource_wait for j in completed]),
        "avg_block_time": avg([j.block_ticks for j in completed]),
        "deadline_misses": sum(1 for j in completed if j.completion > j.deadline),
        "idle_time": sum(1 for a, b, label in gantt if label == "IDLE")
    }
    compressed = []
    for a, b, label in gantt:
        if compressed and compressed[-1][2] == label and compressed[-1][1] == a:
            compressed[-1] = (compressed[-1][0], b, label)
        else:
            compressed.append((a, b, label))
    return summary, details, compressed

CASES = {
    "A": [Task("A", 1, 4, 4), Task("B", 2, 5, 5), Task("C", 3, 10, 10)],
    "B": [Task("X", 2, 5, 5), Task("Y", 4, 7, 7)]
}

def main():
    summaries, details, gantts = [], [], []
    for case, tasks in CASES.items():
        for sync in ("SEM", "MON"):
            for policy in ("FIFO", "RM", "EDF"):
                summary, rows, intervals = simulate(tasks, policy, sync)
                summary["case"] = case
                summaries.append(summary)
                for row in rows:
                    row["case"] = case
                    details.append(row)
                for start, end, label in intervals:
                    gantts.append({"case": case, "sync": sync, "policy": policy,
                                   "start": start, "end": end, "slot": label})
    for filename, rows in (
        ("sem_mon_summary.csv", summaries),
        ("sem_mon_job_details.csv", details),
        ("sem_mon_gantt.csv", gantts),
    ):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    print("case,sync,policy,avg_wait,avg_turnaround,avg_resource_wait,avg_block,deadline_misses")
    for s in summaries:
        print(f'{s["case"]},{s["sync"]},{s["policy"]},{s["avg_waiting_time"]},'
              f'{s["avg_turnaround_time"]},{s["avg_resource_waiting_time"]},'
              f'{s["avg_block_time"]},{s["deadline_misses"]}')
    print("\\nCSV outputs: sem_mon_summary.csv, sem_mon_job_details.csv, sem_mon_gantt.csv")

if __name__ == "__main__":
    main()
