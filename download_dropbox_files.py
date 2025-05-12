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
        raise Exception("❌ Failed to refresh access token")

# Function to delete a file from Dropbox after successful download
def delete_file_from_dropbox(dbx, file_path, log_file):
    try:
        dbx.files_delete_v2(file_path)
        log_file.write(f"✅ Deleted file from Dropbox: {file_path}\n")
        print(f"✅ Deleted file from Dropbox: {file_path}")  # Log in GitHub Actions
    except Exception as e:
        log_file.write(f"❌ Failed to delete {file_path}: {e}\n")
        print(f"❌ Failed to delete {file_path}: {e}")  # Log the error

# Function to download all `.obj` files from a specified Dropbox folder and delete them afterward
def download_files_from_dropbox(dropbox_folder, local_folder, refresh_token, client_id, client_secret, log_file_path):
    """Downloads `.obj` files from Dropbox for Blender simulation and deletes them afterward."""
    
    # Refresh the access token
    access_token = refresh_access_token(refresh_token, client_id, client_secret)
    dbx = dropbox.Dropbox(access_token)

    with open(log_file_path, "a") as log_file:
        log_file.write("🔄 Starting file download process...\n")
        try:
            os.makedirs(local_folder, exist_ok=True)

            has_more = True
            cursor = None
            while has_more:
                if cursor:
                    result = dbx.files_list_folder_continue(cursor)
                else:
                    result = dbx.files_list_folder(dropbox_folder)
                log_file.write(f"📂 Listing files in Dropbox folder: {dropbox_folder}\n")

                for entry in result.entries:
                    if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith(".obj"):
                        # Download `.obj` file
                        local_path = os.path.join(local_folder, entry.name)
                        with open(local_path, "wb") as f:
                            metadata, res = dbx.files_download(path=entry.path_lower)
                            f.write(res.content)
                        log_file.write(f"✅ Downloaded `{entry.name}` to `{local_path}`\n")
                        print(f"✅ Downloaded `{entry.name}`")  # Log success in GitHub Actions

                        # Delete file from Dropbox after downloading
                        delete_file_from_dropbox(dbx, entry.path_lower, log_file)

                has_more = result.has_more
                cursor = result.cursor

            log_file.write("✅ Download and deletion process completed successfully.\n")
        except dropbox.exceptions.ApiError as err:
            log_file.write(f"❌ Error downloading files: {err}\n")
            print(f"❌ Error downloading files: {err}")  # Log the error
        except Exception as e:
            log_file.write(f"❌ Unexpected error: {e}\n")
            print(f"❌ Unexpected error: {e}")  # Log the error

# Entry point for the script
if __name__ == "__main__":
    # Read command-line arguments
    dropbox_folder = sys.argv[1]  # Dropbox folder path
    local_folder = sys.argv[2]  # Local folder path
    refresh_token = sys.argv[3]  # Dropbox refresh token
    client_id = sys.argv[4]  # Dropbox client ID
    client_secret = sys.argv[5]  # Dropbox client secret
    log_file_path = sys.argv[6]  # Path to the log file

    # Call the function
    download_files_from_dropbox(dropbox_folder, local_folder, refresh_token, client_id, client_secret, log_file_path)



