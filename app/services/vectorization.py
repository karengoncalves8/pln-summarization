## TODO Notes for later, Karen was wrong about the Lexicon. Lexicon is different from the tokens.
# Tokens means: ['wordA', 'wordB'] withou stopwords, stemed and without ponctuation.
# What i need to do is also create a dict from the strucutre i mapped that contains the repeatability of that word in the sentence.

from app.models.models import Sentence, BowVector, TfIdfVector, Document
from math import log10

class VectorizationService:
    def execute(self, sentence: Sentence):
        bow_vector = []
        model_lexicon_list = list(sentence.tokens)
        for position in range(len(model_lexicon_list)):
            bow_vector.append(0)
            for w in sentence.text:
                if w == model_lexicon_list[position]:
                    bow_vector[position] +=1
        return bow_vector


class TfIdfTransformService:
    def __init__(self):
        self.vector_service = VectorizationService()

    def execute(self, sentence: Sentence):
        sentence_bow = self.vector_service.execute(sentence)
        tfidf_vector = []
        pos = 0
        for key in self.vector_service.lexicon:            
            tf = (1 +sentence_bow[pos])
            idf = (1+log10(self.lang_model.corpus_sent_size/(1 +self.lang_model.lexicon[key]['sent_counter'])))
            tfidf_vector.append(tf*idf)
            pos+=1
        return tfidf_vector


class LexiconService:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def build_lexicon(self, document: Document):
        ''' Creates a lexicon that corresponds to language model'''
        model_lexicon = {}
        corpus_sent_size = 0
        for sentences in document:
            last_sentence = 0
            sentence_counter = 0
            for sentence in sentences:
                for word in sentence.tokens:
                    if word in model_lexicon:
                        if model_lexicon[word]['last_sentence'] != sentence_counter:
                            model_lexicon[word]['sent_counter'] += 1
                            model_lexicon[word]['last_sentence'] = sentence_counter
                        model_lexicon[word]['counter'] += 1
                    else:
                        model_lexicon[word] = {'counter': 1, 'doc_counter': 1, 'sent_counter': 1}
                        model_lexicon[word]



    def build_model_lexicon(self, document):   
        ''' Creates a lexicon that corresponds to language model''' 
        doc_array = document
        model_lexicon = {}
        document_counter = 0
        last_document = 0   
        self.corpus_sent_size = 0    
        for sentences in doc_array: #single document            
            last_sentence = 0
            sentence_counter = 0
            for sentence in sentences: #single sentence
                words = self.textNormalizer.word_tokenizer(sentence)         
                self.corpus_sent_size +=1              
                for word in words:
                    # stop words removal
                    if word_lower not in self.textNormalizer.stop_words:     
                        if word_lower in model_lexicon:              
                            if model_lexicon[word_lower]['last_document']!= document_counter:
                                model_lexicon[word_lower]['doc_counter'] +=1
                                model_lexicon[word_lower]['last_document'] = document_counter
                            if model_lexicon[word_lower] ['last_sentence'] != sentence_counter:
                                model_lexicon[word_lower]['sent_counter'] +=1
                                model_lexicon[word_lower] ['last_sentence'] = sentence_counter                                
                            model_lexicon[word_lower]['counter'] +=1
                        else:
                            model_lexicon[word_lower] = {'counter':1, 'doc_counter':1, 'sent_counter':1}
                            model_lexicon[word_lower]['last_document'] = document_counter
                            model_lexicon[word_lower]['last_sentence'] = last_sentence
                sentence_counter += 1
            document_counter +=1
        sorted_lexicon = dict(sorted(model_lexicon.items()))
        # removing temporary counters:
        for key in sorted_lexicon.keys():
            del model_lexicon[key]['last_document']
            del model_lexicon[key]['last_sentence']
        self.lexicon = sorted_lexicon
        return self.lexicon
