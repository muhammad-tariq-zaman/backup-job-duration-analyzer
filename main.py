"""Analyse backup job durations and flag jobs over the time limit.

Usage: python3 main.py jobs.csv [--max-minutes 120]
CSV columns: job,system,started,finished.
started and finished are ISO datetimes (YYYY-MM-DDTHH:MM).
Duration = finished minus started, in whole minutes.
- LONG: duration over --max-minutes - the job risks overrunning
  its backup window.
- OK: duration at or under the limit.
Longest job first, then the average duration across all jobs.
"""
import argparse, csv, sys
from datetime import datetime

def analyse(rows, max_minutes=120):
    out = []
    for row in rows:
        started = datetime.fromisoformat(row["started"].strip())
        finished = datetime.fromisoformat(row["finished"].strip())
        minutes = int((finished - started).total_seconds() // 60)
        verdict = "LONG" if minutes > max_minutes else "OK"
        out.append((row["job"].strip(), row["system"].strip(),
                    started.isoformat(), finished.isoformat(), minutes, verdict))
    return sorted(out, key=lambda r: (-r[4], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--max-minutes", type=int, default=120)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = analyse(list(csv.DictReader(f)), args.max_minutes)
    for job, system, started, finished, minutes, verdict in results:
        print(f"{job} [{system}]: {verdict} ({minutes} min, {started} -> {finished})")
    average = round(sum(r[4] for r in results) / len(results), 1) if results else 0.0
    print(f"Average duration: {average:.1f} min across {len(results)} job(s); "
          f"{sum(1 for *_, v in results if v == 'LONG')} job(s) over the {args.max_minutes} min limit.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
