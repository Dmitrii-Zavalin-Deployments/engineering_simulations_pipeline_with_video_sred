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

# **Step 3: Enable the OBJ Import Add-on**
addon_name = "io_scene_obj"
try:
    bpy.ops.preferences.addon_enable(module=addon_name)
    print(f"✅ Successfully enabled '{addon_name}'!")
except Exception as e:
    print(f"⚠️ Warning: Unable to enable '{addon_name}'. It may not be pre-installed.")
    print(f"Error details: {e}")
    sys.exit(1)  # Exit to prevent continuing without OBJ support

# **Step 4: Import the `.obj` File**
try:
    bpy.ops.import_scene.obj(filepath=obj_path)
    print(f"✅ Successfully imported '{obj_path}' into Blender!")
except Exception as e:
    print(f"❌ Failed to import .obj file '{obj_path}'. Error: {e}")
    sys.exit(1)

# Continue with fluid simulation setup...



