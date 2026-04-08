"""Smoke tests: Validate core nd-os modules work end-to-end."""

import sys
from datetime import datetime

# Test all imports
try:
    from nd_os import (
        NDProfile,
        NDType,
        EnergyPattern,
        EnergyMapper,
        EnergyState,
        MomentumTracker,
        MomentumSignal,
        ParallelTrackManager,
        Track,
        TrackStatus,
        ThermalManager,
        ThermalState,
        IntentCompressor,
        CompoundEngine,
        SessionLearning,
        DailyProtocol,
        ProtocolPhase,
    )

    from nd_os.hooks import generate_hooks_json

    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)


def test_profile():
    """Test profile creation and presets."""
    # Default profile
    profile = NDProfile(
        nd_type=NDType.ADHD_PARALLEL,
        name="Test",
        energy_pattern=EnergyPattern.AFTERNOON_PEAK,
    )
    assert profile.nd_type == NDType.ADHD_PARALLEL
    print("✓ Profile creation works")

    # Load preset
    profile = NDProfile.from_preset("adhd_parallel")
    assert profile.min_parallel_tracks == 3
    assert profile.peak_hours_start == 14
    print("✓ Preset loading works")

    # Hour checks
    assert profile.is_peak_hour(15) == True
    assert profile.is_peak_hour(7) == False
    assert profile.is_mud_hour(7) == True
    print("✓ Hour detection works")


def test_energy():
    """Test energy mapping."""
    profile = NDProfile.from_preset("adhd_parallel")
    energy = EnergyMapper(profile)

    state = energy.current_state()
    assert state.state in [EnergyState.MUD, EnergyState.PEAK, EnergyState.COAST]
    print(f"✓ Energy state detection works (current: {state.state.value})")

    work_type = energy.suggest_work_type()
    assert work_type in ["deep_work", "light_admin", "medium_effort", "switch_tracks"]
    print(f"✓ Work type suggestion works (suggested: {work_type})")

    hours = energy.hours_until_peak()
    assert 0 <= hours <= 24
    print(f"✓ Hours until peak calculation works ({hours}h)")


def test_parallel_tracks():
    """Test track management."""
    manager = ParallelTrackManager()

    t1 = manager.add_track("Build API", "building", is_primary=True)
    t2 = manager.add_track("Sales", "selling")
    t3 = manager.add_track("Learning", "learning")

    assert len(manager.tracks) == 3
    assert manager.current_track().name == "Build API"
    print("✓ Track creation works")

    # Switch
    manager.switch_track(t2.track_id)
    assert manager.current_track().name == "Sales"
    print("✓ Track switching works")

    # Check minimums
    assert manager.has_minimum_parallel(3) == True
    assert manager.has_minimum_parallel(4) == False
    print("✓ Parallel track checks work")


def test_momentum():
    """Test momentum tracking."""
    momentum = MomentumTracker(switch_cost_minutes=45)

    momentum.start_flow()
    assert momentum.current_momentum().minutes_in_flow >= 0
    print("✓ Momentum flow start works")

    momentum.interrupt()
    assert MomentumSignal.INTERRUPTION in momentum.detected_signals
    print("✓ Momentum interrupt detection works")

    recovery = momentum.recovery_time_minutes()
    assert recovery >= 0
    print(f"✓ Momentum recovery calculation works ({recovery}min)")


def test_thermal():
    """Test thermal management."""
    thermal = ThermalManager(thermal_threshold_minutes=90)

    thermal.start_focus("building")
    snapshot = thermal.current_temperature()
    assert snapshot.state in [ThermalState.COOL, ThermalState.WARM, ThermalState.HOT, ThermalState.CRITICAL]
    print(f"✓ Thermal state detection works (state: {snapshot.state.value})")

    thermal.log_throttle_signal("headache")
    assert "headache" in thermal.manual_throttle_signals
    print("✓ Thermal signal logging works")


def test_protocol():
    """Test daily protocol."""
    profile = NDProfile.from_preset("adhd_parallel")
    protocol = DailyProtocol(profile)

    phase = protocol.current_phase()
    assert phase in [ProtocolPhase.MORNING, ProtocolPhase.PEAK, ProtocolPhase.NIGHT, ProtocolPhase.WIND_DOWN]
    print(f"✓ Protocol phase detection works (current: {phase.value})")

    todos = protocol.todos_for_phase(phase)
    assert len(todos) > 0
    print(f"✓ Protocol todos loading works ({len(todos)} todos)")


def test_compound():
    """Test cross-session learning."""
    compound = CompoundEngine()

    session = compound.start_session()
    assert session is not None
    print("✓ Session creation works")

    session.add_breakthrough("Found pattern in energy cycles")
    session.add_success("Parallel tracks prevented thrash")
    session.add_failure("Ignored thermal signal until crash")

    assert len(session.breakthrough_moments) == 1
    print("✓ Session learning recording works")

    successes = compound.success_patterns()
    failures = compound.failure_patterns()
    assert "Parallel tracks prevented thrash" in successes
    assert "Ignored thermal signal until crash" in failures
    print("✓ Compound pattern analysis works")


def test_translation():
    """Test translation layer."""
    compressor = IntentCompressor(preferred_format="voice")

    compressor.record_vision("System where parallel tracks feed each other...")
    assert compressor.vision is not None
    print("✓ Vision recording works")

    structured = compressor.compress_to_structured()
    assert len(structured) > 0
    print(f"✓ Intent compression works ({len(structured)} steps)")

    expanded = compressor.expand_for_audience("technical")
    assert expanded != ""
    print("✓ Audience expansion works")


def test_hooks():
    """Test Claude Code hooks generation."""
    profile = NDProfile.from_preset("adhd_parallel")
    energy = EnergyMapper(profile)
    momentum = MomentumTracker(profile.switch_cost_minutes)
    compound = CompoundEngine()
    tracks = ParallelTrackManager()

    hooks_json = generate_hooks_json(profile, energy, momentum, compound, tracks)
    assert "UserPromptSubmit" in hooks_json
    assert "PreToolUse" in hooks_json
    assert "Stop" in hooks_json
    print("✓ Hook generation works")


def main():
    """Run all smoke tests."""
    print("\n=== nd-os Smoke Tests ===\n")

    tests = [
        ("Profile", test_profile),
        ("Energy Mapping", test_energy),
        ("Parallel Tracks", test_parallel_tracks),
        ("Momentum", test_momentum),
        ("Thermal Management", test_thermal),
        ("Daily Protocol", test_protocol),
        ("Cross-Session Learning", test_compound),
        ("Translation Layer", test_translation),
        ("Claude Code Hooks", test_hooks),
    ]

    passed = 0
    failed = 0

    for name, test in tests:
        try:
            print(f"\n{name}:")
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {name} failed: {e}")
            failed += 1

    print(f"\n=== Results ===")
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")

    if failed > 0:
        sys.exit(1)

    print("\n✓ All smoke tests passed!")


if __name__ == "__main__":
    main()
