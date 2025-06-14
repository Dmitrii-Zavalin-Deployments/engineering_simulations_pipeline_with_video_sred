#!/bin/bash

# Dropbox credentials from GitHub Secrets
APP_KEY="${APP_KEY}"
APP_SECRET="${APP_SECRET}"
REFRESH_TOKEN="${REFRESH_TOKEN}"
DROPBOX_BASE_FOLDER="/engineering_simulations_pipeline"

# Output base folder
LOCAL_OUTPUT_DIR="$GITHUB_WORKSPACE/data/testing-input-output"

echo "🔄 Scanning for render output folders in: $LOCAL_OUTPUT_DIR"

# Ensure local directory exists
if [ ! -d "$LOCAL_OUTPUT_DIR" ]; then
    echo "❌ ERROR: Output directory not found: $LOCAL_OUTPUT_DIR"
    exit 1
fi

# Find all layer frame folders matching *_frames/
layer_dirs=$(find "$LOCAL_OUTPUT_DIR" -mindepth 1 -maxdepth 1 -type d -name '*_frames')

if [ -z "$layer_dirs" ]; then
    echo "⚠️ No *_frames directories found in $LOCAL_OUTPUT_DIR. Nothing to upload."
    exit 0
fi

# Iterate over each layer directory and upload all its files
for layer_path in $layer_dirs; do
    echo ""
    echo "📁 Found frame layer: $layer_path"

    find "$layer_path" -type f -print0 | while IFS= read -r -d $'\0' local_file; do
        relative_path="${local_file#$LOCAL_OUTPUT_DIR/}"
        dropbox_path="${DROPBOX_BASE_FOLDER}/${relative_path}"

        echo "📤 Uploading: $local_file → $dropbox_path"

        python3 src/upload_to_dropbox.py \
            "$local_file" \
            "$dropbox_path" \
            "$REFRESH_TOKEN" \
            "$APP_KEY" \
            "$APP_SECRET"

        if [ $? -eq 0 ]; then
            echo "✅ Upload successful"
        else
            echo "❌ ERROR during upload of $local_file"
            exit 1
        fi
    done
done

echo ""
echo "🎉 All render layer frames uploaded successfully to Dropbox!"



