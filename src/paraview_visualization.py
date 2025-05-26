# This script should be run with pvpython (ParaView's Python interpreter)
# e.g., /path/to/ParaView/bin/pvpython paraview_visualization.py --pvd-file /path/to/output/turbine_flow_animation.pvd --turbine-model /path/to/turbine_geometry.vtp

import paraview.simple as pv_s
import sys
import os

# --- Configuration (can be passed as command line arguments or hardcoded) ---
OUTPUT_VIDEO_FILENAME = "turbine_flow_animation.mp4"
PVD_FILE_PATH = None  # To be set by argument
TURBINE_MODEL_PATH = None # Path to your .stl, .obj, or .vtp turbine model

# Parse command line arguments if running from command line
if __name__ == "__main__":
    args = sys.argv
    for i, arg in enumerate(args):
        if arg == "--pvd-file" and i + 1 < len(args):
            PVD_FILE_PATH = args[i+1]
        elif arg == "--turbine-model" and i + 1 < len(args):
            TURBINE_MODEL_PATH = args[i+1]
        elif arg == "--output-video" and i + 1 < len(args):
            OUTPUT_VIDEO_FILENAME = args[i+1]

if not PVD_FILE_PATH or not TURBINE_MODEL_PATH:
    print("Usage: pvpython paraview_visualization.py --pvd-file <path_to_pvd> --turbine-model <path_to_stl/obj/vtp> [--output-video <filename>]")
    sys.exit(1)

# Ensure paths are absolute or correctly relative to where pvpython is run
# In GitHub Actions, these will typically already be absolute due to the workflow's handling
PVD_FILE_PATH = os.path.abspath(PVD_FILE_PATH)
TURBINE_MODEL_PATH = os.path.abspath(TURBINE_MODEL_PATH)

print(f"ParaView: PVD File: {PVD_FILE_PATH}")
print(f"ParaView: Turbine Model: {TURBINE_MODEL_PATH}")
print(f"ParaView: Output Video: {OUTPUT_VIDEO_FILENAME}")

# --- 1. Load Data ---
# Clear existing pipeline
pv_s.ResetSession()

# Load the PVD file (fluid simulation data)
# Corrected based on debug output: PVDReader
fluid_reader = pv_s.PVDReader(FileName=[PVD_FILE_PATH])

# Load the turbine 3D model
# Corrected based on debug output: WavefrontOBJReader
if TURBINE_MODEL_PATH.lower().endswith('.obj'):
    turbine_reader = pv_s.WavefrontOBJReader(FileNames=[TURBINE_MODEL_PATH])
elif TURBINE_MODEL_PATH.lower().endswith('.vtp'):
    turbine_reader = pv_s.XMLPolyDataReader(FileName=[TURBINE_MODEL_PATH])
elif TURBINE_MODEL_PATH.lower().endswith('.stl'):
    turbine_reader = pv_s.STLReader(FileNames=[TURBINE_MODEL_PATH])
else:
    print(f"Error: Unsupported turbine model format: {os.path.splitext(TURBINE_MODEL_PATH)[1]}. Supported: .obj, .vtp, .stl")
    sys.exit(1)

# --- 2. Create Visualization Pipeline for Fluid Data ---
# Get the active view (create one if none exists)
render_view = pv_s.GetActiveViewOrCreate('RenderView')
pv_s.SetActiveView(render_view)

# Show the fluid volume data
fluid_display = pv_s.Show(fluid_reader, render_view)
fluid_display.Representation = 'Volume' # Or 'Outline', 'Surface'
fluid_display.Opacity = 0.3 # Make it semi-transparent
fluid_display.EnableOpacityMapping = 1
# Assuming 'Temperature' is the scalar field you want to visualize in the fluid volume
# Adjust RGBPoints based on your expected temperature range and desired colors
fluid_display.LookupTable = pv_s.GetLookupTableForArray('Temperature', 1,
                                                      RGBPoints=[273.15, 0.0, 0.0, 1.0, # Blue for cold (0 C)
                                                                 323.15, 0.0, 1.0, 0.0, # Green for mid-range (50 C)
                                                                 373.15, 1.0, 0.0, 0.0], # Red for hot (100 C)
                                                      ColorSpace='RGB',
                                                      ScalarRangeInitialized=1.0)
fluid_display.ColorArrayName = ['POINTS', 'Temperature']
print("ParaView: Set up fluid volume display with Temperature colormap.")

# Add streamlines (example using 'Velocity' field)
# Define seed points for streamlines (e.g., a line upstream of the turbine)
# You'll need to know your domain's bounds for this
# Get the data bounds from the fluid reader for robust camera and line source setup
bounds = fluid_reader.GetDataInformation().GetBounds()
print(f"ParaView: Fluid data bounds: {bounds}")

