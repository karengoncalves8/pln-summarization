from pydantic import BaseModel, Field


class Sentence(BaseModel):
    text: str
    tokens: list[str] = []
    bag_of_words: list[int] = []
    score: float = 0.0


class SelectedSentence(BaseModel):
    text: str
    score: float


class SummarizationResult(BaseModel):
    summary: str
    sentences: list[SelectedSentence] = Field(default_factory=list)


class BowVector(BaseModel):
    vocabulary: list[str]
    counts: list[int]

class Document(BaseModel):
    sentences: list[Sentence] = Field(default_factory=list)

class TfIdfVector(BaseModel):
    vocabulary: list[str]
    weights: list[float]

class LexiconEntry(BaseModel):
    counter: int
    sent_counter: int

class Lexicon(BaseModel):
    entries: dict[str, LexiconEntry]
    n_sentences: int = 0
