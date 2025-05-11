import os

# Define paths
LOCAL_FOLDER = "./BlenderInputFiles"
OUTPUT_FOLDER = "./RenderedOutput"
VIDEO_FILE = "./RenderedOutput/video.mp4"

def run_blender_render():
    """Executes Blender rendering in CLI mode with optimized settings, then creates a video."""
    
    print("🔄 Starting rendering process with enhanced settings...")

    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Find .blend files
    blend_files = [f for f in os.listdir(LOCAL_FOLDER) if f.endswith(".blend")]

    if not blend_files:
        print("⚠️ No .blend files found! Skipping rendering.")
        return  # Gracefully exit

    # Select first .blend file
    blend_file = os.path.join(LOCAL_FOLDER, blend_files[0])

    # Run Blender command ensuring correct object selection and optimizations
    render_command = f"""blender -b {blend_file} --python-expr "
import bpy

# Load the .blend file
bpy.ops.wm.open_mainfile(filepath='{blend_file}')

# Find the imported model 'MyImportedModel'
obj = bpy.data.objects.get('MyImportedModel')

if obj:
    # Apply correct scale
    obj.scale *= 1.5  # Increase size if necessary
    obj.rotation_euler.z += 3.14 / 4  # Rotate smoothly

    # Improve lighting conditions
    if not bpy.data.objects.get('AutoSunLight'):
        light_data = bpy.data.lights.new(name='AutoSunLight', type='SUN')
        light_object = bpy.data.objects.new(name='AutoSunLight', object_data=light_data)
        bpy.context.collection.objects.link(light_object)
        light_object.location = (5, -5, 5)  # Adjust light position

    # Enhance render settings for better quality
    bpy.context.scene.cycles.samples = 128  # Increase samples for clearer results

    # Render frames
    for frame in range(1, 31):  # Render 30 frames for smoother animation
        bpy.context.scene.frame_set(frame)
        bpy.context.scene.render.filepath = '{OUTPUT_FOLDER}/frame_' + str(frame).zfill(4)
        bpy.ops.render.render(write_still=True)

else:
    print('❌ Object "MyImportedModel" not found! Skipping rendering.')
" """

    os.system(render_command)

    print(f"✅ Rendering process completed! Check frames in {OUTPUT_FOLDER}")

    # Create a video from frames using FFmpeg
    ffmpeg_command = f"ffmpeg -framerate 24 -i {OUTPUT_FOLDER}/frame_%04d.png -c:v libx264 -pix_fmt yuv420p {VIDEO_FILE}"
    os.system(ffmpeg_command)

    print(f"🎥 Video creation completed! Check the final animation at {VIDEO_FILE}")

if __name__ == "__main__":
    run_blender_render()



