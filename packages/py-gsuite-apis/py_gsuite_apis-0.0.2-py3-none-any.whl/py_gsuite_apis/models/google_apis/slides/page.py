from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel, root_validator

from py_gsuite_apis.models.google_apis.slides.enums import PageType, PropertyState, ThemeColorType
from py_gsuite_apis.models.google_apis.slides.other import SolidFill, Size, AffineTransform, RgbColor


"""
Pages
"""


class PageBackgroundFill(BaseModel):
    """
    The page background fill.
    """

    propertyState: Optional[PropertyState]
    # UNION FIELDS
    solidFill: Optional[SolidFill]
    stretchedPictureFill: Optional[StretchedPictureFill]
    # END UNION FIELDS

    @root_validator
    def only_one_fill(cls, values):
        if len([v for k, v in values.items() if v and k in ["solidFill", "stretchedPictureFill"]]) == 1:
            return values

        raise ValueError("You must choose only one from solidFill and stretchedPictureFill.")


class StretchedPictureFill(BaseModel):
    """

    """

    contentUrl: Optional[str]
    size: Optional[Size]


class ThemeColorPair(BaseModel):
    """

    """

    type: Optional[ThemeColorType]
    color: Optional[RgbColor]


class ColorScheme(BaseModel):
    """

    """

    colors: List[ThemeColorPair] = []


class SlideProperties(BaseModel):
    """
    The properties of Page that are only relevant for pages with pageType SLIDE.
    """

    layoutObjectId: Optional[str]
    masterObjectId: Optional[str]
    notesPage: Optional[GoogleSlidesPage]


class LayoutProperties(BaseModel):
    """
    The properties of Page are only relevant for pages with pageType LAYOUT.
    """

    name: Optional[str]
    displayName: Optional[str]
    masterObjectId: Optional[str]


class NotesProperties(BaseModel):
    """
    The properties of Page that are only relevant for pages with pageType NOTES.
    """

    speakerNotesObjectId: Optional[str]


class PageProperties(BaseModel):
    """
    The properties of the Page.

    The page will inherit properties from the parent page.
    Depending on the page type the hierarchy is defined in either SlideProperties or LayoutProperties.
    """

    pageBackgroundFill: Optional[PageBackgroundFill]
    colorScheme: Optional[ColorScheme]


class MasterProperties(BaseModel):
    """
    he properties of Page that are only relevant for pages with pageType MASTER.
    """

    displayName: Optional[str]


class WordArt(BaseModel):
    """
    A PageElement kind representing word art.
    """

    renderedText: Optional[str]


class GoogleSlidesPageElementBase(BaseModel):
    """
    Base model for a visual element rendered on a page.
    """

    objectId: Optional[str]
    title: Optional[str]
    description: Optional[str]
    size: Optional[str]
    transform: Optional[AffineTransform]


GoogleSlidesPageElementBase.update_forward_refs()


class GoogleSlidesPageElement(GoogleSlidesPageElementBase):
    pass


class GoogleSlidesGroup(GoogleSlidesPageElementBase):
    """
    A PageElement kind representing a joined collection of PageElements.
    """

    children: List[GoogleSlidesPageElementBase] = []


GoogleSlidesGroup.update_forward_refs()


class GoogleSlidesPage(BaseModel):
    objectId: Optional[str]
    revisionId: Optional[str]
    pageType: Optional[PageType]
    pageElements: List[GoogleSlidesPageElement] = []
    pageProperties: Optional[PageProperties]
    # UNION FIELDS
    slideProperties: Optional[SlideProperties]
    layoutProperties: Optional[LayoutProperties]
    notesProperties: Optional[NotesProperties]
    masterProperties: Optional[MasterProperties]
    # END UNION FIELDS

    @root_validator
    def only_one_property(cls, values):
        properties_values = [
            v
            for k, v in values.items()
            if k in ["slideProperties", "layoutProperties", "notesProperties", "masterProperties"]
        ]
        if len([v for v in properties_values if v]) == 1:
            return values

        raise ValueError("You must choose only one from sheetId, overlayPosition, and newSheet.")


GoogleSlidesPage.update_forward_refs()
