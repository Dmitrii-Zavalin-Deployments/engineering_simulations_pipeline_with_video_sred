import os
import sys
import blender_render  # Importing Blender rendering module

# Define paths
DROPBOX_INPUT_FOLDER = "/simulations/Blender/input"
LOCAL_INPUT_FOLDER = "./testing-input-output"  # Now using local simulation output
LOCAL_OUTPUT_FOLDER = "./RenderedOutput"
LOG_FILE_PATH = "./download_log.txt"

def prepare_files():
    """Prepares `.blend` file for rendering and returns its path."""

    print("🔄 Preparing simulation output file...")

    blend_file = os.path.join(LOCAL_INPUT_FOLDER, "simulation_output.blend")

    if not os.path.exists(blend_file):
        print("❌ Error: `simulation_output.blend` not found in `testing-input-output/`!")
        sys.exit(1)

    print(f"✅ Found simulation output file: {blend_file}. Ready for Blender rendering.")
    
    # 🔹 Commented out Dropbox download for now, but kept intact
    """
    print("🔄 Starting file download process...")

    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    CLIENT_ID = os.getenv("APP_KEY")
    CLIENT_SECRET = os.getenv("APP_SECRET")

    if not all([REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET]):
        print("❌ Error: Missing Dropbox credentials! Ensure secrets are set in GitHub Actions.")
        sys.exit(1)

    os.makedirs(LOCAL_INPUT_FOLDER, exist_ok=True)

    download_files_from_dropbox(DROPBOX_INPUT_FOLDER, LOCAL_INPUT_FOLDER, REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET, LOG_FILE_PATH)

    print("✅ Files downloaded successfully! Ready for Blender processing.")
    """

    return blend_file  # ✅ Return blend file path

if __name__ == "__main__":
    blend_file = prepare_files()  # ✅ Capture returned blend file path
    
    # Run Blender rendering with local `.blend` file
    blender_render.run_blender_render(blend_file)

    print("✅ Rendering process completed! Frames saved in RenderedOutput.")
    print("📽️ Next step: Convert frames to a video in GitHub Actions.")
