import bpy
import sys
import os

# **Step 1: Parse Command-Line Arguments Correctly**
args = sys.argv
if "--" in args:
    obj_index = args.index("--") + 1  # Gets argument after `--`
else:
    obj_index = 1  # Default to first argument

if len(args) <= obj_index:
    print("❌ Error: No .obj file path provided!")
    sys.exit(1)

# **Step 2: Convert Relative Path to Absolute Path**
obj_path = os.path.abspath(args[obj_index])

# Debugging: Print the full path for verification
print(f"🔹 Loading .obj file from: {obj_path}")

# **Step 3: Check if the .obj File Exists**
if not os.path.exists(obj_path):
    print(f"❌ Error: .obj file '{obj_path}' not found!")
    sys.exit(1)

# **Step 4: Enable the OBJ Import Add-on**
bpy.ops.preferences.addon_enable(module="io_scene_obj")

# **Step 5: Import the `.obj` File**
bpy.ops.import_scene.obj(filepath=obj_path)

# Center the disk in the scene
disk = bpy.context.selected_objects[0]
disk.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

# **Step 6: Create Fluid Domain**
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
domain = bpy.context.object
domain.name = "FluidDomain"
domain.scale = (3, 3, 3)  # Resize to surround the disk
bpy.ops.object.transform_apply(scale=True)

# Enable Fluid Simulation
domain.modifiers.new(name="FluidSim", type='FLUID')
domain.modifiers["FluidSim"].fluid_type = 'DOMAIN'
domain.modifiers["FluidSim"].domain_settings.domain_type = 'LIQUID'
domain.modifiers["FluidSim"].domain_settings.resolution_max = 64  # Higher values for detail

# **Step 7: Set Disk as an Obstacle**
disk.modifiers.new(name="FluidEffector", type='FLUID')
disk.modifiers["FluidEffector"].fluid_type = 'EFFECTOR'
disk.modifiers["FluidEffector"].effector_settings.surface_sampling = 'NONE'
disk.modifiers["FluidEffector"].effector_settings.use_plane_init = True

# **Step 8: Add Water Source**
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 2))
water_source = bpy.context.object
water_source.name = "WaterSource"

# Enable fluid and set it as an inflow
water_source.modifiers.new(name="FluidFlow", type='FLUID')
water_source.modifiers["FluidFlow"].fluid_type = 'FLOW'
water_source.modifiers["FluidFlow"].flow_settings.flow_type = 'LIQUID'
water_source.modifiers["FluidFlow"].flow_settings.flow_behavior = 'INFLOW'
water_source.modifiers["FluidFlow"].flow_settings.inflow_velocity = (0, 0, -1)  # Water flowing downward

# **Step 9: Save Scene as `.blend`**
blend_output_path = "./BlenderInputFiles/simulation.blend"
bpy.ops.wm.save_mainfile(filepath=blend_output_path)

print(f"✅ Fluid simulation setup complete! Scene saved as '{blend_output_path}' using {obj_path}.")


