import bpy
import sys
import os

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

# **Step 4: Find the First Mesh Object in the Scene**
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
domain.scale = (20, 10, 5)  # Larger domain supports full river flow past the disk
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

# ✅ Convert Water Source to a Wide Plane for River Flow
bpy.ops.mesh.primitive_plane_add(size=12, location=(-8, 0, 0))  # Large inflow source placed at the left
water_source = bpy.context.object
water_source.name = "WaterSource"

# ✅ Adjust Inflow Direction to Move Left to Right (River Flow)
water_source.modifiers.new(name="FluidFlow", type='FLUID')
water_source.modifiers["FluidFlow"].fluid_type = 'FLOW'
water_source.modifiers["FluidFlow"].flow_settings.flow_type = 'LIQUID'
water_source.modifiers["FluidFlow"].flow_settings.flow_behavior = 'INFLOW'

if hasattr(water_source.modifiers["FluidFlow"].flow_settings, "inflow_velocity"):
    water_source.modifiers["FluidFlow"].flow_settings.inflow_velocity = (4, 0, 0)  # Continuous movement along X-axis
    print("✅ Applied correct inflow velocity settings.")
else:
    print("⚠️ WARNING: `inflow_velocity` attribute not found on FluidFlow settings. Skipping velocity setup.")

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
