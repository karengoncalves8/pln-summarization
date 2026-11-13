"""Vectorization services.

Terminology:
- Tokens: the per-sentence list produced by PreProcessingService, e.g. ['wordA', 'wordB'],
  already lemmatized, lowercased and without stopwords/punctuation.
- Lexicon: the vocabulary of the whole document. Each word maps to how many times it
  appears in total (`counter`) and in how many sentences it appears (`sent_counter`).
- Bag of Words: for one sentence, how many times each lexicon word repeats in that
  sentence, aligned with the lexicon's (sorted) vocabulary.
"""

from collections import Counter
from math import log10

from app.models.models import BowVector, Document, Lexicon, LexiconEntry, Sentence, TfIdfVector


class LexiconService:
    def execute(self, document: Document) -> Lexicon:
        """Builds the lexicon (vocabulary + counters) from all sentences of the document."""
        counters: Counter[str] = Counter()
        sent_counters: Counter[str] = Counter()

        for sentence in document.sentences:
            counters.update(sentence.tokens)
            sent_counters.update(set(sentence.tokens))  # each word counts once per sentence

        entries = {
            word: LexiconEntry(counter=counters[word], sent_counter=sent_counters[word])
            for word in sorted(counters)
        }
        return Lexicon(entries=entries, n_sentences=len(document.sentences))


class VectorizationService:
    def execute(self, sentence: Sentence, lexicon: Lexicon) -> BowVector:
        """Builds the Bag of Words of a sentence, aligned with the lexicon vocabulary."""
        token_counts = Counter(sentence.tokens)
        vocabulary = list(lexicon.entries)
        counts = [token_counts.get(word, 0) for word in vocabulary]
        sentence.bag_of_words = counts
        return BowVector(vocabulary=vocabulary, counts=counts)


class TfIdfTransformService:
    def __init__(self):
        self.vector_service = VectorizationService()

    def execute(self, sentence: Sentence, lexicon: Lexicon) -> TfIdfVector:
        """Weights the sentence's Bag of Words by TF-IDF, treating each sentence as a document.

        tf  = 1 + log10(count) if the word appears in the sentence, else 0
        idf = 1 + log10((1 + N) / (1 + sentences containing the word))   (smoothed, always >= 1)
        """
        bow = self.vector_service.execute(sentence, lexicon)
        n_sentences = lexicon.n_sentences

        weights = []
        for word, count in zip(bow.vocabulary, bow.counts):
            if count == 0:
                weights.append(0.0)
                continue
            tf = 1 + log10(count)
            idf = 1 + log10((1 + n_sentences) / (1 + lexicon.entries[word].sent_counter))
            weights.append(tf * idf)

        return TfIdfVector(vocabulary=bow.vocabulary, weights=weights)
