"""Profile system: Configure your neurodivergent brain type and defaults."""

from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional
import json
from pathlib import Path


class NDType(Enum):
    """Neurodivergent brain types with distinct architectural patterns."""

    ADHD_PARALLEL = "adhd_parallel"  # Parallel processor, high context-switching cost
    ADHD_HYPERFOCUS = "adhd_hyperfocus"  # Mono-track lock-in, mission-driven
    AUTISM_SYSTEMATIC = "autism_systematic"  # Pattern matcher, preference for structure
    DYSLEXIA_VISUAL = "dyslexia_visual"  # Spatial/visual thinking, language bandwidth bottleneck
    MIXED = "mixed"  # Multiple ND traits


class EnergyPattern(Enum):
    """Daily energy curves."""

    MORNING_PEAK = "morning_peak"  # Early riser, mud at night
    AFTERNOON_PEAK = "afternoon_peak"  # Common ND pattern: mud morning, peak afternoon/evening
    EVENING_PEAK = "evening_peak"  # Late night productive spike
    BIMODAL = "bimodal"  # Two peaks, usually morning + evening


@dataclass
class NDProfile:
    """
    Your neurodivergent architecture. All systems reference this.

    This is the single source of truth for how your brain works.
    Changing this changes behavior across energy mapping, momentum protection,
    thermal management, and protocol scheduling.
    """

    nd_type: NDType
    name: str
    energy_pattern: EnergyPattern

    # Your personal cycle (24-hour time in 0-23 format)
    mud_hours_start: int = 5  # When low cognition begins
    mud_hours_end: int = 10  # When you can work
    peak_hours_start: int = 14  # When deep work is sacred
    peak_hours_end: int = 22  # When focus cliffs
    coast_hours: list[int] = field(default_factory=lambda: [9, 12, 23])  # Admin/light work

    # Context-switch sensitivity (higher = more costly to interrupt)
    switch_cost_minutes: int = 45  # Time to re-enter flow after break
    momentum_decay_hours: float = 2.0  # How fast momentum fades without continuation

    # Parallel track tolerance (how many threads you can handle)
    min_parallel_tracks: int = 3
    max_parallel_tracks: int = 6

    # Sensory regulation
    prefers_music: bool = True
    music_tempo_bpm: Optional[int] = None  # None = detect from current state
    noise_sensitivity: float = 0.5  # 0=silent preferred, 1=noise helps focus

    # Thermal throttling signals
    thermal_threshold_minutes: int = 90  # How long before overload signal appears
    thermal_recovery_minutes: int = 30  # Recovery time when thermal throttle hits

    # Translation layer preferences
    translation_preferred_format: str = "voice"  # "voice", "sketches", "structured"
    ai_bandwidth_expander: bool = True

    @classmethod
    def from_file(cls, path: str | Path) -> "NDProfile":
        """Load profile from JSON file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Profile not found: {path}")

        with open(path) as f:
            data = json.load(f)

        # Enum conversion
        data["nd_type"] = NDType(data["nd_type"])
        data["energy_pattern"] = EnergyPattern(data["energy_pattern"])

        return cls(**data)

    @classmethod
    def from_preset(cls, preset_name: str) -> "NDProfile":
        """Load a built-in preset (adhd_parallel, adhd_hyperfocus, etc)."""
        preset_dir = Path(__file__).parent / "presets"
        preset_path = preset_dir / f"{preset_name}.json"

        if not preset_path.exists():
            available = [p.stem for p in preset_dir.glob("*.json")]
            raise ValueError(
                f"Preset '{preset_name}' not found. Available: {', '.join(available)}"
            )

        return cls.from_file(preset_path)

    def to_file(self, path: str | Path) -> None:
        """Save profile to JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = asdict(self)
        data["nd_type"] = self.nd_type.value
        data["energy_pattern"] = self.energy_pattern.value

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def is_peak_hour(self, hour: int) -> bool:
        """Check if hour is in peak window."""
        if self.peak_hours_start <= self.peak_hours_end:
            return self.peak_hours_start <= hour < self.peak_hours_end
        # Handle wraparound (e.g., 22:00 to 02:00)
        return hour >= self.peak_hours_start or hour < self.peak_hours_end

    def is_mud_hour(self, hour: int) -> bool:
        """Check if hour is in mud window."""
        if self.mud_hours_start <= self.mud_hours_end:
            return self.mud_hours_start <= hour < self.mud_hours_end
        return hour >= self.mud_hours_start or hour < self.mud_hours_end

    def is_coast_hour(self, hour: int) -> bool:
        """Check if hour is in coast window (admin/light work)."""
        return hour in self.coast_hours

    def __hash__(self) -> int:
        """Make profile hashable for use as dict key."""
        return hash((self.nd_type, self.name, self.energy_pattern))
