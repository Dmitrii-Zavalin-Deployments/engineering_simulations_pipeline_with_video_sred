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

# Function to upload rendered Blender files to Dropbox
def upload_files_to_dropbox(local_folder, dropbox_folder, refresh_token, client_id, client_secret):
    """Uploads all rendered files from the Blender output folder to Dropbox."""
    
    # Refresh the access token
    access_token = refresh_access_token(refresh_token, client_id, client_secret)
    dbx = dropbox.Dropbox(access_token)

    # Ensure the local output directory exists
    if not os.path.isdir(local_folder):
        print(f"⚠️ Warning: Output directory {local_folder} does not exist. Skipping upload.")
        return

    # Upload each file in the local output folder
    for file_name in os.listdir(local_folder):
        local_file_path = os.path.join(local_folder, file_name)
        dropbox_file_path = f"{dropbox_folder}/{file_name}"

        try:
            with open(local_file_path, "rb") as f:
                dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)
            print(f"✅ Uploaded file to Dropbox: {dropbox_file_path}")
        except Exception as e:
            print(f"❌ Failed to upload {file_name} to Dropbox: {e}")

# Entry point for the script
if __name__ == "__main__":
    # Command-line arguments
    local_directory = "./RenderedOutput"           # Blender output folder
    dropbox_folder = "/simulations/Blender/output" # Dropbox output path
    refresh_token = sys.argv[1]                    # Dropbox refresh token
    client_id = sys.argv[2]                        # Dropbox client ID
    client_secret = sys.argv[3]                    # Dropbox client secret

    # Check if the local directory exists
    if not os.path.isdir(local_directory):
        print(f"❌ Directory {local_directory} does not exist. Ensure rendering was successful.")
        sys.exit(1)

    # Upload rendered Blender files to Dropbox
    upload_files_to_dropbox(local_directory, dropbox_folder, refresh_token, client_id, client_secret)

    print("✅ All rendered Blender frames have been uploaded to Dropbox!")



