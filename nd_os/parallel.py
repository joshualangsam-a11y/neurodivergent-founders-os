"""Parallel track manager: Run 3+ threads, context-switch without losing state."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime, timedelta
import uuid


class TrackStatus(Enum):
    """State of a parallel track."""

    ACTIVE = "active"  # Currently working
    PAUSED = "paused"  # Switched away but not abandoned
    BLOCKED = "blocked"  # Waiting on external (find parallel track)
    COMPLETED = "completed"  # Done


@dataclass
class Track:
    """
    Single parallel work stream.

    Tracks maintain their own context so switching doesn't mean forgetting.
    """

    name: str
    domain: str  # "building", "selling", "learning"
    description: str = ""
    status: TrackStatus = TrackStatus.ACTIVE

    # Context preservation
    context: dict = field(default_factory=dict)  # Last state snapshot
    progress_percent: int = 0
    last_active: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)

    # Track metadata
    track_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    is_primary: bool = False  # Is this the main focus right now?
    priority: int = 1  # 1=critical, 2=important, 3=nice-to-have

    def __hash__(self) -> int:
        return hash(self.track_id)

    def mark_active(self) -> None:
        """Switch focus to this track."""
        self.status = TrackStatus.ACTIVE
        self.last_active = datetime.now()

    def pause(self) -> None:
        """Pause without abandoning (context stays)."""
        self.status = TrackStatus.PAUSED

    def mark_blocked(self, reason: str) -> None:
        """Mark as blocked on external dependency."""
        self.status = TrackStatus.BLOCKED
        self.context["blocked_reason"] = reason
        self.context["blocked_at"] = datetime.now().isoformat()

    def save_context(self, state: dict) -> None:
        """Save current work state (for resumption)."""
        self.context = state
        self.last_active = datetime.now()

    def resume_context(self) -> dict:
        """Get last saved context when resuming."""
        return self.context.copy()

    def minutes_since_active(self) -> int:
        """How long since this track was touched."""
        return int((datetime.now() - self.last_active).total_seconds() / 60)


@dataclass
class ParallelTrackManager:
    """
    Manages multiple concurrent work streams.

    Rule: Minimum 3 active tracks (building, selling, learning).
    If one stalls, switch. The subconscious keeps processing.
    """

    tracks: dict[str, Track] = field(default_factory=dict)
    current_track_id: Optional[str] = None

    def add_track(
        self,
        name: str,
        domain: str,
        description: str = "",
        is_primary: bool = False,
        priority: int = 1,
    ) -> Track:
        """Create a new parallel track."""
        track = Track(
            name=name,
            domain=domain,
            description=description,
            is_primary=is_primary,
            priority=priority,
        )

        self.tracks[track.track_id] = track

        if is_primary or len(self.tracks) == 1:
            self.current_track_id = track.track_id

        return track

    def switch_track(self, track_id: str) -> Track:
        """Switch to a different track."""
        if track_id not in self.tracks:
            raise ValueError(f"Track {track_id} not found")

        if self.current_track_id:
            old_track = self.tracks[self.current_track_id]
            if old_track.status == TrackStatus.ACTIVE:
                old_track.pause()

        track = self.tracks[track_id]
        track.mark_active()
        self.current_track_id = track_id
        return track

    def current_track(self) -> Optional[Track]:
        """Get currently active track."""
        if not self.current_track_id:
            return None
        return self.tracks.get(self.current_track_id)

    def get_track(self, track_id: str) -> Track:
        """Retrieve a specific track."""
        return self.tracks[track_id]

    def active_tracks(self) -> list[Track]:
        """Tracks currently in parallel (ACTIVE, PAUSED, or BLOCKED - not COMPLETED)."""
        return [t for t in self.tracks.values() if t.status != TrackStatus.COMPLETED]

    def paused_tracks(self) -> list[Track]:
        """Tracks you switched away from but didn't finish."""
        return [t for t in self.tracks.values() if t.status == TrackStatus.PAUSED]

    def blocked_tracks(self) -> list[Track]:
        """Tracks waiting on external dependency."""
        return [t for t in self.tracks.values() if t.status == TrackStatus.BLOCKED]

    def suggest_next_track(self) -> Optional[Track]:
        """
        When current track stalls, suggest what to switch to.

        Preference: BLOCKED (waiting on external) -> lowest priority active -> newest.
        """
        # Find blocked tracks (perfect candidate)
        blocked = self.blocked_tracks()
        if blocked:
            # Switch to one that's been waiting longest
            return min(blocked, key=lambda t: t.minutes_since_active())

        # Find lowest-priority active track
        active = self.active_tracks()
        if len(active) > 1:
            return min(active, key=lambda t: (t.priority, t.last_active))

        # Find paused track to resume
        paused = self.paused_tracks()
        if paused:
            return max(paused, key=lambda t: t.last_active)

        return None

    def count_by_domain(self) -> dict[str, int]:
        """How many tracks in each domain (building, selling, learning)."""
        counts = {}
        for track in self.tracks.values():
            if track.status != TrackStatus.COMPLETED:
                counts[track.domain] = counts.get(track.domain, 0) + 1
        return counts

    def complete_track(self, track_id: str) -> None:
        """Mark track as done."""
        self.tracks[track_id].status = TrackStatus.COMPLETED

    def has_minimum_parallel(self, minimum: int = 3) -> bool:
        """Do we have minimum parallel tracks running?"""
        active = len(self.active_tracks())
        return active >= minimum
