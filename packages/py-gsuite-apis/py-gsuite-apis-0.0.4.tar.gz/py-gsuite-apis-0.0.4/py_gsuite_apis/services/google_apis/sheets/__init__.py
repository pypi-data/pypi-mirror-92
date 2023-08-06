import pandas as pd
import logging

from py_gsuite_apis.core.config import get_config
from py_gsuite_apis.services.google_apis import GoogleApiClient
from py_gsuite_apis.services.google_apis.auth import GoogleServerAuthCredentials
from py_gsuite_apis.services.google_apis.sheets.charts import GoogleSheetsChartGenerator


# from py_gsuite_apis.models.google_apis.sheets import AddChartsRequest, Spreadsheet
from py_gsuite_apis.models.google_apis.sheets import Spreadsheet


settings = get_config()

logger = logging.getLogger("uvicorn")


class GoogleSheetsApiClient(GoogleApiClient):
    def __init__(
        self,
        *,
        credentials: GoogleServerAuthCredentials,
        build: str,
        version: str,
        scope: str,
    ) -> None:
        super().__init__(
            # credentials_filename=settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILENAME,
            credentials=credentials,
            build=build,
            version=version,
            scope=scope,
            # build=settings.DRIVE.BUILD,
            # version=settings.DRIVE.VERSION,
            # scope=settings.DRIVE.SCOPE,
        )
    # def __init__(self, *, credentials: GoogleServerAuthCredentials) -> None:
    #     super().__init__(
    #         # credentials_filename=settings.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_FILENAME,
    #         credentials=credentials,
    #         build=settings.SHEETS.BUILD,
    #         version=settings.SHEETS.VERSION,
    #         scope=settings.SHEETS.SCOPE,
    #     )
    #     # self.charts_service = GoogleSheetsChartGenerator()

    def write_pandas_dataframe_to_sheet(
        self, *, spreadsheet_id: str, sheet_name: str, df: pd.DataFrame, remove_first_column_title: bool = False
    ) -> None:
        """
        Uploads a pandas.dataframe to the desired page of a google sheets sheet.
        SERVICE ACCOUNT MUST HAVE PERMISIONS TO WRITE IN THE SHEET.
        Aditionally, pass a list with the new names of the columns.
        Data must be utf-8 encoded to avoid errors.
        """

        df.fillna(value=0, inplace=True)
        cols = df.columns.tolist()
        if remove_first_column_title:
            cols[0] = ""
        rows = df.to_numpy().tolist()
        # columnsList = df.columns.tolist()
        # valuesList = df.values.tolist()

        try:

            body = {
                "valueInputOption": "USER_ENTERED",
                "data": [{"range": sheet_name + "!A1", "values": [cols] + rows}],
            }

            self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        except Exception as e:
            logger.warn(e)

    def create_chart_for_hiring_slides(
        self,
        *,
        spreadsheet_id: str,
        sheet_id: int,
        title: str,
        chart_type: str = "COLUMN",
        data_range_start_row_index: int = 0,
        data_range_end_row_index: int = None,
        data_range_start_col_index: int = 0,
        data_range_end_col_index: int = None,
    ) -> None:
        """
        Create a chart for the "This Week" and "To Date" tables in the appropriate Google Sheet
        """
        spreadsheet = None
        sheet = None
        try:
            response = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            spreadsheet = Spreadsheet(**response)
            sheet = spreadsheet.sheets[sheet_id or 0]
        except Exception as e:
            logger.warn(e)
            raise ValueError("Spreadsheet with that ID could not located or accessed.")

        # chart_generator = GoogleSheetsChartGenerator(spreadsheet_id=spreadsheet_id, sheet_id=sheet_id)
        chart_generator = GoogleSheetsChartGenerator(
            spreadsheet_id=spreadsheet.spreadsheetId, sheet_id=sheet.properties.sheetId
        )

        domain = chart_generator.create_basic_chart_domain(
            # sheet_id=None,
            sheet_id=sheet.properties.sheetId,
            start_row_index=data_range_start_row_index,
            end_row_index=data_range_start_row_index + 1,
            start_column_index=data_range_start_col_index,
            end_column_index=data_range_end_col_index,
            # group_rule: ChartGroupRule = None,
            # aggregate_type: ChartAggregateType = None,
        )

        if not data_range_end_row_index:
            # default to last column in sheet if need be
            data_range_end_row_index = sheet.properties.gridProperties.columnCount

        series = [
            chart_generator.create_basic_chart_series(
                sheet_id=sheet.properties.sheetId,
                start_row_index=i,
                end_row_index=i + 1,
                start_column_index=data_range_start_col_index,
                end_column_index=data_range_end_col_index,
                # sheet_id: str = None,
                # start_row_index: int = 0,
                # end_row_index: int = None,
                # start_column_index: int = 0,
                # end_column_index: int = None,
                # target_axis: BasicChartAxisPosition = "LEFT_AXIS",
                # basic_chart_type: BasicChartType = "COLUMN",
                # series_line_style: GoogleLineStyle = None,
                # series_data_label: DataLabel = None,
                # series_color: GoogleColor = None,
                # series_color_style: GoogleColorStyle = None,
                # series_point_style: GooglePointStyle = None,
                # series_style_overrides: BasicSeriesDataPointStyleOverride = None,
            )
            for i in range(data_range_start_row_index + 1, data_range_end_row_index)
        ]

        basic_chart_spec = chart_generator.create_basic_chart_spec(
            # title=title,
            chart_type=chart_type,
            legend_position="BOTTOM_LEGEND",
            domains=[domain],
            series=series,
            header_count=1,
        )

        chart_spec = chart_generator.create_google_sheets_chart_spec(
            title=title,
            basic_charts_spec=basic_chart_spec,
            # need to think about other parameters here
        )

        add_chart_request = chart_generator.generate_add_chart_request(
            chart_id=None,
            chart_spec=chart_spec,
            # chart_id: int = None,
            # chart_spec: GoogleSheetsChartSpec = None,
            # chart_position: GoogleSheetsEmbeddedObjectPosition = None,
            # chart_border: GoogleSheetsEmbeddedObjectBorder = None,
        )

        print(add_chart_request)

        body = {"requests": [add_chart_request.dict(exclude_unset=True)]}

        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet.spreadsheetId,
                body=body,
                # body={"requests": []},
            ).execute()
        except Exception as e:
            logger.warn(e)


async def create_google_sheets_api_client(
    credentials: GoogleServerAuthCredentials,
    build: str = settings.SHEETS.BUILD,
    version: str = settings.SHEETS.VERSION,
    scope: str = settings.SHEETS.SCOPE,
) -> GoogleSheetsApiClient:
    return GoogleSheetsApiClient(credentials=credentials, build=build, version=version, scope=scope)
