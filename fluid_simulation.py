import bpy
import sys

# **Step 1: Get the .obj file path from command-line arguments**
if len(sys.argv) < 2:
    print("❌ Error: No .obj file path provided!")
    sys.exit(1)

obj_path = sys.argv[1]

# **Step 2: Delete Default Objects**
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# **Step 3: Import the `.obj` Model**
bpy.ops.import_scene.obj(filepath=obj_path)

# Center the disk in the scene
disk = bpy.context.selected_objects[0]
disk.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

# **Step 4: Create Fluid Domain**
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

# **Step 5: Set Disk as an Obstacle**
disk.modifiers.new(name="FluidEffector", type='FLUID')
disk.modifiers["FluidEffector"].fluid_type = 'EFFECTOR'
disk.modifiers["FluidEffector"].effector_settings.surface_sampling = 'NONE'
disk.modifiers["FluidEffector"].effector_settings.use_plane_init = True

# **Step 6: Add Water Source**
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 2))
water_source = bpy.context.object
water_source.name = "WaterSource"

# Enable fluid and set it as an inflow
water_source.modifiers.new(name="FluidFlow", type='FLUID')
water_source.modifiers["FluidFlow"].fluid_type = 'FLOW'
water_source.modifiers["FluidFlow"].flow_settings.flow_type = 'LIQUID'
water_source.modifiers["FluidFlow"].flow_settings.flow_behavior = 'INFLOW'
water_source.modifiers["FluidFlow"].flow_settings.inflow_velocity = (0, 0, -1)  # Water flowing downward

# **Step 7: Save Scene as `.blend`**
bpy.ops.wm.save_mainfile(filepath="./BlenderInputFiles/simulation.blend")

print(f"✅ Fluid simulation setup complete! Scene saved as 'simulation.blend' using {obj_path}.")



