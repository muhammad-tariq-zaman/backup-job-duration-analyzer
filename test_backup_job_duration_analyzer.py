import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import analyse

def row(job, system, started, finished):
    return {"job": job, "system": system, "started": started,
            "finished": finished}

class TestBackupJobDuration(unittest.TestCase):
    def test_duration_computed(self):
        r = analyse([row("J-1", "File", "2026-11-10T22:00", "2026-11-10T23:30")])
        self.assertEqual(r[0][4], 90)

    def test_long_over_limit(self):
        r = analyse([row("J-1", "Mail", "2026-11-10T22:00", "2026-11-11T01:15")])
        self.assertEqual(r[0][5], "LONG")

    def test_exactly_at_limit_is_ok(self):
        r = analyse([row("J-1", "File", "2026-11-10T22:00", "2026-11-11T00:00")])
        self.assertEqual(r[0][5], "OK")

    def test_custom_limit(self):
        r = analyse([row("J-1", "File", "2026-11-10T22:00", "2026-11-10T23:30")],
                    max_minutes=60)
        self.assertEqual(r[0][5], "LONG")

    def test_longest_first(self):
        r = analyse([row("J-1", "File", "2026-11-10T22:00", "2026-11-10T22:30"),
                     row("J-2", "Mail", "2026-11-10T22:00", "2026-11-11T01:00")])
        self.assertEqual(r[0][0], "J-2")

    def test_crosses_midnight(self):
        r = analyse([row("J-1", "Mail", "2026-11-10T23:00", "2026-11-11T00:30")])
        self.assertEqual(r[0][4], 90)

    def test_seconds_ignored(self):
        r = analyse([row("J-1", "File", "2026-11-10T22:00:30", "2026-11-10T22:30:45")])
        self.assertEqual(r[0][4], 30)

    def test_empty_input(self):
        self.assertEqual(analyse([]), [])
