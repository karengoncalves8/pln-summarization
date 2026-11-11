from loguru import logger

from app.services.preprocessing import PreProcessingService
from app.services.sentence_extraction import SentenceExtractionService


class SummarizationPipeline:
    def __init__(self):
        self.sentence_extraction = SentenceExtractionService()
        self.preprocessing = PreProcessingService()
        # self.vectorization = summarization_service

    def execute(self, text: str, n_sentences: int) -> str:
        sentences = self.sentence_extraction.execute(text)

        logger.info(f"Extracted {len(sentences)} sentences from the text.")

        for sentence in sentences:
            preprocessed_sentence = self.preprocessing.execute(sentence)

        return "Summary generated successfully."

