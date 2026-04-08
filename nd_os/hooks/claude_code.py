"""Claude Code hook definitions for nd-os integration."""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

from nd_os.profile import NDProfile
from nd_os.energy import EnergyMapper
from nd_os.momentum import MomentumTracker
from nd_os.parallel import ParallelTrackManager
from nd_os.compound import CompoundEngine


@dataclass
class UserPromptSubmitHook:
    """
    Hook: Before Claude processes your prompt.

    Injects energy state context so Claude knows your current capacity.
    """

    hook_name: str = "UserPromptSubmit"
    description: str = "Inject ND energy state context into prompts"

    def generate_system_prompt_injection(
        self,
        profile: NDProfile,
        energy_mapper: EnergyMapper,
        momentum_tracker: MomentumTracker,
    ) -> str:
        """
        Generate a system prompt injection that adds context.

        Claude will see this before processing your message.
        """
        energy = energy_mapper.current_state()
        momentum = momentum_tracker.current_momentum()

        injection = f"""
[ND Context - {datetime.now().strftime('%H:%M')}]
Energy State: {energy.state.value} ({energy.reason})
Momentum: {momentum.current_level:.0%} (in flow {momentum.minutes_in_flow}min)
Brain Type: {profile.nd_type.value}
Current Work: Parallel architecture (min {profile.min_parallel_tracks} tracks)

Guidance:
- If energy=peak: suggest deep work, architecture, complex problems
- If energy=mud: suggest admin, planning, lightweight tasks
- If momentum<50%: protect flow state, minimize interruptions
- If momentum danger signals: address them directly
- Respect parallel processing: suggest multiple tracks/paths, not linear steps
- Translation layer: compress intent, expand for audience

{profile.translation_preferred_format} mode enabled.
"""
        return injection.strip()

    def to_hook_dict(
        self,
        profile: NDProfile,
        energy_mapper: EnergyMapper,
        momentum_tracker: MomentumTracker,
    ) -> dict:
        """Convert to Claude Code hook JSON format."""
        return {
            "hookName": self.hook_name,
            "description": self.description,
            "type": "system_prompt_injection",
            "injection": self.generate_system_prompt_injection(
                profile, energy_mapper, momentum_tracker
            ),
            "priority": "high",
        }


@dataclass
class PreToolUseHook:
    """
    Hook: Before Claude uses any tool.

    Protects flow state. Warns if tool use would break momentum.
    """

    hook_name: str = "PreToolUse"
    description: str = "Protect momentum before tool execution"

    def generate_momentum_check(
        self, momentum_tracker: MomentumTracker, profile: NDProfile
    ) -> dict:
        """Check if tool use will break flow."""
        momentum = momentum_tracker.current_momentum()
        recovery = momentum_tracker.recovery_time_minutes()

        return {
            "current_momentum_percent": int(momentum.current_level * 100),
            "recovery_time_minutes": recovery,
            "is_high_momentum": momentum.current_level >= 0.7,
            "danger_signals": [s.value for s in momentum.danger_signals],
            "recommendations": [
                "If momentum<50%: batch this with other tools (avoid context switch)"
                if momentum.current_level < 0.5
                else "Momentum healthy. Proceed.",
                f"Switch cost: {profile.switch_cost_minutes}min" if recovery > 0 else "No switch cost",
            ],
        }

    def to_hook_dict(
        self, momentum_tracker: MomentumTracker, profile: NDProfile
    ) -> dict:
        """Convert to Claude Code hook JSON format."""
        return {
            "hookName": self.hook_name,
            "description": self.description,
            "type": "pre_tool_use",
            "check": self.generate_momentum_check(momentum_tracker, profile),
            "priority": "high",
        }


@dataclass
class StopHook:
    """
    Hook: When Claude Code session ends.

    Saves session learnings for compound effect.
    Preserves context for next session.
    """

    hook_name: str = "Stop"
    description: str = "Save session learnings and momentum state"

    def generate_session_summary(
        self,
        compound_engine: CompoundEngine,
        parallel_tracks: ParallelTrackManager,
        momentum_tracker: MomentumTracker,
    ) -> dict:
        """Create session learning snapshot."""
        session = compound_engine.start_session()

        # What worked today
        active_tracks = parallel_tracks.active_tracks()
        for track in active_tracks:
            if track.progress_percent > 80:
                session.add_success(f"Completed {track.name} ({track.progress_percent}%)")

        # Momentum data
        momentum = momentum_tracker.current_momentum()
        session.energy_notes = f"Final momentum: {momentum.current_level:.0%} after {momentum.minutes_in_flow}min focus"

        # Next session hint
        next_track = parallel_tracks.suggest_next_track()
        if next_track:
            session.next_session_hint = f"Resume: {next_track.name}"

        return {
            "session_date": session.session_date.isoformat(),
            "successes": session.what_worked,
            "failures": session.what_failed,
            "next_hint": session.next_session_hint,
            "compound_effectiveness": compound_engine.compound_effectiveness_score(),
        }

    def to_hook_dict(
        self,
        compound_engine: CompoundEngine,
        parallel_tracks: ParallelTrackManager,
        momentum_tracker: MomentumTracker,
    ) -> dict:
        """Convert to Claude Code hook JSON format."""
        return {
            "hookName": self.hook_name,
            "description": self.description,
            "type": "session_end",
            "summary": self.generate_session_summary(
                compound_engine, parallel_tracks, momentum_tracker
            ),
            "priority": "high",
        }


def generate_hooks_json(
    profile: NDProfile,
    energy_mapper: EnergyMapper,
    momentum_tracker: MomentumTracker,
    compound_engine: CompoundEngine,
    parallel_tracks: ParallelTrackManager,
) -> str:
    """
    Generate complete Claude Code hooks configuration.

    Add this to your settings.json under `hooks` array.
    """
    hooks = [
        UserPromptSubmitHook().to_hook_dict(
            profile, energy_mapper, momentum_tracker
        ),
        PreToolUseHook().to_hook_dict(momentum_tracker, profile),
        StopHook().to_hook_dict(compound_engine, parallel_tracks, momentum_tracker),
    ]

    return json.dumps(hooks, indent=2)
