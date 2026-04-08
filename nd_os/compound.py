"""Compound engine: Cross-session learning and momentum compounding."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class SessionLearning:
    """Single session's learning snapshot."""

    session_date: datetime
    breakthrough_moments: list[str] = field(default_factory=list)
    patterns_observed: list[str] = field(default_factory=list)
    energy_notes: str = ""
    thermal_events: list[str] = field(default_factory=list)
    what_worked: list[str] = field(default_factory=list)
    what_failed: list[str] = field(default_factory=list)
    momentum_killers: list[str] = field(default_factory=list)
    next_session_hint: str = ""

    def add_breakthrough(self, insight: str) -> None:
        """Record a breakthrough moment."""
        self.breakthrough_moments.append(insight)

    def add_pattern(self, pattern: str) -> None:
        """Note an observed pattern (how you work, what triggers states)."""
        self.patterns_observed.append(pattern)

    def add_success(self, success: str) -> None:
        """What worked (protect/replicate this)."""
        self.what_worked.append(success)

    def add_failure(self, failure: str) -> None:
        """What didn't work (avoid this pattern)."""
        self.what_failed.append(failure)

    def log_momentum_killer(self, killer: str) -> None:
        """What broke your flow."""
        self.momentum_killers.append(killer)


@dataclass
class CompoundEngine:
    """
    Track learnings across sessions.

    Each session teaches you how YOUR brain works. Compound these lessons
    to make future sessions more effective.
    """

    sessions: list[SessionLearning] = field(default_factory=list)

    def start_session(self) -> SessionLearning:
        """Begin new session, create learning snapshot."""
        session = SessionLearning(session_date=datetime.now())
        self.sessions.append(session)
        return session

    def last_session(self) -> Optional[SessionLearning]:
        """Get most recent session."""
        return self.sessions[-1] if self.sessions else None

    def breakthrough_history(self) -> list[tuple[datetime, str]]:
        """All breakthroughs across all sessions."""
        history = []
        for session in self.sessions:
            for breakthrough in session.breakthrough_moments:
                history.append((session.session_date, breakthrough))
        return history

    def success_patterns(self) -> dict[str, int]:
        """What works most often (frequency count)."""
        patterns = {}
        for session in self.sessions:
            for success in session.what_worked:
                patterns[success] = patterns.get(success, 0) + 1
        return dict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))

    def failure_patterns(self) -> dict[str, int]:
        """What fails most often (avoid these)."""
        patterns = {}
        for session in self.sessions:
            for failure in session.what_failed:
                patterns[failure] = patterns.get(failure, 0) + 1
        return dict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))

    def momentum_killer_frequency(self) -> dict[str, int]:
        """Most common flow-breakers across sessions."""
        killers = {}
        for session in self.sessions:
            for killer in session.momentum_killers:
                killers[killer] = killers.get(killer, 0) + 1
        return dict(sorted(killers.items(), key=lambda x: x[1], reverse=True))

    def energy_pattern_summary(self) -> str:
        """Summary of observed energy patterns."""
        if not self.sessions:
            return "No sessions recorded yet."

        patterns = []
        for session in self.sessions:
            if session.energy_notes:
                patterns.append(f"{session.session_date.date()}: {session.energy_notes}")

        return "\n".join(patterns) if patterns else "No energy patterns recorded."

    def pre_session_insight(self) -> list[str]:
        """
        Before you start today, here's what yesterday's self learned.

        Use this to avoid yesterday's mistakes, replicate yesterday's wins.
        """
        if len(self.sessions) < 2:
            return ["No prior session data yet. Record as you go."]

        last = self.last_session()
        if not last:
            return []

        insights = []

        # Top successes to replicate
        successes = self.success_patterns()
        if successes:
            top_success = list(successes.keys())[0]
            insights.append(f"Yesterday's win (replicate): {top_success}")

        # Top failures to avoid
        failures = self.failure_patterns()
        if failures:
            top_failure = list(failures.keys())[0]
            insights.append(f"Yesterday's trap (avoid): {top_failure}")

        # Top momentum killers
        killers = self.momentum_killer_frequency()
        if killers:
            top_killer = list(killers.keys())[0]
            insights.append(f"Flow-breaker to watch: {top_killer}")

        # Energy note
        if last.energy_notes:
            insights.append(f"Energy pattern: {last.energy_notes}")

        # Next hint
        if last.next_session_hint:
            insights.append(f"Resume from: {last.next_session_hint}")

        return insights if insights else ["Empty session. Create new data."]

    def save_session_exit(self, session: SessionLearning, exit_note: str) -> None:
        """End of session: capture final learning for compound effect."""
        session.next_session_hint = exit_note

    def compound_effectiveness_score(self) -> float:
        """
        Simple metric: are you learning?

        Track if success patterns are appearing more often, failures less often.
        """
        if len(self.sessions) < 2:
            return 0.0

        successes = len(self.success_patterns())
        failures = len(self.failure_patterns())

        if successes == 0:
            return 0.0

        # Score: higher when more successes, fewer failures
        return min(1.0, successes / (successes + failures))
