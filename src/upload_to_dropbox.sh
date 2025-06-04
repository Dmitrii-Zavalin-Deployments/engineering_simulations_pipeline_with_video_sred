#!/bin/bash

# Define environment variables from GitHub Actions secrets
APP_KEY="${APP_KEY}"
APP_SECRET="${APP_SECRET}"
REFRESH_TOKEN="${REFRESH_TOKEN}" # Corrected typo from REFREREF_TOKEN if it was there
DROPBOX_BASE_FOLDER="/engineering_simulations_pipeline" # The base folder in your Dropbox where everything will go

# Define the local directory where all generated output files and folders reside
LOCAL_OUTPUT_DIR="$GITHUB_WORKSPACE/data/testing-input-output"

echo "🔄 Attempting to upload files recursively from ${LOCAL_OUTPUT_DIR} to Dropbox folder ${DROPBOX_BASE_FOLDER}..."

# Ensure the local directory exists
if [ ! -d "$LOCAL_OUTPUT_DIR" ]; then
    echo "❌ ERROR: Local output directory '${LOCAL_OUTPUT_DIR}' does not exist. No files to upload."
    exit 1
fi

# Use 'find' to locate all regular files recursively within LOCAL_OUTPUT_DIR
# -type f: ensures only files are processed (not directories)
# -print0: prints results separated by a null character, which is robust for filenames with spaces or special characters
# while IFS= read -r -d $'\0' local_file_path: safely reads each null-separated filename into 'local_file_path'
find "$LOCAL_OUTPUT_DIR" -type f -print0 | while IFS= read -r -d $'\0' local_file_path; do
    # Calculate the path of the file relative to LOCAL_OUTPUT_DIR.
    # This is crucial for recreating the folder structure on Dropbox.
    # Example:
    # LOCAL_OUTPUT_DIR = /home/runner/work/repo/data/testing-input-output
    # local_file_path  = /home/runner/work/repo/data/testing-input-output/turbine_animation_frames/frame_0001.png
    # relative_path    = turbine_animation_frames/frame_0001.png
    relative_path="${local_file_path#$LOCAL_OUTPUT_DIR/}"

    # Construct the full destination path on Dropbox.
    # This will include the base folder and the relative path, preserving the folder structure.
    # Example: /engineering_simulations_pipeline/turbine_animation_frames/frame_0001.png
    dropbox_destination_path="${DROPBOX_BASE_FOLDER}/${relative_path}"

    echo "📤 Uploading ${local_file_path} to Dropbox at: ${dropbox_destination_path}..."

    # Call the Python script to perform the upload.
    # The Python script now expects the full Dropbox destination path as an argument.
    python3 src/upload_to_dropbox.py \
        "$local_file_path" \
        "$dropbox_destination_path" \
        "$REFRESH_TOKEN" \
        "$APP_KEY" \
        "$APP_SECRET"

    # Check the exit status of the Python script.
    if [ $? -eq 0 ]; then
        echo "✅ Successfully uploaded ${local_file_path}."
    else
        echo "❌ ERROR: Failed to upload ${local_file_path} to Dropbox. Aborting further uploads."
        exit 1 # Exit immediately if any single file upload fails
    fi
done




echo "🎉 All relevant files found and attempted to upload successfully!"
