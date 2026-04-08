"""
nd-os: Operating system for neurodivergent founders.

Not how to cope. How to weaponize.
"""

from nd_os.profile import NDProfile, NDType, EnergyPattern
from nd_os.energy import EnergyMapper, EnergyState
from nd_os.momentum import MomentumTracker, MomentumSignal
from nd_os.parallel import ParallelTrackManager, Track, TrackStatus
from nd_os.thermal import ThermalManager, ThermalState
from nd_os.translation import IntentCompressor
from nd_os.compound import CompoundEngine, SessionLearning
from nd_os.protocol import DailyProtocol, ProtocolPhase

__version__ = "0.1.0"

__all__ = [
    "NDProfile",
    "NDType",
    "EnergyPattern",
    "EnergyMapper",
    "EnergyState",
    "MomentumTracker",
    "MomentumSignal",
    "ParallelTrackManager",
    "Track",
    "TrackStatus",
    "ThermalManager",
    "ThermalState",
    "IntentCompressor",
    "CompoundEngine",
    "SessionLearning",
    "DailyProtocol",
    "ProtocolPhase",
]
