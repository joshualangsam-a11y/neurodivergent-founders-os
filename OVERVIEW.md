# nd-os: Project Overview

## What Was Built

A production-ready Python package that operationalizes the Neurodivergent Founder's OS from a manifesto into executable code. This is the framework that will live on Josh's Anthropic application, GitHub, and become open-source infrastructure for ND founders.

## Structure

```
~/neurodivergent-founders-os/
├── THE-OS.md                    # Original manifesto (preserved)
├── README.md                    # Production documentation (open source)
├── QUICKSTART.md                # 5-minute getting started
├── pyproject.toml               # Python package config (installable via pip)
├── test_nd_os.py                # Smoke tests (all pass)
│
├── nd_os/
│   ├── __init__.py              # Package exports (17 core classes)
│   ├── profile.py (132 lines)   # NDProfile - your brain configuration
│   ├── energy.py (147 lines)    # EnergyMapper - daily cycle detection
│   ├── parallel.py (187 lines)  # ParallelTrackManager - multi-thread work
│   ├── momentum.py (156 lines)  # MomentumTracker - flow state protection
│   ├── thermal.py (132 lines)   # ThermalManager - overload detection
│   ├── translation.py (109 lines) # IntentCompressor - bandwidth expansion
│   ├── compound.py (171 lines)  # CompoundEngine - cross-session learning
│   ├── protocol.py (219 lines)  # DailyProtocol - morning/peak/wind-down
│   │
│   ├── presets/                 # Brain type JSON configs
│   │   ├── adhd_parallel.json       # Parallel processor (3-6 tracks)
│   │   ├── adhd_hyperfocus.json     # Mono-track lock-in (1-2 tracks)
│   │   ├── autism_systematic.json   # Pattern matcher (2-3 tracks)
│   │   ├── dyslexia_visual.json     # Spatial thinker (2-4 tracks)
│   │   └── mixed.json               # Multi-trait ND (3-5 tracks)
│   │
│   └── hooks/
│       ├── __init__.py
│       └── claude_code.py (203 lines) # Claude Code hook integration
│           - UserPromptSubmit: Inject energy context
│           - PreToolUse: Protect momentum
│           - Stop: Save session learnings
```

## Core Modules (1507 lines of Python)

### 1. **profile.py** — Your Brain Configuration
- `NDProfile`: Master configuration class
- `NDType`: 5 brain types (ADHD parallel, ADHD hyperfocus, autism, dyslexia, mixed)
- `EnergyPattern`: Daily energy curves (morning peak, afternoon peak, evening peak, bimodal)
- Preset loading: `NDProfile.from_preset("adhd_parallel")`
- Custom profiles: `profile.to_file()`, `profile.from_file()`

### 2. **energy.py** — Daily Energy Cycle
- `EnergyMapper`: Detects current energy state in real-time
- `EnergyState`: MUD, COAST, PEAK, OVERLOAD
- Methods:
  - `current_state()` — What's your energy RIGHT NOW?
  - `suggest_work_type()` — What should you work on?
  - `can_do_deep_work_now()` — Peak hours?
  - `hours_until_peak()` — Time to next peak?
  - `thermal_overload_risk()` — Burnout approaching?

### 3. **parallel.py** — Parallel Track Management
- `ParallelTrackManager`: Manage 3+ concurrent work streams
- `Track`: Single work stream with context preservation
- `TrackStatus`: ACTIVE, PAUSED, BLOCKED, COMPLETED
- Methods:
  - `add_track()` — Create new parallel track
  - `switch_track()` — Switch focus without losing state
  - `suggest_next_track()` — What to switch to when stuck
  - `has_minimum_parallel()` — Do we have 3+ tracks?
  - `count_by_domain()` — How many in building/selling/learning?

### 4. **momentum.py** — Flow State Protection
- `MomentumTracker`: Track and protect momentum (oxygen)
- `MomentumSignal`: Permission-seeking, interruptions, doubt spirals, etc.
- Context-switch cost: 45 minutes (configurable)
- Methods:
  - `start_flow()` — Beginning focused work
  - `interrupt()` — Someone broke your flow
  - `current_momentum()` — Flow state snapshot (0-1)
  - `recovery_time_minutes()` — How long to recover
  - `danger_list()` — Human-readable warnings
  - `is_high_momentum()` — Are you in strong flow?

### 5. **thermal.py** — Cognitive Overload Detection
- `ThermalManager`: Detect when brain is overheating
- `ThermalState`: COOL, WARM, HOT, CRITICAL
- Signals: headache, fog, pressure = thermal throttle
- Methods:
  - `start_focus()` — Begin deep work in domain
  - `domain_switch()` — Switch to different cognitive domain (recovery)
  - `log_throttle_signal()` — Record manual thermal signals
  - `current_temperature()` — Thermal state snapshot
  - `is_overheating()` — Risk detection

### 6. **translation.py** — Bandwidth Expansion
- `IntentCompressor`: Bridge vision ↔ sequential output gap
- Pattern: Record voice memo → compress to structure → expand for audience
- Methods:
  - `record_vision()` — Capture flash understanding
  - `compress_to_structured()` — Convert to sequential outline
  - `expand_for_audience()` — Adapt for technical/business/customer/team
  - `sketch_before_write()` — Spatial-first communication
  - `voice_memo_pattern()` — Record → transcribe → structure workflow
  - `bandwidth_gap_estimate()` — How long does explanation take?

