"""The four site trial briefs, each with the brand color its site trial was
built with, and the middle of the axes, shared by the tests that use them."""
from engine.synthesizer.axes import AXIS_NAMES

TRIALS = {"clinic": "#2563EB", "devtool": "#6D28D9", "restaurant": "#E85D04",
          "fintech-ar": "#0F766E"}
MID = dict(zip(AXIS_NAMES, [0.5] * len(AXIS_NAMES)))
