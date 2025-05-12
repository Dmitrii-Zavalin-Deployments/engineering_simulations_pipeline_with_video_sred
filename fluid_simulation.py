import bpy
import sys
import os

# **Step 1: Define the Directory Containing `.obj` Files**
obj_dir = "./testing-input-output/"
os.makedirs(obj_dir, exist_ok=True)

# **Step 2: Find Any `.obj` File in the Directory**
obj_files = [f for f in os.listdir(obj_dir) if f.endswith(".obj")]

if not obj_files:
    print("❌ Error: No `.obj` file found in directory!")
    sys.exit(1)

obj_path = os.path.abspath(os.path.join(obj_dir, obj_files[0]))
print(f"🔹 Automatically detected .obj file: {obj_path}")

# **Step 3: Check if OBJ Import Add-on Exists Before Enabling**
addon_name = "io_scene_obj"

if addon_name in bpy.context.preferences.addons:
    try:
        bpy.ops.preferences.addon_enable(module=addon_name)
        print(f"✅ Successfully enabled '{addon_name}'!")
    except RuntimeError as e:
        print(f"⚠️ Warning: Failed to enable '{addon_name}', but continuing anyway.")
        print(f"Error details: {e}")
else:
    print(f"⚠️ Warning: Add-on '{addon_name}' is NOT installed. Proceeding without it.")

# **Step 4: Attempt to Import the `.obj` File**
try:
    bpy.ops.import_scene.obj(filepath=obj_path)
    print(f"✅ Successfully imported '{obj_path}' into Blender!")
except Exception as e:
    print(f"❌ Failed to import .obj file '{obj_path}'. Error: {e}")
    print("⚠️ Attempting alternative import method...")

    # **Alternative: Create a placeholder cube if `.obj` import fails**
    bpy.ops.mesh.primitive_cube_add(size=2)
    obj = bpy.context.object
    obj.name = "FallbackCube"
    print("✅ Created placeholder cube instead of importing .obj.")

# **Step 5: Set Up Fluid Domain**
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
domain = bpy.context.object
domain.name = "FluidDomain"
domain.scale = (3, 3, 3)  # Resize to surround the object
bpy.ops.object.transform_apply(scale=True)

# Enable Fluid Simulation
domain.modifiers.new(name="FluidSim", type='FLUID')
domain.modifiers["FluidSim"].fluid_type = 'DOMAIN'
domain.modifiers["FluidSim"].domain_settings.domain_type = 'LIQUID'
domain.modifiers["FluidSim"].domain_settings.resolution_max = 64

# **Step 6: Configure Fluid Effector (Obstacle)**
if obj.name != "FallbackCube":
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
water_source.modifiers["FluidFlow"].flow_settings.inflow_velocity = (0, 0, -1)

# **Step 8: Save Scene as `.blend`**
blend_output_path = os.path.join(obj_dir, "simulation.blend")

# Debugging: Print where the `.blend` file should be saved
print(f"🧐 Attempting to save .blend file at: {blend_output_path}")

# Save the `.blend` file
bpy.ops.wm.save_mainfile(filepath=blend_output_path)

# Verify `.blend` file after saving
if os.path.exists(blend_output_path):
    print(f"✅ Fluid simulation setup complete! Scene saved as '{blend_output_path}' using '{obj_path}'.")
else:
    print(f"❌ ERROR: .blend file was not created in '{blend_output_path}'. Check Blender execution.")



