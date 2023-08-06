from copy import deepcopy

import torch
from transformers import AutoModelWithLMHead, AutoTokenizer

from seaqube.nlp.seaqube_model import SeaQuBeNLPLoader, SeaQuBeNLPDoc
from seaqube.nlp.tools import word_count_list, tokenize_corpus
from seaqube.nlp.types import SeaQuBeWordEmbeddingsModel, RawModelTinCan
from seaqube.tools.io import load_json
from seaqube.tools.math import cosine
from seaqube.nlp.context2vec.context2vec import Context2Vec
import matplotlib.pyplot as plt
from seaqube.nlp.roberta.seaberta import SeaBERTa

import numpy as np

if __name__ == "__main__":


    #c2v = Context2Vec.load("starwars_c2v")

    c2v = Context2Vec.load("/Users/allankarlson/Desktop/roberta/sick_small_c2v_ep30")

    ## todo always TO LOWER!
    #sentence_one = ["how", "you", "get", "so", "big", "!"]
    #sentence_two = ["you","came" ,"in", "that", "thing", "?"]
    sentence_one = ["a", "woman", "likes", "her", "boy" ]
    sentence_two = ["the", "boy", "is", "eating", "tofu"]


    data = np.zeros((6,6))

    for i, word_one in enumerate(sentence_one):
        for j, word_two in enumerate(sentence_two):
            you_1 = c2v.backend_model.context2vec(sentence_one, i)
            you_2 = c2v.backend_model.context2vec(sentence_two, j)
            cos = cosine(you_1, you_2)

            print(word_one, word_two, cos)
            data[i, j] = cos

    cosine(c2v.backend_model.loss_func.W.data[16], c2v.backend_model.loss_func.W.data[17])
    # words without context 0.11067138
    #
    # woman is 16
    # boy is 17



    #a = np.random.random((16, 16))
    #plt.imshow(data,  interpolation='nearest')
    #plt.show()

    class SeaQuBeWordEmbeddingsModelC2V(SeaQuBeWordEmbeddingsModel):
        def __init__(self, c2v: Context2Vec):
            self.c2v = c2v

        def vocabs(self):
            return self.c2v.wv.vocabs

        @property
        def wv(self):
            return self.c2v.wv

        def word_vector(self, word):
            return self.c2v.wv[word]

        def matrix(self):
            return self.c2v.wv.matrix

        def context_embedding(self, words, position):
            return self.c2v.backend_model.context2vec(words, position)

    seaC2V = SeaQuBeWordEmbeddingsModelC2V(c2v)
    tin_can = RawModelTinCan(seaC2V, word_count_list([c2v.wv.vocabs])) # word count is a fake

    nlp = SeaQuBeNLPLoader.load_model_from_tin_can(tin_can, "c2v")
    doc: SeaQuBeNLPDoc = nlp("a woman is not a woman as a boy is not a boy")

    doc[1].similarity(doc[5]) # differnt
    doc[1].similarity(doc[8]) # differnt

    main_output_dir = "/Users/allankarlson/Desktop/roberta/sts_small_bxjgcvjvkuhs/output/checkpoint-20"
    model = AutoModelWithLMHead.from_pretrained(main_output_dir)
    tokenizer = AutoTokenizer.from_pretrained(main_output_dir)


    #text = "a woman is not a woman as a boy is not a boy"
    #text = "hello, my dog is cute"
    text = "he says hello to the boy"
    text_tokenized = tokenize_corpus([text], verbose=False)[0]
    snippets = tokenizer.encode(text)[1:-1]

    input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0)  # Batch size 1
    # input_ids = torch.tensor(tokenizer.encode("a woman is not a woman as a boy is not a boy")).unsqueeze(0)  # Batch size 1
    outputs = model(input_ids)
    last_hidden_states = outputs[0]

    #for token in tokens:
        #print(tokenizer.encode(token)[1:-1])

    #tokenizer.encode("a woman is not a woman as a boy is not a boy")

    vocabs = "/Users/allankarlson/Desktop/roberta/sts_small_bxjgcvjvkuhs/output/checkpoint-20/vocab.json"
    vocabs = load_json(vocabs)
    index_2_word = {v:k for k,v in vocabs.items()}



    splitted = [index_2_word[index] for index in snippets]
    position = 0

    summarized_indices = [ [] for _ in range(len(text_tokenized)) ]

    tmp_orig_tokens = deepcopy(text_tokenized)
    for j, word_part in enumerate(splitted):
        word_part = word_part.replace('Ġ', '')


        print("debug 1", word_part, j, position, tmp_orig_tokens[position])
        if word_part not in tmp_orig_tokens[position]:
            position += 1

        if word_part in tmp_orig_tokens[position]:
            print("IN?")
            summarized_indices[position].append(j+1)
            tmp_orig_tokens[position] = tmp_orig_tokens[position].replace(word_part, '', 1)
            print("debug 2", tmp_orig_tokens[position])

    new_sorted_wes = []
    for _list in summarized_indices:
        new_sorted_wes.append(np.mean(last_hidden_states[0][_list].detach().numpy(), axis=0))

    new_sorted_wes = np.array(new_sorted_wes)