# Create a line source for streamlines. Adjust the points to be within your domain.
# This example places a line across the inlet (min X) face
line_source = pv_s.Line(Point1=[bounds[0], bounds[2], bounds[4]], # min X, min Y, min Z
                        Point2=[bounds[0], bounds[3], bounds[5]]) # min X, max Y, max Z

streamlines = pv_s.StreamTracer(Input=fluid_reader, SeedSource=line_source)
streamlines.Vectors = ['POINTS', 'Velocity'] # Assuming 'Velocity' is a vector field
streamlines.IntegrationDirection = 'Both' # Forward, Backward, Both
streamlines.MaximumPropagation = max(
    bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4]
) * 1.5 # Propagate across domain, maybe a bit more

# Adjust number of streamlines and integration parameters for better visualization
streamlines.NumberOfSourcePoints = 100 # Increase for more streamlines
streamlines.IntegrationStepUnit = 'Length'
streamlines.IntegrationStepLength = 0.01 # Adjust based on your domain size for smoother lines

streamlines_display = pv_s.Show(streamlines, render_view)
streamlines_display.Representation = 'Surface'
streamlines_display.AmbientColor = [1.0, 1.0, 0.0] # Yellow streamlines
streamlines_display.DiffuseColor = [1.0, 1.0, 0.0]
# You can also color streamlines by a scalar, e.g., velocity magnitude
streamlines_display.ColorArrayName = ['POINTS', 'Velocity']
streamlines_display.LookupTable = pv_s.GetLookupTableForArray('Velocity', 3) # Magnitude for vector
print("ParaView: Added streamlines for Velocity field.")

# --- 3. Display Turbine Model ---
turbine_display = pv_s.Show(turbine_reader, render_view)
turbine_display.Representation = 'Surface'
turbine_display.AmbientColor = [0.5, 0.5, 0.5] # Grey
turbine_display.DiffuseColor = [0.8, 0.8, 0.8] # Light grey
print("ParaView: Displaying turbine model.")

# --- 4. Setup Animation ---
animation_scene = pv_s.GetAnimationScene()
animation_scene.PlayMode = 'Snap To TimeSteps' # Important for PVD files
animation_scene.UpdateAnimationSteps() # Get time steps from loaded data

# Set the animation time range to match the loaded data
animation_scene.StartTime = fluid_reader.TimestepValues[0]
animation_scene.EndTime = fluid_reader.TimestepValues[-1]
animation_scene.NumberOfFrames = len(fluid_reader.TimestepValues)
animation_scene.FPS = 10 # Frames per second for the output video. Adjust as desired.
print(f"ParaView: Animation setup complete. Frames: {animation_scene.NumberOfFrames}, FPS: {animation_scene.FPS}")

# --- 5. Camera Setup ---
# Calculate the center of the fluid domain for focal point
bounds = fluid_reader.GetDataInformation().GetBounds() # Re-get bounds in case they changed or were not fully initialized earlier
center_x = bounds[0] + (bounds[1]-bounds[0])/2
center_y = bounds[2] + (bounds[3]-bounds[2])/2
center_z = bounds[4] + (bounds[5]-bounds[4])/2

# Position the camera relative to the center and bounds
# Adjust these values to get a good initial view of your turbine and fluid
render_view.CameraPosition = [center_x + (bounds[1]-bounds[0])*2,
                              center_y + (bounds[3]-bounds[2])*2,
                              center_z + (bounds[5]-bounds[4])*2]
render_view.CameraFocalPoint = [center_x, center_y, center_z]
render_view.CameraViewUp = [0.0, 0.0, 1.0] # Z-up
render_view.ViewSize = [1920, 1080] # High resolution for better video quality

# Ensure all displays are updated with the new view properties
pv_s.Render()
print("ParaView: Camera and view set up.")

# --- 6. Save Animation ---
# Ensure a temporary directory for output if needed
output_dir = os.path.dirname(OUTPUT_VIDEO_FILENAME)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save animation
print(f"ParaView: Saving animation to {OUTPUT_VIDEO_FILENAME}...")
pv_s.SaveAnimation(OUTPUT_VIDEO_FILENAME, render_view,
                   FrameRate=int(animation_scene.FPS),
                   SuffixAndExtension=False, # Save as single video file
                   Quality=2 # Good quality (0-2)
                  )
print(f"ParaView: Animation saved to {OUTPUT_VIDEO_FILENAME}")

# Cleanup
pv_s.Disconnect()
print("ParaView: Disconnected and script finished.")
