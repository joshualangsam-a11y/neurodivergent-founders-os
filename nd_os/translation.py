"""Translation layer: Compress intent, expand bandwidth. Bridge the vision gap."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class IntentCompressor:
    """
    Your biggest bottleneck isn't thinking—it's transmitting.

    You see the whole picture in a flash. Others need it in sentences.
    This tool compresses your intent, expands bandwidth for others.

    Use patterns:
    - Record voice memo when vision hits → compress to structured output
    - Draw before you write (spatial > sequential)
    - Use AI as bandwidth expander
    """

    vision: Optional[str] = None
    structure: Optional[list[str]] = None
    preferred_format: str = "voice"  # voice, sketches, structured

    def record_vision(self, raw_vision: str) -> None:
        """
        Input: Everything you see in a flash.
        This is raw, probably not in sentences. That's fine.
        """
        self.vision = raw_vision

    def compress_to_structured(self) -> list[str]:
        """
        Convert flash vision into sequential outline.

        Returns bullets the audience can follow.
        """
        if not self.vision:
            return []

        # In real usage, this would call Claude API or similar
        # For now, return structure guideline
        return [
            "1. What is this (one sentence)?",
            "2. Why does it matter (problem it solves)?",
            "3. How does it work (mechanism)?",
            "4. What's the proof (evidence or demo)?",
            "5. What's next (one specific step)?",
        ]

    def expand_for_audience(self, audience_type: str) -> str:
        """
        Take your compressed intent, expand for specific audience.

        audience_type: "technical", "business", "customer", "team"
        """
        if not self.vision:
            return ""

        # Placeholder: real version would adapt language
        adaptations = {
            "technical": "Translate to: architecture, APIs, implementation details",
            "business": "Translate to: revenue, moat, market size, competitive advantage",
            "customer": "Translate to: what it does for them, not how it works",
            "team": "Translate to: what each person owns, what blocks them",
        }

        return adaptations.get(audience_type, "Default structure needed")

    def bandwidth_gap_estimate(self, transmission_seconds: int) -> dict[str, int]:
        """
        How long does it take you to explain vs. how long you thought it?

        You think in 2 seconds. Explaining takes 10x longer.
        Budget for it.
        """
        think_time_seconds = 2
        explanation_seconds = transmission_seconds

        ratio = explanation_seconds / think_time_seconds if think_time_seconds > 0 else 0

        return {
            "your_think_time_seconds": think_time_seconds,
            "explanation_time_seconds": explanation_seconds,
            "bandwidth_ratio": int(ratio),
            "gap_warning": "Accept that explanation takes 10x longer than understanding. "
            "Budget for it.",
        }

    def sketch_before_write(self) -> str:
        """
        For spatial/visual thinkers: draw first, write second.

        Spatial thinkers communicate better in diagrams.
        """
        return (
            "Draw/sketch what you see before you write it out.\n"
            "Spatial > sequential for ND brains.\n"
            "Then convert sketch to words for audience."
        )

    def voice_memo_pattern(self) -> str:
        """Record voice memo when vision hits, structure later."""
        return (
            "1. Hit record when you see it (don't interrupt the vision)\n"
            "2. Dump everything into voice memo (no need for sentences)\n"
            "3. Later: transcribe + structure for audience\n"
            "4. This preserves the flash while translating for others"
        )
