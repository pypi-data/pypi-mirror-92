from typing import List

import logging

from py_gsuite_apis.models.google_apis.sheets import AddChartsRequest, AddChartCommand, Spreadsheet
from py_gsuite_apis.models.google_apis.sheets.other import (
    GoogleColor,
    GoogleColorStyle,
    GoogleSheetsGridRange,
    GoogleSheetsEmbeddedObjectPosition,
)

from py_gsuite_apis.models.google_apis.sheets.charts import (
    # ChartData,
    DataLabel,
    BasicChartAxis,
    BasicChartDomain,
    BasicChartSeries,
    BasicChartSpec,
    ChartGroupRule,
    ChartAggregateType,
    ChartSourceRange,
    GoogleLineStyle,
    GooglePointStyle,
    SourceRangeChartData,
    GoogleSheetsChart,
    GoogleSheetsChartSpecBasic,
    # GoogleSheetsChartSpec,
    GoogleSheetsEmbeddedObjectBorder,
    BasicSeriesDataPointStyleOverride,
)
from py_gsuite_apis.models.google_apis.sheets.charts.enums import BasicChartAxisPosition, BasicChartType


logger = logging.getLogger("uvicorn")


class GoogleSheetsChartGenerator:
    """
    Used to generate a chart from data in a provided Google Sheets range
    """

    spreadsheet: Spreadsheet

    def __init__(self, *, spreadsheet_id: str = None, sheet_id: int = 0) -> None:
        self.spreadsheet_id = spreadsheet_id
        self.sheet_id = sheet_id

    def create_google_sheets_grid_range(
        self,
        *,
        sheet_id: int = None,
        start_row_index: int = 0,
        end_row_index: int = None,
        start_column_index: int = 0,
        end_column_index: int = None,
    ) -> GoogleSheetsGridRange:
        return GoogleSheetsGridRange(
            sheetId=sheet_id or self.sheet_id,
            startRowIndex=start_row_index,
            endRowIndex=end_row_index,
            startColumnIndex=start_column_index,
            endColumnIndex=end_column_index,
            # add any other params here later
        )

    def generate_add_chart_request(
        self,
        *,
        chart_id: int = None,
        # chart_spec: GoogleSheetsChartSpec = None,
        chart_spec: GoogleSheetsChartSpecBasic = None,
        chart_position: GoogleSheetsEmbeddedObjectPosition = None,
        chart_border: GoogleSheetsEmbeddedObjectBorder = None,
    ) -> AddChartsRequest:
        """
        Could obviously add more chart creation requests here, but sticking with one for now
        """
        return AddChartsRequest(
            addChart=AddChartCommand(
                chart=GoogleSheetsChart(
                    chartId=chart_id,
                    spec=chart_spec,
                    position=chart_position,
                    border=chart_border,
                    # ).dict(exclude_unset=True)
                )
            )
        )

    def create_google_sheets_chart_spec(
        self, *, title: str = None, subtitle: str = None, basic_charts_spec: BasicChartSpec,
    ) -> GoogleSheetsChartSpecBasic:
        return GoogleSheetsChartSpecBasic(
            title=title,
            subtitle=subtitle,
            basicChart=basic_charts_spec,
            # tons of other fields could go here but we'll leave that for later
        )

    def create_basic_chart_spec(
        self,
        *,
        chart_type: str = "COLUMN",
        legend_position: str = "BOTTOM_LEGEND",
        chart_axes: List[BasicChartAxis] = [
            BasicChartAxis(position="LEFT_AXIS", title="Y Axis"),
            BasicChartAxis(position="BOTTOM_AXIS", title="X Axis"),
        ],
        domains: List[BasicChartDomain] = [],
        series: List[BasicChartSeries] = [],
        header_count: int = 1,
    ) -> BasicChartSpec:
        return BasicChartSpec(
            chartType=chart_type,
            legendPosition=legend_position,
            axis=chart_axes,
            domains=domains,
            series=series,
            headerCount=header_count,
        )

    def create_basic_chart_domain(
        self,
        *,
        sheet_id: str = None,
        start_row_index: int = 0,
        end_row_index: int = None,
        start_column_index: int = 0,
        end_column_index: int = None,
        reversed: bool = False,
        group_rule: ChartGroupRule = None,
        aggregate_type: ChartAggregateType = None,
    ) -> BasicChartDomain:
        """
        Create the domain for a new chart.

        An example would be the different roles hiring candidates might apply for.
        """
        return BasicChartDomain(
            domain=SourceRangeChartData(
                sourceRange=ChartSourceRange(
                    sources=[
                        GoogleSheetsGridRange(
                            sheetId=sheet_id or self.sheet_id,
                            startRowIndex=start_row_index,
                            endRowIndex=end_row_index,
                            startColumnIndex=start_column_index,
                            endColumnIndex=end_column_index,
                            # add any other params
                        )
                    ]
                ),
                groupRule=group_rule,
                aggregateType=aggregate_type,
            ),
            reversed=reversed,
        )

    def create_basic_chart_series(
        self,
        *,
        sheet_id: str = None,
        start_row_index: int = 0,
        end_row_index: int = None,
        start_column_index: int = 0,
        end_column_index: int = None,
        target_axis: BasicChartAxisPosition = "LEFT_AXIS",
        basic_chart_type: BasicChartType = "COLUMN",
        series_line_style: GoogleLineStyle = None,
        series_data_label: DataLabel = None,
        series_color: GoogleColor = None,
        series_color_style: GoogleColorStyle = None,
        series_point_style: GooglePointStyle = None,
        series_style_overrides: BasicSeriesDataPointStyleOverride = None,
    ) -> BasicChartSeries:
        """
        One of the data series being plotted in the chart
        """
        return BasicChartSeries(
            series=SourceRangeChartData(
                sourceRange=ChartSourceRange(
                    sources=[
                        GoogleSheetsGridRange(
                            sheetId=sheet_id or self.sheet_id,
                            startRowIndex=start_row_index,
                            endRowIndex=end_row_index,
                            startColumnIndex=start_column_index,
                            endColumnIndex=end_column_index,
                            # add any other params
                        )
                    ]
                )
            ),
            targetAxis=target_axis,
            type=basic_chart_type,
            lineStyle=series_line_style,
            dataLabel=series_data_label,
            color=series_color,
            colorStyles=series_color_style,
            pointStyle=series_point_style,
            styleOverrides=series_style_overrides,
        )

    def create_column_chart_from_spreadsheet_data() -> None:
        pass

    # def create_column_chart_from_spreadsheet_data(
    #     self, *, spreadsheet_id: str, sheet_name: str, end_col: int, end_row: int
    # ) -> None:
    #     try:
    #         sheet_id = self.get_sheet_id(spreadsheet_id=spreadsheet_id, sheet_name=sheet_name)

    #         body = {
    #             "requests": [
    #                 {
    #                     "addChart": {
    #                         "chart": {
    #                             "spec": {
    #                                 "title": "Model Q1 Sales",
    #                                 "basicChart": {
    #                                     "chartType": "COLUMN",
    #                                     "legendPosition": "BOTTOM_LEGEND",
    #                                     "axis": [
    #                                         {"position": "BOTTOM_AXIS", "title": "Model Numbers"},
    #                                         {"position": "LEFT_AXIS", "title": "Sales"},
    #                                     ],
    #                                     "domains": [
    #                                         {
    #                                             "domain": {
    #                                                 "sourceRange": {
    #                                                     "sources": [
    #                                                         {
    #                                                             "sheetId": sheet_id,
    #                                                             "startRowIndex": 0,
    #                                                             "endRowIndex": end_row,
    #                                                             "startColumnIndex": 0,
    #                                                             "endColumnIndex": end_col,
    #                                                         }
    #                                                     ]
    #                                                 }
    #                                             }
    #                                         }
    #                                     ],
    #                                     "series": [
    #                                         {
    #                                             "series": {
    #                                                 "sourceRange": {
    #                                                     "sources": [
    #                                                         {
    #                                                             "sheetId": sheet_id,
    #                                                             "startRowIndex": 0,
    #                                                             "endRowIndex": end_row,
    #                                                             "startColumnIndex": 1,
    #                                                             "endColumnIndex": end_col,
    #                                                         }
    #                                                     ]
    #                                                 }
    #                                             },
    #                                             "targetAxis": "LEFT_AXIS",
    #                                         },
    #                                         {
    #                                             "series": {
    #                                                 "sourceRange": {
    #                                                     "sources": [
    #                                                         {
    #                                                             "sheetId": sheet_id,
    #                                                             "startRowIndex": 0,
    #                                                             "endRowIndex": end_row,
    #                                                             "startColumnIndex": 2,
    #                                                             "endColumnIndex": end_col,
    #                                                         }
    #                                                     ]
    #                                                 }
    #                                             },
    #                                             "targetAxis": "LEFT_AXIS",
    #                                         },
    #                                         {
    #                                             "series": {
    #                                                 "sourceRange": {
    #                                                     "sources": [
    #                                                         {
    #                                                             "sheetId": sheet_id,
    #                                                             "startRowIndex": 0,
    #                                                             "endRowIndex": end_row,
    #                                                             "startColumnIndex": 3,
    #                                                             "endColumnIndex": end_col,
    #                                                         }
    #                                                     ]
    #                                                 }
    #                                             },
    #                                             "targetAxis": "LEFT_AXIS",
    #                                         },
    #                                     ],
    #                                     "headerCount": 1,
    #                                 },
    #                             },
    #                             "position": {"newSheet": True},
    #                         }
    #                     }
    #                 }
    #             ]
    #         }

    #         self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

    #     except Exception as e:
    #         logger.warn(e)
