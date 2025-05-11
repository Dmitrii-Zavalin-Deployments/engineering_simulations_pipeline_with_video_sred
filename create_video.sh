#!/bin/bash

echo "📽️ Starting video creation with FFmpeg..."

# Ensure FFmpeg is installed
sudo apt update
sudo apt install -y ffmpeg

# Define paths
OUTPUT_FOLDER="./RenderedOutput"
VIDEO_FILE="./RenderedOutput/video.mp4"

# Create video from rendered frames
ffmpeg -framerate 24 -i ${OUTPUT_FOLDER}/frame_%04d.png -c:v libx264 -pix_fmt yuv420p ${VIDEO_FILE}

echo "✅ Video creation completed! Video saved at ${VIDEO_FILE}"



