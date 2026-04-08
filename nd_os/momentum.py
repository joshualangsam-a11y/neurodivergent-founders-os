"""Momentum tracker and protection. Momentum is oxygen."""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional


class MomentumSignal(Enum):
    """Warning signs that momentum is breaking."""

    PERMISSION_SEEKING = "permission_seeking"  # Waiting for approval → kill it
    INTERRUPTION = "interruption"  # Someone broke flow → 45min recovery cost
    DOUBT_SPIRAL = "doubt_spiral"  # Self-doubt → point to evidence
    EXTERNALIZED_URGENCY = "externalized_urgency"  # Someone else's deadline ≠ your emergency
    CONTEXT_THRASH = "context_thrash"  # Too many switches
    FATIGUE = "fatigue"  # Energy drained, can't re-enter


@dataclass
class MomentumSnapshot:
    """Point-in-time momentum measurement."""

    current_level: float  # 0-1, where 1 is full flow state
    last_context_switch: datetime
    minutes_in_flow: int
    estimated_decay_minutes: int  # How long until momentum fades
    danger_signals: list[MomentumSignal] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class MomentumTracker:
    """
    Track and protect your momentum state.

    Momentum cost on context switch = 45min (per THE-OS).
    Protect it like oxygen.
    """

    flow_start: Optional[datetime] = None
    last_switch: Optional[datetime] = None
    switch_cost_minutes: int = 45  # From profile
    momentum_decay_rate_minutes: float = 2.0  # How fast it fades
    detected_signals: list[MomentumSignal] = field(default_factory=list)

    def start_flow(self) -> None:
        """Beginning focused work."""
        self.flow_start = datetime.now()
        self.last_switch = self.flow_start
        self.detected_signals = []

    def interrupt(self, reason: str = "") -> None:
        """Someone/something broke flow."""
        if self.flow_start:
            self.detected_signals.append(MomentumSignal.INTERRUPTION)
            self.last_switch = datetime.now()

    def request_approval(self) -> None:
        """You're waiting for permission instead of just going."""
        self.detected_signals.append(MomentumSignal.PERMISSION_SEEKING)

    def doubt_spiral_detected(self) -> None:
        """Self-doubt creeping in."""
        self.detected_signals.append(MomentumSignal.DOUBT_SPIRAL)

    def external_urgency_detected(self) -> None:
        """Someone else's deadline imposed."""
        self.detected_signals.append(MomentumSignal.EXTERNALIZED_URGENCY)

    def current_momentum(self) -> MomentumSnapshot:
        """Get current flow state."""
        if not self.flow_start or not self.last_switch:
            return MomentumSnapshot(
                current_level=0.0,
                last_context_switch=datetime.now(),
                minutes_in_flow=0,
                estimated_decay_minutes=0,
                danger_signals=self.detected_signals,
            )

        now = datetime.now()
        minutes_in_flow = int((now - self.flow_start).total_seconds() / 60)
        minutes_since_switch = int((now - self.last_switch).total_seconds() / 60)

        # Momentum level based on time in flow and decay
        recovery_cost = min(self.switch_cost_minutes, minutes_since_switch)
        momentum_level = max(0.0, 1.0 - (recovery_cost / self.switch_cost_minutes))

        if minutes_in_flow >= 90:  # Thermal threshold approaches
            momentum_level *= 0.9

        return MomentumSnapshot(
            current_level=momentum_level,
            last_context_switch=self.last_switch,
            minutes_in_flow=minutes_in_flow,
            estimated_decay_minutes=int(
                self.momentum_decay_rate_minutes * (1 - momentum_level)
            ),
            danger_signals=self.detected_signals,
        )

    def recovery_time_minutes(self) -> int:
        """Minutes until full momentum recovery after interruption."""
        snapshot = self.current_momentum()
        if snapshot.current_level >= 0.95:
            return 0
        return int(
            self.switch_cost_minutes * (1 - snapshot.current_level)
        )

    def is_high_momentum(self, threshold: float = 0.7) -> bool:
        """Are you in strong flow state?"""
        return self.current_momentum().current_level >= threshold

    def danger_list(self) -> list[str]:
        """Human-readable list of momentum threats."""
        snapshot = self.current_momentum()
        threats = []

        for signal in snapshot.danger_signals:
            if signal == MomentumSignal.PERMISSION_SEEKING:
                threats.append(
                    "Don't ask for approval. Just go. Permission is the enemy of momentum."
                )
            elif signal == MomentumSignal.INTERRUPTION:
                threats.append(
                    f"Flow broken {snapshot.last_context_switch.strftime('%H:%M')}. "
                    f"Recovery time: {self.recovery_time_minutes()}min"
                )
            elif signal == MomentumSignal.DOUBT_SPIRAL:
                threats.append(
                    "Self-doubt detected. Point to 3 concrete things you've shipped. "
                    "Doubt loses when evidence shows up."
                )
            elif signal == MomentumSignal.EXTERNALIZED_URGENCY:
                threats.append(
                    "Someone else's deadline ≠ your emergency. "
                    "Protect your peak hours for YOUR work."
                )
            elif signal == MomentumSignal.CONTEXT_THRASH:
                threats.append(
                    "Too many context switches. Consolidate. Run parallel tracks, not random jumps."
                )
            elif signal == MomentumSignal.FATIGUE:
                threats.append(
                    "Energy depleted. This is not laziness. Switch tracks or thermal recovery needed."
                )

        return threats

    def reset(self) -> None:
        """Hard reset momentum (end of work session)."""
        self.flow_start = None
        self.last_switch = None
        self.detected_signals = []
