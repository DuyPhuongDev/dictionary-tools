from pydantic import BaseModel
from typing import Optional, List

class VocabularyRequest(BaseModel):
    words: List[str]

class VocabularyItem(BaseModel):
    word: str
    meaning_en: str
    meaning_vi: str
    example_en: str
    example_vi: str
    ipa: str
    pos: str

class VocabularyResponse(BaseModel):
    success: bool
    message: str
    data: List[VocabularyItem]
    total_count: int

class DictionaryData(BaseModel):
    word: str
    meaning: Optional[str] = ""
    example: Optional[str] = ""
    ipa: Optional[str] = ""
    pos: Optional[str] = "" 