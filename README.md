# backup-job-duration-analyzer

Analyse backup job durations from a CSV: duration = finished minus started in whole minutes, LONG when it is over --max-minutes (default 120) and at risk of overrunning its backup window, otherwise OK — longest job first, with the average duration across all jobs.

Sample input is included (sample.csv with three backup jobs).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
JOB-2 [Mail server]: LONG (195 min, 2026-11-10T22:00:00 -> 2026-11-11T01:15:00)
JOB-1 [File server]: OK (90 min, 2026-11-10T22:00:00 -> 2026-11-10T23:30:00)
JOB-3 [DB server]: OK (45 min, 2026-11-10T23:00:00 -> 2026-11-10T23:45:00)
Average duration: 110.0 min across 3 job(s); 1 job(s) over the 120 min limit.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
