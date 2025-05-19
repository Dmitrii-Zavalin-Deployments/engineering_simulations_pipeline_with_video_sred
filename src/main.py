import os
import sys
import blender_render  # Importing Blender rendering module

# Define paths
DROPBOX_INPUT_FOLDER = "/simulations/Blender/input"
LOCAL_INPUT_FOLDER = os.path.join(os.getcwd(), "data/testing-input-output")  # Ensures absolute path
LOCAL_OUTPUT_FOLDER = os.path.join(os.getcwd(), "RenderedOutput")
LOG_FILE_PATH = os.path.join(os.getcwd(), "download_log.txt")
JSON_FILE = os.path.join(LOCAL_INPUT_FOLDER, "fluid_dynamics_animation.json")

def prepare_files():
    """Prepares JSON file for rendering and returns simulation parameters."""

    print("🔄 Preparing fluid dynamics simulation input...")

    # ✅ Debugging: Print expected paths
    print(f"🔍 Expected simulation input directory: {LOCAL_INPUT_FOLDER}")
    print(f"🔍 Listing files in `{LOCAL_INPUT_FOLDER}`:")
    os.system(f"ls -lah {LOCAL_INPUT_FOLDER} || echo '⚠️ Directory not found, continuing...'")

    # ✅ Ensure the correct directory exists
    if not os.path.exists(LOCAL_INPUT_FOLDER):
        print(f"⚠️ Warning: `{LOCAL_INPUT_FOLDER}` does not exist. Creating directory...")
        os.makedirs(LOCAL_INPUT_FOLDER, exist_ok=True)

    # ✅ Verify the JSON file exists
    if not os.path.exists(JSON_FILE):
        print(f"❌ Error: `fluid_dynamics_animation.json` not found in `{LOCAL_INPUT_FOLDER}`!")
        sys.exit(1)

    print(f"✅ Found simulation input file: {JSON_FILE}. Ready for processing.")

    # ✅ Load fluid dynamics simulation parameters
    with open(JSON_FILE, "r") as file:
        simulation_data = file.read()

    print("✅ Fluid dynamics simulation data loaded successfully!")

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

    return simulation_data  # ✅ Return simulation data

if __name__ == "__main__":
    simulation_data = prepare_files()  # ✅ Capture simulation parameters
    
    # Run Blender rendering with JSON-based simulation input
    blender_render.run_blender_render(simulation_data)

    print("✅ Rendering process completed! Frames saved in RenderedOutput.")
    print("📽️ Next step: Convert frames to a video in GitHub Actions.")
