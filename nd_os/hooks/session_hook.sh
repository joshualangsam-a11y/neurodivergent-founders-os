#!/bin/bash
# ND OS Session Hook for Claude Code
# Runs on UserPromptSubmit — adds energy + thermal context
# Output goes into system-reminder for the AI

python3 - << 'PYTHON'
import sys, os
sys.path.insert(0, os.path.expanduser("~/neurodivergent-founders-os"))

from nd_os.energy import EnergyMapper
from nd_os.thermal import ThermalManager
from nd_os.momentum import MomentumTracker
from nd_os.profile import NDProfile

try:
    profile = NDProfile.from_preset("adhd_parallel")
    energy = EnergyMapper(profile)
    thermal = ThermalManager(profile)

    snapshot = energy.current_state()
    phase = snapshot.state.value if hasattr(snapshot.state, 'value') else str(snapshot.state)

    # Only output if it's actionable
    parts = []
    if phase in ("mud", "MUD"):
        parts.append("MUD hours — light tasks only, save deep work for peak.")
    elif phase in ("peak", "PEAK"):
        parts.append("PEAK hours — protect this time for deep building.")

    if parts:
        print(" ".join(parts))
except Exception:
    pass  # Silent fail — never block the prompt
PYTHON
