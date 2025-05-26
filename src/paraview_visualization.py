# This script should be run with pvpython (ParaView's Python interpreter)
# e.g., /path/to/ParaView/bin/pvpython paraview_visualization.py --pvd-file /path/to/output/turbine_flow_animation.pvd --turbine-model /path/to/turbine_geometry.vtp

import paraview.simple as pv_s
import sys
import os

# --- Configuration (can be passed as command line arguments or hardcoded) ---
# Define the output directory for PNG frames. This will be relative to GITHUB_WORKSPACE/data/testing-input-output/
# If you want a different specific folder, change 'turbine_animation_frames'
OUTPUT_FRAMES_SUBDIR = "turbine_animation_frames" # This is the folder that will be committed with PNGs

PVD_FILE_PATH = None  # To be set by argument
TURBINE_MODEL_PATH = None # Path to your .stl, .obj, or .vtp turbine model

# Parse command line arguments if running from command line
if __name__ == "__main__":
    args = sys.argv
    # Find the base output path from the --output-video argument to determine frame storage location
    # We repurpose this argument to ensure the script has a full path context for output.
    base_output_path = None
    for i, arg in enumerate(args):
        if arg == "--pvd-file" and i + 1 < len(args):
            PVD_FILE_PATH = args[i+1]
        elif arg == "--turbine-model" and i + 1 < len(args):
            TURBINE_MODEL_PATH = args[i+1]
        elif arg == "--output-video" and i + 1 < len(args):
            base_output_path = args[i+1] # This will be the full path like data/testing-input-output/turbine_flow_animation.mp4

if not PVD_FILE_PATH or not TURBINE_MODEL_PATH or not base_output_path:
    print("Usage: pvpython paraview_visualization.py --pvd-file <path_to_pvd> --turbine-model <path_to_stl/obj/vtp> --output-video <base_output_video_path_to_derive_frame_dir>")
    sys.exit(1)

# Ensure paths are absolute or correctly relative to where pvpython is run
PVD_FILE_PATH = os.path.abspath(PVD_FILE_PATH)
TURBINE_MODEL_PATH = os.path.abspath(TURBINE_MODEL_PATH)

# Derive the actual full path for the PNG output directory
# For example, if base_output_path is /home/.../data/testing-input-output/turbine_flow_animation.mp4
# then the output dir for frames will be /home/.../data/testing-input-output/turbine_animation_frames/
actual_output_dir = os.path.join(os.path.dirname(base_output_path), OUTPUT_FRAMES_SUBDIR)
# --- FIX APPLIED HERE: Changed from %t to %04d ---
PARAVIEW_OUTPUT_PATTERN = os.path.join(actual_output_dir, "frame_%04d.png") # Use %04d for zero-padded numbers

# Ensure the directory exists for saving frames
if not os.path.exists(actual_output_dir):
    os.makedirs(actual_output_dir)
print(f"✅ Ensured output directory exists: {actual_output_dir}") # Added confirmation print

print(f"ParaView: PVD File: {PVD_FILE_PATH}")
print(f"ParaView: Turbine Model: {TURBINE_MODEL_PATH}")
print(f"ParaView: Output Image Sequence to: {actual_output_dir}")


# --- 1. Load Data ---
pv_s.ResetSession()
fluid_reader = pv_s.PVDReader(FileName=PVD_FILE_PATH)

# Load the turbine 3D model
if TURBINE_MODEL_PATH.lower().endswith('.obj'):
    turbine_reader = pv_s.WavefrontOBJReader(FileName=TURBINE_MODEL_PATH)
elif TURBINE_MODEL_PATH.lower().endswith('.vtp'):
    turbine_reader = pv_s.XMLPolyDataReader(FileName=TURBINE_MODEL_PATH)
elif TURBINE_MODEL_PATH.lower().endswith('.stl'):
    turbine_reader = pv_s.STLReader(FileName=TURBINE_MODEL_PATH)
else:
    print(f"Error: Unsupported turbine model format: {os.path.splitext(TURBINE_MODEL_PATH)[1]}. Supported: .obj, .vtp, .stl")
    sys.exit(1)

# --- 2. Create Visualization Pipeline for Fluid Data ---
render_view = pv_s.GetActiveViewOrCreate('RenderView')
pv_s.SetActiveView(render_view)

