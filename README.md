# nd-os: Neurodivergent Founder's Operating System

Not how to cope. How to weaponize.

An open-source Python framework for ADHD/dyslexic/autistic founders who think in flashes, build in parallel, and were told their brain was broken.

**Status:** Alpha (v0.1.0) — Production-ready architecture, pre-release documentation.

---

## What This Is

Your neurodivergent brain doesn't have a disorder. It has a different instruction set.

- **Parallel processor** → runs 10 threads where others run 1
- **Bandwidth bottleneck** → brain faster than output channels
- **Pain converter** → turns frustration into fuel
- **Pattern matcher** → sees systems, not steps
- **OODA loop speed** → decides in seconds, executes for years

The problem was never your brain. It was the environment. `nd-os` gives you an operating system designed for your architecture.

---

## Core Concepts

### 1. Energy Mapping
You don't have "good days" and "bad days." You have cycles.

```python
from nd_os import EnergyMapper, NDProfile

# Load your brain type
profile = NDProfile.from_preset("adhd_parallel")
energy = EnergyMapper(profile)

# What should I work on right now?
print(energy.suggest_work_type())  # "deep_work" | "light_admin" | "switch_tracks"

# When's my next peak?
print(energy.hours_until_peak())
```

### 2. Parallel Architecture
Minimum 3 active tracks. When one stalls, switch. The subconscious keeps processing.

```python
from nd_os import ParallelTrackManager

tracks = ParallelTrackManager()
tracks.add_track("Build auth system", "building", is_primary=True)
tracks.add_track("Close first client", "selling")
tracks.add_track("Read SICP", "learning")

# Blocked on waiting for API response?
tracks.switch_track(track_id)  # Switch, don't push
```

### 3. Momentum Protection
Momentum is oxygen. Context-switch cost = 45 minutes. Protect it.

```python
from nd_os import MomentumTracker

momentum = MomentumTracker(switch_cost_minutes=45)
momentum.start_flow()

# Someone breaks your flow
momentum.interrupt()
print(f"Recovery time: {momentum.recovery_time_minutes()}min")

# Check danger signals
print(momentum.danger_list())
```

### 4. Thermal Management
Detect when your brain is overheating. Headache/fog/pressure = throttle signal.

```python
from nd_os import ThermalManager

thermal = ThermalManager(thermal_threshold_minutes=90)
thermal.start_focus("building")

# After 90 minutes hyperfocus
snapshot = thermal.current_temperature()
print(snapshot.recommended_action)  # "Switch to selling domain NOW"
```

### 5. Translation Layer
Your biggest bottleneck isn't thinking. It's transmitting.

```python
from nd_os import IntentCompressor

vision = IntentCompressor(preferred_format="voice")
vision.record_vision("whole system I just saw...")

# Convert to structured outline
print(vision.compress_to_structured())

# Adapt for audience
print(vision.expand_for_audience("technical"))
```

### 6. Daily Protocol
Morning (mud), Peak (sacred), Wind-down (90% done).

```python
from nd_os import DailyProtocol

protocol = DailyProtocol(profile)
current = protocol.current_phase()  # MORNING | PEAK | WIND_DOWN | NIGHT
todos = protocol.todos_for_phase(current)

for todo in todos:
    print(f"→ {todo.title}")
```

### 7. Cross-Session Learning
Track what works, what fails, compound the lessons.

```python
from nd_os import CompoundEngine

compound = CompoundEngine()
session = compound.start_session()

# Record breakthroughs
session.add_breakthrough("Parallel tracks prevent context-thrash")
session.add_success("Focus morning on admin, afternoon on building")

# Next session: pre-flight intelligence
print(compound.pre_session_insight())
```

---

## Getting Started

### Installation

```bash
pip install nd-os
```

Or develop locally:

```bash
git clone https://github.com/joshlangsam/nd-os.git
cd nd-os
pip install -e ".[dev]"
pytest
```

### Quick Start: 5 Minutes

