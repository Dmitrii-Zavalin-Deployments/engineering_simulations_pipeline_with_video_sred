import bpy
import sys
import os
import json

# **Step 1: Define the Directory Containing `.blend` Files**
blend_dir = "./testing-input-output/"

# **Step 2: Find Any `.blend` File in the Directory**
blend_files = [f for f in os.listdir(blend_dir) if f.endswith(".blend")]

if not blend_files:
    print("❌ Error: No `.blend` file found in directory!")
    sys.exit(1)

# Take the first `.blend` file found
blend_file = os.path.abspath(os.path.join(blend_dir, blend_files[0]))

# Debugging: Print the detected file for verification
print(f"🔹 Automatically detected .blend file: {blend_file}")

# **Step 3: Open the `.blend` File**
bpy.ops.wm.open_mainfile(filepath=blend_file)
print(f"✅ Successfully loaded '{blend_file}' into Blender!")

# ✅ Set Up Fluid Domain Before Applying Gravity
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
domain = bpy.context.object
domain.name = "FluidDomain"
domain.scale = (50, 10, 5)  # Expanded domain ensures horizontal movement
bpy.ops.object.transform_apply(scale=True)

# ✅ Ensure Gravity Is Fully Disabled
bpy.context.scene.gravity = (0, 0, 0)  # Disables global gravity
domain.modifiers.new(name="FluidSim", type='FLUID')
domain.modifiers["FluidSim"].fluid_type = 'DOMAIN'
domain.modifiers["FluidSim"].domain_settings.domain_type = 'LIQUID'
domain.modifiers["FluidSim"].domain_settings.gravity = (0, 0, 0)  # Disables Mantaflow gravity

# ✅ Apply Stronger Inflow Velocity
water_source.modifiers["FluidFlow"].flow_settings.inflow_velocity = (15, 0, 0)  # Force left-to-right flow

print("✅ Gravity removed, velocity applied!")

# **Step 8: Save `.blend` File**
blend_output_path = os.path.join(blend_dir, "simulation_output.blend")
bpy.ops.wm.save_mainfile(filepath=blend_output_path)
