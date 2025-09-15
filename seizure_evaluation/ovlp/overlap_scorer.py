#!/usr/bin/env python3
"""
Native implementation of Temple NEDC OVERLAP scoring.
This implements any-overlap counting, NOT 1-to-1 matching or fractional TAES.

OVERLAP scoring rules:
- Hit: Any reference event that has ANY overlap with ANY hypothesis event
- Miss: Reference event with NO overlap to any hypothesis
- False Alarm: Hypothesis event with NO overlap to any reference
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Event:
    """Represents a seizure event with start/stop times."""

    start_time: float
    stop_time: float
    label: str = "seiz"
    confidence: float = 1.0

    @property
    def duration(self) -> float:
        """Event duration in seconds."""
        return self.stop_time - self.start_time

    def overlaps(self, other: "Event") -> bool:
        """Check if this event has ANY overlap with another."""
        overlap_start = max(self.start_time, other.start_time)
        overlap_stop = min(self.stop_time, other.stop_time)
        return overlap_stop > overlap_start  # Any overlap counts


@dataclass
class OverlapMetrics:
    """OVERLAP scoring metrics matching Temple NEDC."""

    hits: int  # Number of ref events with any overlap
    misses: int  # Number of ref events with no overlap
    false_alarms: int  # Number of hyp events with no overlap
    total_duration_sec: float
    # Optional: background false alarms for Temple 'Total False Alarm Rate'
    bckg_false_alarms: int = 0

    @property
    def sensitivity(self) -> float:
        """Sensitivity (TPR, Recall) as percentage."""
        total_refs = self.hits + self.misses
        if total_refs == 0:
            return 0.0
        return 100.0 * self.hits / total_refs

    @property
    def fa_per_24h(self) -> float:
        """False alarms per 24 hours."""
        if self.total_duration_sec == 0:
            return float("inf")
        return self.false_alarms * 86400.0 / self.total_duration_sec

    @property
    def total_fa_per_24h(self) -> float:
        """Temple 'Total False Alarm Rate' across SEIZ + BCKG labels."""
        if self.total_duration_sec == 0:
            return float("inf")
        return (self.false_alarms + self.bckg_false_alarms) * 86400.0 / self.total_duration_sec

    @property
    def precision(self) -> float:
        """Precision as percentage."""
        total_hyps = self.hits + self.false_alarms
        if total_hyps == 0:
            return 0.0
        return 100.0 * self.hits / total_hyps

    @property
    def f1_score(self) -> float:
        """F1 score (harmonic mean of precision and recall)."""
        prec = self.precision / 100.0
        rec = self.sensitivity / 100.0
        if prec + rec == 0:
            return 0.0
        return 2 * (prec * rec) / (prec + rec)


class OverlapScorer:
    """
    OVERLAP scoring implementation matching Temple NEDC v6.0.0.

    This implements ANY-OVERLAP counting:
    - Each ref event is either hit (has overlap) or missed (no overlap)
    - Each hyp event is either correct (has overlap) or false alarm (no overlap)
    - No 1-to-1 matching constraint
    """

    def score_events(
        self, ref_events: list[Event], hyp_events: list[Event], total_duration_sec: float
    ) -> OverlapMetrics:
        """
        Score hypothesis events against reference events using OVERLAP method.

        Args:
            ref_events: Ground truth seizure events
            hyp_events: Predicted seizure events
            total_duration_sec: Total recording duration in seconds

        Returns:
            OverlapMetrics with scoring results
        """
        # SEIZ label scoring: any-overlap counting on original events
        ref_has_overlap = [False] * len(ref_events)
        hyp_has_overlap = [False] * len(hyp_events)

        # Check all possible overlaps
        for r_idx, ref in enumerate(ref_events):
            for h_idx, hyp in enumerate(hyp_events):
                if ref.overlaps(hyp):
                    ref_has_overlap[r_idx] = True
                    hyp_has_overlap[h_idx] = True

        # Count SEIZ label results
        hits = sum(ref_has_overlap)  # Refs with any overlap
        misses = len(ref_events) - hits  # Refs with no overlap
        false_alarms = len(hyp_events) - sum(hyp_has_overlap)  # Hyps with no overlap

        # Temple OVERLAP per-label false alarms:
        # Compute false alarms for the BCKG label by constructing
        # background event lists for ref and hyp, then applying the
        # same any-overlap logic at the event level.
        ref_bckg = self._complement_of_events(ref_events, total_duration_sec)
        hyp_bckg = self._complement_of_events(hyp_events, total_duration_sec)

        bckg_false_alarms = 0
        for hb in hyp_bckg:
            # if this hyp background event does NOT overlap any ref background
            # event, it is a BCKG false alarm under Temple OVERLAP
            if not any(
                (hb.start_time < rb.stop_time and rb.start_time < hb.stop_time)
                for rb in ref_bckg
            ):
                bckg_false_alarms += 1

        return OverlapMetrics(
            hits=hits,
            misses=misses,
            false_alarms=false_alarms,
            total_duration_sec=total_duration_sec,
            bckg_false_alarms=bckg_false_alarms,
        )

    def score_from_files(self, ref_csv_bi: Path, hyp_csv_bi: Path) -> OverlapMetrics:
        """
        Score events from CSV_bi file.

        Args:
            ref_csv_bi: Path to reference CSV_bi file
            hyp_csv_bi: Path to hypothesis CSV_bi file

        Returns:
            OverlapMetrics with scoring results
        """
        ref_events, ref_duration = self._parse_csv_bi(ref_csv_bi)
        hyp_events, hyp_duration = self._parse_csv_bi(hyp_csv_bi)

        # Use reference duration for scoring
        return self.score_events(ref_events, hyp_events, ref_duration)

    def _parse_csv_bi(self, csv_bi_path: Path) -> tuple[list[Event], float]:
        """Parse events from CSV_bi file."""
        events = []
        duration = 0.0

        with open(csv_bi_path) as f:
            for line in f:
                line = line.strip()

                # Parse duration from header
                if line.startswith("# duration ="):
                    duration = float(line.split("=")[1].replace("secs", "").strip())

                # Skip headers and empty lines
                if line.startswith("#") or not line or line.startswith("channel"):
                    continue

                # Parse event
                parts = line.split(",")
                if len(parts) >= 5:
                    events.append(
                        Event(
                            start_time=float(parts[1]),
                            stop_time=float(parts[2]),
                            label=parts[3],
                            confidence=float(parts[4]),
                        )
                    )

        return events, duration

    def _complement_of_events(
        self, events: list[Event], total_duration_sec: float
    ) -> list[Event]:
        """Compute background (complement) events over [0, total_duration_sec]."""
        if total_duration_sec <= 0:
            return []
        if not events:
            return [Event(0.0, total_duration_sec, label="bckg")]

        # Merge and sort input events by start time
        events_sorted = sorted(events, key=lambda e: e.start_time)
        merged: list[Event] = []
        cur = None
        for e in events_sorted:
            if cur is None:
                cur = Event(e.start_time, e.stop_time, e.label, e.confidence)
                continue
            if e.start_time <= cur.stop_time:
                cur.stop_time = max(cur.stop_time, e.stop_time)
            else:
                merged.append(cur)
                cur = Event(e.start_time, e.stop_time, e.label, e.confidence)
        if cur is not None:
            merged.append(cur)

        background: list[Event] = []
        t = 0.0
        for e in merged:
            if e.start_time > t:
                background.append(Event(t, e.start_time, label="bckg"))
            t = max(t, e.stop_time)
        if t < total_duration_sec:
            background.append(Event(t, total_duration_sec, label="bckg"))
        return background

