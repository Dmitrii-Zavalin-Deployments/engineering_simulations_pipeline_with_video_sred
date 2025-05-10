import os
import sys
from download_dropbox_files import download_files_from_dropbox
import blender_render  # Importing Blender rendering module
import upload_to_dropbox  # Importing the Dropbox upload module

# Define paths
DROPBOX_INPUT_FOLDER = "/simulations/Blender/input"
DROPBOX_OUTPUT_FOLDER = "/simulations/Blender/output"
LOCAL_INPUT_FOLDER = "./BlenderInputFiles"
LOCAL_OUTPUT_FOLDER = "./RenderedOutput"
LOG_FILE_PATH = "./download_log.txt"

def prepare_files():
    """Downloads .blend files from Dropbox and prepares them for rendering."""

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

if __name__ == "__main__":
    prepare_files()
    
    # Run Blender rendering
    blender_render.run_blender_render()

    print("📤 Uploading rendered results to Dropbox...")
    
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    CLIENT_ID = os.getenv("APP_KEY")
    CLIENT_SECRET = os.getenv("APP_SECRET")
    
    upload_to_dropbox.upload_files_to_dropbox(LOCAL_OUTPUT_FOLDER, DROPBOX_OUTPUT_FOLDER, REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)

    print("✅ All rendered images have been uploaded to Dropbox!")



