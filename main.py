import os
import sys
from download_dropbox_files import download_files_from_dropbox

# Define paths
DROPBOX_FOLDER = "/simulations/Blender/input"  # Adjust as needed
LOCAL_FOLDER = "./BlenderInputFiles"
LOG_FILE_PATH = "./download_log.txt"

def prepare_files():
    """Downloads files from Dropbox and prepares them for Blender."""

    print("Starting file download process...")

    # Get Dropbox credentials from environment variables (GitHub Actions secrets)
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    CLIENT_ID = os.getenv("APP_KEY")
    CLIENT_SECRET = os.getenv("APP_SECRET")

    if not all([REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET]):
        print("Error: Missing Dropbox credentials! Ensure secrets are set in GitHub Actions.")
        sys.exit(1)

    # Ensure local folder exists
    os.makedirs(LOCAL_FOLDER, exist_ok=True)

    # Download files
    download_files_from_dropbox(DROPBOX_FOLDER, LOCAL_FOLDER, REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET, LOG_FILE_PATH)

    print("Files downloaded successfully! Ready for Blender processing.")

    # Placeholder for Blender processing logic
    # Example: os.system(f"blender -b {LOCAL_FOLDER}/your_blend_file.blend -P your_script.py")

if __name__ == "__main__":
    prepare_files()



