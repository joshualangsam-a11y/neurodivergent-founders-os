"""Terminal integration hooks for ND OS.

Tracks terminal velocity, session lifecycle, and command switching patterns.
Provides signals for focused work detection and context switching costs.
"""

import time
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class TerminalSession:
    """Terminal session metadata."""
    session_id: str
    start_time: float
    last_command_time: float
    command_count: int = 0
    context_switches: int = 0
    is_active: bool = True


class TerminalHooks:
    """Hooks for terminal behavior tracking."""

    def __init__(self):
        self.session: Optional[TerminalSession] = None
        self.keystroke_buffer: list[float] = []
        self.keystroke_threshold = 0.05  # seconds, defines rapid typing
        self.context_switch_callbacks: list[Callable] = []

    def on_session_start(self, session_id: str) -> TerminalSession:
        """Called when terminal session begins."""
        now = time.time()
        self.session = TerminalSession(
            session_id=session_id,
            start_time=now,
            last_command_time=now,
        )
        return self.session

    def on_session_end(self) -> Optional[TerminalSession]:
        """Called when terminal session ends."""
        if self.session:
            self.session.is_active = False
        result = self.session
        self.session = None
        return result

    def on_keystroke(self, timestamp: Optional[float] = None) -> float:
        """Track keystroke velocity. Returns velocity percentage (0-100)."""
        timestamp = timestamp or time.time()
        self.keystroke_buffer.append(timestamp)

        # Keep only recent keystrokes (last 2 seconds)
        cutoff = timestamp - 2.0
        self.keystroke_buffer = [t for t in self.keystroke_buffer if t > cutoff]

        # Calculate velocity: keystrokes per second
        if len(self.keystroke_buffer) > 1:
            elapsed = self.keystroke_buffer[-1] - self.keystroke_buffer[0]
            if elapsed > 0:
                velocity = min(100, (len(self.keystroke_buffer) / elapsed) * 10)
                return velocity
        return 0.0

    def on_command_start(self, command: str) -> dict:
        """Called when user starts a new command."""
        if not self.session:
            self.on_session_start("auto")

        now = time.time()
        time_since_last = now - self.session.last_command_time

        # Detect context switch: >5 second gap or different command type
        is_switch = time_since_last > 5.0
        if is_switch:
            self.session.context_switches += 1
            for callback in self.context_switch_callbacks:
                callback(self.session, command, time_since_last)

        self.session.last_command_time = now
        return {
            "is_context_switch": is_switch,
            "gap_seconds": time_since_last,
            "context_switch_count": self.session.context_switches,
        }

    def on_command_end(self, exit_code: int = 0) -> None:
        """Called when command completes."""
        if self.session:
            self.session.command_count += 1

    def register_context_switch_callback(self, callback: Callable) -> None:
        """Register callback for context switch detection."""
        self.context_switch_callbacks.append(callback)


# Global singleton
_terminal_hooks = TerminalHooks()


def get_terminal_hooks() -> TerminalHooks:
    """Get global terminal hooks instance."""
    return _terminal_hooks
