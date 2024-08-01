import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

BACKUP_FOLDER = "/tmp/backup/"
BACKUP_PATH = BACKUP_FOLDER + "vaultwarden-backup.zip"
FILE_ID = "1C38KW923FnSUhhXeMXr2HkbwUr9J4xF-"


def get_credentials():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def create_backup_zip():
    os.system(f"mkdir -p {BACKUP_FOLDER}")
    os.system(f"zip {BACKUP_PATH} -r vaultwarden-data")


def delete_backup_zip():
    os.system(f"rm {BACKUP_PATH}")


def main():
    """Creates a zip backup of the vaultwarden-data folder
    and uploads it to Google Drive."""
    create_backup_zip()

    creds = get_credentials()

    service = None
    try:
        service = build("drive", "v3", credentials=creds)

        media = MediaFileUpload(BACKUP_PATH, mimetype="application/x-zip")
        res = (
            service.files()
            .update(fileId=FILE_ID, media_body=media, fields="id")
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
