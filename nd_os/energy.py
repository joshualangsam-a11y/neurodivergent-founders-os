"""Energy cycle mapper and detector. Know when to push and when to switch."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from collections import deque

from nd_os.profile import NDProfile, EnergyPattern


class EnergyState(Enum):
    """Current cognitive energy state."""

    MUD = "mud"  # Low cognition, don't force deep work
    COAST = "coast"  # Admin/light work window
    PEAK = "peak"  # Deep work sacred time
    OVERLOAD = "overload"  # Thermal throttle, switch tracks


@dataclass
class EnergySnapshot:
    """Moment-in-time energy measurement."""

    state: EnergyState
    hour: int
    confidence: float  # 0-1, how sure we are
    reason: str  # Why this state
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class EnergyMapper:
    """
    Maps your daily energy cycle and suggests what work fits this moment.

    Learns from your profile's energy pattern and adapts with observed patterns.
    """

    profile: NDProfile
    history: deque = field(default_factory=lambda: deque(maxlen=168))  # 7 days * 24 hours
    last_state: Optional[EnergySnapshot] = None

    def current_state(self) -> EnergySnapshot:
        """Detect current energy state based on time and history."""
        now = datetime.now()
        hour = now.hour

        # Use profile defaults
        if self.profile.is_peak_hour(hour):
            return EnergySnapshot(
                state=EnergyState.PEAK,
                hour=hour,
                confidence=0.95,
                reason=f"Peak hours ({self.profile.peak_hours_start}-{self.profile.peak_hours_end})",
            )

        if self.profile.is_mud_hour(hour):
            return EnergySnapshot(
                state=EnergyState.MUD,
                hour=hour,
                confidence=0.90,
                reason=f"Mud hours ({self.profile.mud_hours_start}-{self.profile.mud_hours_end})",
            )

        if self.profile.is_coast_hour(hour):
            return EnergySnapshot(
                state=EnergyState.COAST,
                hour=hour,
                confidence=0.85,
                reason=f"Coast hours (admin/light work)",
            )

        # Fallback
        return EnergySnapshot(
            state=EnergyState.COAST,
            hour=hour,
            confidence=0.5,
            reason="Between defined windows",
        )

    def suggest_work_type(self) -> str:
        """Suggest what kind of work fits this energy state."""
        state = self.current_state()
        self.last_state = state

        if state.state == EnergyState.PEAK:
            return "deep_work"
        elif state.state == EnergyState.MUD:
            return "light_admin"
        elif state.state == EnergyState.COAST:
            return "medium_effort"
        else:  # OVERLOAD
            return "switch_tracks"

    def log_actual_energy(self, state: EnergyState, hour: Optional[int] = None) -> None:
        """Record actual observed energy (for learning/adaptation)."""
        if hour is None:
            hour = datetime.now().hour

        self.history.append((hour, state.value))

    def predict_week_pattern(self) -> dict[int, EnergyState]:
        """Predict your energy state for each hour of next week."""
        pattern = {}
        for hour in range(24):
            # Start with profile
            if self.profile.is_peak_hour(hour):
                pattern[hour] = EnergyState.PEAK
            elif self.profile.is_mud_hour(hour):
                pattern[hour] = EnergyState.MUD
            elif self.profile.is_coast_hour(hour):
                pattern[hour] = EnergyState.COAST
            else:
                pattern[hour] = EnergyState.COAST

        # TODO: Learn from history if > 1 week of data
        return pattern

    def can_do_deep_work_now(self) -> bool:
        """Simple: is this a peak hour?"""
        state = self.current_state()
        return state.state == EnergyState.PEAK

    def hours_until_peak(self) -> int:
        """How many hours until next peak window."""
        now = datetime.now()
        hour = now.hour

        if self.profile.is_peak_hour(hour):
            return 0

        if self.profile.peak_hours_start > hour:
            return self.profile.peak_hours_start - hour

        # Peak is tomorrow
        return (24 - hour) + self.profile.peak_hours_start

    def thermal_overload_risk(self, minutes_focused: int) -> float:
        """
        Risk of thermal throttle (0-1).
        If you've been hyperfocused for N minutes, thermal threshold approaches.
        """
        threshold = self.profile.thermal_threshold_minutes
        if minutes_focused >= threshold:
            return min(1.0, minutes_focused / threshold)
        return minutes_focused / threshold * 0.5  # Not at risk yet
