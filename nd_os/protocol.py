"""Daily protocol: Morning (mud), Peak (sacred), Wind-down (90% done)."""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, time
from typing import Optional

from nd_os.profile import NDProfile


class ProtocolPhase(Enum):
    """Current phase of daily protocol."""

    NIGHT = "night"  # Wind-down, recovery
    MORNING = "morning"  # Mud hours, light work
    PEAK = "peak"  # Sacred deep work
    WIND_DOWN = "wind_down"  # Prep for next day


@dataclass
class ProtocolTodo:
    """Single action item in protocol phase."""

    title: str
    description: str = ""
    completed: bool = False
    time_estimate_minutes: int = 15


@dataclass
class DailyProtocol:
    """
    The daily rhythm that works for ND brains.

    Don't fight your energy. Flow with it.
    """

    profile: NDProfile
    date: datetime = field(default_factory=datetime.now)

    # Night/wind-down
    night_todos: list[ProtocolTodo] = field(default_factory=list)

    # Morning (mud hours)
    morning_todos: list[ProtocolTodo] = field(default_factory=list)

    # Peak hours (sacred)
    peak_todos: list[ProtocolTodo] = field(default_factory=list)

    # Weekly additions
    weekly_todos: list[ProtocolTodo] = field(default_factory=list)

    def __post_init__(self):
        """Initialize with default protocol structure."""
        if not self.night_todos:
            self.night_todos = [
                ProtocolTodo(
                    title="Leave one task 90% done",
                    description="Zeigarnik effect: unfinished work pulls you back tomorrow",
                    time_estimate_minutes=5,
                ),
                ProtocolTodo(
                    title="3 implementation intentions",
                    description='When X, I will Y. Set up tomorrow\'s trigger-action pairs',
                    time_estimate_minutes=10,
                ),
                ProtocolTodo(
                    title="Pre-mortem: biggest risk tomorrow",
                    description="What could derail you? Plan defense.",
                    time_estimate_minutes=10,
                ),
            ]

        if not self.morning_todos:
            self.morning_todos = [
                ProtocolTodo(
                    title="Light tasks (email, admin)",
                    description="Mud hours aren't deep work hours. Use for inbox management.",
                    time_estimate_minutes=30,
                ),
                ProtocolTodo(
                    title="RAS priming: 3 specific targets",
                    description="Name what you're hunting today (not vague goals)",
                    time_estimate_minutes=10,
                ),
                ProtocolTodo(
                    title="Loss-frame the day",
                    description='If I don\'t do X, I lose Y. Combat inertia with loss aversion.',
                    time_estimate_minutes=5,
                ),
                ProtocolTodo(
                    title="2-minute rule: tiniest first step",
                    description="What's the 2-minute version of deep work? Start there.",
                    time_estimate_minutes=2,
                ),
            ]

        if not self.peak_todos:
            self.peak_todos = [
                ProtocolTodo(
                    title="Music on, notifications off",
                    description="Sensory regulation + momentum protection",
                    time_estimate_minutes=1,
                ),
                ProtocolTodo(
                    title="Parallel tracks loaded",
                    description="Have 3+ tracks ready so if one stalls, switch",
                    time_estimate_minutes=5,
                ),
                ProtocolTodo(
                    title="Deep work block (90min+)",
                    description="Sacred time. Nothing else.",
                    time_estimate_minutes=90,
                ),
                ProtocolTodo(
                    title="OODA loop after each meaningful action",
                    description="Observe, Orient, Decide, Act. Feedback to adjust.",
                    time_estimate_minutes=5,
                ),
                ProtocolTodo(
                    title="When breakthrough hits, ride it",
                    description="Cancel everything else. This is the work.",
                    time_estimate_minutes=0,
                ),
                ProtocolTodo(
                    title="When headache hits, switch tracks",
                    description="Don't stop. Redirect. Thermal management.",
                    time_estimate_minutes=5,
                ),
            ]

        if not self.weekly_todos:
            self.weekly_todos = [
                ProtocolTodo(
                    title="Inversion: How would I guarantee failure?",
                    description="Reverse engineer your worst outcomes to prevent them",
                    time_estimate_minutes=30,
                ),
                ProtocolTodo(
                    title="Contrast exposure: 10x-ahead content",
                    description="Watch/read people 10x ahead. Recalibrate standards.",
                    time_estimate_minutes=45,
                ),
                ProtocolTodo(
                    title="Evidence review: what you shipped",
                    description="Built + shipped + sold. Receipts beat doubt.",
                    time_estimate_minutes=20,
                ),
            ]

    def current_phase(self) -> ProtocolPhase:
        """Detect which phase of day we're in."""
        now = datetime.now()
        hour = now.hour

        if self.profile.is_peak_hour(hour):
            return ProtocolPhase.PEAK
        elif self.profile.is_mud_hour(hour):
            return ProtocolPhase.MORNING
        elif self.profile.is_coast_hour(hour):
            return ProtocolPhase.MORNING
        else:
            return ProtocolPhase.NIGHT

    def todos_for_phase(self, phase: ProtocolPhase) -> list[ProtocolTodo]:
        """Get todos for a specific phase."""
        if phase == ProtocolPhase.NIGHT:
            return self.night_todos
        elif phase == ProtocolPhase.MORNING:
            return self.morning_todos
        elif phase == ProtocolPhase.PEAK:
            return self.peak_todos
        else:
            return []

    def next_phase(self) -> ProtocolPhase:
        """Suggest next phase based on time."""
        current = self.current_phase()

        sequence = [ProtocolPhase.MORNING, ProtocolPhase.PEAK, ProtocolPhase.WIND_DOWN, ProtocolPhase.NIGHT]
        idx = sequence.index(current) if current in sequence else 0

        return sequence[(idx + 1) % len(sequence)]

    def phase_summary(self, phase: ProtocolPhase) -> str:
        """Get human-readable summary of phase goals."""
        summaries = {
            ProtocolPhase.NIGHT: (
                "Wind-down: Leave work 90% done (Zeigarnik). "
                "Set 3 implementation intentions. Pre-mortem tomorrow's risks."
            ),
            ProtocolPhase.MORNING: (
                "Mud hours (low cognition). Light admin work. "
                "RAS prime your targets. Loss-frame the day."
            ),
            ProtocolPhase.PEAK: (
                "Sacred deep work. Music on, notifications off. "
                "Parallel tracks ready. Ride breakthroughs. Switch when thermal throttle hits."
            ),
            ProtocolPhase.WIND_DOWN: (
                "Transition: reflect on day. Plan tomorrow. "
                "Don't push into fatigue."
            ),
        }
        return summaries.get(phase, "Phase protocol unknown")

    def mark_todo_done(self, phase: ProtocolPhase, todo_index: int) -> None:
        """Mark a todo as completed."""
        todos = self.todos_for_phase(phase)
        if 0 <= todo_index < len(todos):
            todos[todo_index].completed = True

    def completion_percent(self, phase: ProtocolPhase) -> int:
        """Progress % for current phase."""
        todos = self.todos_for_phase(phase)
        if not todos:
            return 0
        completed = sum(1 for t in todos if t.completed)
        return int((completed / len(todos)) * 100)
