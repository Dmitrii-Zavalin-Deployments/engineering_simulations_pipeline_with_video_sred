import os

# Define paths
LOCAL_FOLDER = "./BlenderInputFiles"
OUTPUT_FOLDER = "./RenderedOutput"

def run_blender_render():
    """Executes Blender rendering in CLI mode, ensuring correct object selection."""

    print("🔄 Starting rendering process...")

    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Find .blend files
    blend_files = [f for f in os.listdir(LOCAL_FOLDER) if f.endswith(".blend")]

    if not blend_files:
        print("⚠️ Warning: No .blend files found for rendering! Skipping Blender execution.")
        return  # Gracefully exit without stopping the entire script

    # Select first .blend file
    blend_file = os.path.join(LOCAL_FOLDER, blend_files[0])

    # Run Blender command ensuring correct object selection
    render_command = f"""blender -b {blend_file} --python-expr "
import bpy

# Load the `.blend` file
bpy.ops.wm.open_mainfile(filepath='{blend_file}')

# Find the imported model 'MyImportedModel'
obj = bpy.data.objects.get('MyImportedModel')

if obj:
    for frame in range(1, 11):  # Render 10 frames
        obj.rotation_euler.z = frame * (3.14 / 5)  # Rotate incrementally
        bpy.context.scene.frame_set(frame)
        bpy.context.scene.render.filepath = '{OUTPUT_FOLDER}/frame_' + str(frame).zfill(4)
        bpy.ops.render.render(write_still=True)
else:
    print('❌ Object "MyImportedModel" not found! Skipping rendering.')
" """
    
    os.system(render_command)

    print(f"✅ Rendering process completed! Check frames in {OUTPUT_FOLDER}")

if __name__ == "__main__":
    run_blender_render()