fluid_display = pv_s.Show(fluid_reader, render_view)
fluid_display.Representation = 'Volume'
fluid_display.Opacity = 0.3
fluid_display.LookupTable = pv_s.GetLookupTableForArray('Temperature', 1,
                                                      RGBPoints=[273.15, 0.0, 0.0, 1.0, # Blue for cold (0 C)
                                                                 323.15, 0.0, 1.0, 0.0, # Green for mid-range (50 C)
                                                                 373.15, 1.0, 0.0, 0.0], # Red for hot (100 C)
                                                      ColorSpace='RGB',
                                                      ScalarRangeInitialized=1.0)
fluid_display.ColorArrayName = ['POINTS', 'Temperature']
print("ParaView: Set up fluid volume display with Temperature colormap.")

bounds = fluid_reader.GetDataInformation().GetBounds()
print(f"ParaView: Fluid data bounds: {bounds}")

line_source = pv_s.Line(Point1=[bounds[0], bounds[2], bounds[4]],
                        Point2=[bounds[0], bounds[3], bounds[5]])
line_source.Resolution = 99

streamlines = pv_s.StreamTracerWithCustomSource(Input=fluid_reader, SeedSource=line_source)
streamlines.Vectors = ['POINTS', 'Velocity']
streamlines.IntegrationDirection = 'BOTH'
streamlines.IntegrationStepUnit = 'Length'

max_domain_extent = max(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4])
streamlines.InitialStepLength = 0.01
streamlines.MaximumSteps = int(max_domain_extent * 1.5 / streamlines.InitialStepLength)
print(f"ParaView: Streamline InitialStepLength set to {streamlines.InitialStepLength}")
print(f"ParaView: Streamline MaximumSteps set to {streamlines.MaximumSteps}")

streamlines_display = pv_s.Show(streamlines, render_view)
streamlines_display.Representation = 'Surface'
streamlines_display.AmbientColor = [1.0, 1.0, 0.0]
streamlines_display.DiffuseColor = [1.0, 1.0, 0.0]
streamlines_display.ColorArrayName = ['POINTS', 'Velocity']
streamlines_display.LookupTable = pv_s.GetLookupTableForArray('Velocity', 3)
print("ParaView: Added streamlines for Velocity field.")

# --- 3. Display Turbine Model ---
turbine_display = pv_s.Show(turbine_reader, render_view)
turbine_display.Representation = 'Surface'
turbine_display.AmbientColor = [0.5, 0.5, 0.5]
turbine_display.DiffuseColor = [0.8, 0.8, 0.8]
print("ParaView: Displaying turbine model.")

# --- 4. Setup Animation ---
animation_scene = pv_s.GetAnimationScene()
animation_scene.PlayMode = 'Snap To TimeSteps'

animation_scene.StartTime = fluid_reader.TimestepValues[0]
animation_scene.EndTime = fluid_reader.TimestepValues[-1]
animation_scene.NumberOfFrames = len(fluid_reader.TimestepValues)
desired_fps = 10 # This FPS is now informational for the user, as FFmpeg is run elsewhere.
print(f"ParaView: Animation setup complete. Frames: {animation_scene.NumberOfFrames}, Desired FPS: {desired_fps}")

# --- 5. Camera Setup ---
bounds = fluid_reader.GetDataInformation().GetBounds()
center_x = bounds[0] + (bounds[1]-bounds[0])/2
center_y = bounds[2] + (bounds[3]-bounds[2])/2
center_z = bounds[4] + (bounds[5]-bounds[4])/2

render_view.CameraPosition = [center_x + (bounds[1]-bounds[0])*2,
                              center_y + (bounds[3]-bounds[2])*2,
                              center_z + (bounds[5]-bounds[4])*2]
render_view.CameraFocalPoint = [center_x, center_y, center_z]
render_view.CameraViewUp = [0.0, 0.0, 1.0]
render_view.ViewSize = [1920, 1080]

pv_s.Render()
print("ParaView: Camera and view set up.")

# --- 6. Save Animation as Image Sequence ---
print(f"ParaView: Saving animation frames to {PARAVIEW_OUTPUT_PATTERN}...")
print(f"DEBUG: Argument to SaveAnimation: '{PARAVIEW_OUTPUT_PATTERN}' of type {type(PARAVIEW_OUTPUT_PATTERN)}") # Still useful for verbose debugging
pv_s.SaveAnimation(PARAVIEW_OUTPUT_PATTERN, render_view,
                   ImageQuality=85 # Image quality for PNG (0-100)
                  )
print(f"ParaView: Animation frames saved to {PARAVIEW_OUTPUT_PATTERN}")

# Cleanup
pv_s.Disconnect()
print("ParaView: Disconnected and script finished.")

# Print out the absolute path to the directory containing the PNGs for the workflow to use
print(f"PNG_OUTPUT_DIR={actual_output_dir}")
