import bpy
import os
import json

# ✅ Define the directory for simulation data
data_dir = "./data/testing-input-output/"
json_file = os.path.join(data_dir, "fluid_dynamics_animation.json")

# ✅ Ensure `data/testing-input-output/` exists
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"✅ Created missing directory: {data_dir}")

# ✅ Verify `fluid_dynamics_animation.json` exists
if not os.path.exists(json_file):
    print("❌ ERROR: No `fluid_dynamics_animation.json` found!")
    exit(1)

# ✅ Load fluid dynamics simulation parameters
with open(json_file, "r") as file:
    simulation_data = json.load(file)

print("✅ Successfully loaded fluid dynamics simulation parameters!")

# ✅ Debugging: Print parsed simulation data
print(f"🔹 Simulation Parameters: {json.dumps(simulation_data, indent=2)}")

# ✅ Process simulation data (example workflow)
velocity_field = simulation_data.get("velocity_field", [])
gravity_enabled = simulation_data.get("gravity_enabled", False)

if not velocity_field:
    print("❌ ERROR: Missing velocity field data!")
    exit(1)

print(f"✅ Gravity Enabled: {gravity_enabled}")
print("✅ Setting up Blender fluid simulation environment...")

# ✅ Set Up Fluid Domain Before Applying Gravity
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
domain = bpy.context.object
domain.name = "FluidDomain"
domain.scale = (50, 10, 5)  # Expanded domain ensures horizontal movement
bpy.ops.object.transform_apply(scale=True)

# ✅ Ensure Gravity Settings Are Applied Based on JSON Input
bpy.context.scene.gravity = (0, 0, 0) if not gravity_enabled else (0, -9.81, 0)
domain.modifiers.new(name="FluidSim", type='FLUID')
domain.modifiers["FluidSim"].fluid_type = 'DOMAIN'
domain.modifiers["FluidSim"].domain_settings.domain_type = 'LIQUID'
domain.modifiers["FluidSim"].domain_settings.gravity = (0, 0, 0) if not gravity_enabled else (0, -9.81, 0)

# ✅ Move Water Source to the Left to Ensure Proper Inflow Direction
bpy.ops.mesh.primitive_plane_add(size=12, location=(-12, 0, 0))  # Water inflow from far left
water_source = bpy.context.object
water_source.name = "WaterSource"

# ✅ Apply Fluid Flow Modifier Based on JSON Input
water_source.modifiers.new(name="FluidFlow", type='FLUID')
water_source.modifiers["FluidFlow"].fluid_type = 'FLOW'
water_source.modifiers["FluidFlow"].flow_settings.flow_type = 'LIQUID'
water_source.modifiers["FluidFlow"].flow_settings.flow_behavior = 'INFLOW'

# ✅ Enable Initial Velocity for Inflow
water_source.modifiers["FluidFlow"].flow_settings.use_initial_velocity = True
water_source.modifiers["FluidFlow"].flow_settings.velocity_factor = simulation_data.get("initial_velocity", 15.0)

print("✅ Gravity adjusted based on JSON data, water source created, velocity applied!")

# ✅ Save the Updated `.blend` File (If Required)
blend_output_path = os.path.join(data_dir, "simulation_output.blend")

print(f"🔹 Attempting to save updated simulation scene to: {blend_output_path}")
bpy.ops.wm.save_mainfile(filepath=blend_output_path)

if os.path.exists(blend_output_path):
    print(f"✅ Fluid simulation setup complete! Scene saved as '{blend_output_path}'.")
else:
    print("❌ ERROR: Failed to save the simulation scene!")
    exit(1)