```python
from nd_os import (
    NDProfile,
    EnergyMapper,
    ParallelTrackManager,
    MomentumTracker,
    DailyProtocol,
)

# 1. Load your brain type
profile = NDProfile.from_preset("adhd_parallel")

# 2. Check energy state
energy = EnergyMapper(profile)
print(f"Work type: {energy.suggest_work_type()}")

# 3. Manage parallel tracks
tracks = ParallelTrackManager()
tracks.add_track("Feature X", "building", is_primary=True)
tracks.add_track("Sales", "selling")
tracks.add_track("Learning", "learning")

# 4. Protect momentum
momentum = MomentumTracker(profile.switch_cost_minutes)
momentum.start_flow()

# 5. Daily protocol
protocol = DailyProtocol(profile)
print(f"Current phase: {protocol.current_phase().value}")
print(f"Todos: {[t.title for t in protocol.todos_for_phase(protocol.current_phase())]}")
```

---

## Claude Code Integration

Use `nd-os` hooks in Claude Code to get energy state context, momentum protection, and session learning.

### Setup

```bash
# Generate hooks JSON
python3 -c "
from nd_os import NDProfile, EnergyMapper, MomentumTracker, CompoundEngine, ParallelTrackManager
from nd_os.hooks import generate_hooks_json

profile = NDProfile.from_preset('adhd_parallel')
energy = EnergyMapper(profile)
momentum = MomentumTracker(profile.switch_cost_minutes)
compound = CompoundEngine()
tracks = ParallelTrackManager()

hooks = generate_hooks_json(profile, energy, momentum, compound, tracks)
print(hooks)
" > hooks.json
```

Add to `~/.claude/settings.json`:

```json
{
  "hooks": [
    {
      "hookName": "UserPromptSubmit",
      "description": "Inject ND energy state context",
      "type": "system_prompt_injection",
      "injection": "[ND Context] Energy: peak | Momentum: 85% | Mode: parallel"
    },
    {
      "hookName": "PreToolUse",
      "description": "Protect momentum before tool use",
      "type": "pre_tool_use"
    },
    {
      "hookName": "Stop",
      "description": "Save session learnings",
      "type": "session_end"
    }
  ]
}
```

---

## Brain Types (Presets)

### ADHD Parallel
- **Energy pattern:** Afternoon peak (mud until 2pm, then sacred hours 2pm-10pm)
- **Parallel tracks:** 3-6 simultaneously
- **Music:** Yes, ~128 BPM
- **Switch cost:** 45 minutes
- **Use when:** You think in flashes, can't do one thing at a time, hyperfocus is real

Load: `NDProfile.from_preset("adhd_parallel")`

### ADHD Hyperfocus
- **Energy pattern:** Afternoon peak, but mono-track lock-in
- **Parallel tracks:** 1-2 (mission-driven, mission-locked)
- **Music:** Yes, ~120 BPM
- **Switch cost:** 60 minutes (higher because you hate context switches)
- **Use when:** You lock into one thing and nothing else exists

Load: `NDProfile.from_preset("adhd_hyperfocus")`

### Autism Systematic
- **Energy pattern:** Morning peak (quiet morning 8am-1pm, deep focus)
- **Parallel tracks:** 2-3 (prefer structure)
- **Music:** No (silence better)
- **Switch cost:** 30 minutes (faster recovery because you pre-structure)
- **Use when:** You think systematically, prefer structure, want clear steps

Load: `NDProfile.from_preset("autism_systematic")`

### Dyslexia Visual
- **Energy pattern:** Bimodal (morning spike, evening spike)
- **Parallel tracks:** 2-4 (visual, not sequential)
- **Music:** Yes, ~110 BPM (helps with rhythmic processing)
- **Switch cost:** 35 minutes
- **Use when:** You think in diagrams, language is a bottleneck, spatial processing is native

Load: `NDProfile.from_preset("dyslexia_visual")`

### Mixed ND
- **ADHD + Dyslexia hybrid**
- **Bimodal energy:** Two peaks (morning + evening)
- **Parallel tracks:** 3-5
- **Music:** Yes, ~120 BPM
- **Use when:** You have multiple ND traits

Load: `NDProfile.from_preset("mixed")`

---

## Customization

### Create Your Own Profile

