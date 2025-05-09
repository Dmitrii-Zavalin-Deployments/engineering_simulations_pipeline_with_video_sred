# Blender Animation Automation  

## Overview  
This repository contains an automated workflow for creating **high-quality animations in Blender**, optimized for **fluid simulations, motion rendering, and other visualization tasks using GitHub Actions**.  

## Features  
- **Automated Rendering** → Uses Blender CLI to process animations remotely.  
- **Cloud-Based Processing** → Offloads high-resolution rendering to GitHub-hosted virtual machines.  
- **File Management with Dropbox** → Fetches input Blender files and stores rendered output in Dropbox.  

## Workflow Summary  
1. **Upload input Blender files** to Dropbox (`/simulations/Blender/input/`).  
2. **Trigger GitHub Actions** to render animations using Blender.  
3. **Retrieve rendered video files** from Dropbox (`/simulations/Blender/output/`).  

## Usage  
To generate an animation:  
1. Prepare the Blender scene and save it in Dropbox.  
2. Trigger the GitHub Actions workflow for cloud rendering.  
3. Download and use the final rendered animation from Dropbox.  



