import dropbox
import os
import requests
import sys

# Function to refresh the Dropbox access token
def refresh_access_token(refresh_token, client_id, client_secret):
    url = "https://api.dropbox.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to refresh access token")

# Function to upload rendered Blender video to Dropbox
def upload_video_to_dropbox(local_video, dropbox_path, refresh_token, client_id, client_secret):
    """Uploads the final Blender-rendered video to Dropbox."""
    
    # Refresh the access token
    access_token = refresh_access_token(refresh_token, client_id, client_secret)
    dbx = dropbox.Dropbox(access_token)

    # Ensure the local video file exists
    if not os.path.isfile(local_video):
        print(f"❌ Error: Video file {local_video} does not exist.")
        sys.exit(1)

    # Upload video file to Dropbox
    try:
        with open(local_video, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        print(f"✅ Uploaded video to Dropbox: {dropbox_path}")
    except Exception as e:
        print(f"❌ Failed to upload video to Dropbox: {e}")
        sys.exit(1)

# Entry point for the script
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("❌ Error: Missing arguments. Expected usage:")
        print("python3 upload_to_dropbox.py <local_video> <dropbox_path> <refresh_token> <client_id> <client_secret>")
        sys.exit(1)

    local_video = sys.argv[1]         # Local video file path
    dropbox_path = sys.argv[2]        # Dropbox destination path
    refresh_token = sys.argv[3]       # Dropbox refresh token
    client_id = sys.argv[4]           # Dropbox client ID
    client_secret = sys.argv[5]       # Dropbox client secret

    # Upload the final Blender-rendered video to Dropbox
    upload_video_to_dropbox(local_video, dropbox_path, refresh_token, client_id, client_secret)

    print("✅ Video upload process completed successfully!")



