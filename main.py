import os
import sys
from download_dropbox_files import download_files_from_dropbox
import blender_render  # Importing the new module

# Define paths
DROPBOX_FOLDER = "/simulations/Blender/input"
LOCAL_FOLDER = "./BlenderInputFiles"
LOG_FILE_PATH = "./download_log.txt"

def prepare_files():
    """Downloads .blend files from Dropbox and prepares them for rendering."""

    print("Starting file download process...")

    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    CLIENT_ID = os.getenv("APP_KEY")
    CLIENT_SECRET = os.getenv("APP_SECRET")

    if not all([REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET]):
        print("Error: Missing Dropbox credentials! Ensure secrets are set in GitHub Actions.")
        sys.exit(1)

    os.makedirs(LOCAL_FOLDER, exist_ok=True)

    download_files_from_dropbox(DROPBOX_FOLDER, LOCAL_FOLDER, REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET, LOG_FILE_PATH)

    print("Files downloaded successfully! Ready for Blender processing.")

if __name__ == "__main__":
    prepare_files()
    blender_render.run_blender_render()  # Calling rendering function



