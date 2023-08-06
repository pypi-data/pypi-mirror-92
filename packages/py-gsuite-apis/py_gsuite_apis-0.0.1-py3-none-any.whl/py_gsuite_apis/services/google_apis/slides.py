import logging

from py_gsuite_apis.core.config import get_config

from py_gsuite_apis.services.google_api import GoogleApiClient, GoogleServerAuthCredentials


from py_gsuite_apis.models.google_apis.slides import GoogleSlidesPresentation
from py_gsuite_apis.models.google_apis.slides.requests import (
    CreateSheetsChartRequest,
    CreateTableRequest,
    PageElementProperties,
)
from py_gsuite_apis.models.google_apis.slides.other import Size, AffineTransform


settings = get_config()

logger = logging.getLogger("uvicorn")


class GoogleSlidesApiClient(GoogleApiClient):
    def __init__(self, *, credentials: GoogleServerAuthCredentials) -> None:
        super().__init__(
            # credentials_filename=settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILENAME,
            credentials=credentials,
            build=settings.SLIDES.BUILD,
            version=settings.SLIDES.VERSION,
            scope=settings.SLIDES.SCOPE,
        )

    def get_presentation_by_id(self, *, presentation_id: str) -> GoogleSlidesPresentation:
        # Call the Slides API
        presentation = self.service.presentations().get(presentationId=presentation_id).execute()
        return GoogleSlidesPresentation(**presentation)

    def construct_create_table_request(
        self,
        *,
        table_object_id: str = None,
        num_rows: int = 1,
        num_columns: int = 1,
        page_object_id: str,
        # apparently these are ignored by the Slides API at the moment
        # element_size: Size = None,
        # element_affine_transform: AffineTransform = None,
    ) -> CreateTableRequest:
        return CreateTableRequest(
            objectId=table_object_id,
            elementProperties=PageElementProperties(
                pageObjectId=page_object_id,  # The object ID of the page where the element is located.
                # size=element_size,
                # transform=element_affine_transform,
            ),
            rows=num_rows,
            columns=num_columns,
        )

    def construct_create_sheets_chart_request(
        self,
        *,
        new_sheets_chart_object_id: str = None,
        spreadsheet_id: str,
        chart_id: str,
        chart_linking_mode: str = "NOT_LINKED_IMAGE",
        page_object_id: str,
        element_size: Size = None,
        element_affine_transform: AffineTransform = None,
    ) -> CreateSheetsChartRequest:
        return CreateSheetsChartRequest(
            objectId=new_sheets_chart_object_id,
            elementProperties=PageElementProperties(
                pageObjectId=page_object_id,  # The object ID of the page where the element is located.
                size=element_size,
                transform=element_affine_transform,
            ),
            spreadsheetId=spreadsheet_id,
            chartId=chart_id,
            linkingMode=chart_linking_mode,
        )


async def create_google_slides_api_client(
    credentials: GoogleServerAuthCredentials,
    build: str = settings.SLIDES.BUILD,
    version: str = settings.SLIDES.VERSION,
    scope: str = settings.SLIDES.SCOPE,
) -> GoogleSlidesApiClient:
    return GoogleSlidesApiClient(credentials=credentials, build=build, version=version, scope=scope)
