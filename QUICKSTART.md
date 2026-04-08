# nd-os Quick Start

Get running in 5 minutes.

## Install

```bash
pip install nd-os
```

## Load Your Brain Type

```python
from nd_os import NDProfile

# Load built-in preset
profile = NDProfile.from_preset("adhd_parallel")

# Or create custom
from nd_os import NDType, EnergyPattern

profile = NDProfile(
    nd_type=NDType.ADHD_PARALLEL,
    name="My ND Brain",
    energy_pattern=EnergyPattern.AFTERNOON_PEAK,
)
```

## Check Energy State

```python
from nd_os import EnergyMapper

energy = EnergyMapper(profile)

print(energy.current_state())  # What's your energy RIGHT NOW?
print(energy.suggest_work_type())  # What should you work on?
print(energy.hours_until_peak())  # When's your next peak?
```

## Manage Parallel Tracks

```python
from nd_os import ParallelTrackManager

tracks = ParallelTrackManager()

# Create 3+ parallel tracks
tracks.add_track("Build API", "building", is_primary=True)
tracks.add_track("Close first client", "selling")
tracks.add_track("Read TypeScript book", "learning")

# When stuck on one, switch to another
next_track = tracks.suggest_next_track()
tracks.switch_track(next_track.track_id)
```

## Protect Momentum

```python
from nd_os import MomentumTracker

momentum = MomentumTracker(switch_cost_minutes=45)

momentum.start_flow()

# Someone interrupts
momentum.interrupt()

# How long to recover?
print(f"Recovery: {momentum.recovery_time_minutes()}min")

# What's breaking your flow?
print(momentum.danger_list())
```

## Detect Thermal Overload

```python
from nd_os import ThermalManager

thermal = ThermalManager(thermal_threshold_minutes=90)

thermal.start_focus("building")

# After deep focus
snapshot = thermal.current_temperature()

if snapshot.state.value == "hot":
    print("Switch domains NOW to avoid burnout")
    thermal.domain_switch("selling")
```

## Daily Protocol

```python
from nd_os import DailyProtocol

protocol = DailyProtocol(profile)

# Morning?
if protocol.current_phase().value == "morning":
    todos = protocol.todos_for_phase(protocol.current_phase())
    for todo in todos:
        print(f"□ {todo.title}")
```

## Cross-Session Learning

```python
from nd_os import CompoundEngine

compound = CompoundEngine()

# End of session
session = compound.start_session()
session.add_success("Parallel tracks saved the day")
session.add_failure("Ignored thermal warning")
session.next_session_hint = "Watch for headache signal at 90min"

# Next session: pre-flight
print("Yesterday's lessons:")
print(compound.pre_session_insight())
```

## Real Example: Morning Workflow

```python
from nd_os import (
    NDProfile,
    EnergyMapper,
    ParallelTrackManager,
    DailyProtocol,
    ProtocolPhase,
)

# Setup
profile = NDProfile.from_preset("adhd_parallel")
energy = EnergyMapper(profile)
tracks = ParallelTrackManager()
protocol = DailyProtocol(profile)

# Add work
tracks.add_track("Build feature", "building", is_primary=True)
tracks.add_track("Sales calls", "selling")
tracks.add_track("Learn React", "learning")

# Morning routine
print(f"Phase: {protocol.current_phase().value}")
print(f"Suggested work: {energy.suggest_work_type()}")

todos = protocol.todos_for_phase(ProtocolPhase.MORNING)
print("\nMorning todos:")
for todo in todos:
    print(f"  □ {todo.title}")

# Show tracks
print(f"\nTracks active: {len(tracks.active_tracks())}")
print(f"✓ {profile.min_parallel_tracks}+ tracks? {tracks.has_minimum_parallel()}")
```

---

## Brain Types Reference

| Type | Energy Pattern | Tracks | Music | Switch Cost |
|------|---|---|---|---|
| `adhd_parallel` | Afternoon peak | 3-6 | Yes 128 BPM | 45min |
| `adhd_hyperfocus` | Afternoon peak | 1-2 | Yes 120 BPM | 60min |
| `autism_systematic` | Morning peak | 2-3 | No | 30min |
| `dyslexia_visual` | Bimodal | 2-4 | Yes 110 BPM | 35min |
| `mixed` | Bimodal | 3-5 | Yes 120 BPM | 45min |

```python
profile = NDProfile.from_preset("adhd_parallel")
```

---

## Core Concepts

### Energy Mapping
You cycle through MUD → COAST → PEAK hours. Never waste peak on email. Use mud for admin.

### Parallel Architecture
Run 3+ threads simultaneously. When one blocks, switch. Subconscious keeps processing.

### Momentum Protection
Context switch costs 45 minutes. Protect flow state like oxygen.

### Thermal Management
Hyperfocus has a limit (~90min). Then you overheat. Switch domains to cool down.

### Translation Layer
Your brain is fast. Explaining takes 10x longer. Use voice memos, diagrams, AI.

### Daily Protocol
Morning (mud/admin) → Peak (deep work) → Wind-down (90% done Zeigarnik).

### Cross-Session Learning
Track what works, what fails, compound the lessons session-to-session.

---

## Next Steps

- Read `THE-OS.md` for philosophy and rules
- Read `README.md` for full API reference
- Check `nd_os/presets/` for brain type definitions
- Create custom profile with `profile.to_file("my_profile.json")`
- Integrate with Claude Code hooks (see README)

---

**Built for ND founders. By ND founder. Not medical advice. Operating manual.**
