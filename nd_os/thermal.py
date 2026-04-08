"""Thermal management: Detect overload, prevent burnout, suggest domain switches."""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional


class ThermalState(Enum):
    """Cognitive thermal state."""

    COOL = "cool"  # Fresh, ready for deep work
    WARM = "warm"  # Focused but sustainable
    HOT = "hot"  # Approaching limits, switch tracks
    CRITICAL = "critical"  # Overload, must stop or switch domain


@dataclass
class ThermalSnapshot:
    """Current thermal state measurement."""

    state: ThermalState
    temperature: float  # 0-1, where 1 is critical
    time_focused_minutes: int
    recovery_needed_minutes: int
    recommended_action: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ThermalManager:
    """
    Detect when your brain is overheating.

    Signal: headache, pressure, fog = thermal throttle.
    Fix: switch tracks (don't stop), not push through same wall.
    """

    thermal_threshold_minutes: int = 90  # Hyperfocus window before overload risk
    recovery_per_minute_switched: float = 0.5  # Cool-down rate when domain-switched
    critical_threshold: float = 0.95  # When to force stop

    focus_start: Optional[datetime] = None
    last_domain_switch: Optional[datetime] = None
    current_domain: Optional[str] = None
    manual_throttle_signals: list[str] = field(default_factory=list)

    def start_focus(self, domain: str) -> None:
        """Beginning focused work in a domain (building, selling, learning, etc)."""
        self.focus_start = datetime.now()
        self.current_domain = domain
        self.last_domain_switch = None

    def log_throttle_signal(self, signal: str) -> None:
        """Log a manual thermal signal (headache, fog, pressure)."""
        self.manual_throttle_signals.append(signal)

    def domain_switch(self, new_domain: str) -> None:
        """Switch to different cognitive domain (not just different task in same domain)."""
        if self.focus_start and self.current_domain != new_domain:
            self.last_domain_switch = datetime.now()
            self.current_domain = new_domain
            self.manual_throttle_signals = []

    def current_temperature(self) -> ThermalSnapshot:
        """Measure thermal state (0-1)."""
        if not self.focus_start:
            return ThermalSnapshot(
                state=ThermalState.COOL,
                temperature=0.0,
                time_focused_minutes=0,
                recovery_needed_minutes=0,
                recommended_action="Start focused work",
            )

        now = datetime.now()
        minutes_focused = int((now - self.focus_start).total_seconds() / 60)

        # Base heat from continuous focus
        heat = min(1.0, minutes_focused / self.thermal_threshold_minutes)

        # Reduce heat if switched domains recently
        if self.last_domain_switch:
            minutes_since_switch = (now - self.last_domain_switch).total_seconds() / 60
            heat *= max(0.0, 1.0 - (minutes_since_switch * self.recovery_per_minute_switched))

        # Manual signals add heat
        if self.manual_throttle_signals:
            heat = min(1.0, heat + 0.3)

        # Determine state
        if heat >= self.critical_threshold:
            state = ThermalState.CRITICAL
            recommended = "STOP. Switch domains completely or take 30min recovery break."
        elif heat >= 0.7:
            state = ThermalState.HOT
            recommended = f"Approaching overload. Switch to {self._opposite_domain()} domain NOW."
        elif heat >= 0.4:
            state = ThermalState.WARM
            recommended = "Still sustainable. Watch for signals. Prepare switch option."
        else:
            state = ThermalState.COOL
            recommended = "Fresh. Push hard."

        return ThermalSnapshot(
            state=state,
            temperature=heat,
            time_focused_minutes=minutes_focused,
            recovery_needed_minutes=int(heat * 30),  # Rough: hotter = longer recovery
            recommended_action=recommended,
        )

    def is_overheating(self) -> bool:
        """Simple: are we at thermal risk?"""
        snapshot = self.current_temperature()
        return snapshot.state in (ThermalState.HOT, ThermalState.CRITICAL)

    def _opposite_domain(self) -> str:
        """Suggest opposite domain (for domain switching)."""
        if self.current_domain == "building":
            return "selling or learning"
        elif self.current_domain == "selling":
            return "building or learning"
        else:
            return "building"

    def clear_for_new_session(self) -> None:
        """Reset after taking recovery break."""
        self.focus_start = None
        self.last_domain_switch = None
        self.current_domain = None
        self.manual_throttle_signals = []