```python
from nd_os import NDProfile, NDType, EnergyPattern

profile = NDProfile(
    nd_type=NDType.ADHD_PARALLEL,
    name="My Custom Profile",
    energy_pattern=EnergyPattern.AFTERNOON_PEAK,
    mud_hours_start=6,
    mud_hours_end=10,
    peak_hours_start=14,
    peak_hours_end=22,
    switch_cost_minutes=45,
    min_parallel_tracks=3,
    max_parallel_tracks=6,
)

# Save for next session
profile.to_file("~/.nd-os/my_profile.json")

# Load later
profile = NDProfile.from_file("~/.nd-os/my_profile.json")
```

### Adjust Thermal Threshold

```python
profile.thermal_threshold_minutes = 120  # I can hyperfocus longer
profile.thermal_recovery_minutes = 45    # But I need more recovery
```

---

## API Reference

### `NDProfile`
Your brain configuration. All systems reference this.

```python
profile.is_peak_hour(14)              # bool
profile.is_mud_hour(7)                # bool
profile.is_coast_hour(9)              # bool
profile.hours_until_peak()            # int
profile.thermal_overload_risk(120)    # float 0-1
```

### `EnergyMapper`
Daily energy cycle detector.

```python
energy = EnergyMapper(profile)

energy.current_state()                # EnergySnapshot
energy.suggest_work_type()            # "deep_work" | "light_admin" | "switch_tracks"
energy.can_do_deep_work_now()         # bool
energy.hours_until_peak()             # int
energy.thermal_overload_risk(mins)    # float
```

### `ParallelTrackManager`
Manage concurrent work streams.

```python
tracks = ParallelTrackManager()

tracks.add_track("name", "domain")    # Track
tracks.switch_track(track_id)         # Track
tracks.current_track()                # Track | None
tracks.active_tracks()                # [Track]
tracks.paused_tracks()                # [Track]
tracks.blocked_tracks()               # [Track]
tracks.suggest_next_track()           # Track | None
tracks.count_by_domain()              # {domain: count}
tracks.has_minimum_parallel(3)        # bool
```

### `MomentumTracker`
Flow state protection.

```python
momentum = MomentumTracker(switch_cost_minutes=45)

momentum.start_flow()                 # None
momentum.interrupt()                  # None
momentum.current_momentum()           # MomentumSnapshot
momentum.is_high_momentum(0.7)        # bool
momentum.recovery_time_minutes()      # int
momentum.danger_list()                # [str] human-readable warnings
momentum.reset()                      # None
```

### `ThermalManager`
Cognitive overload detection.

```python
thermal = ThermalManager(thermal_threshold_minutes=90)

thermal.start_focus("building")       # None
thermal.domain_switch("selling")      # None
thermal.log_throttle_signal("headache")  # None
thermal.current_temperature()         # ThermalSnapshot
thermal.is_overheating()              # bool
```

### `DailyProtocol`
Morning/Peak/Wind-down rhythm.

```python
protocol = DailyProtocol(profile)

protocol.current_phase()              # ProtocolPhase
protocol.todos_for_phase(phase)       # [ProtocolTodo]
protocol.next_phase()                 # ProtocolPhase
protocol.mark_todo_done(phase, idx)   # None
protocol.completion_percent(phase)    # int 0-100
```

### `CompoundEngine`
Cross-session learning.

```python
compound = CompoundEngine()

session = compound.start_session()    # SessionLearning
compound.last_session()               # SessionLearning | None
compound.breakthrough_history()       # [(datetime, str)]
compound.success_patterns()           # {pattern: count}
compound.failure_patterns()           # {pattern: count}
compound.pre_session_insight()        # [str]
```

---

## Real-World Examples

### Example 1: Morning Routine

```python
profile = NDProfile.from_preset("adhd_parallel")
energy = EnergyMapper(profile)
protocol = DailyProtocol(profile)

# Morning (mud hours)
print(f"Phase: {protocol.current_phase().value}")
print(f"Suggested work: {energy.suggest_work_type()}")

# Run morning todos
morning = protocol.todos_for_phase(ProtocolPhase.MORNING)
for todo in morning:
    print(f"□ {todo.title}")
```

