import dropbox
import os
import requests
import sys

# Function to refresh the access token
def refresh_access_token(refresh_token, client_id, client_secret):
    """Refreshes the Dropbox access token using the refresh token."""
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
        # Provide more detailed error message for debugging
        raise Exception(f"Failed to refresh access token: Status Code {response.status_code}, Response: {response.text}")

# Function to upload a file to Dropbox
def upload_file_to_dropbox(local_file_path, dropbox_file_path, refresh_token, client_id, client_secret):
    """Uploads a local file to a specified path on Dropbox."""
    try:
        # Refresh the access token before each upload attempt
        access_token = refresh_access_token(refresh_token, client_id, client_secret)
        dbx = dropbox.Dropbox(access_token)

        # Open the local file in binary read mode
        with open(local_file_path, "rb") as f:
            # Upload the file, overwriting if it already exists
            dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)
        print(f"✅ Successfully uploaded file to Dropbox: {dropbox_file_path}")
        return True # Indicate success
    except Exception as e:
        print(f"❌ Failed to upload file '{local_file_path}' to Dropbox: {e}")
        return False # Indicate failure

# Entry point for the script
if __name__ == "__main__":
    # The script expects 5 command-line arguments:
    # 1. local_file_path (absolute path to the file to upload)
    # 2. dropbox_folder (the destination folder in Dropbox)
    # 3. refresh_token
    # 4. client_id (APP_KEY)
    # 5. client_secret (APP_SECRET)
    if len(sys.argv) != 6:
        print("Usage: python src/upload_to_dropbox.py <local_file_path> <dropbox_folder> <refresh_token> <client_id> <client_secret>")
        sys.exit(1) # Exit with an error code for incorrect usage

    # Parse command-line arguments
    local_file_to_upload = sys.argv[1]
    dropbox_folder = sys.argv[2]
    refresh_token = sys.argv[3]
    client_id = sys.argv[4]
    client_secret = sys.argv[5]

    # Extract the filename from the local_file_to_upload path
    output_file_name = os.path.basename(local_file_to_upload)

    # Construct the full destination path on Dropbox
    dropbox_file_path = f"{dropbox_folder}/{output_file_name}"

    # Verify that the local file exists before attempting to upload
    if not os.path.exists(local_file_to_upload):
        print(f"❌ Error: The output file '{local_file_to_upload}' was not found. Please ensure the preceding steps successfully generated this file.")
        sys.exit(1) # Exit with an error code if the file is not found

    # Call the upload function
    if not upload_file_to_dropbox(local_file_to_upload, dropbox_file_path, refresh_token, client_id, client_secret):
        sys.exit(1) # Exit with an error code if the upload itself fails


