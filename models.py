from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl



# /objects
class ObjectsList(BaseModel):
    total: int
    objectIDs: List[int]



# Constituents
class Constituent(BaseModel):
    constituentID: int
    role: Optional[str]
    name: Optional[str]
    constituentULAN_URL: Optional[HttpUrl]
    constituentWikidata_URL: Optional[HttpUrl]
    gender: Optional[str]



# Tags
class Tag(BaseModel):
    term: str
    AAT_URL: Optional[HttpUrl]
    Wikidata_URL: Optional[HttpUrl]



# Measurements
class ElementMeasurement(BaseModel):
    elementName: str
    elementDescription: Optional[str]
    elementMeasurements: Dict[str, float]  # Height/Width/etc.



# Полная карточка объекта
class ArtObject(BaseModel):
    objectID: int
    isHighlight: bool
    accessionNumber: str
    accessionYear: Optional[str]
    isPublicDomain: bool
    primaryImage: Optional[str]
    primaryImageSmall: Optional[str]
    additionalImages: List[str] = []
    constituents: Optional[List[Constituent]]
    department: Optional[str]
    objectName: Optional[str]
    title: Optional[str]
    culture: Optional[str]
    period: Optional[str]
    dynasty: Optional[str]
    reign: Optional[str]
    portfolio: Optional[str]
    artistRole: Optional[str]
    artistPrefix: Optional[str]
    artistDisplayName: Optional[str]
    artistDisplayBio: Optional[str]
    artistSuffix: Optional[str]
    artistAlphaSort: Optional[str]
    artistNationality: Optional[str]
    artistBeginDate: Optional[str]
    artistEndDate: Optional[str]
    artistGender: Optional[str]
    artistWikidata_URL: Optional[str]
    artistULAN_URL: Optional[str]
    objectDate: Optional[str]
    objectBeginDate: Optional[int]
    objectEndDate: Optional[int]
    medium: Optional[str]
    dimensions: Optional[str]
    measurements: Optional[List[ElementMeasurement]]
    creditLine: Optional[str]
    geographyType: Optional[str]
    city: Optional[str]
    state: Optional[str]
    county: Optional[str]
    country: Optional[str]
    region: Optional[str]
    subregion: Optional[str]
    locale: Optional[str]
    locus: Optional[str]
    excavation: Optional[str]
    river: Optional[str]
    classification: Optional[str]
    rightsAndReproduction: Optional[str]
    linkResource: Optional[str]
    metadataDate: Optional[str]
    repository: Optional[str]
    objectURL: Optional[str]
    tags: Optional[List[Tag]]
    objectWikidata_URL: Optional[str]
    isTimelineWork: Optional[bool]
    GalleryNumber: Optional[str]



# /departments
class Department(BaseModel):
    departmentId: int
    displayName: str


class DepartmentsResponse(BaseModel):
    departments: List[Department]



# /search
class SearchResponse(BaseModel):
    total: int
    objectIDs: Optional[List[int]]