### Example 2: Peak Hour Protection

```python
momentum = MomentumTracker(switch_cost_minutes=45)
thermal = ThermalManager(thermal_threshold_minutes=90)

momentum.start_flow()
thermal.start_focus("building")

# 60 minutes later
snapshot = thermal.current_temperature()
if snapshot.state == ThermalState.HOT:
    print("Overload approaching. Switch tracks.")
    thermal.domain_switch("selling")

# Check recovery time
print(f"Will be fresh in {momentum.recovery_time_minutes()}min")
```

### Example 3: Track Switching

```python
tracks = ParallelTrackManager()
tracks.add_track("Build API", "building", is_primary=True)
tracks.add_track("Email investors", "selling")
tracks.add_track("Read TypeScript", "learning")

# Blocked waiting for API response
tracks.get_track(track_id).mark_blocked("Waiting for DB migration")

# What should I do?
next_track = tracks.suggest_next_track()
print(f"Switch to: {next_track.name}")
tracks.switch_track(next_track.track_id)
```

### Example 4: Session Learning

```python
compound = CompoundEngine()
session = compound.start_session()

# End of session
session.add_success("Parallel tracks prevented context-thrash")
session.add_failure("Interrupted by Slack at 2pm broke 90min focus")
session.next_session_hint = "Block Slack during peak hours"

# Tomorrow, before starting:
print("Pre-flight intelligence:")
for insight in compound.pre_session_insight():
    print(f"  → {insight}")
```

---

## Philosophy

### The Reframe
Everything you were told was weakness is actually architecture.

| They Said | It Actually Is |
|-----------|---|
| Can't focus | Parallel processor |
| Can't sit still | Momentum engine |
| Can't articulate | Bandwidth bottleneck |
| Impulsive | OODA loop speed |
| Goes down rabbit holes | Autodidact wiring |
| Too emotional | Pain-to-output converter |
| Doesn't follow instructions | Cross-domain pattern matcher |

### The Operating System
Your brain doesn't break the rules. It runs a different ruleset.

`nd-os` is the ruleset. It explains:

1. **Why parallel processing works** — You're not distracted, you're multi-threaded
2. **Why energy mapping matters** — You're not lazy, you're cycling
3. **Why momentum is oxygen** — Context switches aren't "quick," they're 45 minutes
4. **Why thermal throttle is real** — Hyperfocus has a limit, then you're done
5. **Why translation is hard** — Your vision is whole; explaining takes sequential time

### The Truth
You will build things neurotypical brains cannot build. Not because you're better—because you're different. Your parallel processing, your pain conversion, your pattern matching, your speed of decision—these aren't compensations for a deficit. They're capabilities that don't exist in the neurotypical stack.

The world wasn't designed for your brain. So you'll design your own world.

That's not a cope. That's the plan.

---

## Contributing

This is open source. The more ND founders use this and contribute learnings, the better it gets.

```bash
git clone https://github.com/joshlangsam/nd-os.git
cd nd-os
pip install -e ".[dev]"
pytest
```

### Adding a Preset
Create a new JSON file in `nd_os/presets/`:

```json
{
  "nd_type": "your_type",
  "name": "Your Profile Name",
  "energy_pattern": "afternoon_peak",
  ...
}
```

### Adding a Module
Each module should be independently useful. Add to `nd_os/`, expose in `__init__.py`.

### Tests
```bash
pytest --cov=nd_os
```

---

## License

MIT. Use freely, build on top, fork, remix. The code is yours.

---

## References

### Inspiration & Research
- [The Bandwidth Expanders Paper](#) — Why ND founders' biggest bottleneck is transmission
- "Why Are We Here?" — ADHD executive function research
- Cross-domain pattern matching in autism
- Pain-to-output conversion in adversity studies

### Built From
- 145 systems in one night (Josh Langsam)
- Lived experience: ADHD + dyslexia + TBI recovery
- 10 years shipping as founder with ND brain

---

**Status:** This is not medical advice. This is an operating manual from one ND founder to another.

For updates and community: [GitHub](https://github.com/joshlangsam/nd-os)
