from py_gsuite_apis.services.google_apis import GoogleServerAuthCredentials, create_google_auth_services_credentials
from py_gsuite_apis.services.google_apis.drive import GoogleDriveApiClient, create_google_drive_api_client
from py_gsuite_apis.services.google_apis.sheets import GoogleSheetsApiClient, create_google_sheets_api_client
from py_gsuite_apis.services.google_apis.drive import GoogleSlidesApiClient, create_google_slides_api_client


name = "py-gsuite-apis"

__version__ = "0.0.2"
__all__ = [
    "GoogleServerAuthCredentials",
    "create_google_auth_services_credentials",
    "GoogleDriveApiClient",
    "create_google_drive_api_client",
    "GoogleSheetsApiClient",
    "create_google_sheets_api_client",
    "GoogleSlidesApiClient",
    "create_google_slides_api_client",
]
