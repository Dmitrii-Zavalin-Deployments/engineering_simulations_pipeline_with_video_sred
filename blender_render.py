import os

# Define paths
LOCAL_FOLDER = "./BlenderInputFiles"
OUTPUT_FOLDER = "./RenderedOutput"

def run_blender_render():
    """Executes Blender rendering in CLI mode with a simple rotation animation on the imported model."""

    print("Starting simple test animation rendering...")

    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Find .blend files
    blend_files = [f for f in os.listdir(LOCAL_FOLDER) if f.endswith(".blend")]

    if not blend_files:
        print("⚠️ Warning: No .blend files found for rendering! Skipping Blender execution.")
        return  # Gracefully exit without stopping the entire script

    # Select first .blend file
    blend_file = os.path.join(LOCAL_FOLDER, blend_files[0])

    # Run Blender command to find imported model and apply rotation
    render_command = f"""blender -b {blend_file} --python-expr "
import bpy
scene = bpy.context.scene

# Ensure the imported model is selected (exclude default cube)
valid_objects = [obj for obj in scene.objects if 'Cube' not in obj.name]  # Filters out default cube
obj = valid_objects[0] if valid_objects else None  # Pick first imported object

if obj:
    for frame in range(1, 11):  # Render 10 frames
        obj.rotation_euler.z = frame * (3.14 / 5)  # Rotate incrementally
        scene.frame_set(frame)
        scene.render.filepath = '{OUTPUT_FOLDER}/frame_' + str(frame).zfill(4)
        bpy.ops.render.render(write_still=True)
else:
    print('❌ No valid imported object found! Skipping rendering.')
" """
    
    os.system(render_command)

    print(f"✅ Simple rotating animation completed! Check frames in {OUTPUT_FOLDER}")

if __name__ == "__main__":
    run_blender_render()



