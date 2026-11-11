import nltk
nltk.download('punkt_tab', quiet=True)
from nltk.tokenize import PunktTokenizer

from app.models.models import Sentence


class SentenceExtractionService:
    def execute(self, text: str) -> list[Sentence]:
        tokenizer = PunktTokenizer('portuguese')
        raw_sentences = tokenizer.tokenize(text)
        sentences = [Sentence(text=sentence) for sentence in raw_sentences]
        return sentences