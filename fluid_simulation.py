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

# ✅ Ensure Gravity Is Fully Disabled in Scene & Fluid Domain Settings
bpy.context.scene.gravity = (0, 0, 0)  # Completely disables gravity
domain.modifiers["FluidSim"].domain_settings.gravity = (0, 0, 0)  # Disables Mantaflow gravity effects

# **Step 4: Load Velocity Data from JSON File**
velocity_file_path = os.path.join(blend_dir, "velocity_data.json")
if os.path.exists(velocity_file_path):
    with open(velocity_file_path, "r") as file:
        velocity_data = json.load(file)
        print("✅ Loaded velocity data from JSON file.")
else:
    print("❌ ERROR: Velocity data file not found!")
    sys.exit(1)

# **Step 5: Apply Velocity Values at Each Fluid Particle Position**
for entry in velocity_data["fluid_velocity"]:
    position = (entry["x"], entry["y"], entry["z"])
    velocity = (entry["vx"], entry["vy"], entry["vz"])
    
    # ✅ Directly set velocity values (instead of force fields)
    water_source = bpy.context.object
    water_source.modifiers["FluidFlow"].flow_settings.inflow_velocity = (velocity[0], velocity[1], velocity[2])

print("✅ Velocity fields applied successfully!")

# **Step 6: Find the First Mesh Object in the Scene**
objs = [obj for obj in bpy.data.objects if obj.type == 'MESH']

if not objs:
    print("❌ No mesh objects found in the `.blend` file! Creating a placeholder cube...")
    bpy.ops.mesh.primitive_cube_add(size=2)
    obj = bpy.context.object
    obj.name = "FallbackCube"
    print("✅ Created placeholder cube.")
else:
    obj = objs[0]  # Use the first mesh object found

# ✅ Rotate the Disk to Align Horizontally
obj.rotation_euler = (0, 1.5708, 0)  # 90-degree rotation, making disk perpendicular to X-axis

# ✅ Set Up Fluid Domain
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
domain = bpy.context.object
domain.name = "FluidDomain"
domain.scale = (50, 10, 5)  # Expanded domain prevents vertical movement
bpy.ops.object.transform_apply(scale=True)

# Enable Fluid Simulation
domain.modifiers.new(name="FluidSim", type='FLUID')
domain.modifiers["FluidSim"].fluid_type = 'DOMAIN'
domain.modifiers["FluidSim"].domain_settings.domain_type = 'LIQUID'
domain.modifiers["FluidSim"].domain_settings.resolution_max = 128  # Improved fluid resolution

# ✅ Configure Fluid Effector (Obstacle - Disk)
if "FluidEffector" not in obj.modifiers:
    effector = obj.modifiers.new(name="FluidEffector", type='FLUID')
    effector.fluid_type = 'EFFECTOR'
    effector.effector_settings.use_plane_init = True
    effector.effector_settings.surface_distance = 0.01  # Helps water wrap around the disk properly
    print("✅ Added FluidEffector modifier to the object.")
else:
    obj.modifiers["FluidEffector"].fluid_type = 'EFFECTOR'
    obj.modifiers["FluidEffector"].effector_settings.use_plane_init = True
    print("⚠️ FluidEffector modifier already present on object.")

# ✅ Move Water Source to the Left to Ensure Proper Inflow Direction
bpy.ops.mesh.primitive_plane_add(size=12, location=(-12, 0, 0))  # Water inflow from far left
water_source = bpy.context.object
water_source.name = "WaterSource"

# ✅ Adjust Inflow Velocity to Ensure Left-to-Right Flow
water_source.modifiers.new(name="FluidFlow", type='FLUID')
water_source.modifiers["FluidFlow"].fluid_type = 'FLOW'
water_source.modifiers["FluidFlow"].flow_settings.flow_type = 'LIQUID'
water_source.modifiers["FluidFlow"].flow_settings.flow_behavior = 'INFLOW'
water_source.modifiers["FluidFlow"].flow_settings.inflow_velocity = (15, 0, 0)  # Stronger horizontal flow

# ✅ Verify Fluid Domain Orientation to Prevent Vertical Movement
domain.rotation_euler = (0, 0, 0)  # Reset rotation

# ✅ Correct Animation Playback Direction
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 250
bpy.context.scene.render.fps = 30  # Ensure proper animation frame rate
bpy.context.scene.frame_current = 1  # Reset start position to prevent reversal

# **Step 8: Save Scene as `.blend`**
blend_output_path = os.path.join(blend_dir, "simulation_output.blend")

# Debugging: Print where the `.blend` file should be saved
print(f"🧐 Attempting to save .blend file at: {blend_output_path}")

# Save the `.blend` file
bpy.ops.wm.save_mainfile(filepath=blend_output_path)

# Verify `.blend` file after saving
if os.path.exists(blend_output_path):
    print(f"✅ Fluid simulation setup complete! Scene saved as '{blend_output_path}'.")
else:
    print(f"❌ ERROR: `.blend` file was not created in '{blend_output_path}'. Check Blender execution.")
