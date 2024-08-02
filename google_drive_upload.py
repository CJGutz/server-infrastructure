import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account


SCOPES = ["https://www.googleapis.com/auth/drive.file"]

BACKUP_FOLDER = "/tmp/backup/"
BACKUP_PATH = BACKUP_FOLDER + "vaultwarden-backup.zip"
FILE_ID = "1LQcFPGEil7xfiFh-shud4HdRZDN3q2nG"
SERVICE_KEY = "service-key.json"


def get_credentials():
    if not os.path.exists(SERVICE_KEY):
        raise FileNotFoundError(
            f"Service key file not found: {SERVICE_KEY}. Generate from Google."
        )
    return service_account.Credentials.from_service_account_file(
        SERVICE_KEY, scopes=SCOPES
    )


def create_backup_zip():
    os.system(f"mkdir -p {BACKUP_FOLDER}")
    os.system(f"zip {BACKUP_PATH} -r vaultwarden-data")


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

        media = MediaFileUpload(BACKUP_PATH, mimetype="application/x-zip")
        res = (
            service.files()
            .update(media_body=media, fields="id,name", fileId=FILE_ID)
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
