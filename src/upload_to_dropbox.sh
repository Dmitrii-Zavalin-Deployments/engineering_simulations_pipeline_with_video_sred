#!/bin/bash

APP_KEY="${APP_KEY}"
APP_SECRET="${APP_SECRET}"
REFRESH_TOKEN="${REFRESH_TOKEN}"
DROPBOX_UPLOAD_FOLDER="/engineering_simulations_pipeline"

LOCAL_OUTPUT_DIR="$GITHUB_WORKSPACE/data/testing-input-output"

echo "🔄 Attempting to upload files from ${LOCAL_OUTPUT_DIR} to Dropbox folder ${DROPBOX_UPLOAD_FOLDER}..."

# Ensure the directory exists
if [ ! -d "$LOCAL_OUTPUT_DIR" ]; then
    echo "❌ ERROR: Directory $LOCAL_OUTPUT_DIR does not exist."
    exit 1
fi

# Loop through all files in the directory
for file in "$LOCAL_OUTPUT_DIR"/*; do
    if [ -f "$file" ]; then
        echo "📤 Uploading $file..."
        python3 src/upload_to_dropbox.py \
            "$file" \
            "$DROPBOX_UPLOAD_FOLDER" \
            "$REFRESH_TOKEN" \
            "$APP_KEY" \
            "$APP_SECRET"

        if [ $? -eq 0 ]; then
            echo "✅ Successfully uploaded $file to Dropbox."
        else
            echo "❌ ERROR: Failed to upload $file to Dropbox."
            exit 1
        fi
    fi
done

echo "🎉 All files uploaded successfully!"



