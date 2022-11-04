import torch
import re
from hanspell import spell_checker

def remove_word(sentences):
    

    for i,sentence in enumerate(sentences):
        punct = sentence[-1]
        sentence = sentence.lower()
        # 자모 제거
        sentence = re.sub("[ㄱ-ㅎ]+", ' ', sentence)
        # 특수문자 제거
        sentence = re.sub("!+", '!', sentence)
        sentence = re.sub("?+", '?', sentence)
        sentence = re.sub("~+", '~', sentence)
        sentence = re.sub(";+", ';', sentence)
        # spell check
        sentence = re.sub("[&\(\)]", '', sentence)
        sentence = spell_checker.check(sentence).as_dict()['checked']
        # 중복공백 제거
        sentence = re.sub(" +", ' ', sentence.strip())
        # 구두점
        if punct in ['!', '.', '?', '~']:
            sentence += punct

        sentences[i] = sentence
    return sentences

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)