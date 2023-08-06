import logging

from py_gsuite_apis.core.config import get_config

from py_gsuite_apis.services.google_api import GoogleApiClient, GoogleServerAuthCredentials


settings = get_config()

logger = logging.getLogger("uvicorn")


class GoogleDriveApiClient(GoogleApiClient):
    def __init__(self, credentials: GoogleServerAuthCredentials) -> None:
        super().__init__(
            # credentials_filename=settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILENAME,
            credentials=credentials,
            build=settings.DRIVE.BUILD,
            version=settings.DRIVE.VERSION,
            scope=settings.DRIVE.SCOPE,
        )

    def create_slides_presentation_copy(self, *, slides_presentation_id: str, copy_title: str) -> str:
        """
        Creates a copy of the given slides presentation in Google Drive and returns the copied
        slide deck ID
        """
        body = {"name": copy_title}
        drive_response = self.service.files().copy(fileId=slides_presentation_id, body=body).execute()
        slides_presentation_copy_id = drive_response.get("id")
        return slides_presentation_copy_id


async def create_google_drive_api_client(
    credentials: GoogleServerAuthCredentials,
    build: str = settings.DRIVE.BUILD,
    version: str = settings.DRIVE.VERSION,
    scope: str = settings.DRIVE.SCOPE,
) -> GoogleDriveApiClient:
    return GoogleDriveApiClient(credentials=credentials, build=build, version=version, scope=scope)
