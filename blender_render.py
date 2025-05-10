import os

# Define paths
LOCAL_FOLDER = "./BlenderInputFiles"
OUTPUT_FOLDER = "./RenderedOutput"

def run_blender_render():
    """Executes Blender rendering in CLI mode."""

    print("Starting Blender rendering process...")

    # Ensure output folder exists
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Find .blend files
    blend_files = [f for f in os.listdir(LOCAL_FOLDER) if f.endswith(".blend")]

    if not blend_files:
        print("⚠️ Warning: No .blend files found for rendering! Skipping Blender execution.")
        return  # Gracefully exit without stopping the entire script

    # Select first .blend file (or loop for multiple files)
    blend_file = os.path.join(LOCAL_FOLDER, blend_files[0])

    # Run Blender rendering command with explicit output format
    render_command = f"blender -b {blend_file} -o {OUTPUT_FOLDER}/rendered_frame_#### -F PNG -a"
    os.system(render_command)

    print(f"✅ Blender rendering completed! Check output in {OUTPUT_FOLDER}")

if __name__ == "__main__":
    run_blender_render()



