# src/debug_paraview_env.py

import paraview.simple as ps
import sys
import os

print("--- ParaView Environment Debug Info ---")
try:
    print(f"ParaView version (if available): {ps.ParaViewVersion()}")
except AttributeError:
    print("ParaViewVersion() not found.")
print(f"paraview.simple module path: {ps.__file__}")

print("\n--- Attributes in paraview.simple ---")
for attr in sorted(dir(ps)):
    if not attr.startswith('__'): # Filter out internal attributes
        print(attr)
print("------------------------------------")
print("Debugging ParaView environment complete.")
