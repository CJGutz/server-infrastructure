"""
Script to upload a tar ball backup of vaultwarden-data to Google Drive.
Uses a service account to upload to a folder that is shared from an existing 
Drive account.

Create Service Accounts: Google Cloud Console > IAM & Admin > Service Accounts
Click three dots > Mange keys > Add key > JSON > Download to service-key.json
Share a folder with the service account email address.
Make the service account first create its own file in the folder
and retrieve the id of that file. That file is now ready to be updated.

Should run on a scheduler like cron.
Example cronjob setting:
0 0 */7 * * /usr/bin/python3 /path/to/google_drive_upload.py
"""
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

TMP_BACKUP_STORAGE = os.environ.get("TMP_BACKUP_STORAGE", "/tmp/")
BACKUP_PATH = TMP_BACKUP_STORAGE + "vaultwarden-backup.tar.gz"
FOLDER_TO_BACKUP = os.environ.get("FOLDER_TO_BACKUP", "vaultwarden-data")

FILE_ID = os.environ.get("BACKUP_FILE_ID")
SERVICE_KEY = os.environ.get("SERVICE_KEY_FILE", "service-key.json")


def get_credentials():
    if not os.path.exists(SERVICE_KEY):
        raise FileNotFoundError(
            f"Service key file not found: {SERVICE_KEY}. Generate from Google."
        )
    return service_account.Credentials.from_service_account_file(
        SERVICE_KEY, scopes=SCOPES
    )


def create_backup_zip():
    os.system(f"mkdir -p {TMP_BACKUP_STORAGE}")
    os.system(f"tar -czvf {BACKUP_PATH} {FOLDER_TO_BACKUP}")


def delete_backup_zip():
    os.system(f"rm {BACKUP_PATH}")


def main():
    """Creates a zip backup of the vaultwarden-data folder
    and uploads it to Google Drive."""

    creds = get_credentials()

    create_backup_zip()

    service = None
    try:
        service = build("drive", "v3", credentials=creds)

        media = MediaFileUpload(BACKUP_PATH, mimetype="application/gzip")
        res = (
            service.files()
            .update(fileId=FILE_ID, media_body=media, fields="id,name")
            .execute()
        )
        print("Results from upload:", res)

    except HttpError as error:
        print(f"An error occurred: {error}")

    finally:
        if service:
            service.close()

    delete_backup_zip()


if __name__ == "__main__":
    main()
