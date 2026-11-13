from loguru import logger

from app.services.preprocessing import PreProcessingService
from app.services.sentence_extraction import SentenceExtractionService
from app.services.vectorization import TfIdfTransformService, LexiconService
from app.models.models import Document


class SummarizationPipeline:
    def __init__(self):
        self.sentence_extraction = SentenceExtractionService()
        self.preprocessing = PreProcessingService()
        self.tf_idf_service = TfIdfTransformService()
        self.lexicon_service = LexiconService()

    def execute(self, text: str, n_sentences: int) -> str:
        sentences = self.sentence_extraction.execute(text)

        logger.info(f"Extracted {len(sentences)} sentences from the text.")

        document = Document()
        
        for sentence in sentences:
            preprocessed_sentence = self.preprocessing.execute(sentence)
            document.sentences.append(preprocessed_sentence)

        lexicon = self.lexicon_service.execute(document)

        vectors = []

        for sentence in document.sentences:
            vector = self.tf_idf_service.execute(sentence, lexicon)
            vectors.append(vector)

        return "Summary generated successfully."
