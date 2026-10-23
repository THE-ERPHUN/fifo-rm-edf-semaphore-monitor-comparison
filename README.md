# fifo-rm-edf-semaphore-monitor-comparison
Educational Python simulation comparing FIFO, Rate Monotonic (RM), and Earliest Deadline First (EDF) scheduling with semaphore and monitor synchronization.
Comparative Study of FIFO, Rate Monotonic (RM), and Earliest Deadline First (EDF) Scheduling with Semaphore and Monitor Synchronization
This repository contains an educational Python simulation and the accompanying paper comparing three CPU scheduling policies—FIFO, Rate Monotonic (RM), and Earliest Deadline First (EDF)—in task sets that access a shared resource. The project also explores semaphore- and monitor-labelled synchronization configurations and exports per-job and summary data to CSV files.
Model scope: This is a simplified, discrete-time teaching model, not a production real-time operating-system scheduler. In the current implementation, SEM and MON use closely related queue/handoff mechanics and therefore do not represent a complete behavioral comparison of real semaphore and monitor implementations. Priority inheritance is not modeled. The paper's schematic Gantt figure is illustrative rather than a plot generated from the simulation output.

Repository contents
- fifo_rm_edf_sem_monitor_comparison.py — Python simulation source code.
- FIFO_RM_EDF_SEM_MON_Comparison_final.pdf — paper in PDF format.
- FIFO_RM_EDF_SEM_MON_Comparison_final.docx — editable paper.
- sem_mon_summary.csv — generated aggregate metrics (created when the script runs).
- sem_mon_job_details.csv — generated per-job timing details (created when the script runs).
- sem_mon_gantt.csv — generated compressed execution intervals (created when the script runs).
Scheduling policies
- FIFO: non-preemptive scheduling in release order.
- RM: preemptive fixed-priority scheduling; tasks with shorter periods receive higher priority.
- EDF: preemptive dynamic-priority scheduling; jobs with earlier absolute deadlines receive higher priority.
Task sets
Task set A
Task	Execution time (C)	Period (T)	Relative deadline (D)
A	1	4	4
B	2	5	5
C	3	10	10


Hyperperiod: 20 time units. Total utilization: 0.95.
Task set B
Task	Execution time (C)	Period (T)	Relative deadline (D)
X	2	5	5
Y	4	7	7


Hyperperiod: 35 time units. Total utilization: approximately 0.9714.

The critical section is placed at the end of each job and has length min(2, C). Scheduling decisions occur at integer time boundaries. The simulation uses one shared resource and does not model priority inheritance.
Requirements
- Python 3.10 or newer (the script uses modern type-union syntax).
- No third-party packages are required; the simulation uses the Python standard library.
Run
From this directory, execute:
python fifo_rm_edf_sem_monitor_comparison.py
The program prints a compact summary and writes three CSV files into the current working directory:
1. sem_mon_summary.csv
2. sem_mon_job_details.csv
3. sem_mon_gantt.csv
Run the script from a writable directory so the CSV files can be created.
Metrics exported
The summary includes average waiting time, turnaround time, response time, resource waiting time, block time, deadline misses, and idle time. The job-level file includes release time, deadline, first start, completion time, and derived timing metrics. Interpret the metrics in light of the simplified model and its assumptions.
Limitations and future work
This code is intended for learning and reproducibility. Before using it to support strong research conclusions, the model should be validated and extended to implement semaphores and monitors with clearly distinct semantics, accurately handle blocking and ready queues, define whether jobs can be suspended while holding the resource, and test against hand-calculated schedules. Further extensions could include priority inheritance/ceiling protocols, context-switch overhead, release jitter, and larger task sets.
Suggested citation
Barati, Erfan. A Comparative Study of FIFO, Rate Monotonic (RM), and Earliest Deadline First (EDF) Scheduling with Semaphore and Monitor Synchronization. Accompanying paper and educational simulation, 2026.
License
No license is specified yet. Add a license file before inviting reuse or redistribution under explicit terms.
