import spacy

from app.models.models import Sentence



class PreProcessingService:
    def __init__(self):
        self.nlp = spacy.load('pt_core_news_sm')

    def execute(self, sentence: Sentence) -> Sentence:
        doc = self.nlp(sentence.text)                    # tokenize and lemmatize the sentence
        lemas = []
        for t in doc:
            if t.is_punct or t.is_space or t.like_num:   # if it's punctuation, space or number, skip it
                continue
            if t.is_stop:                                 # if it's a stopword, skip it
                continue
            if not t.is_alpha or len(t.text) <= 2:        # if it's not alphabetic or has 2 or fewer characters, skip it
                continue
            lemas.append(t.lemma_.lower())                # append the lemma in lowercase to the list of lemmas
        sentence.tokens = lemas
        return sentence