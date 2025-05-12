import bpy
import sys
import os

# **Step 1: Define the Directory Containing `.obj` Files**
obj_dir = "./testing-input-output/"

# **Step 2: Find Any `.obj` File in the Directory**
obj_files = [f for f in os.listdir(obj_dir) if f.endswith(".obj")]

if not obj_files:
    print("❌ Error: No `.obj` file found in directory!")
    sys.exit(1)

# Take the first `.obj` file found
obj_path = os.path.abspath(os.path.join(obj_dir, obj_files[0]))

# Debugging: Print the detected file for verification
print(f"🔹 Automatically detected .obj file: {obj_path}")

# **Step 3: Enable the OBJ Import Add-on**
bpy.ops.preferences.addon_enable(module="io_scene_obj")

# **Step 4: Import the `.obj` File**
bpy.ops.import_scene.obj(filepath=obj_path)

# Center the object in the scene
obj = bpy.context.selected_objects[0]
obj.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

# **Step 5: Create Fluid Domain**
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
domain = bpy.context.object
domain.name = "FluidDomain"
domain.scale = (3, 3, 3)  # Resize to surround the imported object
bpy.ops.object.transform_apply(scale=True)

# Enable Fluid Simulation
domain.modifiers.new(name="FluidSim", type='FLUID')
domain.modifiers["FluidSim"].fluid_type = 'DOMAIN'
domain.modifiers["FluidSim"].domain_settings.domain_type = 'LIQUID'
domain.modifiers["FluidSim"].domain_settings.resolution_max = 64  # Higher values for detail

# **Step 6: Set Imported Object as an Obstacle**
obj.modifiers.new(name="FluidEffector", type='FLUID')
obj.modifiers["FluidEffector"].fluid_type = 'EFFECTOR'
obj.modifiers["FluidEffector"].effector_settings.surface_sampling = 'NONE'
obj.modifiers["FluidEffector"].effector_settings.use_plane_init = True

# **Step 7: Add Water Source**
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 2))
water_source = bpy.context.object
water_source.name = "WaterSource"

# Enable fluid and set it as an inflow
water_source.modifiers.new(name="FluidFlow", type='FLUID')
water_source.modifiers["FluidFlow"].fluid_type = 'FLOW'
water_source.modifiers["FluidFlow"].flow_settings.flow_type = 'LIQUID'
water_source.modifiers["FluidFlow"].flow_settings.flow_behavior = 'INFLOW'
water_source.modifiers["FluidFlow"].flow_settings.inflow_velocity = (0, 0, -1)  # Water flowing downward

# **Step 8: Ensure the Output Directory Exists**
blend_output_path = os.path.join(obj_dir, "simulation.blend")
os.makedirs(obj_dir, exist_ok=True)  # Ensure the directory exists

# **Step 9: Save Scene as `.blend`**
bpy.ops.wm.save_mainfile(filepath=blend_output_path)

print(f"✅ Fluid simulation setup complete! Scene saved as '{blend_output_path}' using '{obj_path}'.")