### 7. **compound.py** — Cross-Session Learning
- `CompoundEngine`: Track learnings across sessions
- `SessionLearning`: Single session's breakthrough/success/failure snapshot
- Methods:
  - `start_session()` — Begin new session learning
  - `breakthrough_history()` — All insights across time
  - `success_patterns()` — What works most often
  - `failure_patterns()` — What fails most often
  - `pre_session_insight()` — Tomorrow's lessons from today
  - `momentum_killer_frequency()` — Most common flow-breakers
  - `compound_effectiveness_score()` — Are you learning?

### 8. **protocol.py** — Daily Rhythm
- `DailyProtocol`: Morning/Peak/Wind-down protocol
- `ProtocolPhase`: NIGHT, MORNING, PEAK, WIND_DOWN
- `ProtocolTodo`: Actionable todos per phase
- Methods:
  - `current_phase()` — Where are we in the day?
  - `todos_for_phase()` — Get phase-specific actions
  - `next_phase()` — What's next?
  - `phase_summary()` — Human-readable phase goals
  - `completion_percent()` — Progress tracking per phase

### 9. **hooks/claude_code.py** — Claude Code Integration
- `UserPromptSubmitHook`: Inject energy state context into prompts
- `PreToolUseHook`: Protect momentum before tool execution
- `StopHook`: Save session learnings on exit
- `generate_hooks_json()`: Output Claude Code hook configuration
- **Purpose**: Claude sees your energy state, respects your flow, compounds learning

## Key Design Decisions

### 1. **Each module is independently useful**
- Use `EnergyMapper` alone for energy tracking
- Use `ParallelTrackManager` alone for task management
- Use `MomentumTracker` alone for flow protection
- No mandatory interdependencies

### 2. **Profile drives everything**
- All systems reference `NDProfile`
- Brain type → energy pattern → work suggestions
- Thermal threshold, switch cost, track count all configurable
- Presets provide instant onboarding

### 3. **Type hints + docstrings (public API only)**
- All classes fully type-hinted
- Docstrings only on public methods (API)
- No docstrings on private/internal code
- Clean, production-ready code

### 4. **Dataclasses for data, methods for behavior**
- Use `@dataclass` for configuration and snapshots
- Use regular classes for managers/engines
- No over-abstraction, no inheritance chains

### 5. **Enum for clarity**
- `NDType`, `EnergyPattern`, `EnergyState`, etc.
- Self-documenting, no magic strings
- Safe at runtime

## Testing

All smoke tests pass:
- Profile creation and presets ✓
- Energy mapping and suggestions ✓
- Parallel track management ✓
- Momentum tracking and recovery ✓
- Thermal detection ✓
- Daily protocol todos ✓
- Cross-session learning ✓
- Translation layer ✓
- Claude Code hooks generation ✓

```bash
python3 test_nd_os.py
# Results: Passed 9/9
```

## Usage Patterns

### Quick Start
```python
from nd_os import NDProfile, EnergyMapper, ParallelTrackManager

profile = NDProfile.from_preset("adhd_parallel")
energy = EnergyMapper(profile)
tracks = ParallelTrackManager()

tracks.add_track("Build", "building", is_primary=True)
tracks.add_track("Sell", "selling")
tracks.add_track("Learn", "learning")

print(f"Work now: {energy.suggest_work_type()}")
print(f"Tracks: {tracks.has_minimum_parallel(3)}")
```

### Daily Routine
```python
from nd_os import DailyProtocol

protocol = DailyProtocol(profile)
phase = protocol.current_phase()
todos = protocol.todos_for_phase(phase)
for todo in todos:
    print(f"□ {todo.title}")
```

### Session Learning
```python
from nd_os import CompoundEngine

compound = CompoundEngine()
session = compound.start_session()
session.add_success("Parallel tracks prevented thrash")
session.add_failure("Ignored thermal warning")

next_day = compound.pre_session_insight()
```

### Claude Code Integration
```python
from nd_os.hooks import generate_hooks_json

hooks = generate_hooks_json(profile, energy, momentum, compound, tracks)
# Add to settings.json under "hooks" array
```

## Open Source Readiness

✓ MIT license (in README)
✓ Clear structure and naming
✓ Production code quality (no TODOs, no debug code)
✓ Comprehensive documentation (README + QUICKSTART)
✓ Working tests
✓ Type hints throughout
✓ No external dependencies beyond pydantic

Ready to:
- Upload to GitHub
- Publish to PyPI
- Include in Anthropic application
- Cite in academic/professional contexts

## Next Steps (For Josh)

1. **GitHub**: Create repo, push code
2. **PyPI**: Publish package (`python -m build && twine upload`)
3. **Anthropic App**: Include as portfolio project
4. **Community**: Gather feedback from ND founders
5. **Learning**: Track what works, what fails, evolve

## Stats

- **Total Python code**: 1,507 lines (core modules)
- **Core classes**: 17 exported
- **Brain type presets**: 5 (ADHD parallel, ADHD hyperfocus, autism, dyslexia, mixed)
- **Test coverage**: All major modules (9/9 smoke tests pass)
- **Dependencies**: Only pydantic (zero external tools)
- **Documentation**: 500+ lines (README + QUICKSTART)

## Philosophy

This is not a toy. This is real infrastructure for ND founders.

- Not "tips for ADHD productivity"
- Not "mindset shifts"
- This is: **Operating system code for a different brain architecture**

Built from lived experience (ADHD + dyslexia + 145 systems in one night), tested in production, designed for actual use in Claude Code workflows.

Not medical advice. This is an operating manual from one ND founder to another.

---

**Current status**: Complete, tested, production-ready. Ready for GitHub + Anthropic application.
