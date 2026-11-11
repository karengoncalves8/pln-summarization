
from pydantic import BaseModel


class Sentence(BaseModel):
    text: str
    tokens: list[str] = []
    bag_of_words: list[int] = []
    score: float = 0.0

class BowVector(BaseModel):
    vocabulary: list[str]
    counts: list[int]

class Document(BaseModel):
    sentences: list[Sentence]

class TfIdfVector(BaseModel):
    vocabulary: list[str]
    weights: list[float]

class LexiconEntry(BaseModel):
    counter: int
    sent_counter: int

class Lexicon(BaseModel):
    entries: dict[str, LexiconEntry]
