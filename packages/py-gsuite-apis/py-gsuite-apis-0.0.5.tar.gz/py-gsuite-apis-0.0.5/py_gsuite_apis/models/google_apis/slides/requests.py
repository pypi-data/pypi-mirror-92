from typing import Optional, List

from pydantic import BaseModel, root_validator

from py_gsuite_apis.models.google_apis.slides.other import Size, AffineTransform
from py_gsuite_apis.models.google_apis.slides.enums import PredefinedLayout, ShapeType, LinkingMode
from py_gsuite_apis.models.google_apis.slides.shape import Placeholder

"""
Update Presentation Requests
"""


class ObjectIdMixin(BaseModel):
    objectId: Optional[str]


class PageElementProperties(BaseModel):
    """
    Common properties for a page element.

    Note: When you initially create a PageElement,
    the API may modify the values of both size and transform ,
    but the visual size will be unchanged.
    """

    pageObjectId: Optional[str]
    size: Optional[Size]
    transform: Optional[AffineTransform]


class SubstringMatchCriteria(BaseModel):
    """
    A criteria that matches a specific string of text in a shape or table.
    """

    text: Optional[str]
    matchCase: Optional[bool]


class CreateSheetsChartRequest(ObjectIdMixin):
    """
    CreateSheetsChartRequest

    Creates an embedded Google Sheets chart.

    NOTE: Chart creation requires at least one of the spreadsheets.readonly, spreadsheets,
    drive.readonly, drive.file, or drive OAuth scopes.

    """

    elementProperties: Optional[PageElementProperties]
    spreadsheetId: Optional[str]
    chartId: Optional[int]
    linkingMode: Optional[LinkingMode]


class ReplaceAllShapesWithSheetsChartRequest(BaseModel):
    """
    ReplaceAllShapesWithSheetsChartRequest

    Replaces all shapes that match the given criteria with the provided Google Sheets chart.
    The chart will be scaled and centered to fit within the bounds of the original shape.

    NOTE: Replacing shapes with a chart requires at least one of the spreadsheets.readonly,
    spreadsheets, drive.readonly, or drive OAuth scopes.
    """

    containsText: Optional[SubstringMatchCriteria]
    spreadsheetId: Optional[str]
    chartId: Optional[int]
    linkingMode: Optional[LinkingMode]
    pageObjectIds: List[str] = []


class CreateShapeRequest(ObjectIdMixin):
    """

    """

    elementProperties: Optional[PageElementProperties]
    shapeType: Optional[ShapeType]


class LayoutReference(BaseModel):
    """
    Slide layout reference. This may reference either:

    - A predefined layout
    - One of the layouts in the presentation.
    """

    predefinedLayout: Optional[PredefinedLayout]
    layoutId: Optional[str]

    @root_validator
    def only_one(cls, values):
        if len([v for v in values.values() if v]) == 1:
            return values

        raise ValueError("You must choose only one from predefinedLayout and layoutId - not both")


class LayoutPlaceholderIdMapping(ObjectIdMixin):
    """
    The user-specified ID mapping for a placeholder that will be created on a slide from a specified layout.
    """

    layoutPlaceholder: Optional[Placeholder]
    layoutPlaceholderObjectId: Optional[str]

    @root_validator
    def only_one(cls, values):
        if len([v for k, v in values.items() if v and k in ["layoutPlaceholder", "layoutPlaceholderObjectId"]]) == 1:
            return values

        raise ValueError("You must choose only one from predefinedLayout and layoutId - not both")


class CreateSlideRequest(ObjectIdMixin):
    """
    Create a New Slide
    """

    objectId: Optional[str]
    insertionIndex: Optional[int]
    slideLayoutReference: Optional[LayoutReference]
    placeholderIdMappings: Optional[LayoutPlaceholderIdMapping]


class CreateTableRequest(ObjectIdMixin):
    objectId: Optional[str]
    elementProperties: Optional[PageElementProperties]
    rows: Optional[int]
    columns: Optional[int]
