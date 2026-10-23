# fifo-rm-edf-semaphore-monitor-comparison
Educational Python simulation comparing FIFO, Rate Monotonic (RM), and Earliest Deadline First (EDF) scheduling with semaphore and monitor synchronization.
# FIFO, RM, and EDF Scheduling with Semaphore and Monitor

## Overview

This project presents a Python-based simulation and comparative study of three CPU scheduling algorithms: First-In, First-Out (FIFO), Rate Monotonic (RM), and Earliest Deadline First (EDF). It also discusses synchronization mechanisms, focusing on semaphores and monitors, for managing access to shared resources in real-time systems.

The project accompanies a research paper that explains the scheduling algorithms, task sets, simulation methodology, evaluation metrics, and limitations.

## Objectives

- Compare FIFO, Rate Monotonic (RM), and Earliest Deadline First (EDF) scheduling.
- Explore synchronization concepts using semaphores and monitors.
- Simulate periodic real-time tasks with execution times, periods, and deadlines.
- Generate CSV files containing scheduling summaries and job-level information.
- Provide a reproducible educational example for real-time operating systems.

## Scheduling Algorithms

### 1. First-In, First-Out (FIFO)

FIFO schedules tasks in arrival order. In this simulation, it uses non-preemptive execution.

### 2. Rate Monotonic (RM)

RM is a fixed-priority scheduling algorithm. Tasks with shorter periods receive higher priorities. The simulation models preemption at discrete time intervals.

### 3. Earliest Deadline First (EDF)

EDF is a dynamic-priority scheduling algorithm. The task with the earliest absolute deadline receives the highest priority. The simulation models preemption at discrete time intervals.

## Synchronization Mechanisms

### Semaphore

A semaphore is a synchronization mechanism used to control access to shared resources and coordinate concurrent activities.

### Monitor

A monitor encapsulates shared data and the operations that access it. In concurrent systems, monitor implementations commonly use mutual exclusion and condition variables.

**Implementation note:** The current simulation uses a simplified shared-resource model. Semaphore and monitor labels do not yet represent fully distinct synchronization implementations. Therefore, the results should be interpreted as educational scheduling results rather than a definitive experimental comparison of semaphore and monitor behavior.

## Task Sets

The simulation uses two example task sets.

### Task Set A

| Task | Execution Time (C) | Period (T) | Deadline (D) |
|---|---:|---:|---:|
| A | 1 | 4 | 4 |
| B | 2 | 5 | 5 |
| C | 3 | 10 | 10 |

- Hyperperiod: 20 time units
- Total utilization: 0.95

### Task Set B

| Task | Execution Time (C) | Period (T) | Deadline (D) |
|---|---:|---:|---:|
| X | 2 | 5 | 5 |
| Y | 4 | 7 | 7 |

- Hyperperiod: 35 time units
- Total utilization: approximately 0.9714

## Requirements

- Python 3.10 or later
- No third-party packages are required for the basic simulation, unless additional plotting functionality is added.

## How to Run

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/fifo-rm-edf-semaphore-monitor-comparison.git
cd fifo-rm-edf-semaphore-monitor-comparison
```

Run the simulation:

```bash
python fifo_rm_edf_sem_monitor_comparison.py
```

Replace `YOUR_USERNAME` with your GitHub username.

## Output Files

After execution, the program is expected to generate the following CSV files:

- `sem_mon_summary.csv` — summary of scheduling metrics.
- `sem_mon_job_details.csv` — job-level execution and scheduling information.
- `sem_mon_gantt.csv` — compressed execution intervals that can be used to build Gantt charts.

The exact contents depend on the simulation implementation and its configuration.

## Evaluation Metrics

The study discusses scheduling metrics such as:

- CPU utilization
- Job completion times
- Deadline misses
- Response and turnaround times, where supported by the simulation output
- Scheduling behavior under different task priorities

Metrics should only be interpreted when they are explicitly calculated by the code. Theoretical expectations and simulated measurements are not interchangeable.

## Project Structure

```text
fifo-rm-edf-semaphore-monitor-comparison/
├── README.md
├── fifo_rm_edf_sem_monitor_comparison.py
├── FIFO_RM_EDF_SEM_MON_Comparison_final.pdf
├── FIFO_RM_EDF_SEM_MON_Comparison_final.docx
└── .gitignore
```

## Limitations

- The simulation uses discrete time steps.
- FIFO is modeled as non-preemptive, while RM and EDF are modeled as preemptive.
- The shared-resource and critical-section model is simplified.
- Priority inheritance and other advanced real-time synchronization protocols are not fully modeled.
- The current semaphore and monitor variants do not yet implement all of their distinct synchronization semantics.
- Illustrative Gantt charts should not be treated as measured execution traces unless generated directly from the simulation output.

## Future Improvements

- Implement genuinely distinct semaphore and monitor synchronization mechanisms.
- Add blocking, waiting queues, and resource-contention behavior.
- Model priority inversion and priority inheritance.
- Generate Gantt charts directly from simulation results.
- Add automated tests and broader task-set experiments.
- Compare deadline-miss rates and response-time distributions across multiple workloads.

## Research Paper

The repository includes the accompanying paper in PDF and DOCX formats. Please consult the paper for the detailed methodology, figures, discussion, and references.

## License

No license has been specified yet. Add an appropriate open-source license before allowing others to reuse or redistribute this project.

## Author

**Erfan Barati**

This project is intended for educational and research purposes in real-time systems, CPU scheduling, and synchronization mechanisms.
