from loguru import logger

from app.services.preprocessing import PreProcessingService
from app.services.sentence_extraction import SentenceExtractionService
from app.services.vectorization import TfIdfTransformService, LexiconService
from app.services.similarity_measurement import SimilarityMeasurementService
from app.models.models import Document, SelectedSentence, SummarizationResult


class SummarizationPipeline:
    def __init__(self):
        self.sentence_extraction = SentenceExtractionService()
        self.preprocessing = PreProcessingService()
        self.tf_idf_service = TfIdfTransformService()
        self.lexicon_service = LexiconService()
        self.similarity_service = SimilarityMeasurementService()

    def execute(self, text: str, n_sentences: int | None = 5) -> SummarizationResult:
        sentences = self.sentence_extraction.execute(text)

        logger.info(f"Extracted {len(sentences)} sentences from the text.")

        if not sentences:
            return SummarizationResult(summary="")

        document = Document()
        for sentence in sentences:
            preprocessed_sentence = self.preprocessing.execute(sentence)
            document.sentences.append(preprocessed_sentence)

        lexicon = self.lexicon_service.execute(document)

        vectors = []
        for sentence in document.sentences:
            vector = self.tf_idf_service.execute(sentence, lexicon)
            vectors.append(vector.weights)

        matrix = self.similarity_service.build_similarity_matrix(vectors)

        scores = self.similarity_service.textrank(matrix)
        for sentence, score in zip(document.sentences, scores):
            sentence.score = score
            logger.debug(f"{score:.4f} | {sentence.text[:60]}")

        ranked = sorted(
            range(len(document.sentences)),
            key=lambda i: document.sentences[i].score,
            reverse=True
        )

        selected = sorted(ranked[:n_sentences])
        selected_sentences = [
            SelectedSentence(
                text=document.sentences[i].text,
                score=document.sentences[i].score,
            )
            for i in selected
        ]

        return SummarizationResult(
            summary=" ".join(sentence.text for sentence in selected_sentences),
            sentences=selected_sentences,
        )
