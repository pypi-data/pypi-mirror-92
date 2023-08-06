from typing import Optional, List

from pydantic import BaseModel

from py_gsuite_apis.models.google_apis.slides.page import GoogleSlidesPage
from py_gsuite_apis.models.google_apis.slides.other import Size, ImageProperties


"""
Slides Charts
"""


class SheetsChartProperties(BaseModel):
    chartImageProperties: Optional[ImageProperties]


class SheetsChart(BaseModel):
    spreadsheetId: Optional[str]
    chartId: Optional[int]
    contentUrl: Optional[str]
    sheetsChartProperties: Optional[SheetsChartProperties]


"""
Presentations
"""


class GoogleSlidesPresentation(BaseModel):
    presentationId: Optional[str]
    title: Optional[str]
    locale: Optional[str]
    revisisonId: Optional[str]
    pageSize: Optional[Size]
    slides: List[GoogleSlidesPage] = []
    masters: List[GoogleSlidesPage] = []
    layouts: List[GoogleSlidesPage] = []
    notesMaster: Optional[GoogleSlidesPage]
